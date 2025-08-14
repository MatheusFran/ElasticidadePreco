# app.py
import streamlit as st
import pandas as pd
import joblib
import os

# =========================
# Caminhos fixos
# =========================
MODEL_PATH = '../models/finalmodel.joblib'
DATA_PATH = '../data/interim/preprocessado.joblib'  # seu dataframe rea

# =========================
# Carregar modelo
# =========================
model_package = joblib.load(MODEL_PATH)

if isinstance(model_package, dict):
    model = model_package["model"]
    feature_cols = model_package["features"]
else:
    model = model_package
    feature_cols = []

# =========================
# Carregar dataset
# =========================
df = joblib.load(DATA_PATH)
# df = pd.read_csv(dados)

# =========================
# Função de elasticidade
# =========================
def calcular_elasticidade(model, base_input, aumento_percentual, feature_cols):
    X_original = pd.DataFrame([base_input])
    X_original = pd.get_dummies(X_original, drop_first=True).reindex(columns=feature_cols, fill_value=0)

    X_aumento = pd.DataFrame([base_input])
    X_aumento["amount"] *= (1 + aumento_percentual / 100)
    X_aumento = pd.get_dummies(X_aumento, drop_first=True).reindex(columns=feature_cols, fill_value=0)

    pred_original = model.predict(X_original).mean()
    pred_aumento = model.predict(X_aumento).mean()

    delta_q = (pred_aumento - pred_original) / pred_original
    delta_p = aumento_percentual / 100
    elasticidade = delta_q / delta_p

    return pred_original, pred_aumento, elasticidade

# =========================
# Interface Streamlit
# =========================
st.set_page_config(page_title="Dashboard Elasticidade", layout="wide")
st.title("📦 Dashboard de Elasticidade - Previsão de Boxes Shipped")
st.markdown("Insira os dados do produto e o percentual de alteração para calcular a elasticidade.")

# Select produto com base no DataFrame real
produto_sel = st.selectbox("🛒 Produto", sorted(df['product'].unique()))

# Puxar o ticket médio do produto selecionado
ticket_medio = df.loc[df['product'] == produto_sel, 'amount'].mean()
st.write(f"💲 Ticket médio atual: {ticket_medio:.2f}")

# Input do usuário para amount e percentual
amount_val = st.number_input("💲 Amount atual", min_value=0.0, value=float(ticket_medio), step=10.0)
aumento_percentual = st.number_input("📈 Percentual de alteração (%)", value=10.0, step=1.0)

# Montar entrada
entrada_usuario = {
    "product": produto_sel,
    "amount": amount_val
    # Adicione outras variáveis do modelo, se houver
}

# Calcular elasticidade
if st.button("Calcular Elasticidade"):
    pred_original, pred_aumento, elasticidade = calcular_elasticidade(
        model, entrada_usuario, aumento_percentual, feature_cols
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Vendas Originais", f"{pred_original:.2f} caixas")
    m2.metric("Vendas com Aumento", f"{pred_aumento:.2f} caixas", delta=f"{(pred_aumento - pred_original):.2f}")
    m3.metric("Elasticidade", f"{elasticidade:.2f}")
