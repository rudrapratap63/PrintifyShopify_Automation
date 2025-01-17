import json
import os
import sys
from datetime import datetime
import requests
import base64
import io
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def retry_failed_downloads(failed_downloads_file):
    """Retry downloading images that previously failed"""
    with open(failed_downloads_file, 'r') as f:
        failed_downloads = json.load(f)
    
    new_failed_downloads = []
    success_count = 0
    
    print(f"\nRetrying {len(failed_downloads)} failed downloads...")
    
    for item in failed_downloads:
        file_name = item['file_name']
        image_url = item['url']
        directory = os.path.dirname(file_name)
        
        try:
            image_content = requests.get(image_url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            
            # Ensure directory exists
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            image.save(file_name, "JPEG")
            print(f"Success: {file_name}")
            success_count += 1
            
        except Exception as e:
            print(f"Failed again: {file_name} - {str(e)}")
            new_failed_downloads.append({
                'file_name': file_name,
                'url': image_url,
                'error': str(e),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    if new_failed_downloads:
        new_log_filename = f"failed_downloads_retry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(new_log_filename, 'w') as f:
            json.dump(new_failed_downloads, f, indent=2)
        print(f"\nSome downloads still failed. Check {new_log_filename} for details.")
    
    print(f"\nRetry Results:")
    print(f"Successfully downloaded: {success_count}")
    print(f"Still failed: {len(new_failed_downloads)}")

def retry_failed_uploads(failed_uploads_file):
    """Retry uploading images that previously failed"""
    with open(failed_uploads_file, 'r') as f:
        failed_uploads = json.load(f)
    
    # Get Shopify credentials
    shopify_url = os.getenv("SHOPIFY_URL")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    new_failed_uploads = []
    success_count = 0
    
    print(f"\nRetrying {len(failed_uploads)} failed uploads...")
    
    for item in failed_uploads:
        file_name = item['file_name']
        product_id = item['product_id']
        
        try:
            # Read and encode the image
            with open(file_name, "rb") as image_file:
                image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
            
            # Prepare upload data
            if "main" in file_name.lower():
                data = {
                    "image": {
                        "attachment": base64_image,
                        "filename": os.path.basename(file_name)
                    }
                }
            else:
                data = {
                    "image": {
                        "attachment": base64_image,
                        "filename": os.path.basename(file_name)
                    }
                }
            
            # Upload to Shopify
            response = requests.post(
                f"{shopify_url}/admin/api/2023-10/products/{product_id}/images.json",
                json=data,
                headers=headers,
                timeout=(60, 120)
            )
            
            if response.status_code == 200:
                print(f"Success: {file_name}")
                success_count += 1
            else:
                raise Exception(f"Status code: {response.status_code}")
                
        except Exception as e:
            print(f"Failed again: {file_name} - {str(e)}")
            new_failed_uploads.append({
                'file_name': file_name,
                'product_id': product_id,
                'error': str(e),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    if new_failed_uploads:
        new_log_filename = f"failed_uploads_retry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(new_log_filename, 'w') as f:
            json.dump(new_failed_uploads, f, indent=2)
        print(f"\nSome uploads still failed. Check {new_log_filename} for details.")
    
    print(f"\nRetry Results:")
    print(f"Successfully uploaded: {success_count}")
    print(f"Still failed: {len(new_failed_uploads)}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python retry_failed_images.py <download|upload> <failed_log_file>")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    log_file = sys.argv[2]
    
    if not os.path.exists(log_file):
        print(f"Error: Log file {log_file} not found")
        sys.exit(1)
    
    if action == "download":
        retry_failed_downloads(log_file)
    elif action == "upload":
        retry_failed_uploads(log_file)
    else:
        print("Error: First argument must be either 'download' or 'upload'")
        sys.exit(1)

if __name__ == "__main__":
    main() 