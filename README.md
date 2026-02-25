# 🛡️ Market Tracker Pipeline

> **Automated Asset Monitoring & Data Engineering Pipeline**

Este projeto é um pipeline de dados desenvolvido em Python focado em **Inteligência de Mercado**. O objetivo é rastrear preços de ativos em tempo real via API, comparar com metas estratégicas de uma empresa e disparar alertas automáticos para tomada de decisão.

## Sumário
- [Tecnologias](#-tecnologias)
- [O Problema de Negócio](#-o-problema-de-negócio)
- [Arquitetura do Pipeline](#-arquitetura-do-pipeline)
- [Funcionalidades](#-funcionalidades)
- [Como Executar](#-como-executar)
- [Licença](#-licença)

---

## Tecnologias
- **Python**: Linguagem principal para lógica e automação.
- **Requests**: Ingestão de dados via APIs REST (Coinbase).
- **JSON/CSV**: Manipulação de diferentes formatos de arquivos para integração de dados.
- **Git/GitHub**: Controle de versão e documentação.

---

## O Problema de Negócio
Empresas de investimento e varejo precisam reagir rapidamente às mudanças de preço do mercado. A coleta manual de dados é lenta e suscetível a erros. O **Market Tracker** resolve isso automatizando a vigilância de preços, garantindo que o time de operações receba um alerta no momento exato em que um ativo atinge o valor alvo (target price).

---

## Arquitetura do Pipeline
O projeto segue o fluxo fundamental de Engenharia de Dados:

1. **Ingestão (Extract):** Coleta de preços em tempo real da API da Coinbase e leitura de metas de negócio em arquivos locais.
2. **Transformação (Transform):** - Limpeza de dados nulos e tratamento de erros de leitura.
    - Normalização para duas casas decimais.
    - Cálculo de diferença entre preço real e meta corporativa.
3. **Carga/Alerta (Load):** - Exportação dos dados processados para um relatório final em JSON.
    - Disparo de logs de alerta baseados em regras de negócio (Price Watch).

---

## Funcionalidades
- **Monitoramento Multiativos:** Rastreamento de Bitcoin (BTC), Ethereum (ETH) e ativos financeiros.
- **Priorização de Alertas:** Lógica integrada para classificar ativos por nível de prioridade (Alta, Média, Baixa).
- **Relatório de Diferença:** Cálculo automático do spread entre valor de mercado e valor alvo.
- **Persistência de Dados:** Geração de arquivos de saída para auditoria e histórico de execuções.

---

## Licença
**MIT License**

Copyright (c) 2026 Jéssica Cristina de Rezende

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
