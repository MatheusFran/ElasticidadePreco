import matplotlib.pyplot as plt
import seaborn as sns
import math
import pandas as pd


def categoricalDistri(df, list_features):
    ncol = 3
    nrow = math.ceil(len(list_features) / ncol)

    fig, ax = plt.subplots(nrow, ncol, figsize=(6 * ncol, 5 * nrow))
    ax = ax.flatten()

    for i, feature in enumerate(list_features):
        palette = sns.dark_palette("#79C", df[feature].nunique())
        sns.countplot(
            ax=ax[i],
            data=df,
            x=feature,
            palette=palette,
            order=df[feature].value_counts().sort_values(ascending=False).index
        )
        ax[i].set_xlabel(feature)
        ax[i].set_ylabel("Frequência")
        ax[i].set_title(f"Distribuição de {feature}")
        ax[i].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()


def numericalDistri(df, list_features, colunas, logScale=False):
    ncol = colunas
    nrow = math.ceil(len(list_features) / ncol)

    fig, ax = plt.subplots(nrow, ncol, figsize=(6 * ncol, 5 * nrow))
    ax = ax.flatten()

    # Criar uma paleta de cores contínua para todos os gráficos
    palette = sns.dark_palette("#79C", len(list_features))

    for i, feature in enumerate(list_features):
        sns.histplot(
            ax=ax[i],
            data=df,
            kde=True,
            x=feature,
            color=palette[i],
            log_scale=logScale,
        )
        ax[i].set_xlabel(feature)
        ax[i].set_ylabel('Frequência')
        ax[i].set_title(f"Distribuição de {feature}")

    plt.tight_layout()
    plt.show()


def bivariate_analysis(df, var_x, var_y):
    """
    Gera gráficos bivariados dependendo do tipo das variáveis.
    """
    # Verificar tipos
    is_x_num = pd.api.types.is_numeric_dtype(df[var_x])
    is_y_num = pd.api.types.is_numeric_dtype(df[var_y])
    palette = sns.dark_palette("#79C")

    if is_x_num and is_y_num:
        # Numérica × Numérica
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=df, x=var_x, y=var_y, alpha=0.6)
        sns.regplot(data=df, x=var_x, y=var_y, scatter=False, color="red")
        plt.title(f"Relação entre {var_x} e {var_y}")
        plt.show()

    elif is_x_num and not is_y_num:
        # Numérica × Categórica (inverter e chamar de novo para manter padrão)
        bivariate_analysis(df, var_y, var_x)

    elif not is_x_num and is_y_num:
        # Categórica × Numérica
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x=var_x, y=var_y)
        sns.stripplot(data=df, x=var_x, y=var_y, color="black", alpha=0.3)
        plt.title(f"{var_y} por {var_x}")
        plt.xticks(rotation=90)
        plt.show()

    else:
        # Categórica × Categórica
        ctab = pd.crosstab(df[var_x], df[var_y])
        plt.figure(figsize=(8, 5))
        sns.heatmap(ctab, annot=True, fmt="d", cmap="Blues")
        plt.title(f"Frequência cruzada de {var_x} e {var_y}")
        plt.show()


