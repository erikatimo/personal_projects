## Gestão de Riscos - 3ª Avaliação

04 de abril de 2022

Erika Timo de Oliveira - 18/0119567

Vitor Dolabela - 15/0151594

#### Questão 1

O objetivo é avaliar o impacto de um evento a um ativo ou a uma carteira de ativos.
No caso, estudaremos o impacto da invasão da Russia ao território ucraniano realizada em 24 de fevereiro de 2022.
Utilizaremos uma janela de estimação de 150 dias e uma janela de evento de 25 dias.


![Representação temporal](./questao_1/rep_temporal_evento.png)

Uma vez coletados os dados necessários, vamos partir para a mensuração dos retornos normais e anormais. A fórmula abaixo será aplicada para o cálculo do retorno anormal, que é definido pela diferença entre o retorno observado e o retorno estimado pelo modelo que foi aplicado à janela de estimação.

$$ AR_{i\tau} = R_{i\tau} - E(R_{i\tau}|f_\tau)$$

Utilizaremos o modelo base do CAPM da firma i no periodo $\tau$ a estimação:

$$ E(\hat{R}_{i\tau}) = \hat{\alpha} + \hat{\beta}E(R_{m\tau})$$

Em seguida serão calculados os retornos anormais acumulados:

$$ CAR_i(\tau_1, \tau_2) = \sum_{\tau=\tau_1}^{\tau_2} AR_{i\tau}$$

A anormalidade será identificada pelo valor de CAR, caso este seja significativo e diferente de zero. 

Finalmente, será realizado o teste de hipóteses. A hipótese nula é de que não existe retornos anormais e retornos anormais acumulados.

Todos estes cálculos foram realizados na planilha **Estudo de Eventos - Setor Bancário**.

Acerca dos resultados: alguns registros rejeitam H0 e outros não. O $CAR$ total da janela de eventos ficou zerado, o que representaria uma não significância do evento. Além disso, o valor da carteira aumentou durante a janela do evento, o que é um fato contraditório em se tratando de um contexto sensível, em que um conflito com impactos globais se inicia. Devemos considerar ainda a possibilidade de interferência de outros eventos durante este período. Deste modo, considera-se esta análise inconclusiva com relação ao impacto do conflito Rússia-Ucrânia ao setor bancário brasileiro

---

#### Questão 2

O objetivo é realizar uma classificação de risco, a partir da tabela SAATY.
As etapas são:
1. Definir as preferências com base na tabela SATTY, para riscos do tipo financeiro, de mercado e operacional.
2. Normalizar as matrizes 
3. Obter a média para cada critério
4. Sintetizar a matriz de preferências
5. Realizar a comparação entre os critérios
6. Normalização dos critérios e cálculo das médias
7. Multiplicas as médias dos projetos com a média dos critérios
8. Realizar o teste de coerência
9. Determinar o y máximo para encontrar o índice de coerência das respostas
10. Comparar o IC com o IA

Fórmulas e cálculos estão indicados na aba **AV3-Q2** da planilha **AV2 e AV3 - Vitor Dolabela e Érika Timo vf**.


---

#### Questão 3

O objetivo é realizar a análise discriminante, por meio dos passos a seguir:
1. Análise descriminante para cada um dos grupos - covariância
2. Cálculo da diferença entre as médias
3. Cálculo das Somas dos Quadrados
4. Achar a função
5. Substituir a função
6. Cálculo da média das médias

Fórmulas e cálculos estão indicados na aba **AV3-Q3** da planilha **AV2 e AV3 - Vitor Dolabela e Érika Timo vf**.

---

#### Questão 4

A ideia é implementar a teoria de Análise Envoltória de Dados, considerando a existência de uma empresa com filiais Ei. 
Os dados de insumos e produtos para cada DMU foram inseridos no arquivo **data.csv**.

@import "questao_4/data.csv"

Desta maneira, deseja-se calcular o rank de eficiência destas filiais com índice de eficiência θ de 0% a 100% e analisar o Benchmark dessas unidades.

