import re
import pandas as pd
from abc import ABC, abstractmethod

# Abstract Base Class for Feature Extraction Strategy
class FeatureExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        """Abstract method to extract features from the DataFrame."""
        pass

# Concrete Strategy for Gender Extraction
class GenderExtraction(FeatureExtractionStrategy):
    def __init__(self):
        self.gender_patterns = {
            "Women's": r"\bWomen's\b",
            "Men's": r"\bMen's\b",
            "Kids'": r"\bKids'\b",
            "Toddler": r"\bToddler\b",
            "Unisex": r"\bUnisex\b"
        }

    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        def extract_gender(name):
            for gender, pattern in self.gender_patterns.items():
                if re.search(pattern, name, re.IGNORECASE):
                    return gender
            return "Unspecified"
        
        df['Gender'] = df['Product Name'].apply(extract_gender)
        return df

# Concrete Strategy for Brand Extraction
class BrandExtraction(FeatureExtractionStrategy):
    def __init__(self):
        # Define gender keywords for detecting the beginning of the product description after brand
        self.gender_patterns = ["Women's", "Men's", "Unisex", "Toddler"]

    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        def extract_brand(name):
            # Build a pattern to find the first occurrence of any gender keyword
            gender_pattern = r'\b(?:' + '|'.join(self.gender_patterns) + r")\b"
            match = re.search(gender_pattern, name, re.IGNORECASE)
            
            # Extract brand as everything before the gender keyword
            if match:
                brand = name[:match.start()].strip()
            else:
                brand = "Unknown"  # Default if no gender keyword is found
            
            return brand

        # Apply the brand extraction to the 'Product Name' column
        df['Brand'] = df['Product Name'].apply(extract_brand)
        return df

class DiscountExtraction(FeatureExtractionStrategy):
    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the discount percentage based on Current Price and Original Price.
        
        Parameters:
        df (pd.DataFrame): The dataframe containing 'Original Price' and 'Current Price' columns.

        Returns:
        pd.DataFrame: DataFrame with a new column 'Discount Percentage'.
        """
        df = df.copy()
        # Calculate discount percentage and handle cases where Original Price is 0 or NaN
        df['Discount Percentage'] = ((df['Original Price'] - df['Current Price']) / 
                                     df['Original Price']).fillna(0) * 100
        df['Discount Percentage'] = df['Discount Percentage'].apply(lambda x: max(x, 0))  # Ensure non-negative values
        return df


# Context Class for Feature Extraction
class FeatureExtractor:
    def __init__(self, strategy: FeatureExtractionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: FeatureExtractionStrategy):
        self._strategy = strategy

    def apply_extraction(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._strategy.extract(df)
