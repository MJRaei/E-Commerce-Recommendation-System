import logging
from typing import Annotated

import mlflow
import numpy as np
import pandas as pd
import tensorflow as tf
from zenml import ArtifactConfig, step
from zenml.client import Client

# Get the active experiment tracker from ZenML
experiment_tracker = Client().active_stack.experiment_tracker

class AutoencoderWorthinessScorer:
    def __init__(self, input_dim: int, encoding_dim: int = None):
        """
        Initializes the Autoencoder for worthiness scoring.
        
        Parameters:
        - input_dim (int): The dimension of the input data.
        - encoding_dim (int): Dimension of the encoding layer (default: input_dim / 2).
        """
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim or int(input_dim / 2)
        self.autoencoder = self._build_autoencoder()

    def _build_autoencoder(self):
        """Builds the autoencoder model with one hidden encoding layer using TensorFlow's Keras API."""
        input_layer = tf.keras.layers.Input(shape=(self.input_dim,))
        encoded = tf.keras.layers.Dense(self.encoding_dim, activation="relu")(input_layer)
        decoded = tf.keras.layers.Dense(self.input_dim, activation="linear")(encoded)

        autoencoder = tf.keras.models.Model(inputs=input_layer, outputs=decoded)
        autoencoder.compile(optimizer="adam", loss="mse")
        return autoencoder

    def train_and_score(self, X: np.ndarray, epochs: int = 50, batch_size: int = 16) -> np.ndarray:
        """
        Trains the autoencoder and calculates the worthiness score for the entire dataset.
        
        Parameters:
        - X (np.ndarray): The feature data for worthiness calculation.
        
        Returns:
        - np.ndarray: Worthiness scores for each product based on reconstruction error.
        """
        logging.info("Training the autoencoder model on the entire dataset.")
        self.autoencoder.fit(X, X, epochs=epochs, batch_size=batch_size, shuffle=True, verbose=0)
        logging.info("Autoencoder training completed.")

        logging.info("Calculating worthiness scores using reconstruction error.")
        X_pred = self.autoencoder.predict(X)
        reconstruction_error = np.mean(np.power(X - X_pred, 2), axis=1)
        return reconstruction_error


@step(enable_cache=False, experiment_tracker=experiment_tracker.name)
def autoencoder_worthiness_step(
    data: pd.DataFrame
) -> Annotated[pd.DataFrame, ArtifactConfig(name="autoencoder_worthiness", is_model_artifact=True)]:
    """
    Builds and trains an Autoencoder to calculate worthiness scores for each product based on anomaly detection.

    Parameters:
    data (pd.DataFrame): The full dataset for worthiness calculation.

    Returns:
    pd.DataFrame: DataFrame with calculated worthiness scores.
    """
    # Ensure input is a DataFrame
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a pandas DataFrame.")

    # Select only the necessary columns for TensorFlow
    selected_columns = ["Current Price", "Rating", "Number of Reviews", 
                        "Discount Percentage", "Top Rated", "Best Seller", "Clearance"]
    data = data[selected_columns]
    
    # Ensure all data is in float32 format
    data = data.astype("float32")

    # Extract dimensions and initialize the autoencoder scorer
    input_dim = data.shape[1]
    scorer = AutoencoderWorthinessScorer(input_dim=input_dim)

    # Start an MLflow run to log the training process
    if not mlflow.active_run():
        mlflow.start_run()

    try:
        # Enable MLflow autologging
        mlflow.tensorflow.autolog()

        # Train the autoencoder on the selected dataset and calculate worthiness scores
        worthiness_scores = scorer.train_and_score(data.values)

        # Create a DataFrame with original features and worthiness scores
        data_with_scores = data.copy()
        data_with_scores["Worthiness Score"] = worthiness_scores

        # Log worthiness score statistics
        mlflow.log_metric("average_worthiness_score", np.mean(worthiness_scores))
        mlflow.log_metric("max_worthiness_score", np.max(worthiness_scores))
        mlflow.log_metric("min_worthiness_score", np.min(worthiness_scores))
        logging.info("Worthiness score statistics logged.")

    except Exception as e:
        logging.error(f"Error during autoencoder training or scoring: {e}")
        raise e

    finally:
        # End the MLflow run
        mlflow.end_run()

    return data_with_scores
