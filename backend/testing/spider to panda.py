import pandas as pd

# Load the JSON data
df_energy = pd.read_json('energy_data.json')

# Load the original spreadsheet
df = pd.read_excel('230425_EPC_Charlie.xlsx')

# Merge the two DataFrames on the 'address' column
df_merged = pd.merge(df, df_energy, on='address', how='left')

# Update the corresponding columns in the original DataFrame
df_merged['kWh per year for heating'] = df_merged['heating_value']
df_merged['kWh per year for hot water'] = df_merged['hot_water_value']

# Save the updated spreadsheet
df_merged.to_excel('230425_EPC_Charlie_updated.xlsx', index=False)