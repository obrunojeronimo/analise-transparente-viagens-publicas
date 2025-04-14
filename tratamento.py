# src/tratamento.py
import os
import pandas as pd


def filtrar_cargos_relevantes(df_viagens, df_consolidado):
    df_cargos_ano = (
        df_viagens.groupby(["Ano", "Cargo"])["Nome"].count().reset_index(name="count")
    )
    df_cargos_ano["proportion"] = df_cargos_ano["count"] / df_viagens.shape[0]
    cargos_ano_relevantes = df_cargos_ano.loc[
        df_cargos_ano["proportion"] > 0.01, ["Ano", "Cargo"]
    ]
    filtro = df_consolidado.apply(
        lambda row: (row["Ano"], row["Cargo"])
        in zip(cargos_ano_relevantes["Ano"], cargos_ano_relevantes["Cargo"]),
        axis=1,
    )
    return df_consolidado[filtro]
