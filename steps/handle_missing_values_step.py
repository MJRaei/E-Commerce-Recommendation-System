import pandas as pd
from typing import Optional
from src.handle_missing_values import (
    DropMissingValuesStrategy,
    FillMissingValuesStrategy,
    MissingValueHandler,
)
from zenml import step


@step
def handle_missing_values_step(df: pd.DataFrame, strategy: str = "mean", specific_column: Optional[str] = None) -> pd.DataFrame:
    """
    Handles missing values using MissingValueHandler and the specified strategy.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing missing values.
    - strategy (str): The strategy to handle missing values ("drop", "mean", "median", "mode", or "constant").
    - specific_column (Optional[str]): The specific column to check for missing values if using the "drop" strategy.

    Returns:
    - pd.DataFrame: The DataFrame with missing values handled.
    """
    
    if strategy == "drop":
        handler = MissingValueHandler(DropMissingValuesStrategy(axis=0, specific_column=specific_column))
    elif strategy in ["mean", "median", "mode", "constant"]:
        handler = MissingValueHandler(FillMissingValuesStrategy(method=strategy))
    else:
        raise ValueError(f"Unsupported missing value handling strategy: {strategy}")

    cleaned_df = handler.handle_missing_values(df)
    return cleaned_df
