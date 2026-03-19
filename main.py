# %%
# Imports and Configurations
import requests
import pandas as pd

# Market Data Settings
coins_list = ["USD-BRL", "EUR-BRL", "BTC-BRL"]
query = ",".join(coins_list)
URL = f"https://economia.awesomeapi.com.br/last/{query}"

# Tax
import_tax = 0.60    # 60%

# Data Extraction
try:
    response = requests.get(URL)
    response.raise_for_status() # Check if the request was successful
    raw_data = response.json()
except Exception as e:
    print(f" Critical Error during extraction: {e}")
    raw_data = {}

# Processing and Intelligence Pipeline
if raw_data:
    # Transformation
    formatted_list = list(raw_data.values())
    df = pd.DataFrame(formatted_list)
    
    # Data Cleaning and Column Selection
    df = df[['code', 'codein', 'bid', 'pctChange', 'create_date']]
    df.columns = ['Currency', 'Base', 'Current_Price', 'Pct_Change', 'Query_Date']
    
    # Loading (Historical Record)
    df.to_csv("market_price.csv", sep=";", index=False, encoding='utf-8')
    print("✅ Market data updated and saved to 'market_price.csv'.")

    # Price Mapping
    # Dictionary to store the latest prices for easy access
    live_prices = {
        "USD": float(df.loc[df['Currency'] == 'USD', 'Current_Price'].values[0]),
        "EUR": float(df.loc[df['Currency'] == 'EUR', 'Current_Price'].values[0]),
        "BTC": float(df.loc[df['Currency'] == 'BTC', 'Current_Price'].values[0])
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

    profit_value = input(f"Insira sua margem de lucro: ")
    profit_margin = float(profit_value)

    print(f"Moedas disponíveis: {list(live_prices.keys())}")
    
    user_choice = input("Escolha uma das moedas disponíveis (USD/EUR/BTC): ").upper()
    
    if user_choice in live_prices:
        try:
            cost_input = input(f"Insira o valor do produto em {user_choice}: ")
            product_value = float(cost_input)
            
            final_price = final_selling_price(
                live_prices[user_choice], 
                product_value, 
                import_tax, 
                profit_margin
            )
            
            print(f"\nResultado:")
            print(f"Valor {user_choice} atual: R$ {live_prices[user_choice]:.2f}")
            print(f"Taxa aplicada: 60.00%")
            print(f"Margem de lucro: {profit_margin:.2f}%")
            print(f"Custo do produto em {user_choice}: {product_value:.2f}")
            print(f"Melhor preço para venda: R$ {final_price:.2f}")

        except ValueError:
            print("Error: Por favor insira um valor válido!")
    else:
        print(f"Esta moeda '{user_choice}' não é suportada pelo sistema!")

else:
    print("Ocorreu um erro no sistema devido a API")