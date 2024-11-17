import pandas as pd
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataCleaner:
    def __init__(self):
        logging.info("DataCleaner initialized.")

    def clean_price_column(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Cleans multiple price columns, converting them from string formats like '$74.99' to numeric formats.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the price columns.
        columns (list): A list of column names to clean.

        Returns:
        pd.DataFrame: DataFrame with the cleaned price columns.
        """
        for column in columns:
            logging.info(f"Cleaning price column: {column}")
            df[column] = df[column].replace('[\$,]', '', regex=True).astype(float)
        logging.info("Price columns cleaned.")
        return df

    def remove_whitespace(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Removes leading and trailing whitespace from multiple specified columns.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the columns.
        columns (list): A list of column names to clean.

        Returns:
        pd.DataFrame: DataFrame with whitespace removed from the specified columns.
        """
        for column in columns:
            logging.info(f"Removing whitespace in column: {column}")
            df[column] = df[column].str.strip()
        logging.info("Whitespace removed.")
        return df

    def convert_boolean_to_numeric(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Converts boolean columns from True/False to 1/0.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the boolean columns.
        columns (list): A list of column names to convert.

        Returns:
        pd.DataFrame: DataFrame with boolean columns converted to 1 and 0.
        """
        for column in columns:
            if df[column].dtype == 'bool':  # Only convert boolean columns
                logging.info(f"Converting boolean column to numeric: {column}")
                df[column] = df[column].astype(int)
        logging.info("Boolean columns converted to numeric.")
        return df
