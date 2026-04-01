# ⚽ Football Data Pipeline · GCP

Pipeline Data Engineering end-to-end sur Google Cloud Platform.  
Ingestion quotidienne → BigQuery → dbt → ML → Dashboard public.

## 🔗 Liens

- 📊 [Dashboard Looker Studio](https://lookerstudio.google.com/reporting/bb0c6db3-2690-4467-9407-49f771e8bb55)
- 🔮 [App Prédictions ML](https://football-pipeline-e5oceao3swkex579zcmkqt.streamlit.app/#75cb2433)
- 📐 [Lineage dbt](URL_GITHUB_PAGES)

## 🏗 Architecture

```
API-Sports → Cloud Run → GCS → BigQuery → dbt → XGBoost → Streamlit
```

## 📈 Stats

- 308 matchs ingérés (Ligue 1 2024)
- Pipeline automatisée chaque nuit via Cloud Scheduler
- Modèle XGBoost · précision 47% (3 classes : victoire/nul/défaite)
- Tests dbt en CI sur GitHub Actions ✅

## 🛠 Stack

`Python` `SQL` `dbt` `BigQuery` `GCS` `Cloud Run` `Cloud Scheduler`  
`Vertex AI` `scikit-learn` `XGBoost` `Streamlit` `Looker Studio` `Docker` `GitHub Actions`
