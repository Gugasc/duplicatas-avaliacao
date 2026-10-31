"""Benchmark reproduzível do pior caso, sem incluir criação da entrada."""

import csv
import json
import platform
import statistics
import sys
import time
from pathlib import Path

from av2_ordenacao.algoritmo import av2_ordenacao
from av3_conjunto.algoritmo import av3_conjunto
from src.duplicatas import original

RAIZ = Path(__file__).resolve().parents[1]
RESULTADOS = RAIZ / 'resultados'
TAMANHOS = (250, 500, 1000, 2000, 4000)
REPETICOES = 5
VERSOES = (('Original', original), ('Av2 ordenacao', av2_ordenacao),
           ('Av3 conjunto', av3_conjunto))


def medir(funcao, dados):
    amostras = []
    for _ in range(REPETICOES):
        inicio = time.perf_counter_ns()
        resultado = funcao(dados)
        amostras.append((time.perf_counter_ns() - inicio) / 1_000_000)
        assert resultado is False
    return statistics.median(amostras), min(amostras)


def main():
    RESULTADOS.mkdir(exist_ok=True)
    linhas = []
    for n in TAMANHOS:
        dados = list(range(n))  # Sem duplicatas: pior caso para os três.
        for nome, funcao in VERSOES:
            mediana, menor = medir(funcao, dados)
            linhas.append({'n': n, 'versao': nome,
                           'mediana_ms': f'{mediana:.6f}',
                           'menor_ms': f'{menor:.6f}',
                           'repeticoes': REPETICOES})
            print(f'{n:5d} {nome:15s} {mediana:12.6f} ms')
    with (RESULTADOS / 'tempos.csv').open('w', newline='', encoding='utf-8') as arq:
        gravador = csv.DictWriter(arq, fieldnames=linhas[0].keys())
        gravador.writeheader()
        gravador.writerows(linhas)
    (RESULTADOS / 'ambiente.json').write_text(json.dumps({
        'python': sys.version, 'plataforma': platform.platform(),
        'processador': platform.processor(), 'repeticoes': REPETICOES,
        'medida': 'mediana de tempo de parede em ms',
        'dados': 'inteiros sequenciais sem repeticao, gerados fora da medicao',
        'data_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }, indent=2, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
