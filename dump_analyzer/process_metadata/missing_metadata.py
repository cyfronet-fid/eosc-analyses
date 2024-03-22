import pandas as pd

from dump_analyzer.settings import settings


def analyze_missing_values(df, file) -> pd.DataFrame:
    """
    Analyze missing values in each column of a DataFrame

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        file (string): The file name to add more context into df

    Returns:
        pd.DataFrame: A DataFrame containing information about missing values.
    """
    column_names = []
    total_counts = []
    existing_counts = []
    missing_counts = []
    missing_percentages = []

    for col in df.columns:

        if 'one_level_data.parquet' in file:
            id_col = "id"
        else:
            id_col = "rp_id"

        column_names.append(col)

        total_count = df[id_col].nunique()
        total_counts.append(total_count)

        none_count = df[id_col][df[col].isna()].nunique()
        none_ids_set = set(df[id_col][df[col].isna()])

        filtered_df = df[~df[col].isna()]

        len_zero_count = filtered_df[id_col][
            (filtered_df[col].apply(lambda x: len(x) if hasattr(x, '__len__') else 1) == 0) &
            (~filtered_df[id_col].isin(none_ids_set))
            ].nunique()

        missing_count = none_count + len_zero_count
        missing_counts.append(missing_count)

        existing_count = total_count - missing_count
        existing_counts.append(existing_count)

        missing_percentage = (missing_count / total_count) * 100
        missing_percentages.append(missing_percentage)

    missing_data_df = pd.DataFrame(
        {
            "file_name": file,
            "yyyymm": settings.DUMP_YYYYMM,
            "column_name": column_names,
            "total_count": total_counts,
            "existing_count": existing_counts,
            "missing_count": missing_counts,
            "missing_percentage": missing_percentages,
        }
    )

    return missing_data_df


def aggregate_missing_data(missing_data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates missing data information, excluding certain columns and recalculating percentages.

    Args:
        missing_data_df (pd.DataFrame): DataFrame containing missing data information for each file.

    Returns:
        pd.DataFrame: Aggregated missing data information.
    """
    excluded_columns = ['rp_id', 'rp_type', 'rp_language', 'rp_publisher']
    filtered_df = missing_data_df[~missing_data_df['column_name'].isin(excluded_columns)]

    aggregated_data = filtered_df.groupby('column_name').agg({
        'total_count': 'sum',
        'existing_count': 'sum',
        'missing_count': 'sum'
    }).reset_index()

    aggregated_data['missing_percentage'] = (aggregated_data['missing_count'] / aggregated_data['total_count']) * 100

    aggregated_data['file_name'] = 'aggregated'
    aggregated_data['yyyymm'] = settings.DUMP_YYYYMM

    return aggregated_data
