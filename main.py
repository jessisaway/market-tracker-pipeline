# Imports and Configurations
import requests
import pandas as pd
import json
import os
import time

# Market Data Settings
coins_list = ["USD-BRL", "EUR-BRL", "BTC-BRL"]
query = ",".join(coins_list)
url = f"https://economia.awesomeapi.com.br/last/{query}"
headers = {"User-Agent": "market-tracker-pipeline/1.0"}

# Data Extraction
raw_data = {}
for attempt in range(3):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
        break
    except Exception as e:
        print(f"Tentativa {attempt + 1} falhou: {e}")
        if attempt < 2:
            time.sleep(10)

# Processing and Intelligence Pipeline
if raw_data:
    try:
        with open("business_config.json", "r") as f:
            config = json.load(f)

        targets = {k: v for k, v in config.items() if k in ["USD", "EUR", "BTC"]}
        margin_from_json = config.get("profit_margin", 20.0)
        tax_from_json = config.get("import_tax", 0.60)

    except FileNotFoundError:
        print("Arquivo business_config.json não encontrado.")
        targets = {"USD": 0, "EUR": 0, "BTC": 0}

    # Transformation
    formatted_list = list(raw_data.values())
    df = pd.DataFrame(formatted_list)

    # Data Cleaning and Column Selection
    df = df[['code', 'bid', 'create_date']]
    df.columns = ['Currency', 'Price', 'Timestamp']
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').astype(float)

    df['Target'] = df['Currency'].map(targets)
    df['Difference'] = (df['Price'] - df['Target']).round(2)

    # Loading (Historical Record)
    file_exists = os.path.isfile("market_price.csv")

    df.to_csv("market_price.csv",
              mode='a',
              sep=";",
              index=False,
              header=not file_exists,
              encoding='utf-8')

    # JSON (overwrite with the most recent data)
    df.to_json("market_status.json", orient="records", indent=4)

    print(f"✅ Pipeline executado com sucesso! Dados atualizados em: {df['Timestamp'].iloc[0]}")
else:
    print("❌ Falha na extração de dados após 3 tentativas.")
