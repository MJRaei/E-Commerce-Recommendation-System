from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the Selenium WebDriver (e.g., Chrome)
driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed

# Navigate to the webpage
url = 'https://www.sportchek.ca/en/search-results.html?q=boots'
driver.get(url)

# Wait for the page to load fully and for a specific element to be present
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'nl-product-card__title'))
    )
    print("Page is ready!")
except TimeoutException:
    print("Loading took too long!")

# Initialize lists to store product information
product_names = []
current_prices = []
original_prices = []
ratings = []
num_reviews = []
is_top_rated = []
is_best_seller = []
is_clearance = []
is_new = []
colors = []

# Function to scroll the page incrementally and load all items
def scroll_and_extract_items():
    SCROLL_PAUSE_TIME = 0.5  # Adjust as needed
    SCROLL_INCREMENT = 1000  # Scroll by 1000 pixels at a time

    while True:
        # Scroll down by SCROLL_INCREMENT pixels
        driver.execute_script(f"window.scrollBy(0, {SCROLL_INCREMENT});")

        # Wait for the page to load
        time.sleep(SCROLL_PAUSE_TIME)

        # Check if we've reached the bottom by comparing scroll height and window height
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight")

        if scroll_position >= scroll_height:
            break  # If we've reached the bottom, stop scrolling

    # Once the page is fully scrolled and loaded, get the page source
    html_content = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract product details from each product container
    for product in soup.find_all('li', class_='nl-product__content'):
        # Extract product name and other common attributes
        name_tag = product.find("div", class_="nl-product-card__title")
        product_name = name_tag.get_text(strip=True) if name_tag else None

        rating_tag = product.find("div", class_="bv_averageRating_component_container")
        rating = rating_tag.get_text(strip=True) if rating_tag else None

        review_tag = product.find("div", class_="bv_numReviews_component_container")
        num_review = review_tag.get_text(strip=True).replace("(", "").replace(")", "") if review_tag else None

        # Check for specific tags
        tag_container = product.find("div", class_="nl-plp-badges")
        tags = tag_container.find_all("span") if tag_container else []
        top_rated = any("Top Rated" in tag.get_text() for tag in tags)
        best_seller = any("Best Seller" in tag.get_text() for tag in tags)
        clearance = any("Clearance" in tag.get_text() for tag in tags)
        new = any("New" in tag.get_text() for tag in tags)

        # Find the color options and only click if there are multiple colors
        color_container = product.find("ul", class_="nl-variants__variant-list")
        color_elements = color_container.find_all("div", class_="nl-variants__variant--colour-swatches") if color_container else []

        if len(color_elements) > 1:  # Only click if more than one color
            for color_element in color_elements:
                color = color_element.get("aria-label", "").strip()
                
                # Click the color element to update the displayed price
                color_element_selenium = driver.find_element(By.XPATH, f"//div[@aria-label='{color}']")
                driver.execute_script("arguments[0].click();", color_element_selenium)
                time.sleep(2)  # Wait for the price to update

                # Extract the current and original prices for the selected color
                current_price_tag = product.find("span", class_="nl-price--total--red") or product.find("span", class_="nl-price--total")
                current_price = current_price_tag.get_text(strip=True) if current_price_tag else None

                original_price_tag = product.find("span", class_="sr-only")
                original_price = original_price_tag.get_text(strip=True).replace("price was", "").strip() if original_price_tag else None

                # Append each color variant as a new row
                product_names.append(product_name)
                current_prices.append(current_price)
                original_prices.append(original_price)
                ratings.append(rating)
                num_reviews.append(num_review)
                is_top_rated.append(top_rated)
                is_best_seller.append(best_seller)
                is_clearance.append(clearance)
                is_new.append(new)
                colors.append(color)
        else:  # If only one color, extract without clicking
            color = color_elements[0].get("aria-label", "").strip() if color_elements else None

            # Extract prices
            current_price_tag = product.find("span", class_="nl-price--total--red") or product.find("span", class_="nl-price--total")
            current_price = current_price_tag.get_text(strip=True) if current_price_tag else None

            original_price_tag = product.find("span", class_="sr-only")
            original_price = original_price_tag.get_text(strip=True).replace("price was", "").strip() if original_price_tag else None

            # Append the single color as a row
            product_names.append(product_name)
            current_prices.append(current_price)
            original_prices.append(original_price)
            ratings.append(rating)
            num_reviews.append(num_review)
            is_top_rated.append(top_rated)
            is_best_seller.append(best_seller)
            is_clearance.append(clearance)
            is_new.append(new)
            colors.append(color)

# Start scraping all pages
while True:
    # Scroll through and extract items on the current page
    scroll_and_extract_items()

    # Check if there is a "Next" button
    try:
        # Find the "Next" button using its rel attribute
        next_button = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')

        # Click the "Next" button if it exists
        if next_button:
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the next page to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'nl-product-card__title'))
            )

            print("Navigated to next page.")
            time.sleep(5)  # Adjust the wait time if necessary
        else:
            break  # If the "Next" button is not found, exit the loop
    except Exception as e:
        print(f"No more pages found or an error occurred: {e}")
        break

# Create a DataFrame with the scraped data
df_final_web = pd.DataFrame({
    'Product Name': product_names,
    'Current Price': current_prices,
    'Original Price': original_prices,
    'Rating': ratings,
    'Number of Reviews': num_reviews,
    'Top Rated': is_top_rated,
    'Best Seller': is_best_seller,
    'Clearance': is_clearance,
    'New': is_new,
    'Color': colors
})

# Save the data to CSV
df_final_web.to_csv('scraped_boots_with_colors.csv', index=False)

# Close the browser
driver.quit()

print("Data scraped and saved successfully.")
