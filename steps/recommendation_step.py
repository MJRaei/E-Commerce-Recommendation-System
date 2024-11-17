import pandas as pd
from zenml import step

@step
def recommendation_step(
    df: pd.DataFrame, 
    n_recommendations: int = 5, 
    gender: str = None,
    rating_weight: float = 0.15,
    discount_weight: float = 0.5,
    reviews_weight: float = 0.2,
    top_rated_weight: float = 0.05,
    best_seller_weight: float = 0.05,
    clearance_weight: float = 0.05
) -> pd.DataFrame:
    """
    Recommends the top n products based on specified features, with weights for additional binary indicators (Not used in this project).
    
    Parameters:
    - df (pd.DataFrame): The DataFrame containing the engineered features.
    - n_recommendations (int): Number of top products to recommend.
    - gender (str): The gender category to filter by (e.g., "Men's", "Women's").
    - rating_weight, discount_weight, reviews_weight: Weights for main features.
    - top_rated_weight, best_seller_weight, clearance_weight: Weights for additional binary indicators.
    
    Returns:
    - pd.DataFrame: A DataFrame with the top recommended products.
    """
    df = df.copy()
    
    # Filter by gender if specified
    if gender:
        df = df[df['Gender'] == gender]

    # Define the scoring system
    df['Worthiness Score'] = (
        df['Rating'] * rating_weight + 
        df['Discount Percentage'] * discount_weight + 
        df['Number of Reviews'] * reviews_weight +
        df['Top Rated'].astype(int) * top_rated_weight +
        df['Best Seller'].astype(int) * best_seller_weight +
        df['Clearance'].astype(int) * clearance_weight
    )
    
    # Sort by the calculated score and select the top n products
    recommended_products = df.sort_values(by="Worthiness Score", ascending=False).head(n_recommendations)
    return recommended_products[['Product Name', 'Gender', 'Current Price', 'Original Price', 'Rating', 
                                 'Discount Percentage', 'Number of Reviews', 'Top Rated', 'Best Seller', 
                                 'Clearance', 'Worthiness Score']]
