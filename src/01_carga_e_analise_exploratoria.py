"""
============================================================================
UNIVERSIDADE PRESBITERIANA MACKENZIE
Faculdade de Computação e Informática - FCI
Inteligência Artificial – 7ºK SI – Noite | Prof. Dr. Leandro Zerbinatti

Projeto: GrafitoIA - Predição de Risco de Inadimplência em Empréstimos a
          Pequenos Negócios (com aplicação potencial a MEIs via Grafito)

Membros da Equipe:
    1. André Contarelli Lima         - RA: 10410280 - 10410280@mackenzista.com.br
    2. Lucas Bittencourt de Oliveira - RA: 10409476 - 10409476@mackenzista.com.br
    3. Fernando Paiva                - RA: 10416680 - 10416680@mackenzista.com.br

Arquivo: 01_carga_e_analise_exploratoria.py
Síntese do Conteúdo:
    Carga, saneamento e análise exploratória de dados (EDA) do conjunto real
    "SBA National Dataset" (Should This Loan be Approved or Denied?). Realiza
    a conversão de variáveis monetárias de texto para ponto flutuante, filtra
    status resolutivos (PIF e CHGOFF), gera a variável-alvo binária Default,
    extrai setores da classificação NAICS, constrói atributos derivados
    (PercentualGarantidoSBA e ValorPorFuncionario) e produz sumários estatísticos
    e gráficos de suporte para o relatório da N1.

Como Obter o Dataset:
    O dataset bruto não é versionado diretamente por restrições de tamanho:
    1) Criar conta gratuita em https://www.kaggle.com
    2) Baixar em:
       https://www.kaggle.com/datasets/mirbektoktogaraev/should-this-loan-be-approved-or-denied
    3) Salvar o arquivo descompactado como "SBAnational.csv" na pasta do script
       ou na pasta data/ (ajustar CAMINHO_CSV se necessário).

Histórico de Alterações:
    Data       | Autor                         | Descrição da Atualização
    -----------+-------------------------------+------------------------------------------
    2026-09-11 | André Contarelli Lima         | Criação inicial do script de carga e EDA.
    2026-09-11 | Lucas Bittencourt de Oliveira | Mapeamento setorial dos códigos NAICS e
               |                               | rotinas de conversão monetária.
    2026-09-11 | Fernando Paiva                | Geração e estilização das figuras de EDA
               |                               | (balanceamento de classes e setor).
============================================================================
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CAMINHO_CSV = "SBAnational.csv"

# Mapeamento dos dois primeiros dígitos do NAICS para o setor econômico
SETOR_NAICS = {
    "11": "Agricultura, silvicultura, pesca e caça",
    "21": "Mineração, extração de petróleo e gás",
    "22": "Utilidades (água, energia, gás)",
    "23": "Construção",
    "31": "Manufatura", "32": "Manufatura", "33": "Manufatura",
    "42": "Comércio atacadista",
    "44": "Comércio varejista", "45": "Comércio varejista",
    "48": "Transporte e armazenagem", "49": "Transporte e armazenagem",
    "51": "Informação",
    "52": "Finanças e seguros",
    "53": "Imóveis e locação",
    "54": "Serviços profissionais, científicos e técnicos",
    "55": "Gestão de empresas",
    "56": "Serviços administrativos e de apoio",
    "61": "Serviços educacionais",
    "62": "Saúde e assistência social",
    "71": "Artes, entretenimento e recreação",
    "72": "Alojamento e alimentação",
    "81": "Outros serviços",
    "92": "Administração pública",
}


def carregar_dataset(caminho=CAMINHO_CSV):
    """Carrega o CSV bruto da SBA com tratamento de exceção amigável."""
    try:
        df = pd.read_csv(caminho, low_memory=False)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Arquivo '{caminho}' não encontrado. Baixe o dataset em: "
            "https://www.kaggle.com/datasets/mirbektoktogaraev/should-this-loan-be-approved-or-denied "
            "e posicione-o com o nome 'SBAnational.csv' no mesmo diretório deste script."
        ) from exc
    return df


def limpar_e_preparar(df):
    """Limpeza, tratamento e engenharia de atributos do dataset SBA."""
    df = df.copy()

    # Colunas monetárias com texto (ex: "$45,000.00") -> float
    colunas_monetarias = [
        "DisbursementGross", "BalanceGross", "ChgOffPrinGr",
        "GrAppv", "SBA_Appv",
    ]
    for col in colunas_monetarias:
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = (
                df[col].astype(str)
                .str.replace(r"[\$,]", "", regex=True)
                .str.strip()
                .replace({"": np.nan, "nan": np.nan})
                .astype(float)
            )

    # Filtragem de registros com desfecho resolutivo conhecido
    df = df[df["MIS_Status"].isin(["P I F", "PIF", "CHGOFF"])].copy()
    df["MIS_Status"] = df["MIS_Status"].replace({"P I F": "PIF"})

    # Variável binária dependente: 1 = inadimplência (CHGOFF), 0 = adimplente (PIF)
    df["Default"] = np.where(df["MIS_Status"] == "CHGOFF", 1, 0)

    # Agregação setorial via NAICS
    df["NAICS"] = df["NAICS"].astype(str)
    df["Setor"] = df["NAICS"].str[:2].map(SETOR_NAICS).fillna("Não informado")

    # Tratamento de campos temporais
    for col in ["ApprovalDate", "DisbursementDate", "ChgOffDate"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d-%b-%y", errors="coerce")

    # Engenharia de características (Features)
    df["PercentualGarantidoSBA"] = np.where(
        df["GrAppv"] > 0, df["SBA_Appv"] / df["GrAppv"], np.nan
    )
    df["ValorPorFuncionario"] = np.where(
        (df["NoEmp"].fillna(0) + 1) > 0,
        df["DisbursementGross"] / (df["NoEmp"].fillna(0) + 1),
        np.nan,
    )
    df["NegocioNovo"] = np.where(df["NewExist"] == 2, 1, 0)

    return df


def analise_exploratoria(df, prefixo_saida="eda"):
    """Gera sumários estatísticos e salva as figuras descritivas."""
    resumo = df.describe(include="number").T
    resumo.to_csv(f"{prefixo_saida}_resumo_estatistico.csv")

    taxa_geral = df["Default"].mean()
    print(f"Taxa geral de inadimplência (Default=1): {taxa_geral:.2%}")

    taxa_por_setor = df.groupby("Setor")["Default"].mean().sort_values(ascending=False)
    taxa_por_setor.to_csv(f"{prefixo_saida}_taxa_default_por_setor.csv")

    # Gráfico 1: Inadimplência por setor
    plt.figure(figsize=(9, 5.5))
    taxa_por_setor.plot(kind="barh", color="#C44E52")
    plt.xlabel("Taxa de Inadimplência (Default)")
    plt.title("Taxa de Inadimplência por Setor Econômico (NAICS)")
    plt.tight_layout()
    plt.savefig(f"{prefixo_saida}_fig1_taxa_default_por_setor.png", dpi=140)
    plt.close()

    # Gráfico 2: Proporção das classes do alvo
    plt.figure(figsize=(4.5, 4.5))
    df["Default"].value_counts(normalize=True).sort_index().plot(
        kind="bar", color=["#4C72B0", "#DD8452"]
    )
    plt.xticks([0, 1], ["Quitado (0)", "Inadimplente (1)"], rotation=0)
    plt.ylabel("Proporção Amostral")
    plt.title("Balanceamento da Variável-Alvo (Default)")
    plt.tight_layout()
    plt.savefig(f"{prefixo_saida}_fig2_balanceamento_classe_alvo.png", dpi=140)
    plt.close()

    # Gráfico 3: Maturidade do negócio versus inadimplência
    plt.figure(figsize=(5, 4.5))
    df.groupby("NegocioNovo")["Default"].mean().plot(kind="bar", color="#4C72B0")
    plt.xticks([0, 1], ["Negócio Existente", "Negócio Novo"], rotation=0)
    plt.ylabel("Taxa Média de Inadimplência")
    plt.title("Inadimplência: Negócio Novo vs. Existente")
    plt.tight_layout()
    plt.savefig(f"{prefixo_saida}_fig3_novo_vs_existente.png", dpi=140)
    plt.close()

    return {"taxa_geral": taxa_geral, "taxa_por_setor": taxa_por_setor}


if __name__ == "__main__":
    bruto = carregar_dataset()
    preparado = limpar_e_preparar(bruto)
    preparado.to_csv("SBAnational_preparado.csv", index=False)
    analise_exploratoria(preparado)
    print("Processamento concluído com sucesso.")
