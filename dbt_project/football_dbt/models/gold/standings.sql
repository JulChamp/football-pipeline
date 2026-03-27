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
  form,
  CASE team_name
    WHEN 'Paris Saint Germain' THEN 'PSG'
    WHEN 'Lyon'                THEN 'OL'
    WHEN 'Marseille'           THEN 'OM'
    WHEN 'Monaco'              THEN 'ASM'
    WHEN 'Lens'                THEN 'Lens'
    WHEN 'Lille'               THEN 'LOSC'
    WHEN 'Nice'                THEN 'Nice'
    WHEN 'Stade Brestois 29'   THEN 'Brest'
    WHEN 'Strasbourg'          THEN 'Strasbourg'
    WHEN 'Montpellier'         THEN 'MHSC'
    WHEN 'Toulouse'            THEN 'TFC'
    WHEN 'Saint Etienne'       THEN 'ASSE'
  ELSE team_name
END AS team_short
FROM {{ source('football_raw', 'standings') }}
ORDER BY rank ASC