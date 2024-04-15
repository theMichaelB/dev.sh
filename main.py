import json
import requests
import os

def get_access_token(client_id, client_secret, tenantId, scope=None):
    
    token_url = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    
    # Get the credentials

    
    # Set the scope (if not provided)
    if scope is None:
        scope = "https://graph.microsoft.com/.default"
    
    # Set the request parameters
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope
    }
    
    # Make the request
    response = requests.post(token_url.format(tenant=tenantId), data=data)
    
    # Save the token
    token = response.json()['access_token']
    with open('./.credentials/token.txt', 'w') as file:
        file.write(token)

    return token


def get_credentials():
    # Get the credentials from environment variables
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    tenantId = os.environ.get('TENANT_ID')
    subscriptionId = os.environ.get('SUBSCRIPTION_ID')
    
    return client_id, client_secret, tenantId, subscriptionId
    

def get_azure_locations(access_token, subscriptionId):
    # Define the URL
    api_version = "2022-12-01"
    endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/locations?api-version={api_version}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Make the request
    response = requests.get(endpoint, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        locations = response.json()["value"]
        for location in locations:
            print(location["name"])
    else:
        print(f"Error: {response.status_code}") 
        return None

    

    locations = response.json()["value"]
    blank_subscriptionId = "00000000-0000-0000-0000-000000000000"

    # dump to text string 
    json_str = json.dumps(locations, indent=4)

    # search string for subscriptionId and replace with blank_subscriptionId
    json_str = json_str.replace(subscriptionId, blank_subscriptionId)

    # write to file 
    with open('./output/locations.json', 'w') as file:
        file.write(json_str)

def main():
    client_id, client_secret, tenantId, subscriptionId = get_credentials()
    
    # Define the scope
    scope = "https://management.azure.com/.default"
    
    # Get the access token
    access_token = get_access_token(client_id, client_secret, tenantId, scope)
    
    # Get the Azure locations
    get_azure_locations(access_token, subscriptionId)

if __name__ == "__main__":
    main()
