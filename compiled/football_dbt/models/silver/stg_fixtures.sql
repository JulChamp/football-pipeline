WITH raw AS (
  SELECT * FROM `football-dashboard-490415`.`football_raw`.`fixtures`
)
SELECT
  fixture.id                          AS fixture_id,
  fixture.date                        AS match_date,
  fixture.status.short                AS status,
  league.round                        AS round,
  teams.home.id                       AS home_team_id,
  teams.home.name                     AS home_team_name,
  teams.away.id                       AS away_team_id,
  teams.away.name                     AS away_team_name,
  goals.home                          AS home_goals,
  goals.away                          AS away_goals,
  CASE
    WHEN goals.home > goals.away  THEN 'home_win'
    WHEN goals.home < goals.away  THEN 'away_win'
    WHEN goals.home = goals.away  THEN 'draw'
    ELSE 'pending'
  END                                 AS result
FROM raw
WHERE fixture.status.short = 'FT'  -- matchs terminés seulement