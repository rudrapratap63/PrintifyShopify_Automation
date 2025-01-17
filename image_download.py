import json
import requests
import io
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import sys
import time
import os
from datetime import datetime

directory = sys.argv[1]
product_num = int(sys.argv[2])



#for delete the images
for filename in os.listdir(directory):
# Join the directory path and filename
    file_path = os.path.join(directory, filename)
    
    # Check if the file is an image file (you may need to modify this based on your file extensions)
    if file_path.endswith('.jpg') or file_path.endswith('.png') or file_path.endswith('.jpeg'):
        # Delete the file
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    else:
        print(f"Skipped: {file_path}")

print("All files deleted.")


global imageCount
imageCount = 0

failed_downloads = []

def download_image(image_data):
    global imageCount
    image_url, file_name = image_data
    retries = 3  # Number of retries
    retry_delay = 5  # Delay between retries in seconds

    for attempt in range(retries):
        try:
            image_content = requests.get(image_url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            image.save(f"{directory}/{file_name}", "JPEG")
            print(f"Success: {file_name}")
            imageCount += 1
            return
        except Exception as e:
            if attempt == retries - 1:  # If this was the last attempt
                failed_downloads.append({
                    'file_name': file_name,
                    'url': image_url,
                    'error': str(e),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            if isinstance(e, ConnectionError) or isinstance(e, requests.exceptions.ConnectionError):
                print(f"Retrying download for {file_name} (Attempt {attempt + 1}/{retries})")
                time.sleep(retry_delay)
            else:
                print(f"Retrying download for {file_name} (Attempt {attempt + 1}/{retries})")
                time.sleep(retry_delay)

    print(f"FAILED - {file_name}: Maximum number of retries reached.")

def process_product(product_data):
    image_data = []

    for num, image in enumerate(product_data['images']):
        image_url = image['src']
        variant_id = image['variant_ids'][0]
        is_mainImage = image['is_default']

        for variant in product_data['variants']:
            if variant_id == variant['id']:
                name = variant['title'].replace(" ", "").replace("/", "-")
                sku = variant['sku']
                if is_mainImage:
                    file_name = f"{name}__main__{sku}__{num}.jpg"
                else:
                    file_name = f"{name}__{sku}__{num}.jpg"
                image_data.append((image_url, file_name))
                break

    with ThreadPoolExecutor() as executor:
        executor.map(download_image, image_data)

with open('./printify_product_data.json') as f:
    data = json.load(f)

process_product(data['data'][product_num])

# Save failed downloads to a log file if any
if failed_downloads:
    log_filename = f"failed_downloads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_filename, 'w') as f:
        json.dump(failed_downloads, f, indent=2)
    print(f"\nSome downloads failed. Check {log_filename} for details.")

print("All Images download successfully ")
print(f"Total {imageCount} images downloaded")