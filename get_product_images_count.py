import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime

def get_product_images_count():
    # Load environment variables
    load_dotenv()
    
    url = os.getenv("SHOPIFY_URL")
    token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    shopify_url = f"{url}"
    access_token = f"{token}"
    
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    # Read the product IDs from shopify_products_idList.json
    try:
        with open("shopify_products_idList.json", "r") as file:
            products_data = json.load(file)
    except FileNotFoundError:
        print("Error: shopify_products_idList.json not found")
        return
    
    # Initialize results list
    results = []
    total_images = 0
    
    # Process each product
    for product in products_data["products"]:
        product_id = product["id"]
        product_title = product["title"]
        
        try:
            # Make API request to get image count
            response = requests.get(
                f"{shopify_url}/admin/api/2025-01/products/{product_id}/images/count.json",
                headers=headers
            )
            
            if response.status_code == 200:
                count_data = response.json()
                image_count = count_data.get("count", 0)
                total_images += image_count
                
                results.append({
                    "product_id": product_id,
                    "title": product_title,
                    "image_count": image_count
                })
                print(f"Successfully got count for product {product_id}: {image_count} images")
            else:
                print(f"Failed to get count for product {product_id}. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error processing product {product_id}: {str(e)}")
    
    # Prepare final output
    output_data = {
        "total_images": total_images,
        "total_products": len(results),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "products": results
    }
    
    # Save to JSON file
    output_filename = f"product_image_counts.json"
    
    try:
        with open(output_filename, "w") as file:
            json.dump(output_data, file, indent=4)
        print(f"\nResults saved to {output_filename}")
        print(f"Total images across all products: {total_images}")
        print(f"Total products processed: {len(results)}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    get_product_images_count() 