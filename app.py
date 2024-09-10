import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Streamlit app title and description
st.title("Product Price Scraper")
st.write("Enter the URL of the product page to scrape product names and prices, then download the data as a CSV file.")

# Method to extract data
def extract(url):
     # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    
    # Set up the WebDriver (make sure to have the correct ChromeDriver version installed)
    driver = webdriver.Chrome()
    driver.get(url)

    # Extract the page source and parse it with BeautifulSoup
    code = driver.page_source
    soup = BeautifulSoup(code, 'html.parser')

    # Find all products based on the class name
    products = soup.find_all(class_='buTCk')

    product_list = []
    price_list = []

    # Loop through products and extract product names and prices
    for item in products:
        product_name = item.find(class_='RfADt')
        product_price = item.find(class_='ooOxS')

        if product_name and product_price:
            product_list.append(product_name.text)
            price_list.append(product_price.text)

    # Close the driver after extraction
    driver.quit()

    # Create a DataFrame with the extracted data
    product_price_df = pd.DataFrame({'product': product_list, 'price': price_list})

    return product_price_df

# Streamlit user input
url = st.text_input("Enter the product page URL")

# When the "Scrape Data" button is pressed
if st.button("Scrape Data"):
    if url:
        with st.spinner('Scraping data...'):
            try:
                df = extract(url)
                st.success("Data scraped successfully!")
                st.write(df)

                # Button to download the CSV file
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='product_price.csv',
                    mime='text/csv',
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a URL.")


