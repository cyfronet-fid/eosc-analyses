import asyncio
import logging
import ast
import os

import httpx
import numpy as np
import pandas as pd

from aiolimiter import AsyncLimiter
import concurrent.futures

from config import OUTPUT_PATH, URLS_BY_PUBLISHER, SAMPLE, PREPROCESSED
from config import (
    SEEDS,
    ERROR_CODES,
    INITIAL_SLEEP_DURATION,
    ERRORS_TO_KEEP_PERCENTAGE,
    THREADS,
    MAX_WORKERS,
)
from data_loader import load_and_process_data
from request_handlers import async_request_publisher_data, sync_request_data
from utils import extract_response_code

# Clear the log file
log_file = "logfile.log"
if os.path.exists(log_file):
    open(log_file, "w").close()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("logfile.log")],
)


def convert_to_list(s):
    """Convert a string representation of a list to an actual list."""
    try:
        return ast.literal_eval(s)
    except ValueError:
        return []


def fetch_data(url):
    with httpx.Client(verify=False) as client:
        response = sync_request_data(client, url)
        return {"url": url, "response": str(response)}


# Load and preprocess data
preprocessed = PREPROCESSED
if preprocessed:
    # Load preprocessed data
    with open(URLS_BY_PUBLISHER, "r", newline="") as file:
        urls_by_publisher = pd.read_csv(file)

    list_columns = ["urls"]
    urls_by_publisher[list_columns] = urls_by_publisher[list_columns].map(
        convert_to_list
    )
else:
    # Load and preprocess data
    urls_by_publisher = load_and_process_data()

# Calculate URL statistics
urls_by_publisher.loc[:, "urls_count"] = urls_by_publisher["urls"].apply(
    lambda x: len(x)
)
total_urls = urls_by_publisher["urls_count"].sum()
urls_by_publisher.loc[:, "urls_percentage"] = (
    urls_by_publisher["urls_count"] / total_urls * 100
)

# Calculate top 8 publishers by URLs
top_8_publishers_by_urls = (
    urls_by_publisher[["publisher", "urls_percentage"]]
    .sort_values(by="urls_percentage", ascending=False)
    .head(8)
)

urls_total_sample = int(round(total_urls * SAMPLE, 0))
top_8_publishers_by_urls.loc[:, "sample_count"] = round(
    top_8_publishers_by_urls["urls_percentage"] * urls_total_sample / 100, 0
)

rest_sample = round(
    urls_total_sample - top_8_publishers_by_urls["sample_count"].sum(), 0
)


# Main data collection process
async def main(seed):
    np.random.seed(seed)

    top_8_publishers = top_8_publishers_by_urls["publisher"].tolist()
    rest_publishers = urls_by_publisher[
        ~urls_by_publisher["publisher"].isin(top_8_publishers)
    ]["publisher"].tolist()

    # Explode URLs
    exploded_urls = urls_by_publisher[["publisher", "urls"]].explode("urls")
    sample_urls = []

    for publisher in top_8_publishers:
        urls = exploded_urls[exploded_urls["publisher"] == publisher]["urls"].tolist()
        sample_count = int(
            top_8_publishers_by_urls[
                top_8_publishers_by_urls["publisher"] == publisher
            ]["sample_count"].iloc[0]
        )
        selected_urls = np.random.choice(urls, size=sample_count, replace=False)
        sample_urls.extend([(publisher, url) for url in selected_urls])

    # Sample URLs for the rest publishers
    rest_sample_urls = exploded_urls[
        exploded_urls["publisher"].isin(rest_publishers)
    ].sample(n=int(rest_sample), random_state=seed)
    sample_urls.extend(
        [(row["publisher"], row["urls"]) for _, row in rest_sample_urls.iterrows()]
    )

    # additional saving used to find what is wrong with URLs
    # sample_urls_df = pd.DataFrame(sample_urls)
    # sample_urls_df.to_csv('output/sample_urls_df.csv', index=False)

    rate_limit = AsyncLimiter(150, 5)
    async with httpx.AsyncClient(
        limits=httpx.Limits(max_connections=750), verify=False
    ) as client:
        sample_results = []
        for publisher, url in sample_urls:
            response = await async_request_publisher_data(client, [url], rate_limit)
            sample_results.append(
                {"publisher": publisher, "url": url, "response": str(response)}
            )

    return sample_results


