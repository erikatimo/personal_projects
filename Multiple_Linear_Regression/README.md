# **Multiple Linear Regression: Model and Tests**

Created at: march/2022

---

## **Resumo**

Regressão linear múltipla:
- **Variável dependente**: Índice Nasdaq-100 (^NDX)
- **Variáveis independentes**: empresas que compõem o índice Nasdaq-100 e que interromperam completamente as suas atividades na Rússia (Withdrawal label), após a abertura do conflito com a Ucrânia. 
    - Airbnb (ABNB), 
    - Autodesk (ADSK), 
    - Advanced Micro Devices (AMD), 
    - Activision Blizzard (ATVI), 
    - Booking Holdings (BKNG), 
    - eBay (EBAY), 
    - Fortinet (FTNT), 
    - Netflix (NFLX)
- **Período contemplado**:
    - Primeira Janela: 30/01/2022 a 23/02/2022
    - Segunda Janela: 24/02/2022 a 20/03/2022

---
## **Dataset**

Inicialmente, foram consideradas à análise as empresas que fazem parte da composição do índice da Nasdaq, **Nasdaq-100**, obtidas através do [site](https://www.nasdaq.com/market-activity/quotes/nasdaq-ndx-index) da bolsa americana.

Em seguida, o artigo da [Yale](https://som.yale.edu/story/2022/over-600-companies-have-withdrawn-russia-some-remain) foi utilizado para clusterizar este conjunto de empresas conforme a sua reação ao conflito Rússia-Ucrânia, iniciado em 24/2/2022.

As empresas foram segregadas nas seguintes categorias:
- **Digging In**: empresas que continuam normalmente o seu modelo de negócio usual na Russia.
- **Buying Time**: empresas que adiaram a execução de atividades relacionadas a novos investimentos ou marketing já planejadas, enquanto permanecem operando substancialmente.
- **Scaling Back**: empresas que reduziram algumas operações de maneira significante, mas permanecem com outras.
- **Suspension**: empresas que restringiram temporariamente a operação na Russia, mantendo a opção de retorno em aberto.
- **Withdrawal**: empresas que interromperam completamente as atividades na Russia.

O cruzamento resultante foi:
- **Digging In**: ALGN, JD, PCAR
- **Buying Time**: AZN, IDXX, KHC, MAR, MDLZ
- **Scaling Back**: MSFT, PEP
- **Suspension**: AAPL, ADBE, ADI, ADP, AMZN, ANSS, COST, CSCO, FB, GOOG, GOOGL, HON, INTC, INTU, MRVL, MU, NVDA, PYPL, QCOM, SBUX, TEAM
- **Withdrawal**: ABNB, ADSK, AMD, ATVI, BKNG, EBAY, FTNT, NFLX
- **Not Applicable**: AEP, AMAT, AMGN, ASML, AVGO, BIDU, BIIB, CDNS, CEG, CHTR, CMCSA, CPRT, CRWD, CSX, CTAS, CTSH, DDOG, DLTR, DOCU, DXCM, EA, EXC, FAST, FISV, GILD, ILMN, ISRG, KDP, KLAC, LCID, LRCX, LULU, MCHP, MELI, MNST, MRNA, MTCH, NTES, NXPI, ODFL, OKTA, ORLY, PANW, PAYX, PDD, REGN, ROST, SGEN, SIRI, SNPS, SPLK, SWKS, TMUS, TSLA, TXN, VRSK, VRSN, VRTX, WBA, WDAY, XEL, ZM, ZS

A label **Not Applicable** foi dado por mim para as empresas que fazem parte do grupo da Nasdaq, mas que não foram citadas no estudo de Yale.

A base resultante encontra-se no arquivo **companies.xlsx**

---
## **Resultados**
