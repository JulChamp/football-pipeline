from google.cloud import bigquery
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

client  = bigquery.Client()
PROJECT = os.getenv("GCP_PROJECT_ID")

QUERY = f"""
SELECT
  f.fixture_id,
  h.wins_last5        AS home_wins_l5,
  h.draws_last5       AS home_draws_l5,
  h.losses_last5      AS home_losses_l5,
  a.wins_last5        AS away_wins_l5,
  a.draws_last5       AS away_draws_l5,
  a.losses_last5      AS away_losses_l5,
  f.result            AS target
FROM `{PROJECT}.football_curated.stg_fixtures` f
JOIN `{PROJECT}.football_curated.team_form` h ON h.team_id = f.home_team_id
JOIN `{PROJECT}.football_curated.team_form` a ON a.team_id = f.away_team_id
WHERE f.result != 'pending'
"""

df = client.query(QUERY).to_dataframe()
df.to_csv("ml/dataset.csv", index=False)
print(f"Dataset: {len(df)} matchs")
print(df["target"].value_counts())