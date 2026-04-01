
    
    

with dbt_test__target as (

  select fixture_id as unique_field
  from `football-dashboard-490415`.`football_curated`.`stg_fixtures`
  where fixture_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


