# EC-Project

É possível encontrar soluções para os números de João Brandão e para o Knapsack.

## Números de João Brandão

O código com o algoritmo evolucionário para os números de João Brandão encontra-se no ficheiro "sea.py".

Para correr o algoritmo é necessário usar o comando:

```bash
python JBTeste.py <freq> <replace_n> <method> <seed>
```
### Parâmetros:
- "freq" é a percentagem de frequência de troca [0, 1]
- "replace_n" é a percentagem de indivíduos a serem trocados [0, 1]
- "method" é o método das trocas dos elementos da população [1, 3]
- "seed" é a seed utilizada para gerar números aleatórios

## Problema de Knapsack

O código com o algoritmo evolucionário para o Knapsack encontra-se no ficheiro "sea_knapsack.py".

Para correr o algoritmo é necessário usar o comando:

```bash
python knapsackTeste.py <freq> <replace_n> <method> <seed>
```
### Parâmetros:
- "freq" é a percentagem de frequência de troca [0, 1]
- "replace_n" é a percentagem de indivíduos a serem trocados [0, 1]
- "method" é o método das trocas dos elementos da população [1, 3]
- "seed" é a seed utilizada para gerar números aleatórios
