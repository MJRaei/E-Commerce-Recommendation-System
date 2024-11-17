import pandas as pd
from src.ingest_data import DataIngestorFactory
from zenml import step
import os

@step
def data_ingestion_step(file_path: str) -> pd.DataFrame:
    """Ingest data from a ZIP or CSV file using the appropriate DataIngestor."""
    # Determine the file extension
    file_extension = os.path.splitext(file_path)[1].lower()  # Gets the file extension dynamically

    # Get the appropriate DataIngestor
    data_ingestor = DataIngestorFactory.get_data_ingestor(file_extension)

    # Ingest the data and load it into a DataFrame
    df = data_ingestor.ingest(file_path)
    return df