# Processing and saving results
async def analyze_and_save(sample_results, filename):
    sample_df = pd.DataFrame(sample_results)

    with open(f"{filename}.csv", "w", newline="") as file:
        file.truncate(0)

        sample_df.to_csv(file, index=False)
        logging.info(f"File saved: {file}")

    sample_df["response_code"] = sample_df["response"].apply(extract_response_code)
    sample_code_count = (
        sample_df.groupby("response_code").size().reset_index(name="count")
    )
    sample_count = sample_code_count["count"].sum()
    sample_code_count.loc[:, "count_percent"] = (
        sample_code_count["count"] / sample_count * 100
    )

    with open(f"{filename}_count.csv", "w", newline="") as file:
        file.truncate(0)

        sample_code_count.to_csv(file, index=False)
        logging.info(f"File saved: {file}")

    retry_needed = True
    error_codes = ERROR_CODES
    errors_to_keep = round(len(sample_df) * ERRORS_TO_KEEP_PERCENTAGE, 0)

    initial_sleep_duration = INITIAL_SLEEP_DURATION

    while retry_needed:
        # Identify URLSs with status code 4290
        urls_with_errors = sample_df[sample_df["response_code"].isin(error_codes)][
            "url"
        ]

        retry_responses = []
        if len(urls_with_errors) > errors_to_keep:
            if THREADS:
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=MAX_WORKERS
                ) as executor:
                    # Submit tasks for each URL
                    futures = [
                        executor.submit(fetch_data, url) for url in urls_with_errors
                    ]

                    # Retrieve results as they complete
                    for future in concurrent.futures.as_completed(futures):
                        response_data = future.result()
                        retry_responses.append(response_data)
            else:
                with httpx.Client(verify=False) as client:
                    for url in urls_with_errors:
                        response = sync_request_data(client, url)
                        retry_responses.append({"url": url, "response": str(response)})

            retry_responses = pd.DataFrame(retry_responses)

            # Update responses for URLs with status code 429
            for _, row in retry_responses.iterrows():
                sample_df.loc[sample_df["url"] == row["url"], "response"] = str(
                    row["response"]
                )

            # Save the updated DataFrame
            sample_df["response_code"] = sample_df["response"].apply(
                extract_response_code
            )

            with open(f"{filename}.csv", "w", newline="") as file:
                file.truncate(0)
                sample_df.to_csv(file, index=False)
                logging.info(f"File saved: {file}")

            sample_code_count = (
                sample_df.groupby("response_code").size().reset_index(name="count")
            )
            sample_count = sample_code_count["count"].sum()
            sample_code_count.loc[:, "count_percent"] = (
                sample_code_count["count"] / sample_count * 100
            )

            with open(f"{filename}_count.csv", "w", newline="") as file:
                file.truncate(0)
                sample_code_count.to_csv(file, index=False)
                logging.info(f"File saved: {file}")
        else:
            retry_needed = False

        initial_sleep_duration -= 5
        if initial_sleep_duration <= 0:
            initial_sleep_duration = 5

        # Sleep for 5 minutes before the next iteration
        print(
            f"Sleeping for {initial_sleep_duration} seconds before the next iteration..."
        )
        await asyncio.sleep(initial_sleep_duration)

        with open(f"{filename}.csv", "r") as file:
            sample_df = pd.read_csv(file)


if __name__ == "__main__":
    for seed in SEEDS:
        loop = asyncio.get_event_loop()
        sample_results = loop.run_until_complete(main(seed))

        # Save results with seed number in the filename
        filename = f"{OUTPUT_PATH}/urls_sample_seed_{seed}"
        loop.run_until_complete(analyze_and_save(sample_results, filename))
