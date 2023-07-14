import openpyxl
import requests
import csv
import pandas as pd

# Function to retrieve energy usage data from the UK government site for a given postcode ---------------

def retrieve_energy_usage(postcode):
    energy_usage = {
        'space_heating': '',
        'water_heating': ''
    }
    search_url = f"https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?lang=en&property_type=domestic&postcode={postcode}"
    response = requests.get(search_url)

    if response.status_code == 200:
        # Extract the energy usage data from the response
        text = response.text
        space_heating_start = text.find("Estimated energy needed in this property is:") + len("Estimated energy needed in this property is:")
        space_heating_end = text.find("kWh per year for heating", space_heating_start)
        energy_usage['space_heating'] = text[space_heating_start:space_heating_end].strip().replace(",", "")

        water_heating_start = text.find("kWh per year for hot water") + len("kWh per year for hot water")
        water_heating_end = text.find(".", water_heating_start)
        energy_usage['water_heating'] = text[water_heating_start:water_heating_end].strip().replace(",", "")

    print(f"Postcode: {postcode}, Space Heating: {energy_usage['space_heating']}, Water Heating: {energy_usage['water_heating']}")
    return energy_usage


# Specify the file paths
excel_file_path = 'C:/Users/laura.cullen/Downloads/230425_EPC_Charlie.xls'
csv_file_path = r"C:/Users/laura.cullen/Downloads/230425_EPC_Charlie.csv"
sheet_name = "230425_EPC_Master_sample"

# Load the Excel file using pandas
excel_file = pd.ExcelFile(excel_file_path)

# Read the specified sheet into a DataFrame
df = excel_file.parse(sheet_name)

# Retrieve the postcodes from the DataFrame
postcodes = df["POSTCODE"].tolist()

# Update the CSV file with the retrieved energy usage data
with open(csv_file_path, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row to the CSV file
    csv_writer.writerow(df.columns.tolist() + ["Estimated energy used: space heating (kWh/A)", "Estimated energy used: water heating (kWh/A)"])

    # Iterate over the postcodes
    for postcode in postcodes:
        energy_usage = retrieve_energy_usage(postcode)

        # Create a new row with the retrieved energy usage data
        new_row = df[df["POSTCODE"] == postcode].values.flatten().tolist()
        new_row += [str(energy_usage['space_heating']), str(energy_usage['water_heating'])]
        csv_writer.writerow(new_row)

print("CSV file updated successfully.")
