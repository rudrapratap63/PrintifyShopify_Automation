import tkinter as tk
from tkinter import filedialog
import subprocess
import json
import re
from tkinter import ttk
from tkinter import font as tkfont

global containProductId
containProductId = None 

productArrayWant = ["iPhone Case - Illuminati Part",
                    "iPhone Case - Illunminati Dark",
                    "iPhone Case - Inspire Healthy Life Style",
                    "iPhone Case - Jolly Office Culture",
                    "iPhone Case - Loki",
                    "iPhone Case - Love Nature Food",
                    ]
productArray = ["iPhone Case - Golden Vein White Marble",
                    "iPhone Case - Greenish Marble",
                    "iPhone Case - Hulk",
                    "iPhone Case - I love you Mom",
                    "iPhone Case - Illuminati Abstract",
                    "iPhone Case - Illuminati Part",
                    "iPhone Case - Illunminati Dark",
                    "iPhone Case - Inspire Healthy Life Style",
                    "iPhone Case - Jolly Office Culture",
                    "iPhone Case - Loki",
                    "iPhone Case - Love Nature Food",
                    ]


def load_product_ids():
    try:
        with open("shopify_products_idList.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("shopify_products_idList.json file not found.")
        return 
    global product_id_options
    product_id_options = {}  # Initialize as an empty dictionary
    
    for product in data["products"]:
        x = product['title'].split(" ")
        title = "".join(x).lower()
        product_id = product['id']
        product_id_options[title] = product_id  # Add key-value pair to dictionary
            
    
def get_product_id(product_title, product_id_options):
    return product_id_options.get(product_title, None)


def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)
    else:
        directory_entry.insert(0, "img")
        
def run_printify_data_download(search_product_num):
    global containProductId
    
    
    
    directory = directory_entry.get()
    if directory == "":
        directory = "img"
    # search_product_num = search_var.get()
    print("in printify data download : "+search_product_num)
    x = search_product_num.split(", ")[0].split(" ")
    product_title = "".join(x).lower()
    print("in printify down prod title : "+product_title)
    
    containProductId = get_product_id(product_title, product_id_options)
    if not containProductId:
        print("you need to manually put product id for uploading")
    
    product_num = search_product_num.split(", ")[1]
    # product_num = search_product_num
    subprocess.run(["python", "printify_data_download.py"])
    subprocess.run(["python", "image_download.py", directory, product_num])

def run_shopify_data_upload():
    global containProductId
    
    directory = directory_entry.get()
    if directory == "":
        directory = "img"
        
    if containProductId:
        product_info = str(containProductId)
        product_id = re.findall(r'\d+', product_info)[0]
        
        subprocess.run(["python", "shopify_variant_download.py", directory,product_id])
        subprocess.run(["python", "image_upload.py", directory, product_id])
        
    elif search_dropdown.get() != "Enter product name...":
        # Get the product title from dropdown and find its ID
        selected_product = search_dropdown.get()
        x = selected_product.split(", ")[0].split(" ")
        product_title = "".join(x).lower()
        product_id = get_product_id(product_title, product_id_options)
        
        if product_id:
            subprocess.run(["python", "shopify_variant_download.py", directory, str(product_id)])
            subprocess.run(["python", "image_upload.py", directory, str(product_id)])
        else:
            print("Could not find product ID for the selected product")
            
    elif product_id_entry.get().strip():  # Check if manual product ID is entered
        product_id = product_id_entry.get()
        
        subprocess.run(["python", "shopify_variant_download.py", directory,product_id])
        subprocess.run(["python", "image_upload.py", directory, product_id])
    else:
        print("Please either select a product from dropdown or enter a product ID manually")


