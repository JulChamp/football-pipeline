import os, json, requests
from datetime import datetime
from google.cloud import storage
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

API_KEY = os.getenv("API_SPORTS_KEY")
BUCKET  = os.getenv("GCS_BUCKET")
SEASON  = os.getenv("SEASON", "2025")
LEAGUE_ID = 61  # Ligue 1

HEADERS = {
    "x-apisports-key": API_KEY
}
BASE_URL = "https://v3.football.api-sports.io"

def fetch_endpoint(endpoint, params):
    r = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()["response"]

def upload_to_gcs(data, blob_name):
    client = storage.Client()
    bucket = client.bucket(BUCKET)
    blob   = bucket.blob(blob_name)
    blob.upload_from_string(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type="application/json"
    )
    print(f"✅ Uploaded {blob_name} ({len(data)} records)")

def run_ingestion():
    today = datetime.today().strftime("%Y-%m-%d")

    # 1. Matchs de la saison
    fixtures = fetch_endpoint("fixtures", {
        "league": LEAGUE_ID, "season": SEASON
    })
    upload_to_gcs(fixtures, f"bronze/fixtures/{today}.json")

    # 2. Classement actuel
    standings = fetch_endpoint("standings", {
        "league": LEAGUE_ID, "season": SEASON
    })
    upload_to_gcs(standings, f"bronze/standings/{today}.json")

    # 3. Stats des équipes
    team_ids = [85,80,81,91,79,84]  # PSG, Lyon, OM, Monaco…
    all_stats = []
    for tid in team_ids:
        stats = fetch_endpoint("teams/statistics", {
            "league": LEAGUE_ID, "season": SEASON, "team": tid
        })
        all_stats.append(stats)
    upload_to_gcs(all_stats, f"bronze/team_stats/{today}.json")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def trigger():
    try:
        run_ingestion()
        return jsonify({"status": "ok", "message": "Ingestion terminée"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)