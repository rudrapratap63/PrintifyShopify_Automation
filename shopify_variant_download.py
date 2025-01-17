import requests
import json
from dotenv import load_dotenv
import os
import sys

load_dotenv()

url = os.getenv("SHOPIFY_URL")
token = os.getenv("SHOPIFY_ACCESS_TOKEN")

shopify_url = f"{url}"
access_token = f"{token}"

product_id = int(sys.argv[2])

headers = {
    "X-Shopify-Access-Token": access_token,
    "Content-Type": "application/json"
}

response = requests.get(
    f"{shopify_url}/admin/api/2023-10/products/{product_id}/variants.json",
    headers=headers
)

if response.status_code == 200:
    # Parse the response JSON
    data = response.json()
    
    # Save the data into a JSON file
    with open("product_variants.json", "w") as file:
        json.dump(data, file, indent=4)
        
    print("Data has been successfully saved to printify_product_data.json")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(f"Response: {response.text}")


