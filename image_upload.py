import requests
import base64
import os
import re
import json
from dotenv import load_dotenv
import sys
import threading
import multiprocessing
import queue
import time

load_dotenv()

# Set the directory where the JPG files are located
directory = sys.argv[1]
count = 0

url = os.getenv("SHOPIFY_URL")
token = os.getenv("SHOPIFY_ACCESS_TOKEN")

shopify_url = f"{url}"
access_token = f"{token}"

headers = {
    "X-Shopify-Access-Token": access_token,
    "Content-Type": "application/json"
}

# Read the JSON file once
with open('./product_variants.json', 'r') as file:
    data = json.load(file)

def extract_sku(file_name):
    pattern = r'__(\d+)__'
    match = re.search(pattern, file_name)
    if match:
        return match.group(1)
    else:
        return None

def extract_ids(sku):
    for variant in data['variants']:
        if variant['sku'] == sku:
            return variant['id'], variant['product_id']
    return None, None

def process_file(file_name, file_path):
    sku = extract_sku(file_name)
    if sku:
        print(f"Processing file: {file_name}")
        # print(f"SKU: {sku}")

        variant_id, product_id = extract_ids(sku)

        modified_file_path = file_path.replace("\\", "/")
        product_ids = set()
        images = []

        with open(modified_file_path, "rb") as image_file:
            image_data = image_file.read()

        base64_image = base64.b64encode(image_data).decode("utf-8")

        if "main" in file_name.lower():
            data = {
                "image": {
                    "variant_ids": [variant_id],
                    "attachment": base64_image,
                    "filename": file_name
                }
            }
        else:
            data = {
                "image": {
                    "attachment": base64_image,
                    "filename": file_name
                }
            }

        if len(data["image"]["attachment"]) > 0:
            product_ids.add(product_id)
            images.append(data)

    if len(images) > 0:
        retry_count = 0
        max_retries = 5
        retry_delay = 2  # Initial delay in seconds

        while retry_count < max_retries:
            global count
            try:
                update_response = requests.post(
                    f"{shopify_url}/admin/api/2023-10/products/{product_id}/images.json",
                    json=data,
                    headers=headers,
                    timeout=(60, 120)
                )
                update_response.raise_for_status()
                if update_response.status_code == 200:
                    count+=1
                    print(f"Image updated successfully. Count: {count}")
                elif update_response.status_code == 409:
                    print("Error updating image:", update_response.status_code, update_response.text)
                else:
                    print("Error updating image:", update_response.status_code, update_response.text)
                break
            except requests.exceptions.RequestException as e:
                retry_count += 1
                print(f"Error uploading image: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
        else:
            print("Maximum retries reached. Unable to upload image.")
    else:
        print(f"Invalid file name format: {file_name}")

def worker():
    while True:
        try:
            filename, file_path = file_queue.get(block=False)
            process_file(filename, file_path)
            file_queue.task_done()
        except queue.Empty:
            break

if __name__ == "__main__":
    # Create a queue to hold the file paths
    file_queue = multiprocessing.JoinableQueue()

    # Create a pool of worker threads
    num_threads = 4
    thread_pool = [threading.Thread(target=worker) for _ in range(num_threads)]

    # Populate the queue with file paths
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".JPG"):
            file_path = os.path.join(directory, filename)
            file_queue.put((filename, file_path))

    # Start the worker threads
    for thread in thread_pool:
        thread.start()

    # Wait for the worker threads to finish
    file_queue.join()

    print("All files processed.")
    print(f"Total Image Uploaded is {count}")
    