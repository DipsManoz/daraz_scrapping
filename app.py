import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def extract(url):
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use webdriver_manager to automatically manage ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
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

# Streamlit App
st.title("Product Price Extractor")

# Input field for URL
url = st.text_input("Enter the URL of the product page:")

if st.button("Extract"):
    if url:
        with st.spinner("Extracting product information..."):
            # Call the extract function and display the result in Streamlit
            try:
                product_data = extract(url)
                st.success("Extraction successful!")
                st.write(product_data)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL")
