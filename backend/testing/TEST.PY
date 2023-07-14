import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the spreadsheet
df = pd.read_excel('C:/Users/laura.cullen/Downloads/230425_EPC_Charlie.xls')

# Set up the WebDriver (adjust the path to your WebDriver executable)
driver = webdriver.Chrome('c:/Users/laura.cullen/Downloads/chromedriver.exe')

# Iterate through each row of the spreadsheet
for index, row in df.iterrows():
    postcode = row['POSTCODE']
    address = row['ADDRESS1']

    # Construct the URL with the postcode
    url = f"https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?lang=en&property_type=domestic&postcode={postcode}"

    # Open the URL in the browser
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.result')))

    # Find the correct address link
    link = driver.find_element(By.LINK_TEXT, address)

    # Click on the link
    link.click()

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.text-centre')))

    # Extract the required numbers
    heating_text = driver.find_element(By.XPATH, "//p[contains(text(), 'heating')]").text
    hot_water_text = driver.find_element(By.XPATH, "//p[contains(text(), 'hot water')]").text

    heating_value = int(heating_text.split()[0].replace(',', ''))
    hot_water_value = int(hot_water_text.split()[0].replace(',', ''))

    # Update the corresponding cells in the spreadsheet
    df.at[index, 'kWh per year for heating'] = heating_value
    df.at[index, 'kWh per year for hot water'] = hot_water_value

# Save the updated spreadsheet
df.to_excel('230425_EPC_Charlie_updated.xlsx', index=False)

# Close the browser
driver.quit()
