# %%
# Imports and Configurations
import requests
import pandas as pd
import json
import os

# Market Data Settings
coins_list = ["USD-BRL", "EUR-BRL", "BTC-BRL"]
query = ",".join(coins_list)
URL = f"https://economia.awesomeapi.com.br/last/{query}"

# Data Extraction
try:
    response = requests.get(URL)
    response.raise_for_status() # Check if the request was successful
    raw_data = response.json()
except Exception as e:
    print(f" Erro durante a extração: {e}")
    raw_data = {}

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
    df['Price'] = df['Price'].astype(float).round(2)

    df['Target'] = df['Currency'].map(targets)
    df['Difference'] = (df['Price'] - df['Target']).round(2)
    
    # Loading (Historical Record)
    file_exists = os.path.isfile("market_price.csv")
    
    df.to_csv("market_price.csv", 
              mode='a',           # 'a' for append: adds to the end of the file
              sep=";", 
              index=False, 
              header=not file_exists, # only add the header if the file does NOT exist
              encoding='utf-8')
    
    # JSON (overwrite with the most recent data)
    df.to_json("market_status.json", orient="records", indent=4)
    
    print("\n--- MONITORAMENTO DE METAS CORPORATIVAS ---")
    print(f"Margem configurada: {margin_from_json}% | Imposto: {tax_from_json*100}%")
    for index, row in df.iterrows():
        moeda = row['Currency']
        preco = row['Price']
        meta = row['Target']
        dif = row['Difference']
        
        status = "🚨 ALERTA: COMPRAR" if preco <= meta else "✅ AGUARDAR (Acima da Meta)"
        
        print(f"{moeda}: Atual R$ {preco:.2f} | Meta R$ {meta:.2f} | Dif: R$ {dif:.2f}")
        print(f"Status: {status}\n")

    # Price Mapping
    # Dictionary to store the latest prices for easy access
    live_prices = {
        "USD": float(df.loc[df['Currency'] == 'USD', 'Price'].values[0]),
        "EUR": float(df.loc[df['Currency'] == 'EUR', 'Price'].values[0]),
        "BTC": float(df.loc[df['Currency'] == 'BTC', 'Price'].values[0])
    }

    # Business Logic Function
    def final_selling_price(exchange_rate, product_cost, tax, margin):
        """
        Calculates the final selling price considering conversion, taxes, and profit.
        """
        converted_cost = exchange_rate * product_cost
        # Applying percentage-based increase
        return converted_cost * (1 + tax + (margin/100))

    # User Interaction Loop
    profit_input = input(f"Insira sua margem de lucro (Padrão {margin_from_json}%): ")
    profit_margin = float(profit_input) if profit_input else margin_from_json
    print(f"Moedas disponíveis: {list(live_prices.keys())}")
    user_choice = input("Escolha uma das moedas disponíveis (USD/EUR/BTC): ").upper()

    if user_choice in live_prices:
        try:
            cost_input = input(f"Insira o valor do produto em {user_choice}: ")
            product_value = float(cost_input)       

            final_price = final_selling_price(
                live_prices[user_choice],
                product_value,
                tax_from_json,
                profit_margin
            )
 
            print(f"\nResultado:")
            print(f"Valor {user_choice} atual: R$ {live_prices[user_choice]:.2f}")
            print(f"Taxa aplicada: 60.00%")
            print(f"Margem de lucro: {profit_margin:.2f}%")
            print(f"Custo do produto em {user_choice}: {product_value:.2f}")
            print(f"Melhor preço para venda em BRL: {final_price:.2f}")

        except ValueError:
            print("Error: Por favor insira um valor válido!")
    else:
        print(f"Esta moeda '{user_choice}' não é suportada pelo sistema!")

else:
    print("Erro na extração.")

# %%
