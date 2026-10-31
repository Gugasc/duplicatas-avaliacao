# Detecção de duplicatas em Python

Projeto de Análise e Otimização de Sistemas, Av2 e Av3. Tema 1 do enunciado.
O projeto anterior enviado como referência aborda autocompletar por prefixo (tema 3).

## Contrato

As três funções aceitam uma lista de inteiros, retornam `True` quando existem
dois índices com valores iguais, e não modificam a lista. A restrição a inteiros
garante que ordenação e hashing sejam aplicáveis. Igualdade entre objetos
arbitrários ou não hashable não faz parte deste contrato.

| Etapa | Implementação | Tempo no pior caso | Espaço adicional |
| --- | --- | --- | --- |
| Inicial | Pares com laços aninhados | O(n²) | O(1) |
| Av2 | Copiar, ordenar e comparar vizinhos | O(n log n) | O(n) |
| Av3 | Conjunto de valores já vistos | O(n) esperado | O(n) |

A ordenação é O(n log n) no pior caso, embora a entrada sequencial do benchmark
possa favorecer o Timsort de Python. A busca/inserção no conjunto custa O(1)
em média; colisões adversariais podem alterar o pior caso. A versão final pode
encerrar ao encontrar uma duplicata cedo, como a original.

## Organização

- `src/duplicatas.py`: versão original e acesso às duas otimizações.
- `av2_ordenacao/algoritmo.py`: implementação da Av2.
- `av3_conjunto/algoritmo.py`: implementação da Av3.
- `scripts/` e `resultados/tempos.csv`: benchmark, gerador e dados compartilhados.

A Av3 usa um conjunto; por isso sua pasta se chama `av3_conjunto`.

## Execução

Na raiz do projeto, com Python 3.10 ou superior:

```bash
python -m unittest discover -s tests -v
python -m scripts.benchmark
```

O benchmark grava `resultados/tempos.csv` e `resultados/ambiente.json`.
Para gerar somente a análise, instale as dependências e rode o script após o
benchmark:

```bash
python -m pip install -r requirements.txt
python -m scripts.gerar_entregas
```

O script cria `av2_ordenacao/relatorios/Analise_Av2_Duplicatas.pdf` e
`av3_conjunto/relatorios/Analise_Av3_Duplicatas.pdf`, com tabelas de
complexidade, tempos, ganhos e gráficos. Cada gráfico é salvo na subpasta
`resultados/` de sua etapa. Ele não gera textos de relatório, apresentações
ou notas. As pastas de saída são criadas quando o gerador é executado.

## Interpretação

As medições isolam a função; não incluem a geração da lista, I/O ou outras
partes de um sistema. São cinco repetições por configuração e a tabela usa a
mediana. O benchmark fornecido usa entradas ordenadas sem duplicatas; também
vale repetir com dados em ordem embaralhada, duplicatas precoces e outras
máquinas. Não extrapole os tempos absolutos para produção.

## Equipe e integridade

Preencher os nomes da equipe e adaptar a apresentação oral antes da entrega.
Os textos, scripts de apoio e estrutura foram elaborados com auxílio de IA.
O grupo deve revisar o conteúdo, compreender o código e declarar o uso de IA
conforme as orientações da disciplina. Não foram copiados trechos de fontes
externas; a versão inicial é o exemplo fornecido no enunciado.
