SELECT
  team_name,
  rank,
  points,
  played,
  wins,
  draws,
  losses,
  goals_for,
  goals_against,
  goals_diff,
  form
FROM {{ source('football_raw', 'standings') }}
ORDER BY rank ASC