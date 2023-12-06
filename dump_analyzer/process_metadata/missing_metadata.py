import pandas as pd


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
        column_names.append(col)

        total_count = len(df)
        total_counts.append(total_count)

        none_count = df[col].isna().sum()

        filtered_df = df[df[col].notna()]

        len_zero_count = 0
        if not pd.api.types.is_float_dtype(df[col].dtype) and not pd.api.types.is_integer_dtype(df[col].dtype):
            len_zero_count = (filtered_df[col].apply(len) == 0).sum()

        missing_count = none_count + len_zero_count
        missing_counts.append(missing_count)

        existing_count = total_count - missing_count
        existing_counts.append(existing_count)

        missing_percentage = (missing_count / total_count) * 100
        missing_percentages.append(missing_percentage)

    missing_data_df = pd.DataFrame({
        'file_name': file,
        'column_name': column_names,
        'total_count': total_counts,
        'existing_count': existing_counts,
        'missing_count': missing_counts,
        'missing_percentage': missing_percentages
    })

    return missing_data_df
