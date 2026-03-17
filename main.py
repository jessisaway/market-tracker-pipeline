# %%
import requests
import pandas as pd
import json

# 1. Configuração 
coins_list = ["USD-BRL", "EUR-BRL", "BTC-BRL"]
coins_query = ",".join(coins_list) # Transforma em "USD-BRL,EUR-BRL,BTC-BRL"
url = f"https://economia.awesomeapi.com.br/last/{coins_query}"

# 2. Extração com tratamento de erro
try:
    resposta = requests.get(url)
    resposta.raise_for_status() # Lança erro se o status não for 200
    dados_brutos = resposta.json()
except Exception as e:
    print(f"Erro na extração: {e}")
    dados_brutos = {}

# 3. Transformação 
if dados_brutos:
    # Valores em lista
    lista_formatada = list(dados_brutos.values())
    
    df = pd.DataFrame(lista_formatada)

    # Selecionando apenas o que importa
    df = df[['code', 'codein', 'bid', 'pctChange', 'create_date']]
    
    # Renomeando 
    df.columns = ['Moeda', 'Base', 'Preco_Atual', 'Variacao_Pct', 'Data_Consulta']
    
    # 4. Carga
    df.to_csv("precos_mercado.csv", sep=";", index=False, encoding='utf-8')
    print("Pipeline finalizado!")
    
    print(df.head())

# %%