def download_and_upload():
    # Implement the logic to download and upload data
    try:
        with open("printify_product_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("printify_product_data.json file not found.")
        return
    
    for product in productArrayWant: 
        for num in range(len(data['data'])):
            if(product == data['data'][num]['title']):
                titleProduct = f"{data['data'][num]['title']}, {num}"
                run_printify_data_download(titleProduct)
                run_shopify_data_upload()
                
def download_essential_data_for_searchField():
    subprocess.run(["python", "printify_data_download.py"])
    subprocess.run(["python", "shopify_products.py"])
    
    refresh_search()

def refresh_search():
    populate_search_options()
    load_product_ids()
    search_dropdown.delete(0, tk.END)
    

def populate_search_options():
    try:
        with open("printify_product_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("printify_product_data.json file not found.")
        return
    
    global search_options
    search_options = []
    for num in range(len(data['data'])):
        search_options.append(f"{data['data'][num]['title']}, {num}")
    
    search_dropdown.configure(values=search_options)

root = tk.Tk()
root.title("Printify to Shopify Automation")

# Set a custom font for the application
custom_font = tkfont.Font(family="Arial", size=10)

# Main Frames
left_frame = tk.Frame(root, bg="#f0f0f0")
left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

center_frame = tk.Frame(root, bg="#f0f0f0")
center_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

right_frame = tk.Frame(root, bg="#f0f0f0")
right_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Left Frame - Downloading
download_label = tk.Label(left_frame, text="Download", font=("Arial", 18, "bold"), bg="#f0f0f0")
download_label.pack(pady=15)

search_label = tk.Label(left_frame, text="Product Name:", font=custom_font, bg="#f0f0f0")
search_label.pack(anchor=tk.W, pady=5)

search_var = tk.StringVar()
search_dropdown = ttk.Combobox(left_frame, textvariable=search_var, width=35, font=custom_font)
search_dropdown.pack(anchor=tk.W, pady=5)

search_dropdown.insert(0, "Enter product name...")
search_dropdown.config(state="readonly")

directory_frame = tk.Frame(left_frame, bg="#f0f0f0")
directory_frame.pack(anchor=tk.W, pady=10)

directory_label = tk.Label(directory_frame, text="Select Directory:", font=custom_font, bg="#f0f0f0")
directory_label.pack(side=tk.TOP, padx=5)

directory_entry = tk.Entry(directory_frame, width=25, font=custom_font)
directory_entry.pack(side=tk.LEFT, padx=5)

select_directory_button = tk.Button(directory_frame, text="Select", command=select_directory, font=custom_font, bg="#007bff", fg="white", padx=10, pady=5)
select_directory_button.pack(side=tk.LEFT, padx=5)

run_printify_data_button = tk.Button(left_frame, text="Run Printify Data Download", command=run_printify_data_download, font=custom_font, bg="#28a745", fg="white", padx=10, pady=5)
run_printify_data_button.pack(anchor=tk.W, pady=10)

# Center Frame - Essential Data
essential_data_label = tk.Label(center_frame, text="Essential Data", font=("Arial", 18, "bold"), bg="#f0f0f0")
essential_data_label.pack(pady=15)

essential_data_for_searchField_button = tk.Button(center_frame, text="Download Essential Data", command=download_essential_data_for_searchField, font=custom_font, bg="#007bff", fg="white", padx=10, pady=5)
essential_data_for_searchField_button.pack(pady=10)

refresh_button = tk.Button(center_frame, text="Refresh", command=refresh_search, font=custom_font, bg="#6c757d", fg="white", padx=10, pady=5)
refresh_button.pack(pady=10)

download_upload_button = tk.Button(center_frame, text="Download + Upload", command=download_and_upload, font=custom_font, bg="#28a745", fg="white", padx=10, pady=5)
download_upload_button.pack(pady=10)

# Right Frame - Uploading
upload_label = tk.Label(right_frame, text="Upload", font=("Arial", 18, "bold"), bg="#f0f0f0")
upload_label.pack(pady=15)

product_id_label = tk.Label(right_frame, text="Product id. :", font=custom_font, bg="#f0f0f0")
product_id_label.pack(anchor=tk.W, pady=5)

product_id_entry = tk.Entry(right_frame,  width=35, font=custom_font)
product_id_entry.pack(anchor=tk.W, pady=5)


run_shopify_data_button = tk.Button(right_frame, text="Run Shopify Data Upload", command=run_shopify_data_upload, font=custom_font, bg="#007bff", fg="white", padx=10, pady=5)
run_shopify_data_button.pack(pady=10)

# Call functions to populate options
populate_search_options()
load_product_ids()



root.mainloop()