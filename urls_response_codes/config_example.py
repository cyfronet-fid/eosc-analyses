AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
S3_ENDPOINT = "S3_ENDPOINT"
S3_BUCKET = "S3_BUCKET"
URLS_BY_PUBLISHER = "input\urls_by_publisher.csv"
OUTPUT_PATH = "output"
PREPROCESSED = False
SAMPLE = 0.0025
SEEDS = [1]
# ERROR_CODES = [TOO MANY REQUESTS, ERROR_CODE_TIMEOUT, ERROR_CODE_REQUEST_ERROR]
ERROR_CODES = [429, 2.0, 3.0]
INITIAL_SLEEP_DURATION = 300
ERRORS_TO_KEEP_PERCENTAGE = 0.05