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

headers = {
    "X-Shopify-Access-Token": access_token,
    "Content-Type": "application/json"
}

all_products = []
next_page_info = None
limit = 250  # Set the maximum limit allowed by the Shopify API

while True:
    if next_page_info:
        response = requests.get(
            f"{shopify_url}/admin/api/2024-07/products.json",
            headers=headers,
            params={"page_info": next_page_info, "limit": limit}
        )
    else:
        response = requests.get(
            f"{shopify_url}/admin/api/2024-07/products.json",
            headers=headers,
            params={"limit": limit}
        )
    
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # Append the products to the all_products list
        all_products.extend(data["products"])
        
        # Check if there are more pages to fetch
        if data.get("has_next_page"):
            next_page_info = data.get("next_page_info")
        else:
            break
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        break

# Save the data into a JSON file
with open("shopify_products_idList.json", "w") as file:
    json.dump({"products": all_products}, file, indent=4)

print(f"Data has been successfully saved to shopify_products_idList.json. Total products: {len(all_products)}")