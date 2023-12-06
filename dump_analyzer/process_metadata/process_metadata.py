import os

import pandas as pd
import pyarrow.parquet as pq

from missing_metadata import analyze_missing_values

# TODO create .env file and piplock
folder_path = '../../data/openaire/202308'
exclude_columns = ['id', 'folder_name', 'file_name']


combined_missing_df = pd.DataFrame()

for file in os.listdir(folder_path):
    if file.endswith('.parquet'):
        print(f"processing {file}")
        file_path = os.path.join(folder_path, file)

        schema = pq.read_schema(file_path)

        all_columns = schema.names

        columns_to_include = [col for col in all_columns if col not in exclude_columns]

        table = pq.read_table(file_path, columns=columns_to_include)

        df = table.to_pandas()

        missing_df = analyze_missing_values(df, file)
        combined_missing_df = pd.concat([combined_missing_df, missing_df], ignore_index=True, sort=False)
        print(f"{file} ended")

combined_missing_df.to_csv('missing_data.csv', index=False)


