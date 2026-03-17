from google.cloud import bigquery, storage
import json, os
from dotenv import load_dotenv
load_dotenv()

client  = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
PROJECT = os.getenv("GCP_PROJECT_ID")
BUCKET  = os.getenv("GCS_BUCKET")

def flatten_standings(data):
    """Aplatit la structure imbriquée du standings"""
    records = []
    for item in data:
        league = item.get("league", {})
        standings = league.get("standings", [[]])[0]
        for team in standings:
            records.append({
                "league_id":   league.get("id"),
                "league_name": league.get("name"),
                "season":      league.get("season"),
                "rank":        team.get("rank"),
                "team_id":     team.get("team", {}).get("id"),
                "team_name":   team.get("team", {}).get("name"),
                "points":      team.get("points"),
                "goals_diff":  team.get("goalsDiff"),
                "form":        team.get("form"),
                "played":      team.get("all", {}).get("played"),
                "wins":        team.get("all", {}).get("win"),
                "draws":       team.get("all", {}).get("draw"),
                "losses":      team.get("all", {}).get("lose"),
                "goals_for":   team.get("all", {}).get("goals", {}).get("for"),
                "goals_against": team.get("all", {}).get("goals", {}).get("against"),
            })
    return records

def load_json_to_bq(gcs_pattern, table_id, flatten_fn=None):
    gcs_client = storage.Client()
    blobs = list(gcs_client.list_blobs(BUCKET, prefix=gcs_pattern))

    if not blobs:
        print(f"⚠️ Aucun fichier trouvé pour {gcs_pattern}")
        return

    all_records = []
    for blob in blobs:
        data = json.loads(blob.download_as_text())
        if flatten_fn:
            all_records.extend(flatten_fn(data))
        elif isinstance(data, list):
            all_records.extend(data)
        else:
            all_records.append(data)

    ndjson = "\n".join(json.dumps(r, ensure_ascii=False) for r in all_records)
    tmp_blob = storage.Client().bucket(BUCKET).blob(
        f"tmp/{gcs_pattern.replace('/', '_')}.ndjson"
    )
    tmp_blob.upload_from_string(ndjson, content_type="application/json")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    job = client.load_table_from_uri(
        f"gs://{BUCKET}/tmp/{gcs_pattern.replace('/', '_')}.ndjson",
        table_id, job_config=job_config
    )
    job.result()
    print(f"✅ {table_id} chargé ({len(all_records)} records)")

# Fixtures — structure plate, pas besoin de flatten
load_json_to_bq("bronze/fixtures", f"{PROJECT}.football_raw.fixtures")

# Standings — structure imbriquée, on aplatit
load_json_to_bq("bronze/standings", f"{PROJECT}.football_raw.standings",
                flatten_fn=flatten_standings)