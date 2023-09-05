# URL Checker

URL Checker is a Python script designed to check the correctness of URLs from Amazon S3 EOSC dump datasets. It calculates various statistics related to the URLs and provides insights into their status codes.

## Overview

This script performs the following tasks:

- Loads and preprocess data from Amazon S3 EOSC dump datasets.
- Calculate URL statistics such as counts and percentages.
- Select the top 8 publishers by URL count.
- Samples URLs from these top publishers according to the specified percentage.
- Collects data from sampled URLs using asynchronous and synchronous HTTP requests.
- Handles errors and retries for specific HTTP status codes.
- Logs information for debugging and monitoring.
- Saves the collcted data and statistics to CSV files.

## Usage

To use this script, follow these steps:

1. Install the required Python packages listed in 'requirements.txt' using pip:<br>`pip install -r requirements.txt`
2. Configute the script by editing the 'config_example.py' file to set the necessary parameters such as AWS credentials, S3 endpoint, and more. Do not foget to rename it to 'config.py'.
3. Run the script: `python main.py`
4. The script will collect data and save it to CSV files in the specified 'OUTPUT_PATH'.

## Configuration

Before running the script, configure the 'config_example.py' file with your specific setting and rename it to 'config.py'.

- 'AWS_ACCESS_KEY_ID' and 'AWS_SECRET_ACCESS_KEY': Your Amazon S3 access credentials.
- 'S3_ENDPOINT': The endpoint URL for your S3 storage.
- 'S3_BUCKET': The name of the S3 bucket containing the datasets.
- 'PREFIX': The prefix for the dataset objects.
- Other configuration options related to sampling, error handing, and logging.

## License

This project is licened under the.....