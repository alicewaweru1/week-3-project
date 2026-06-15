import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
CSV_FILE = SCRIPT_DIR / "jumia_phones.csv"
EXCEL_FILE = SCRIPT_DIR / "jumia_phones.xlsx"
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "")

SECRETS_FILE = SCRIPT_DIR / "secrets.txt"
if not API_KEY and SECRETS_FILE.exists():
    with open(SECRETS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                if key.strip() == "EXCHANGE_RATE_API_KEY":
                    API_KEY = value.strip()
                    break

use_usd_conversion = bool(API_KEY)

try:
    url = "https://www.jumia.co.ke/catalog/?q=phones"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("article", class_="prd")

    names = []
    prices_kes = []

    for product in products[:10]:
        name_tag = product.find("h3", class_="name")
        price_tag = product.find("div", class_="prc")

        if name_tag and price_tag:
            name = name_tag.text.strip()

            price = (
                price_tag.text
                .replace("KSh", "")
                .replace(",", "")
                .strip()
            )

            try:
                price = float(price)
            except ValueError:
                continue

            names.append(name)
            prices_kes.append(price)

    prices_usd = None
    if use_usd_conversion:
        rate_url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/KES"
        rate_response = requests.get(rate_url)
        rate_response.raise_for_status()
        rate_data = rate_response.json()
        usd_rate = rate_data.get("conversion_rates", {}).get("USD")

        if usd_rate is None:
            raise ValueError("USD rate not found in API response.")

        prices_usd = [round(price * usd_rate, 2) for price in prices_kes]

    df_data = {
        "Product Name": names,
        "Price (KES)": prices_kes,
    }
    if prices_usd is not None:
        df_data["Price (USD)"] = prices_usd

    df = pd.DataFrame(df_data)

    print(df)

    df.to_csv(CSV_FILE, index=False)
    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")
    print(f"Saved {CSV_FILE.name} and {EXCEL_FILE.name}.")

except requests.exceptions.RequestException as e:
    print("Connection Error:", e)

except Exception as e:
    print("Error:", e)