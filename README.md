# PrintifyShopify_Automation

1.Generate PRINTIFY_ACCESS_TOKEN from Printify App Dashboard :
	Account -> Connections -> Generate

2.Generate Shop_id by following command : 
    curl -X GET https://api.printify.com/v1/shops.json --header "Authorization: Bearer {PRINTIFY_ACCESS_TOKEN}


3.Generate SHOPIFY_ACCESS_TOKEN :
   (a)Create a custom app in your Shopify Partner Dashboard :
	Log in to your Shopify account, go to the Apps section(admin panel), and click "Create app". Enter the app 	name and developer name, then click "Create app".
   (b)Configure the app: 
	In the "App setup" section, specify the API scopes (permissions) your app requires. Be specific about the 	data and actions your app needs access to.
   (c)Install the app:
	Go to your Shopify store's admin, click on "Apps", then "Manage private apps". Click "Create private app" 	and fill out the required information, including the permissions and the store it's associated with
   (d)Generate the access token:
	Once the private app is created, you'll receive an access token. Use this token to verify your app's 	identity when making API requests to the associated Shopify store.

4.After that open .env file from shopify_automation/dist/main/.env and put value of required fields in the .env file :
	# PRINTIFY_ACCESS_TOKEN=your_printify_access_token
	# SHOP_ID=your_shop_id
	# SHOPIFY_ACCESS_TOKEN=your_shopify_access_token
	# SHOPIFY_URL=your_shopify_store_url
		
5. Run python main.py

6.For create shortcut go to shopify_automation folder right click in main.exe :
	Right-click on the main.exe(shortcut) and select "Properties".
	In the "Properties" window, go to the "Shortcut" tab.
	In the "Target" field, add the path to the executable file.
		For example : "C:\path\to\your\project\dist\main\main.exe"
