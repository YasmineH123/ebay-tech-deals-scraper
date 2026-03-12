import pandas as pd

df = pd.read_csv("ebay_tech_deals.csv", dtype=str)

df["price"] = df["price"].str.replace("$", "", regex=False)
df["price"] = df["price"].str.replace(",", "", regex=False).str.strip()

df["original_price"] = df["original_price"].str.replace("$", "", regex=False)
df["original_price"] = df["original_price"].str.replace(",", "", regex=False).str.strip()

df["original_price"] = df["original_price"].replace("N/A", None)
df["original_price"] = df["original_price"].fillna(df["price"])

df["shipping"] = df["shipping"].replace("N/A", "Shipping info unavailable")

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["original_price"] = pd.to_numeric(df["original_price"], errors="coerce")

df["discount_percentage"] = (
    (df["original_price"] - df["price"]) / df["original_price"] * 100
).round(2)

df.to_csv("cleaned_ebay_deals.csv", index=False)

print("Cleaning completed successfully.")