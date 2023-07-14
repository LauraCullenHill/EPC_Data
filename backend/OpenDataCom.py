import pandas as pd
import requests
import json
import re
from API import get_auth_token

# Read the spreadsheet containing the postcodes and addresses
df = pd.read_excel('C:/Users/laura.cullen/Downloads/230425_EPC_Charlie.xls')

# Create empty columns in the DataFrame for the certificate data and match status
column_names = []
certificate_data = {}
df['MATCH_STATUS'] = ""

# Set the headers for API authentication
headers = {
    'Authorization': f'Basic {get_auth_token()}',
    'Accept': 'application/json'
}

# Initialize counters for matched and unmatched properties
matched_count = 0
unmatched_count = 0

# Loop through the rows and retrieve the EPC data
for index, row in df.iterrows():
    postcode = row['POSTCODE']
    address = row['ADDRESS1']

    # Skip rows with missing or invalid postcodes or addresses
    if pd.isnull(postcode) or pd.isnull(address) or not isinstance(postcode, str) or not isinstance(address, str):
        print(f"Skipping invalid postcode or address at row {index}")
        continue

    # Remove any whitespace from the postcode and address
    postcode = postcode.strip()
    address = address.strip()

    # Extract only the numeric part from the address
    numeric_address = re.sub(r'\D', '', address)

    # Search for the property based on the postcode and numeric address
    search_url = f'https://epc.opendatacommunities.org/api/v1/domestic/search?postcode={postcode}&address={numeric_address}'
    response = requests.get(search_url, headers=headers)

    # Check if the response contains valid JSON data
    try:
        search_results = response.json()
    except json.JSONDecodeError:
        print(f"Invalid JSON response for postcode: {postcode} and address: {numeric_address}")
        print(f"Response Content: {response.content}")
        continue

    if 'rows' in search_results:
        rows = search_results['rows']
        if rows:
            property_id = rows[0].get('lmk-key')
            if property_id:
                # Retrieve the certificate data
                certificate_url = f'https://epc.opendatacommunities.org/api/v1/domestic/certificate/{property_id}'
                response = requests.get(certificate_url, headers=headers)

                # Check if the response is valid
                if response.status_code == 200:
                    # Extract the certificate data
                    certificate_data = response.json()

                    # Store the column names for the certificate data
                    if not column_names:
                        column_names = certificate_data['column-names']
                        # Create new columns in the DataFrame with the same column headings as the API
                        for column in column_names:
                            df[column] = ""

                    # Update the corresponding columns in the DataFrame
                    for column in column_names:
                        df.loc[index, column] = certificate_data['rows'][0].get(column)

                    # Set match status as "Matched"
                    df.loc[index, 'MATCH_STATUS'] = "Matched"
                    matched_count += 1
                else:
                    print(f"Failed to download certificate for postcode: {postcode} and address: {numeric_address}")
                    continue
            else:
                print(f"Missing property ID for postcode: {postcode} and address: {numeric_address}")
                # Set match status as "Not Matched"
                df.loc[index, 'MATCH_STATUS'] = "Not Matched"
                unmatched_count += 1
                continue
        else:
            print(f"No search results for postcode: {postcode} and address: {numeric_address}")
            # Set match status as "Not Matched"
            df.loc[index, 'MATCH_STATUS'] = "Not Matched"
            unmatched_count += 1
            continue
    else:
        print(f"Invalid JSON response for postcode: {postcode} and address: {numeric_address}")
        print(f"Response Content: {response.content}")
        continue

# Save the updated DataFrame as a CSV file
df.to_csv('updated_spreadsheet.csv', index=False)

# Print the counts of matched and unmatched properties
print(f"Matched properties: {matched_count}")
print(f"Unmatched properties: {unmatched_count}")

