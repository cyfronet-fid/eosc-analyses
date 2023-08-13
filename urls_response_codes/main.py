import asyncio
import httpx
import pandas as pd
import numpy as np
import ast
from aiolimiter import AsyncLimiter
from request_handlers import request_publisher_data
from utils import extract_response_code
from data_loader import load_and_process_data
from config import OUTPUT_PATH, URLS_BY_PUBLISHER

def convert_to_list(s):
    try:
        return ast.literal_eval(s)
    except ValueError:
        return []
    
# Load and preprocess data
preprocessed = True
if preprocessed:
    # Load preprocessed data
    urls_by_publisher = pd.read_csv(URLS_BY_PUBLISHER)
    list_columns = ['urls']
    urls_by_publisher[list_columns] = urls_by_publisher[list_columns].applymap(convert_to_list)
else:
    # Load and preprocess data
    urls_by_publisher = load_and_process_data()

urls_by_publisher.loc[:, 'urls_count'] = urls_by_publisher['urls'].apply(lambda x: len(x))

total_urls = urls_by_publisher['urls_count'].sum()

urls_by_publisher.loc[:, 'urls_percentage'] = urls_by_publisher['urls_count'] / total_urls * 100 

top_8_publishers_by_urls = urls_by_publisher[['publisher', 'urls_percentage']].sort_values(by='urls_percentage', ascending=False).head(8)

urls_total_sample = int(round(total_urls * 0.05, 0))

top_8_publishers_by_urls.loc[:, 'sample_count'] = round(top_8_publishers_by_urls['urls_percentage'] * urls_total_sample / 100, 0)
 

rest_sample = round(urls_total_sample - top_8_publishers_by_urls['sample_count'].sum(), 0)

# Main data collection process
async def main():
    seed = 1234
    np.random.seed(seed)

    top_8_publishers = top_8_publishers_by_urls['publisher'].tolist()
    rest_publishers = urls_by_publisher[~urls_by_publisher['publisher'].isin(top_8_publishers)]['publisher'].tolist()

    # Explode URLs
    exploded_urls = urls_by_publisher[['publisher', 'urls']].explode('urls')
    sample_urls = []

    for publisher in top_8_publishers:
        urls = exploded_urls[exploded_urls['publisher'] == publisher]['urls'].tolist()
        sample_count = int(top_8_publishers_by_urls[top_8_publishers_by_urls['publisher'] == publisher]['sample_count'].iloc[0])
        selected_urls = np.random.choice(urls, size=sample_count, replace=False)
        sample_urls.extend([(publisher, url) for url in selected_urls])

    # Sample URLs for the rest publishers
    rest_sample_urls = exploded_urls[exploded_urls['publisher'].isin(rest_publishers)].sample(n=int(rest_sample), random_state=seed)
    sample_urls.extend([(row['publisher'], row['urls']) for _, row in rest_sample_urls.iterrows()])

    rate_limit = AsyncLimiter(100, 5)
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=1000), verify=False) as client:
        sample_data = []
        for publisher, url in sample_urls:
            responses = await request_publisher_data(client, publisher, [url], rate_limit)
            sample_data.append({'publisher': publisher, 'url': url, 'response': responses})

    return sample_data

# processing and saving results
async def analyze_and_save(sample_data, filename):
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv(f'{filename}.csv', index=False)

    sample_df['response_code'] = sample_df['response'].apply(extract_response_code)
    sample_code_count = sample_df.groupby('response_code').size().reset_index(name='count')
    sample_count = sample_code_count['count'].sum()
    sample_code_count.loc[:, 'count_percent'] = sample_code_count['count'] / sample_count * 100
    sample_code_count.to_csv(f'{filename}_count.csv', index=False)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    sample_results = loop.run_until_complete(main())
    
    # Save results with seed number in the filename
    seed = 1234  # Set your seed value here
    filename = f"{OUTPUT_PATH}/urls_sample_seed_{seed}"
    
    loop.run_until_complete(analyze_and_save(sample_results, filename))
