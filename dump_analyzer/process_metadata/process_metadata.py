import os

import pandas as pd
import pyarrow.parquet as pq
from tqdm import tqdm

from dump_analyzer.process_metadata.missing_metadata import analyze_missing_values, aggregate_missing_data
from dump_analyzer.settings import settings


def process_metadata(folder_path):
    """"""
    combined_missing_df = pd.DataFrame()

    for directory in tqdm(os.listdir(folder_path), desc="Processing Directories"):
        for file in tqdm(os.listdir(os.path.join(folder_path, directory)), desc=f"Processing Files in {directory}", leave=False):
            if file.endswith(".parquet"):
                file_path = os.path.join(folder_path, directory, file)

                table = pq.read_table(file_path)

                df = table.to_pandas()

                missing_df = analyze_missing_values(df, file)
                combined_missing_df = pd.concat(
                    [combined_missing_df, missing_df], ignore_index=True, sort=False
                )

    aggregated_data = aggregate_missing_data(combined_missing_df)

    final_df = pd.concat([combined_missing_df, aggregated_data], ignore_index=True)

    final_df.to_csv(os.path.join(settings.PROCESSED_METADATA_PATH, "missing_data.csv"), index=False)
