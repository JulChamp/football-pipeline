import streamlit as st
from google.cloud import aiplatform
from google.oauth2 import service_account
import os

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

aiplatform.init(
    project=st.secrets["GCP_PROJECT_ID"],
    location="europe-west1",
    credentials=credentials,
)

endpoint = aiplatform.Endpoint(st.secrets["VERTEX_ENDPOINT_ID"])

st.set_page_config(page_title="⚽ Match Predictor", page_icon="⚽")
st.title("⚽ Football Match Predictor")
st.caption(
    "Prédiction basée sur la forme des 5 derniers matchs · Modèle XGBoost déployé sur Vertex AI"
)

st.subheader("Équipe à domicile")
col1, col2, col3 = st.columns(3)
hw = col1.number_input("Victoires", 0, 5, 2, key="hw")
hd = col2.number_input("Nuls", 0, 5, 1, key="hd")
hl = col3.number_input("Défaites", 0, 5, 2, key="hl")

st.subheader("Équipe à l'extérieur")
col4, col5, col6 = st.columns(3)
aw = col4.number_input("Victoires", 0, 5, 1, key="aw")
ad = col5.number_input("Nuls", 0, 5, 2, key="ad")
al = col6.number_input("Défaites", 0, 5, 2, key="al")

if st.button("🔮 Prédire le résultat", type="primary"):
    aiplatform.init(project=os.getenv("GCP_PROJECT_ID"), location="europe-west1")
    endpoint = aiplatform.Endpoint(os.getenv("VERTEX_ENDPOINT_ID"))
    prediction = endpoint.predict([[hw, hd, hl, aw, ad, al]])
    labels = ["away_win", "draw", "home_win"]
    result = labels[prediction.predictions[0]]
    emoji = {"home_win": "🏠✅", "away_win": "✈️✅", "draw": "🤝"}
    st.success(f"Résultat prédit : **{result}** {emoji[result]}")
