# src/processamento.py
import os
import pandas as pd

# Configurações globais
df_configs = {"display.max_columns": None, "display.float_format": "{:.2f}".format}
for key, value in df_configs.items():
    pd.set_option(key, value)

# configuração de exibição de colunas
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "{:.2f}".format)


def carregar_dados(anos):
    dfs = []
    for y in anos:
        caminho_arq = f"data/{y}_Viagem.csv"
        dfs.append(
            pd.read_csv(caminho_arq, encoding="Windows-1252", sep=";", decimal=",")
        )
    return pd.concat(dfs, ignore_index=True)


def calcular_despesas(df):
    df["Despesas"] = (
        df["Valor diárias"] + df["Valor passagens"] + df["Valor outros gastos"]
    )
    return df


def converter_datas(df):
    df["Período - Data de início"] = pd.to_datetime(
        df["Período - Data de início"], format="%d/%m/%Y"
    )
    df["Período - Data de fim"] = pd.to_datetime(
        df["Período - Data de fim"], format="%d/%m/%Y"
    )
    return df


def criar_colunas_temporais(df):
    df["Mês da viagem"] = df["Período - Data de início"].dt.month_name()
    df["Dias de viagem"] = (
        df["Período - Data de fim"] - df["Período - Data de início"]
    ).dt.days
    df["Ano"] = df["Período - Data de início"].dt.year
    return df


def consolidar_dados(df):
    df_consolidado = (
        df.groupby(["Cargo", "Ano"])
        .agg(
            despesa_media=("Despesas", "mean"),
            duracao_media=("Dias de viagem", "mean"),
            despesas_totais=("Despesas", "sum"),
            destino_mais_frequente=("Destinos", pd.Series.mode),
            n_viagens=("Nome", "count"),
        )
        .reset_index()
        .sort_values(by="despesas_totais", ascending=False)
    )
    return df_consolidado


def preparar_dados_evolucao_top5(df):
    """
    Prepara os dados para o gráfico de evolução dos 5 órgãos com maior gasto total.

    Parâmetros:
        df (pd.DataFrame): DataFrame contendo as colunas 'Ano', 'Nome órgão solicitante' e 'Despesas'.

    Retorna:
        pd.DataFrame: DataFrame filtrado e processado para a plotagem.
    """
    # Agrupando por órgão solicitante e ano, e somando as despesas totais
    df_gasto_por_requisitante_ano = (
        df.groupby(["Ano", "Nome órgão solicitante"])
        .agg(despesas_totais=("Despesas", "sum"))
        .reset_index()
        .sort_values(by="despesas_totais", ascending=False)
    )

    # Selecionar os top 5 órgãos com maior gasto total
    top5_orgaos = (
        df_gasto_por_requisitante_ano.groupby("Nome órgão solicitante")[
            "despesas_totais"
        ]
        .sum()
        .nlargest(5)
        .index
    )

    # Filtrar os dados para os top 5 órgãos
    df_gasto_por_requisitante_ano_top5 = df_gasto_por_requisitante_ano[
        df_gasto_por_requisitante_ano["Nome órgão solicitante"].isin(top5_orgaos)
    ]

    # Filtrar apenas os anos 2022, 2023 e 2024
    anos_recentes = [2022, 2023, 2024]
    df_gasto_por_requisitante_ano_top5_recente = df_gasto_por_requisitante_ano_top5[
        df_gasto_por_requisitante_ano_top5["Ano"].isin(anos_recentes)
    ]

    # Calcular o percentual de crescimento ou queda em relação ao ano anterior
    df_gasto_por_requisitante_ano_top5_recente["percentual_variacao"] = (
        df_gasto_por_requisitante_ano_top5_recente.sort_values(
            by=["Nome órgão solicitante", "Ano"]
        )
        .groupby("Nome órgão solicitante")["despesas_totais"]
        .pct_change()
        * 100
    )

    return df_gasto_por_requisitante_ano_top5_recente
