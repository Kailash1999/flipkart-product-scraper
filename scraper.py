import pandas as pd
import requests
from bs4 import BeautifulSoup

# Step 1: Store the Flipkart search URL

# Use a normal URL string, not Markdown format

url = "https://www.flipkart.com/search?q=mobile+under+15000+rs"

# Step 2: Set headers to make the request resemble a browser request

headers = {
"User-Agent": "Mozilla/5.0"
}

# Step 3: Send a GET request to Flipkart

r = requests.get(url, headers=headers, timeout=15)

# Check whether the request was successful

print("Status Code:", r.status_code)

# Stop if the server returned an unsuccessful HTTP status

r.raise_for_status()

# Step 4: Parse the HTML using BeautifulSoup

soup = BeautifulSoup(r.text, "lxml")

# Step 5: Find a product link

# find() returns the first matching element or None

np = soup.find("a", class_="jgg0SZ")
if np:
    product_link = np.get("href")

    # Convert a relative URL into a complete URL
    if product_link and product_link.startswith("/"):
        product_link = "https://www.flipkart.com" + product_link

    print("Product Link:", product_link)

else:
    print("Product link not found. The HTML class may have changed.")
# Step 6: Create empty lists to store the extracted information

productname = []
price = []
description = []

# Step 7: Extract product names

# find_all() returns all elements matching the specified class

names = soup.find_all("div", class_="RG5Slk")

for name in names:
# get_text(strip=True) extracts text and removes extra whitespace
 productname.append(name.get_text(strip=True))

print("Product Names Found:", len(productname))

# Step 8: Extract product prices

prices = soup.find_all("div", class_="hZ3P6w DeU9vF")

for p in prices:
# Use p for the current HTML element.
# Keep price as the list so we can append values to it.
    price.append(p.get_text(strip=True))

print("Prices Found:", len(price))

# Step 9: Extract product descriptions

descriptions = soup.find_all("ul", class_="HwRTzP")

for desc in descriptions:
# Join description text while keeping words separated by spaces
 description.append(desc.get_text(" ", strip=True))

print("Descriptions Found:", len(description))

# Step 10: Create a Pandas DataFrame

# Series allows columns to have different lengths.

# Missing values will appear as NaN.

df = pd.DataFrame({
"Product Name": pd.Series(productname),
"Price": pd.Series(price),
"Description": pd.Series(description)
})

# Step 11: Display the extracted data

print("\nScraped Data:")
print(df.to_string(index=False))

# Step 12: Save the data to a CSV file

df.to_csv("flipkart_mobiles.csv", index=False, encoding="utf-8-sig")

print("\nData saved to flipkart_mobiles.csv")
