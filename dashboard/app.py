import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
import joblib, tempfile

st.set_page_config(page_title="⚽ Match Predictor", page_icon="⚽")

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)


@st.cache_resource
def load_model():
    client = storage.Client(credentials=credentials)
    bucket = client.bucket("football-pipeline-football-dashboard-490415")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".joblib") as f:
        bucket.blob("models/model.joblib").download_to_file(f)
        model = joblib.load(f.name)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".joblib") as f:
        bucket.blob("models/label_encoder.joblib").download_to_file(f)
        le = joblib.load(f.name)
    return model, le


st.title("⚽ Football Match Predictor")
st.caption("Prédiction basée sur la forme des 5 derniers matchs · XGBoost")

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
    with st.spinner("Chargement du modèle..."):
        model, le = load_model()
    pred = model.predict([[hw, hd, hl, aw, ad, al]])
    result = le.inverse_transform(pred)[0]
    emoji = {"home_win": "🏠✅", "away_win": "✈️✅", "draw": "🤝"}
    st.success(f"Résultat prédit : **{result}** {emoji.get(result, '❓')}")
