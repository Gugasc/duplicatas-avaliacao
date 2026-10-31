"""Versão original e acesso às duas otimizações.

Retorna True se dois índices distintos contêm o mesmo valor. A entrada não é
modificada. A versão original reproduz o exemplo do enunciado da disciplina.
"""

from av2_ordenacao.algoritmo import av2_ordenacao
from av3_conjunto.algoritmo import av3_conjunto


def original(valores: list[int]) -> bool:
    for i in range(len(valores)):
        for j in range(i + 1, len(valores)):
            if valores[i] == valores[j]:
                return True
    return False
