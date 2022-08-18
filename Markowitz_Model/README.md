# **Markowitz Model**

Created at: march/2022

---

## **Modelo**
A partir dos conceitos de medição de risco e retorno apresentados, entende-se que a carteira de investimentos ideal é aquela que maximiza o retorno esperado e minimiza o risco - a volatilidade - dos ativos. 
Deste modo, Markowitz propõe um método para reduzir o risco de
um potifólio de investimentos a partir da diversificação. Dado um nível de risco, calculado com base em uma série histórica de preços dos ativos, combina-se todas os pesos possíveis para a carteira, de modo a encontrar a distribuição de pesos mais eficiente, aquela que gera o melhor retorno.

Princípio da dominância: suponha três ativos, A, B e C. Se o ativo A possui um retorno maior do que o ativo B e ambos possuem o mesmo grau de volatilidade, diz que o ativo A é dominante em relação ao ativo B. O ativo C, no entanto, em comparação a A possui um maior risco e um maior retorno. Neste caso, nada se pode afirmar, uma vez que a escolha
entre um e outro depende do perfil do investidor. Mantém-se, obviamente, a premissa de que um maior risco só é aceitável sob a condição de um maior retorno - prêmio de risco.

Assim, a ideia é de que, dado um retorno esperado, o investidor possa escolher entre os portifólios aquele que contém a menor variância. O investidor também tem a possibilidade de, dado uma determinada vriância, escolher o portifólio de maior rentabilidade esperada.

Para avaliar o risco e o retorno de uma carteira como um todo, deve-se realizar a média ponderada dos retornos individuais de cada ativo, com base em variáveis percentuais, cuja soma é igual a 1. 

O cálculo do retorno da carteira é realizado através da fórmulaÇ
$$ R_c = \sum_{i=1}^{N} X_i R_i $$
em que $X_i$ é a variável peso do ativo $i$ e $R_i$ é o retorno do ativo i.
