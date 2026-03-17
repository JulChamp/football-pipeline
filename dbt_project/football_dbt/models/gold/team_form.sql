-- Forme sur les 5 derniers matchs par équipe
WITH home_matches AS (
  SELECT home_team_id AS team_id, match_date, result AS team_result
  FROM {{ ref('stg_fixtures') }}
  UNION ALL
  SELECT away_team_id, match_date,
    CASE result
      WHEN 'away_win' THEN 'home_win'
      WHEN 'home_win' THEN 'away_win'
      ELSE result
    END
  FROM {{ ref('stg_fixtures') }}
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY team_id ORDER BY match_date DESC) AS rn
  FROM home_matches
)
SELECT
  team_id,
  COUNTIF(team_result = 'home_win' AND rn <= 5) AS wins_last5,
  COUNTIF(team_result = 'draw' AND rn <= 5)     AS draws_last5,
  COUNTIF(team_result = 'away_win' AND rn <= 5) AS losses_last5
FROM ranked
GROUP BY team_id