# 🛡️ Market Tracker Pipeline & Dashboard

> **Automated Data Engineering Pipeline & Real-time Business Intelligence**

Este projeto é uma solução de **Engenharia de Dados** desenvolvida em Python. Ele automatiza o ciclo de vida do dado: desde a ingestão via API REST até a visualização em um Dashboard interativo, focado em suporte à decisão para operações de importação e câmbio.

## Tecnologias e Ferramentas
- **Python**: Core da aplicação e lógica de negócios.
- **Pandas**: Processamento, limpeza e pivotagem de dados (Time Series).
- **Streamlit**: Interface de usuário (Dashboard) de alta performance.
- **Requests**: Ingestão de dados em tempo real (AwesomeAPI).
- **GitHub Actions**: Orquestração e automação de jobs na nuvem (CI/CD).
- **JSON/CSV**: Estruturas de persistência para estado atual e histórico.

---

## O Problema de Negócio
Empresas que dependem de importação sofrem com a volatilidade do câmbio (USD, EUR, BTC). O **Market Tracker** resolve a latência na tomada de decisão ao:
1.  **Monitorar** ativos 24/7 sem intervenção humana.
2.  **Comparar** preços de mercado com metas corporativas predefinidas.
3.  **Simular** preços de venda final considerando impostos (60%) e margens de lucro dinâmicas.

---

## Arquitetura do Sistema
O projeto é dividido em quatro camadas principais:

1.  **Ingestão (Extract):** O `main.py` consome a AwesomeAPI e carrega configurações de metas via `business_config.json`.
2.  **Processamento (Transform):** Normalização de decimais, cálculo de *spread* (diferença para a meta) e tratamento de erros de conexão.
3.  **Armazenamento (Load):** - `market_status.json`: Estado atual para leitura rápida do Dashboard.
    - `market_price.csv`: Histórico cumulativo para análise de tendência.
4.  **Entrega (Serve):** Dashboard interativo (`app.py`) com gráficos de volatilidade e calculadora de conversão.

---

## Automação (CI/CD)
Este repositório utiliza **GitHub Actions** para garantir a atualização autônoma dos dados.
- **Frequência:** O pipeline é executado automaticamente a cada 60 minutos via Cron Job.
- **Persistência:** Os novos preços são commitados e versionados automaticamente no histórico (`market_price.csv`) pelo próprio GitHub.

---

## Funcionalidades do Dashboard
- **Cards de Cotação:** Visualização imediata com indicadores de "🚨 HORA DE COMPRAR" ou "✅ AGUARDAR".
- **Tendência Individual:** Gráficos de linha independentes para cada ativo, permitindo análise de volatilidade sem distorção de escala.
- **Calculadora de Importação:** Interface para simular custos de produtos, aplicando automaticamente a cotação do momento, impostos e lucro desejado.
  
---

## Como Executar

### Preparação do Ambiente
Instale as bibliotecas necessárias:
pip install requests pandas streamlit

### Iniciar o Dashboard
Para visualizar os dados e usar a calculadora:
streamlit run app.py

### Execução Manual do Pipeline
Caso deseje forçar uma atualização dos dados fora do agendamento automático do GitHub:
python main.py

---

### Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

Copyright (c) 2026 Jéssica Cristina de Rezende
