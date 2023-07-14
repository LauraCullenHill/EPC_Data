import base64
import requests

# Set your email address and API key
email = 'laurahill207@hotmail.com'
API_KEY = 'aaa8ef5e43a9afd27e1ddedfdd2821c021838825'

# Base64-encode the email and API key
token = base64.b64encode(f'{email}:{API_KEY}'.encode()).decode()

# Get the authentication token
def get_auth_token():
    return token

# Define the headers
headers = {
    'Authorization': f'Basic {get_auth_token()}',
    'Accept': 'application/json' 
}

# Certificate LMK key to retrieve
lmk_key = '219873319402019053122194154717408'

# API endpoint for retrieving the certificate
api_endpoint_url = f'https://epc.opendatacommunities.org/api/v1/domestic/certificate/{lmk_key}'

# Make a GET request to retrieve the certificate
response = requests.get(api_endpoint_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Connected to the API.")
else:
    print("Failed to connect to the API.")

