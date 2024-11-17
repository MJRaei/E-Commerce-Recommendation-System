# E-Commerce Recommendation System

This project demonstrates a complete pipeline for analyzing e-commerce data, focusing on data cleaning, feature engineering, and discovering exceptional deals using autoencoders. The system employs robust data science techniques and tools to extract insights and highlight unique deals to users based on product attributes.

## Project Highlights

### 1. **Web Scraping**
- Implemented a custom scraper to gather real-world data, showcasing the integration of external data sources into the pipeline.
- Scraped product details, ratings, prices, and reviews, forming the foundation of the analysis.

### 2. **Data Preparation**
- Automated data ingestion pipelines to handle raw data from multiple formats (CSV, ZIP) and load it into structured DataFrames.
- Cleaned and standardized data by:
  - Formatting price columns.
  - Removing extraneous whitespace and converting boolean columns into numeric formats.
  - Addressing missing values through dropping or filling using statistical methods (mean, median, mode).
- Ensured high-quality, structured data for analysis and modeling.

### 3. **Exploratory Data Analysis (EDA)**
- Conducted comprehensive univariate, bivariate, and multivariate analyses to uncover patterns and relationships within the data.
- Visualized key insights to guide feature selection and modeling decisions.

### 4. **Feature Engineering and Extraction**
- Transformed raw data into meaningful features using techniques such as log transformations, scaling, and one-hot encoding.
- Extracted critical features such as product gender classification, brand identification, and discount percentages from textual and numeric data.

### 5. **Exceptional Deal Finder**
- Built a system to identify and highlight exceptional deals by leveraging autoencoders for anomaly detection.
- The autoencoder model evaluates product features such as discounts, ratings, reviews, and other attributes, assigning a "worthiness score" to each product.
- Exceptional deals are detected based on reconstruction errors, representing deviations from typical product data.
- Delivered personalized insights into the best deals, filtered by user preferences, such as gender and product type.

### 6. **Training Pipeline**
- Automated the entire data preparation and modeling pipeline using ZenML.
- Enabled reproducible workflows by modularizing steps for data ingestion, cleaning, engineering, and model evaluation.

## Technologies Used
- **Languages**: Python
- **Libraries**: Pandas, NumPy, TensorFlow, MLflow
- **Frameworks**: ZenML for pipeline automation
- **Tools**: Jupyter Notebook for EDA, custom-built modules for modularization

## Key Skills Demonstrated
- End-to-end pipeline development for data science projects.
- Advanced feature engineering and extraction techniques.
- Building and deploying anomaly-based deal discovery systems.
- Integration of machine learning and anomaly detection.
- Automation of workflows for scalable and reproducible results.
