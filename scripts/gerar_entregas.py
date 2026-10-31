"""Gera apenas tabelas, indicadores e gráficos da análise de duplicatas."""

import csv
import os
import tempfile
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "projeto_duplicatas_matplotlib")
)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


RAIZ = Path(__file__).resolve().parents[1]
RESULTADOS = RAIZ / "resultados"
PASTAS = {"Av2": RAIZ / "av2_ordenacao", "Av3": RAIZ / "av3_conjunto"}
VERSOES = ("Original", "Av2 ordenacao", "Av3 conjunto")
CORES = ("#BC5630", "#28729B", "#087F69")
AZUL = colors.HexColor("#17324D")

# O Matplotlib fornece a fonte em Windows, Linux e macOS.
fonte = font_manager.findfont("DejaVu Sans")
negrito = font_manager.findfont(
    font_manager.FontProperties(family="DejaVu Sans", weight="bold")
)
pdfmetrics.registerFont(TTFont("DejaVu", fonte))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", negrito))

ESTILOS = getSampleStyleSheet()
ESTILOS.add(ParagraphStyle(name="TituloAnalise", fontName="DejaVu-Bold",
                          fontSize=18, leading=23, textColor=AZUL, spaceAfter=10))
ESTILOS.add(ParagraphStyle(name="SecaoAnalise", fontName="DejaVu-Bold",
                          fontSize=11, leading=15, textColor=AZUL,
                          spaceBefore=10, spaceAfter=6))
ESTILOS.add(ParagraphStyle(name="CelulaAnalise", fontName="DejaVu",
                          fontSize=8, leading=11))
ESTILOS.add(ParagraphStyle(name="NotaAnalise", fontName="DejaVu",
                          fontSize=7.5, leading=11,
                          textColor=colors.HexColor("#526578")))


def p(texto, estilo="CelulaAnalise"):
    return Paragraph(str(texto), ESTILOS[estilo])


def tabela(cabecalho, linhas, larguras):
    dados = [[p(valor) for valor in cabecalho]]
    dados.extend([p(valor) for valor in linha] for linha in linhas)
    item = Table(dados, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7F0F2")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F6F8F9")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, AZUL),
    ]))
    return item


def carregar_tempos(caminho):
    with caminho.open(newline="", encoding="utf-8") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    if not linhas:
        raise ValueError(f"CSV sem medições: {caminho}")
    tempos = {}
    for linha in linhas:
        n, versao, tempo = int(linha["n"]), linha["versao"], float(linha["mediana_ms"])
        if n <= 0 or tempo <= 0:
            raise ValueError(f"n e mediana_ms devem ser positivos: {linha}")
        if (n, versao) in tempos:
            raise ValueError(f"Medição duplicada: n={n}, versão={versao}")
        tempos[n, versao] = tempo
    tamanhos = sorted({n for n, _ in tempos})
    faltantes = [(n, v) for n in tamanhos for v in VERSOES if (n, v) not in tempos]
    if faltantes:
        raise ValueError(f"Medições ausentes: {faltantes}")
    return tamanhos, tempos


def gerar_grafico(tamanhos, tempos, versoes, caminho):
    fig, eixo = plt.subplots(figsize=(8, 4.2), dpi=160)
    for versao in versoes:
        eixo.plot(tamanhos, [tempos[n, versao] for n in tamanhos],
                  marker="o", linewidth=2, color=CORES[VERSOES.index(versao)],
                  label=versao)
    eixo.set_yscale("log")
    eixo.set_xlabel("Quantidade de inteiros (n)")
    eixo.set_ylabel("Mediana do tempo (ms) - escala logarítmica")
    eixo.set_xticks(tamanhos)
    eixo.grid(True, which="both", alpha=0.2)
    eixo.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(caminho, bbox_inches="tight")
    plt.close(fig)


def gerar_analise(etapa, tamanhos, tempos, grafico):
    versoes = VERSOES[:2] if etapa == "Av2" else VERSOES
    complexidades = [["Original", "O(n²)", "O(1)"],
                     ["Av2 - ordenação", "O(n log n)", "O(n)"]]
    if etapa == "Av3":
        complexidades.append(["Av3 - conjunto", "O(n) esperado", "O(n)"])
    tempos_linhas = [[str(n)] + [f"{tempos[n, v]:.4f}" for v in versoes]
                    for n in tamanhos]
    ganhos_linhas = [[str(n)] + [f"{tempos[n, 'Original'] / tempos[n, v]:.2f}×"
                                 for v in versoes[1:]] for n in tamanhos]
    conteudo = [
        p(f"Análise de desempenho - {etapa}", "TituloAnalise"),
        p("Complexidade assintótica", "SecaoAnalise"),
        tabela(["Versão", "Tempo", "Espaço adicional"],
               complexidades, [6 * cm, 5.5 * cm, 5.5 * cm]),
        p("Tempos medianos (ms)", "SecaoAnalise"),
        tabela(["n"] + [f"{v} (ms)" for v in versoes], tempos_linhas,
               [2 * cm] + [15 * cm / len(versoes)] * len(versoes)),
        p("Ganho sobre a versão original", "SecaoAnalise"),
        tabela(["n"] + list(versoes[1:]), ganhos_linhas,
               [2 * cm] + [15 * cm / (len(versoes) - 1)] * (len(versoes) - 1)),
        Spacer(1, 8),
        Image(str(grafico), width=16 * cm, height=8.2 * cm),
        p("Fonte: resultados/tempos.csv. Entrada sequencial sem duplicatas; "
          "mediana de cinco execuções por configuração. Eixo vertical em "
          "escala logarítmica.", "NotaAnalise"),
    ]
    destino = PASTAS[etapa] / "relatorios" / f"Analise_{etapa}_Duplicatas.pdf"
    documento = SimpleDocTemplate(str(destino), pagesize=A4,
                                  leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                                  topMargin=1.4 * cm, bottomMargin=1.4 * cm)
    documento.build(conteudo)
    return destino


def main():
    RESULTADOS.mkdir(exist_ok=True)
    tamanhos, tempos = carregar_tempos(RESULTADOS / "tempos.csv")
    for etapa, versoes in (("Av2", VERSOES[:2]), ("Av3", VERSOES)):
        pasta = PASTAS[etapa]
        (pasta / "resultados").mkdir(parents=True, exist_ok=True)
        (pasta / "relatorios").mkdir(exist_ok=True)
        grafico = pasta / "resultados" / "escalabilidade.png"
        gerar_grafico(tamanhos, tempos, versoes, grafico)
        destino = gerar_analise(etapa, tamanhos, tempos, grafico)
        print(f"Criados: {destino} e {grafico}")


if __name__ == "__main__":
    main()
