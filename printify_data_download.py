import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

shop_id = os.getenv("SHOP_ID")
token = os.getenv("PRINTIFY_ACCESS_TOKEN")

# Debug: Print values (with partial masking for security)
print(f"Shop ID: {shop_id}")
print(f"Token: {token[:4]}...{token[-4:] if token else ''}")

# Initialize variables for pagination
all_products = []
page = 1
limit = 50  # Maximum limit allowed by Printify API (changed from 100)

while True:
    # Define the URL with pagination parameters
    url = f"https://api.printify.com/v1/shops/{shop_id}/products.json"
    
    # Set up the headers for the request
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Set up pagination parameters
    params = {
        "page": page,
        "limit": limit
    }

    print(f"\nMaking request to: {url}")
    print(f"With parameters: {params}")
    
    try:
        # Make the GET request to fetch product data
        response = requests.get(url, headers=headers, params=params)
        
        # Print response status and headers for debugging
        print(f"Response Status Code: {response.status_code}")
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()
            
            # Check if data exists and has the expected structure
            if isinstance(data, dict) and 'data' in data:
                current_page_products = data['data']
                if not current_page_products:
                    print("No more products to fetch")
                    break
                
                # Add the products from this page to our collection
                all_products.extend(current_page_products)
                print(f"Fetched page {page} with {len(current_page_products)} products")
                
                # Check if we've reached the total number of products
                total = data.get('total', 0)
                if len(all_products) >= total:
                    print(f"Reached total number of products ({total})")
                    break
                
                page += 1
            else:
                print(f"Unexpected response structure: {data}")
                break
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            if response.status_code == 401:
                print("Unauthorized access - check your access token.")
            elif response.status_code == 403:
                print("Forbidden - check your permissions.")
            print(f"Response: {response.text}")
            break
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        break
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Raw response: {response.text}")
        break
    except Exception as e:
        print(f"Unexpected error: {e}")
        break

# Create the final data structure
final_data = {
    "data": all_products
}

# Save the data into a JSON file
with open("printify_product_data.json", "w") as file:
    json.dump(final_data, file, indent=4)

print(f"\nFinal Summary:")
print(f"Total products fetched: {len(all_products)}")
print("Data has been saved to printify_product_data.json")
