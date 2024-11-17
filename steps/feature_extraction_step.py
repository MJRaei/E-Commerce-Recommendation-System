import pandas as pd
from zenml import step
from src.feature_extraction import FeatureExtractor, GenderExtraction, BrandExtraction, DiscountExtraction

@step
def feature_extraction_step(
    df: pd.DataFrame, strategy: str = "combined"
) -> pd.DataFrame:
    """Applies feature extraction based on the selected strategy."""

    # Choose the appropriate feature extraction strategy
    if strategy == "gender":
        extractor = FeatureExtractor(GenderExtraction())
    elif strategy == "brand":
        extractor = FeatureExtractor(BrandExtraction())
    elif strategy == "discount":
        extractor = FeatureExtractor(DiscountExtraction())
    else:
        raise ValueError(f"Unsupported feature extraction strategy: {strategy}")
    
    # Apply the extraction strategy
    extracted_df = extractor.apply_extraction(df)
    return extracted_df

