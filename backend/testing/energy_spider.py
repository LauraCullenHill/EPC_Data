import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Load the original spreadsheet
df = pd.read_excel('C:/Users/laura.cullen/Downloads/230425_EPC_Charlie.xls')


# Create new columns for the energy values
df['kWh per year for heating'] = ""
df['kWh per year for hot water'] = ""

# Iterate through each row of the spreadsheet
for index, row in df.iterrows():
    postcode = row['POSTCODE']
    address = row['ADDRESS1']
    
    # Construct the URL with the postcode
    url = f"https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?lang=en&property_type=domestic&postcode={postcode}"
    
    print(f"Processing address: {address}")
    
    # Retry a few times in case of network errors
    max_retries = 3
    retries = 0
    success = False
    
    while retries < max_retries and not success:
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            
            if response.status_code == 200:
                print("Successfully retrieved search page")
                
                # Parse the HTML content of the response
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find the correct address link
                link = soup.find("a", string=address)
                
                if link:
                    print("Found matching address link")
                    
                    # Get the link URL
                    link_url = link['href']
                    
                    # Retry a few times in case of network errors
                    address_retries = 0
                    address_success = False
                    
                    while address_retries < max_retries and not address_success:
                        try:
                            # Send a GET request to the address link
                            response_address = requests.get(link_url)
                            
                            if response_address.status_code == 200:
                                print("Successfully retrieved address page")
                                
                                # Parse the HTML content of the response
                                soup_address = BeautifulSoup(response_address.content, 'html.parser')
                                
                                # Extract the required numbers
                                heating_value_tag = soup_address.find("p", string="heating")
                                hot_water_value_tag = soup_address.find("p", string="hot water")
                                
                                if heating_value_tag and hot_water_value_tag:
                                    heating_value = heating_value_tag.find_next("p").text.split()[0].replace(',', '')
                                    hot_water_value = hot_water_value_tag.find_next("p").text.split()[0].replace(',', '')
                                    
                                    print("Successfully extracted energy values")
                                    
                                    # Update the corresponding columns in the DataFrame
                                    df.at[index, 'kWh per year for heating'] = heating_value
                                    df.at[index, 'kWh per year for hot water'] = hot_water_value
                                    
                                    # Set success flag
                                    success = True
                                    address_success = True
                                else:
                                    print("Failed to extract energy values")
                            else:
                                print("Failed to retrieve address page")
                            
                        except requests.exceptions.RequestException as e:
                            print(f"Error retrieving address page: {str(e)}")
                            address_retries += 1
                            time.sleep(1)  # Add a small delay before retrying
                    
                else:
                    print("Matching address link not found")
                    
            else:
                print("Failed to retrieve search page")
                
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving search page: {str(e)}")
            retries += 1
            time.sleep(1)  # Add a small delay before retrying

# Save the updated spreadsheet
df.to_excel('230425_EPC_Charlie_updated.xlsx', index=False)


# Save the updated spreadsheet
df.to_excel('C:/Users/laura.cullen/Downloads/230425_EPC_Charlie.xls', index=False)
