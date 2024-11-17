import pandas as pd
from src.data_cleaning import DataCleaner
from zenml import step

@step
def data_cleaning_step(
    df: pd.DataFrame, cleaning_task: str = "clean_price", columns: list = ["Price"]
) -> pd.DataFrame:
    """
    Cleans specified columns in the DataFrame based on the cleaning task provided.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to be cleaned.
    - cleaning_task (str): The cleaning task to be performed 
                           (e.g., "clean_price", "remove_whitespace", or "convert_booleans").
    - columns (list): A list of column names to apply the cleaning task.

    Returns:
    - pd.DataFrame: The cleaned DataFrame.
    """
    cleaner = DataCleaner()

    # Determine which cleaning task to execute
    if cleaning_task == "clean_price":
        cleaned_df = cleaner.clean_price_column(df, columns)
    elif cleaning_task == "remove_whitespace":
        cleaned_df = cleaner.remove_whitespace(df, columns)
    elif cleaning_task == "convert_booleans":
        cleaned_df = cleaner.convert_boolean_to_numeric(df, columns)
    else:
        raise ValueError(f"Unsupported cleaning task: {cleaning_task}")

    return cleaned_df
