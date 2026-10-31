"""Detecção de duplicatas com um conjunto de valores vistos."""


def av3_conjunto(valores: list[int]) -> bool:
    """Conjunto de valores vistos: O(n) esperado, espaço O(n)."""
    vistos: set[int] = set()
    for valor in valores:
        if valor in vistos:
            return True
        vistos.add(valor)
    return False
