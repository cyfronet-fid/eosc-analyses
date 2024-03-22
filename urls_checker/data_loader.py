import json
import logging
from typing import List, Dict, Any

import numpy as np
import pandas as pd

import boto3
from boto3.session import Session

import config


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logfile.log")],
)


def connect_to_s3(access_key: str, secret_key: str, endpoint: str) -> boto3.client:
    """Connect to Amazon S3"""
    session = Session()
    s3_client = session.client(
        service_name="s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint,
    )

    return s3_client


def process_object(obj: bytes, selected_fields: List[str]) -> pd.DataFrame:
    """Process an S3 object and return a DataFrame."""
    rows = []
    obj_str = obj.decode("utf-8")
    for line in obj_str.split("\n"):
        line = line.strip()
        if line != "":
            try:
                doc = json.loads(line)
                row = {field: doc.get(field) for field in selected_fields}
                rows.append(row)
            except json.JSONDecodeError as e:
                logging.error("Invalid JSON object: %s, errorL %s", line, str(e))
    df = pd.DataFrame(rows)
    new_df = df.apply(compute_row_values, axis=1, result_type="expand")
    return new_df


def compute_row_values(row: pd.Series) -> Dict[str, Any]:
    """Compute additional values for each row."""
    num_urls = len(row["url"])
    unique_urls = len(set([url.lower() for url in row["url"]]))

    return {
        "id": row["id"],
        "publisher": row["publisher"],
        "urls": row["url"],
        "number_urls": num_urls,
        "number_unique_urls": unique_urls,
    }


def close_s3_client(s3_client: boto3.client):
    """Close the S3 client."""
    s3_client.close()


def load_and_process_data() -> pd.DataFrame:
    access_key = config.AWS_ACCESS_KEY_ID
    secret_key = config.AWS_SECRET_ACCESS_KEY
    endpoint = config.S3_ENDPOINT
    bucket = config.S3_BUCKET
    selected_fields = ["id", "doi", "publisher", "url"]
    prefix = config.PREFIX

    s3_client = connect_to_s3(access_key, secret_key, endpoint=endpoint)

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

        result_dfs = []
        # Process S3 objects and concatenate the results
        for page in pages:
            for obj in page["Contents"]:
                obj_data = s3_client.get_object(Bucket=bucket, Key=obj["Key"])[
                    "Body"
                ].read()
                result_dfs.append(process_object(obj_data, selected_fields))

        # Concatenate dataframes
        result_df = pd.concat(result_dfs, ignore_index=True)

        publishers = set(result_df["publisher"].to_list())

        data = []
        for publisher in publishers:
            # Filter out NaN values fo each publisher
            publisher_urls = (
                result_df["urls"][result_df["publisher"] == publisher]
                .explode()
                .dropna()
                .tolist()
            )

            if publisher_urls:
                data.append({"publisher": publisher, "urls": publisher_urls})

        urls_by_publisher = pd.DataFrame(data)

        with open(config.URLS_BY_PUBLISHER, "w", newline="") as file:
            file.truncate(0)
            urls_by_publisher.to_csv(file, index=False)
            logging.info(f"File saved: {file}")

        return urls_by_publisher
    finally:
        close_s3_client(s3_client)
