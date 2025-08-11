import matplotlib.pyplot as plt
import seaborn as sns
import math


def categoricalDistri(df, list_features):
    ncol = 3
    nrow = math.ceil(len(list_features) / ncol)

    fig, ax = plt.subplots(nrow, ncol, figsize=(6 * ncol, 5 * nrow))
    ax = ax.flatten()

    for i, feature in enumerate(list_features):
        sns.countplot(
            ax=ax[i],
            data=df,
            x=feature,
            palette=sns.color_palette("viridis",i),
            order=df[feature].value_counts().sort_values(ascending=False).index
        )
        ax[i].set_xlabel(feature)
        ax[i].set_ylabel("Frequência")
        ax[i].set_title(f"Distribuição de {feature}")
        ax[i].tick_params(axis='x', rotation=45)

    fig.suptitle("Distribuições Categóricas", fontsize=20, fontweight="bold")
    plt.tight_layout()
    plt.show()


def numericalDistri(df, list_features,colunas,logScale=False):
    ncol = colunas
    nrow = math.ceil(len(list_features) / ncol)

    fig, ax = plt.subplots(nrow, ncol, figsize=(6 * ncol, 5 * nrow))
    ax = ax.flatten()

    for i, feature in enumerate(list_features):
        sns.histplot(
            ax=ax[i],
            data=df,
            kde=True,
            x=feature,
            palette=sns.color_palette("viridis")[i],
            log_scale=logScale,
        )
        ax[i].set_xlabel(feature)
        ax[i].set_ylabel('Frequência')
        ax[i].set_title(f"Distribuição de {feature}")

    fig.suptitle("Distribuições Númericas", fontsize=20, fontweight="bold")
    plt.tight_layout()
    plt.show()
