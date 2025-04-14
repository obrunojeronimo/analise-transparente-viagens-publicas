# src/plotagem.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plotar_viagens_por_cargo(df):
    df_pivot = df.pivot(index="Cargo", columns="Ano", values="n_viagens").fillna(0)
    df_pivot = df_pivot[sorted(df_pivot.columns, reverse=True)]

    fig, ax = plt.subplots(figsize=(16, 6))
    df_pivot.plot(kind="barh", ax=ax, colormap="Set2")
    for container in ax.containers:
        ax.bar_label(
            container,
            labels=[f"{int(v):,}" for v in container.datavalues],
            label_type="edge",
            color="black",
        )
    ax.set_facecolor("#f0f0f0")
    fig.suptitle("Viagens por cargo público divididas por ano", fontsize=16)
    plt.figtext(
        0.65,
        0.89,
        "Fonte: Portal da Transparência (https://portaldatransparencia.gov.br/)",
        fontsize=8,
    )
    plt.grid(color="gray", linestyle="--", linewidth=0.5)
    plt.yticks(fontsize=8)
    plt.xlabel("Número de viagens")
    plt.ylabel("Cargo")
    plt.legend(title="Ano")
    plt.show()


def plotar_gasto_por_cargo(df):
    df["Cargo (Ano)"] = df.apply(lambda row: f"{row['Cargo']} ({row['Ano']})", axis=1)
    fig, ax = plt.subplots(figsize=(21, 7))
    ax.barh(df["Cargo (Ano)"], df["despesas_totais"], color="#9c0402")
    ax.invert_yaxis()
    for index, value in enumerate(df["despesas_totais"]):
        ax.text(
            value,
            index,
            f"{value:,.0f}",
            fontsize=12,
            va="center",
            ha="left",
            color="black",
        )
    ax.set_facecolor("#f0f0f0")
    fig.suptitle("Gasto total por cargo público", fontsize=16)
    plt.figtext(
        0.65,
        0.89,
        "Fonte: Portal da Transparência (https://portaldatransparencia.gov.br/)",
        fontsize=8,
    )
    plt.grid(color="gray", linestyle="--", linewidth=0.5)
    plt.yticks(fontsize=8)
    plt.xlabel("Despesas Totais (R$ - Valores em milhões)")
    plt.show()


def plotar_gasto_ministerio(df):
    df_gasto_por_ministerio_ano = (
        df.groupby(["Ano", "Nome do órgão superior"])
        .agg(despesas_totais=("Despesas", "sum"))
        .reset_index()
        .sort_values(by="despesas_totais", ascending=False)
    )
    df_gasto_por_ministerio_ano["Ministério (Ano)"] = df_gasto_por_ministerio_ano.apply(
        lambda row: f"{row['Nome do órgão superior']} ({row['Ano']})", axis=1
    )

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.barh(
        df_gasto_por_ministerio_ano["Ministério (Ano)"].head(10),
        df_gasto_por_ministerio_ano["despesas_totais"].head(10),
        color="#FFC300",
    )
    ax.invert_yaxis()
    for i, v in enumerate(df_gasto_por_ministerio_ano["despesas_totais"].head(10)):
        ax.annotate(
            f"{v:,.0f}",
            xy=(v, i),
            xytext=(5, -5),
            textcoords="offset points",
            fontsize=10,
            color="black",
        )
    ax.set_facecolor("#f0f0f0")
    ax.set_xlim(0, df_gasto_por_ministerio_ano["despesas_totais"].max() * 1.1)
    fig.suptitle("Gasto total por ministério", fontsize=16)
    plt.figtext(
        0.65,
        0.89,
        "Fonte: Portal da Transparência (https://portaldatransparencia.gov.br/)",
        fontsize=8,
    )
    plt.grid(color="gray", linestyle="--", linewidth=0.5)
    plt.yticks(fontsize=8)
    plt.xlabel("Despesas Totais (R$ - Valores em milhões)")
    plt.show()


def plotar_gasto_por_requisitante(df):
    df_gasto_por_requisitante_ano = (
        df.groupby(["Ano", "Nome órgão solicitante"])
        .agg(despesas_totais=("Despesas", "sum"))
        .reset_index()
        .sort_values(by="despesas_totais", ascending=False)
    )
    df_gasto_por_requisitante_ano["Requisitante (Ano)"] = (
        df_gasto_por_requisitante_ano.apply(
            lambda row: f"{row['Nome órgão solicitante']} ({row['Ano']})", axis=1
        )
    )

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.barh(
        df_gasto_por_requisitante_ano["Requisitante (Ano)"].head(10),
        df_gasto_por_requisitante_ano["despesas_totais"].head(10),
        color="#5f8c0d",
    )
    ax.invert_yaxis()
    for i, v in enumerate(df_gasto_por_requisitante_ano["despesas_totais"].head(10)):
        ax.annotate(
            f"{v:,.0f}",
            xy=(v, i),
            xytext=(5, -5),
            textcoords="offset points",
            fontsize=10,
            color="black",
        )
    ax.set_facecolor("#f0f0f0")
    ax.set_xlim(0, df_gasto_por_requisitante_ano["despesas_totais"].max() * 1.1)
    fig.suptitle("Gasto total por requisitante", fontsize=16)
    plt.figtext(
        0.65,
        0.89,
        "Fonte: Portal da Transparência (https://portaldatransparencia.gov.br/)",
        fontsize=8,
    )
    plt.grid(color="gray", linestyle="--", linewidth=0.5)
    plt.yticks(fontsize=8)
    plt.xlabel("Despesas Totais (R$ - Valores em milhões)")
    plt.show()


