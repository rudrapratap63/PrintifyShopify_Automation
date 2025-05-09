# 🛍️ Printify-Shopify Automation

Automate product uploads from Printify to Shopify using access tokens and API integration.

---

## 🔐 1. Generate Printify Access Token

1. Go to your **Printify App Dashboard**.  
2. Navigate to:  
   `Account → Connections → Generate`  
3. Copy the **PRINTIFY_ACCESS_TOKEN** for later use.

---

## 🏪 2. Get Shop ID

Run the following command to get your Shop ID:

```bash
curl -X GET https://api.printify.com/v1/shops.json \
--header "Authorization: Bearer {PRINTIFY_ACCESS_TOKEN}"
```

Replace `{PRINTIFY_ACCESS_TOKEN}` with your actual token.

---

## 🔑 3. Generate Shopify Access Token

### (a) Create a Custom App

- Log in to your Shopify store admin panel.
- Go to **Apps** → Click **Create App**.
- Enter app name and developer name → Click **Create app**.

### (b) Configure the App

- In the **App Setup** section, set the required **API scopes** (permissions).

### (c) Install the App

- Go to **Apps** → **Manage private apps** → Click **Create private app**.
- Provide necessary details and select appropriate permissions.

### (d) Get the Access Token

- After the app is created, you’ll receive a **Shopify Access Token**.
- Save it securely. This token will be used for authenticating API requests.

---

## ⚙️ 4. Configure Environment Variables

Open the `.env` file located at:  
`shopify_automation/dist/main/.env`

Update it with your credentials:

```env
PRINTIFY_ACCESS_TOKEN=your_printify_access_token
SHOP_ID=your_shop_id
SHOPIFY_ACCESS_TOKEN=your_shopify_access_token
SHOPIFY_URL=your_shopify_store_url
```

---

## 🚀 5. Run the Script

Execute the Python script:

```bash
python main.py
```

---

## 📌 6. Create Shortcut for Windows

To create a shortcut for `main.exe`:

1. Go to the `shopify_automation` folder.
2. Right-click on `main.exe` → Select **Properties**.
3. In the **Shortcut** tab, update the **Target** field with the executable path:

```
"C:\path\to\your\project\dist\main\main.exe"
```

  
![Shopify_Automation](https://github.com/user-attachments/assets/869a2e4c-72e4-4f72-b1ff-6c379cd3068d)

