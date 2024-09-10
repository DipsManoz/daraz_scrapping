import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Method to extract data
def extract(url): 
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
    
    # Save the DataFrame to a CSV file
    product_price_df.to_csv('product_price.csv', index=False)
    print("CSV file downloaded successfully.")

# Take URL input from the user
url = input("Enter the URL: ")

# Call the function
extract(url)