def plotar_evolucao_gasto_top5(df):
    """
    Plota a evolução do gasto total dos 5 órgãos com maior gasto.

    Parâmetros:
        df (pd.DataFrame): DataFrame processado contendo os dados para a plotagem.
    """
    import matplotlib.pyplot as plt  # Importando matplotlib dentro da função

    # Verifica se as colunas necessárias estão presentes no DataFrame
    colunas_necessarias = [
        "Ano",
        "Nome órgão solicitante",
        "despesas_totais",
        "percentual_variacao",
    ]
    if not all(coluna in df.columns for coluna in colunas_necessarias):
        raise ValueError(f"O DataFrame deve conter as colunas: {colunas_necessarias}")

    # Criar subplots
    orgao_unicos = df["Nome órgão solicitante"].unique()
    fig, axes = plt.subplots(
        len(orgao_unicos), 1, figsize=(12, len(orgao_unicos) * 3), sharex=True
    )

    # Plotar os gráficos para cada órgão
    for ax, orgao in zip(axes, orgao_unicos):
        dados_orgao = df[df["Nome órgão solicitante"] == orgao]
        ax.plot(
            dados_orgao["Ano"],
            dados_orgao["despesas_totais"],
            marker="o",
            color="#5f8c0d",
        )
        ax.set_title(orgao, fontsize=10)
        ax.set_ylabel("Despesas Totais (R$ - Valores em milhões)", fontsize=8)
        ax.grid(color="gray", linestyle="--", linewidth=0.5, axis="y")

        # Ajustar os limites do eixo y para incluir os rótulos
        max_valor = dados_orgao["despesas_totais"].max()
        ax.set_ylim(0, max_valor * 1.2)  # Aumenta o limite superior em 20%

        # Adicionar rótulos de dados com percentual de variação
        for x, y, var in zip(
            dados_orgao["Ano"],
            dados_orgao["despesas_totais"],
            dados_orgao["percentual_variacao"],
        ):
            label = f"{y:,.0f}\n({var:+.1f}%)" if not pd.isna(var) else f"{y:,.0f}"
            ax.annotate(
                label,
                xy=(x, y),
                xytext=(0, 5),
                textcoords="offset points",
                fontsize=8,
                ha="center",
            )

        # Ajustar o eixo x para exibir apenas os anos como categorias
        ax.set_xticks([2022, 2023, 2024])
        ax.set_xticklabels(["2022", "2023", "2024"], fontsize=10)

    # Ajustes finais
    axes[-1].set_xlabel("Ano", fontsize=10)
    plt.tight_layout()
    plt.show()


def plotar_correlacao(df):
    if "n_viagens" not in df.columns:
        df["n_viagens"] = df.groupby("Ano")[
            "Identificador do processo de viagem"
        ].transform("count")
    correlacao = df[["n_viagens", "Despesas"]].corr()
    print("Correlação entre número de viagens e despesas totais:")
    print(correlacao)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["n_viagens"], df["Despesas"], alpha=0.6, color="#5f8c0d")
    ax.set_title("Correlação entre número de viagens e despesas")
    ax.set_xlabel("Número de Viagens")
    ax.set_ylabel("Despesas Totais (R$)")
    plt.show()


def plotar_eficiencia_orgaos(df):
    df_orgao_eficiencia = (
        df.groupby("Nome órgão solicitante")
        .agg(
            total_viagens=("Nome", "count"),
            total_gasto=("Despesas", "sum"),
            custo_medio=("Despesas", "mean"),
        )
        .reset_index()
        .sort_values(by="total_viagens", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        df_orgao_eficiencia["total_viagens"],
        df_orgao_eficiencia["custo_medio"],
        c=df_orgao_eficiencia["total_gasto"],
        cmap="viridis",
        alpha=0.8,
    )
    ax.set_title(
        "Relação entre número de viagens e custo médio por viagem", fontsize=14
    )
    ax.set_xlabel("Número de Viagens", fontsize=12)
    ax.set_ylabel("Custo Médio por Viagem (R$)", fontsize=12)
    ax.grid(color="gray", linestyle="--", linewidth=0.5)
    cbar = plt.colorbar(scatter)
    cbar.set_label("Total Gasto (R$)", fontsize=12)
    plt.tight_layout()
    plt.show()


def plotar_desperdicio(df):
    df_orgao_desperdicio = (
        df.groupby("Nome órgão solicitante")
        .agg(
            total_viagens=("Nome", "count"),
            total_gasto=("Despesas", "sum"),
            custo_medio=("Despesas", "mean"),
        )
        .reset_index()
        .sort_values(by="total_gasto", ascending=False)
    )
    df_orgao_desperdicio["desperdicio"] = (
        df_orgao_desperdicio["total_gasto"] / df_orgao_desperdicio["total_viagens"]
    )
    df_top_desperdicio = df_orgao_desperdicio.sort_values(
        by="desperdicio", ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(
        df_top_desperdicio["Nome órgão solicitante"],
        df_top_desperdicio["desperdicio"],
        color="#FF5733",
    )
    ax.set_title(
        "Órgãos com maior custo por viagem (possível desperdício)", fontsize=14
    )
    ax.set_xlabel("Custo Médio por Viagem (R$)", fontsize=12)
    ax.set_ylabel("Órgão Solicitante", fontsize=12)
    ax.grid(color="gray", linestyle="--", linewidth=0.5, axis="x")
    for i, v in enumerate(df_top_desperdicio["desperdicio"]):
        ax.text(v, i, f"{v:,.2f}", fontsize=9, va="center", ha="left", color="black")
    plt.tight_layout()
    plt.show()
