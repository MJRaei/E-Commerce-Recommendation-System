import re
import pandas as pd

class FeatureExtractionAnalysis:
    def __init__(self, df: pd.DataFrame):
        """
        Initializes the FeatureExtractionAnalysis with the input DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame to perform feature extraction on.
        """
        self.df = df.copy()  # Work with a copy to avoid modifying the original data

    def extract_gender(self) -> pd.DataFrame:
        """
        Extracts the gender based on keywords in the 'Product Name' column.

        Returns:
        pd.DataFrame: DataFrame with a new column 'Gender'.
        """
        gender_patterns = {
            "Women's": r"\bWomen's\b",
            "Men's": r"\bMen's\b",
            "Kids'": r"\bKids'\b",
            "Toddler": r"\bToddler\b",
            "Unisex": r"\bUnisex\b"
        }

        def detect_gender(name):
            for gender, pattern in gender_patterns.items():
                if re.search(pattern, name, re.IGNORECASE):
                    return gender
            return "Unspecified"
        
        self.df['Gender'] = self.df['Product Name'].apply(detect_gender)
        return self.df

    def extract_brand(self) -> pd.DataFrame:
        """
        Extracts the brand by identifying text before gender keywords in the 'Product Name' column.

        Returns:
        pd.DataFrame: DataFrame with a new column 'Brand'.
        """
        gender_keywords = ["Women's", "Men's", "Unisex", "Toddler", "Kids'"]
        gender_pattern = r'\b(?:' + '|'.join(gender_keywords) + r")\b"

        def detect_brand(name):
            match = re.search(gender_pattern, name, re.IGNORECASE)
            return name[:match.start()].strip() if match else "Unknown"

        self.df['Brand'] = self.df['Product Name'].apply(detect_brand)
        return self.df

    def extract_discount(self) -> pd.DataFrame:
        """
        Calculates the discount percentage based on 'Current Price' and 'Original Price'.

        Returns:
        pd.DataFrame: DataFrame with a new column 'Discount Percentage'.
        """
        # Calculate discount percentage and handle cases where Original Price is 0 or NaN
        self.df['Discount Percentage'] = ((self.df['Original Price'] - self.df['Current Price']) / 
                                          self.df['Original Price']).fillna(0) * 100
        self.df['Discount Percentage'] = self.df['Discount Percentage'].apply(lambda x: max(x, 0))  # Ensure non-negative values
        return self.df

    def get_data(self) -> pd.DataFrame:
        """
        Returns the DataFrame with all extracted features.
        
        Returns:
        pd.DataFrame: The DataFrame with extracted features.
        """
        return self.df
