import random
import unittest

from av2_ordenacao.algoritmo import av2_ordenacao
from av3_conjunto.algoritmo import av3_conjunto
from src.duplicatas import original


class TesteDuplicatas(unittest.TestCase):
    def testar_casos_limite(self):
        casos = [([], False), ([1], False), ([1, 1], True),
                 ([3, 2, 1], False), ([-2, 0, -2], True),
                 ([0, 1, 2, 2], True)]
        for entrada, esperado in casos:
            for funcao in (original, av2_ordenacao, av3_conjunto):
                with self.subTest(entrada=entrada, versao=funcao.__name__):
                    copia = entrada.copy()
                    self.assertEqual(funcao(entrada), esperado)
                    self.assertEqual(entrada, copia)

    def testar_diferencial_aleatorio(self):
        gerador = random.Random(42)
        for n in range(0, 81):
            for _ in range(12):
                entrada = [gerador.randrange(-50, 50) for _ in range(n)]
                esperado = original(entrada)
                self.assertEqual(av2_ordenacao(entrada), esperado)
                self.assertEqual(av3_conjunto(entrada), esperado)


if __name__ == '__main__':
    unittest.main()
