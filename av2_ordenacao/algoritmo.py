"""Detecção de duplicatas por ordenação de uma cópia da entrada."""


def av2_ordenacao(valores: list[int]) -> bool:
    """Cópia ordenada e inspeção de vizinhos: O(n log n), espaço O(n)."""
    ordenados = sorted(valores)
    return any(ordenados[i] == ordenados[i - 1]
               for i in range(1, len(ordenados)))