O modelo DEA parte do seguinte pressuposto de otimização.

$$ Max \; \frac{\sum_{r=1}^{s} u_ry_{r0}}{\sum_{i=1}^{m} v_ix_{i0}} $$

Sujeito a 

$$ \frac{\sum_{r=1}^{s} u_ry_{r}}{\sum_{i=1}^{m} v_ix_{i}   } \leq 1, \, j = 1,2,...,n$$

$$ u_r \geq 0, \; r = 1,2,...,s$$

$$ v_i \geq 0, \; i = 1,2,...,m$$

Sendo que j representa o índice de cada DMU, variando de 1 até n. $y_{rj}$ e $x_{ij}$, por sua vez, representam os valores da r-ésima variável de saída e da i-ésima variável de entrada para a j-ésima DMU, respectivamente. Paralelamente, $u_r$ é o peso dado para a r-ésima variável de saída e $v_i$ o peso da i-ésima variável de entrada. $w_{j}$ é a eficiência relativa da $DMU_j$

O problema de otimização deve ser solucionado para cada DMU. Sendo assim, para a empresa E, que possui 10 DMUs, devemos rodar a otimização 10 vezes.

A função clássica de otimização da produtividade necessita de uma solução de programação fracionária. Para transformar a solução em uma programação linear, iguala-se o denominador desta equação a 1.
As premissas da otimização passam a ser:

$$ Max \; \sum_{r=1}^{s} u_ry_{r0} = w_0$$   

Sujeito a 

$$\sum_{i=1}^{m} v_ix_{i0} = 1 $$

$$ \sum_{r=1}^{s} u_ry_{r0} - \sum_{i=1}^{m} v_ix_{i0} \leq 0, \, j = 1,2,...,n$$

$$ u_r \geq 0, \; r = 1,2,...,s$$

$$ v_i \geq 0, \; i = 1,2,...,m$$


Este é o modelo primal, orientado a input. Já este abaixo é o modelo dual, orientado a output.

$$ Min \; \theta_0$$   

Sujeito a

$$ x_{i0}\theta_0 \geq \sum_{j\in J} x_{ij} \lambda _j $$

$$ y_{r0} \leq \sum_{j\in J} y_{rj} \lambda _j, \; \forall j \in J$$

$$ \lambda _j \geq 0, \; \forall j \in J$$

$$\sum_{j\in J} \lambda _j \leq 1$$ 


O modelo BCC acrescenta ao modelo CCR uma constante $C_0$, conhecida como fator de escala, que permite que a fronteira de eficiência seja delimitada por retornos variáveis de escala ao invés de retornos constantes apenas. Tal fato representa, de fato, o "envelopamento" dos dados.

As equações abaixo delimitam o modelo primal BCC, orientado a insumos.

$$ Max \; \sum_{r=1}^{s} u_ry_{r0} + C_0= w_0$$   

Sujeito a 

$$\sum_{i=1}^{m} v_ix_{i0} = 1 $$ 

$$ \sum_{r=1}^{s} u_ry_{r0} - \sum_{i=1}^{m} v_ix_{i0} + C_0\leq 0, \, j = 1,2,...,n$$

$$ u_r \geq 0, \; r = 1,2,...,s$$

$$ v_i \geq 0, \; i = 1,2,...,m$$

$$ C_0 \; livre $$

A base de dados da empresa E, no entanto, é favorável à aplicação do modelo CCR, uma vez que não apresenta retornos variáveis de escala. 

Outro ponto é que não foram dadas informações suficientes para uma discussão sobre a opção de utilizar um modelo orientado a inputs ou outputs. Sendo assim, vamos supor que as DMUs da empresa "E" possam realizar uma melhor gestão dos insumos, minimizando-os, mantendo-se os outputs fixos. Deste modo, vamos focar na aplicação do modelo CCR – produto orientado para uma melhor eficiëncia de alocação.

Pois bem, a aplicação da análise foi modelada na classe DEA, cujo código foi retirado e validado do seguinte repositório: https://github.com/metjush/envelopment-py/blob/master/envelopment.py


