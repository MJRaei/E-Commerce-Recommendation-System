from steps.data_ingestion_step import data_ingestion_step
from steps.data_cleaning_step import data_cleaning_step
from steps.handle_missing_values_step import handle_missing_values_step
from steps.feature_engineering_step import feature_engineering_step
from steps.feature_extraction_step import feature_extraction_step
from steps.worthiness_calculation_step import autoencoder_worthiness_step

import pandas as pd
from zenml import Model, pipeline, step


@pipeline(
    model=Model(
        name="prices_predictor"
    ),
)
def ml_pipeline():
    """Define an end-to-end machine learning pipeline."""

    # Data Ingestion Step
    raw_data = data_ingestion_step(
        file_path="/Users/mjraei/Desktop/Projects/Price-Predictor/data/scraped_boots_with_colors.csv"
    )

    # Data Cleaning Steps
    cleaned_data = data_cleaning_step(df=raw_data, cleaning_task="clean_price", columns=["Current Price", "Original Price"])
    cleaned_data = handle_missing_values_step(cleaned_data, strategy="drop", specific_column="Original Price")
    cleaned_data = data_cleaning_step(df=cleaned_data, cleaning_task="convert_booleans", columns=["Top Rated", "Best Seller", "Clearance"])

    # Handling Missing Values Step
    filled_data = handle_missing_values_step(cleaned_data)

    # Feature Extraction Steps (Brand, Gender, Discount)
    df_with_brand = feature_extraction_step(df=filled_data, strategy="brand")
    df_with_gender_brand = feature_extraction_step(df=df_with_brand, strategy="gender")
    df_with_gender_brand_discount = feature_extraction_step(df=df_with_gender_brand, strategy="discount")

    # Feature Engineering Step
    engineered_data = feature_engineering_step(
        df_with_gender_brand_discount, strategy="standard_scaling", 
        features=["Current Price", "Rating", "Number of Reviews", "Discount Percentage"]
    )

    # Worthiness Scoring Step (Autoencoder)
    data_with_scores = autoencoder_worthiness_step(data=engineered_data)

    return data_with_scores


if __name__ == "__main__":
    # Running the pipeline
    run = ml_pipeline()
    
    # Access the raw data with original details from the ingestion step
    original_data = run.steps['data_ingestion_step'].output.load()

    # Access the final data with worthiness scores
    data_with_scores = run.steps['autoencoder_worthiness_step'].output.load()
    
    # Combine Worthiness Scores with original data for final output
    final_data_with_scores = original_data.copy()
    final_data_with_scores["Worthiness Score"] = data_with_scores["Worthiness Score"]
    
    # Sort and display the top 10 products with the highest worthiness scores
    top_10_products = final_data_with_scores.sort_values(by="Worthiness Score", ascending=False).head(20)
    
    print("\nTop 10 Products with Highest Worthiness Scores:")
    print(top_10_products)
