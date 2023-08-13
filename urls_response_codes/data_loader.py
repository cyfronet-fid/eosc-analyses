import config
import boto3
import json
from boto3.session import Session
import pandas as pd
from typing import List, Dict, Any

def connect_to_s3(access_key: str, secret_key: str, endpoint: str) -> Session:
    """Connect to s3"""
    session = boto3.session.Session()

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
    obj_str = obj.decode('utf-8')
    for line in obj_str.split('\n'):
        line = line.strip()
        if line != '':
            try:
                doc = json.loads(line)
                row = {field: doc.get(field) for field in selected_fields}
                rows.append(row)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON object: {line}, error: {str(e)}")
    df = pd.DataFrame(rows)
    new_df = df.apply(compute_row_values, axis=1, result_type='expand')
    return new_df

def compute_row_values(row: pd.Series) -> Dict[str, Any]:
    """Compute additional values for each row."""
    num_urls = len(row['url'])
    unique_urls = len(set([url.lower() for url in row['url']]))

    return {
        'id': row['id'],
        'publisher': row['publisher'],
        'urls': row['url'],
        'number_urls': num_urls,
        'number_unique_urls': unique_urls
    }

def load_and_process_data() -> pd.DataFrame:
    access_key = config.AWS_ACCESS_KEY_ID
    secret_key = config.AWS_SECRET_ACCESS_KEY
    endpoint = config.S3_ENDPOINT
    bucket = config.S3_BUCKET
    selected_fields = ['id', 'doi', 'publisher', 'url']
    prefix = config.PREFIX

    s3_client = connect_to_s3(access_key, secret_key, endpoint=endpoint)

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    result_dfs = []
    # Process S3 objects and concatenate the results
    for page in pages:
        for obj in page['Contents']:
            obj_data = s3_client.get_object(Bucket=bucket, Key=obj['Key'])['Body'].read()
            result_dfs.append(process_object(obj_data, selected_fields))
            del obj_data

    # Concatenate dataframes
    result_df = pd.concat(result_dfs, ignore_index=True)

    publishers = set(result_df['publisher'].to_list())

    data = []
    for publisher in publishers:
        publisher_urls = result_df['urls'][result_df['publisher'] == publisher].explode().to_list()
        data.append({'publisher': publisher, 'urls': publisher_urls})

    urls_by_publisher = pd.DataFrame(data)
    return urls_by_publisher
