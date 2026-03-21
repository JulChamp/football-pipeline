from google.cloud import aiplatform, storage
import os
from dotenv import load_dotenv
load_dotenv()

PROJECT = os.getenv("GCP_PROJECT_ID")
BUCKET  = os.getenv("GCS_BUCKET")

# 1. Upload le modèle dans GCS
client = storage.Client()
bucket = client.bucket(BUCKET)
for f in ["model.joblib", "label_encoder.joblib"]:
    bucket.blob(f"models/{f}").upload_from_filename(f"ml/{f}")

# 2. Enregistrer dans Vertex AI Model Registry
aiplatform.init(project=PROJECT, location="europe-west1")
model = aiplatform.Model.upload(
    display_name="football-result-predictor",
    artifact_uri=f"gs://{BUCKET}/models/",
    serving_container_image_uri=
    "europe-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-7:latest"
)

# 3. Déployer comme endpoint
endpoint = model.deploy(
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=1
)
print(f"✅ Endpoint: {endpoint.resource_name}")