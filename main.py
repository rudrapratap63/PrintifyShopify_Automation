import tkinter as tk
from tkinter import filedialog, ttk, font as tkfont
import subprocess
import json
import re
import os

class PrintifyShopifyAutomation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Printify to Shopify Automation")
        self.selected_products = set()
        self.product_id_options = {}
        self.search_options = []
        self.containProductId = None
        
        # Set up fonts and styles
        self.custom_font = tkfont.Font(family="Arial", size=10)
        self.style = ttk.Style()
        self.style.configure("TCheckbutton", background="#f0f0f0")
        self.style.configure("TFrame", background="#f0f0f0")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frames
        self.left_frame = self.create_frame()
        self.center_frame = self.create_frame()
        self.right_frame = self.create_frame()
        
        # Set up the UI components
        self.setup_left_frame()
        self.setup_center_frame()
        self.setup_right_frame()
        
        # Initialize data
        self.load_product_ids()
        self.populate_search_options()

    def create_frame(self):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
        return frame

    def setup_left_frame(self):
        # Download section
        tk.Label(self.left_frame, text="Download", font=("Arial", 18, "bold"), 
                bg="#f0f0f0").pack(pady=15)
        
        # Directory selection
        self.directory_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        self.directory_frame.pack(anchor=tk.W, pady=10)
        
        self.directory_entry = tk.Entry(self.directory_frame, width=25, font=self.custom_font)
        self.directory_entry.insert(0, "img")
        self.directory_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.directory_frame, text="Select Directory", 
                 command=self.select_directory, font=self.custom_font,
                 bg="#007bff", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Products selection
        self.products_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        self.products_frame.pack(fill="both", expand=True, pady=10)
        
        tk.Label(self.products_frame, text="Select Products:", 
                font=self.custom_font, bg="#f0f0f0").pack(anchor="w", padx=5)

    def setup_center_frame(self):
        # Essential Data section
        tk.Label(self.center_frame, text="Essential Data", 
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=15)
        
        tk.Button(self.center_frame, text="Download Essential Data",
                 command=self.download_essential_data,
                 font=self.custom_font, bg="#007bff", fg="white").pack(pady=10)
        
        tk.Button(self.center_frame, text="Download + Upload",
                 command=self.download_and_upload,
                 font=self.custom_font, bg="#28a745", fg="white").pack(pady=10)
        
        # Add button to get product image count
        tk.Button(self.center_frame, text="Get Product Image Count",
                 command=self.get_product_image_count,
                 font=self.custom_font, bg="#17a2b8", fg="white").pack(pady=10)

    def setup_right_frame(self):
        # Upload section
        tk.Label(self.right_frame, text="Upload", 
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=15)
        
        # Add product ID label
        tk.Label(self.right_frame, text="Product id. :", 
                font=self.custom_font, bg="#f0f0f0").pack(anchor=tk.W, pady=5)
        
        # Add search dropdown
        self.search_var = tk.StringVar()
        self.search_dropdown = ttk.Combobox(
            self.right_frame, 
            textvariable=self.search_var, 
            width=35, 
            font=self.custom_font
        )
        self.search_dropdown.pack(anchor=tk.W, pady=5)
        self.search_dropdown.insert(0, "Enter product name...")
        self.search_dropdown.config(state="readonly")
        
        # Product ID entry
        self.product_id_entry = tk.Entry(self.right_frame, width=35, font=self.custom_font)
        self.product_id_entry.pack(anchor=tk.W, pady=5)
        
        # Upload button
        tk.Button(self.right_frame, 
                 text="Run Shopify Data Upload",
                 command=self.upload_selected,
                 font=self.custom_font, 
                 bg="#007bff", 
                 fg="white", 
                 padx=10, 
                 pady=5).pack(pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            if not os.path.exists(directory):
                os.makedirs(directory)
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)

    def on_checkbox_toggle(self, product_name, var):
        if var.get():
            self.selected_products.add(product_name)
        else:
            self.selected_products.discard(product_name)
        print(f"Selected products: {self.selected_products}")

    def populate_search_options(self):
        try:
            with open("printify_product_data.json", "r") as file:
                data = json.load(file)
            
            # Load image counts from product_image_counts.json
            try:
                with open("product_image_counts.json", "r") as count_file:
                    image_counts = json.load(count_file)
                    # Create a dictionary for quick lookup
                    image_count_dict = {
                        product["title"]: product["image_count"] 
                        for product in image_counts["products"]
                    }
            except FileNotFoundError:
                print("product_image_counts.json not found")
                image_count_dict = {}
            
        except FileNotFoundError:
            print("printify_product_data.json not found. Please download essential data first.")
            return

        # Clear existing checkboxes
        for widget in self.products_frame.winfo_children()[1:]:  # Skip the label
            widget.destroy()

        # Create scrollable frame
        canvas = tk.Canvas(self.products_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(self.products_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add checkboxes
        self.checkbox_vars = {}  # Store checkbox variables
        for num, product in enumerate(data['data']):
            var = tk.BooleanVar()
            self.checkbox_vars[product['title']] = var
            
            # Get image count for this product
            image_count = image_count_dict.get(product['title'], 0)
            
            # Create checkbox with image count
            checkbox = ttk.Checkbutton(
                scrollable_frame,
                text=f"{product['title']} | (total images: {image_count})",
                variable=var,
                command=lambda p=product['title'], v=var: self.on_checkbox_toggle(p, v)
            )
            checkbox.pack(anchor="w", padx=5, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Update scroll region
        scrollable_frame.bind("<Configure>", 
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def download_essential_data(self):
        subprocess.run(["python", "printify_data_download.py"])
        subprocess.run(["python", "shopify_products.py"])
        self.load_product_ids()
        self.populate_search_options()

    def download_and_upload(self):
        if not self.selected_products:
            print("No products selected")
            return

        directory = self.directory_entry.get()
        if not os.path.exists(directory):
            os.makedirs(directory)

        for product in self.selected_products:
            try:
                self.download_product(product)
                self.upload_product(product)
            except Exception as e:
                print(f"Error processing {product}: {str(e)}")

    def download_product(self, product_title):
        try:
            with open("printify_product_data.json", "r") as file:
                data = json.load(file)
            
            for num, prod in enumerate(data['data']):
                if prod['title'] == product_title:
                    subprocess.run(["python", "printify_data_download.py"])
                    subprocess.run(["python", "image_download.py", 
                                  self.directory_entry.get(), str(num)])
                    break
        except Exception as e:
            print(f"Download error for {product_title}: {str(e)}")
            raise

    def upload_product(self, product_title):
        try:
            x = product_title.split(" ")
            title = "".join(x).lower()
            product_id = self.product_id_options.get(title)
            
            if product_id:
                directory = self.directory_entry.get()
                subprocess.run(["python", "shopify_variant_download.py", directory, str(product_id)])
                subprocess.run(["python", "image_upload.py", directory, str(product_id)])
            else:
                print(f"No product ID found for {product_title}")
        except Exception as e:
            print(f"Upload error for {product_title}: {str(e)}")
            raise

    def load_product_ids(self):
        try:
            with open("shopify_products_idList.json", "r") as file:
                data = json.load(file)
            
            self.product_id_options = {
                "".join(product['title'].split(" ")).lower(): product['id']
                for product in data["products"]
            }
        except FileNotFoundError:
            print("shopify_products_idList.json not found")

    def upload_selected(self):
        """Handle the upload of selected products"""
        directory = self.directory_entry.get()
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if self.search_dropdown.get() != "Enter product name...":
            # Get the product title from dropdown and find its ID
            selected_product = self.search_dropdown.get()
            x = selected_product.split(", ")[0].split(" ")
            product_title = "".join(x).lower()
            product_id = self.product_id_options.get(product_title)
            
            if product_id:
                subprocess.run(["python", "shopify_variant_download.py", directory, str(product_id)])
                subprocess.run(["python", "image_upload.py", directory, str(product_id)])
            else:
                print("Could not find product ID for the selected product")
            
        elif self.product_id_entry.get().strip():  # Check if manual product ID is entered
            product_id = self.product_id_entry.get()
            subprocess.run(["python", "shopify_variant_download.py", directory, product_id])
            subprocess.run(["python", "image_upload.py", directory, product_id])
        else:
            print("Please either select a product from dropdown or enter a product ID manually")

    def get_product_image_count(self):
        """Run the script to get product image counts and refresh the checkboxes"""
        try:
            # Run the script to get product image counts
            subprocess.run(["python", "get_product_images_count.py"])
            
            # Refresh the checkboxes with updated image counts
            self.populate_search_options()
        except Exception as e:
            print(f"Error running get_product_images_count.py: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PrintifyShopifyAutomation()
    app.run()