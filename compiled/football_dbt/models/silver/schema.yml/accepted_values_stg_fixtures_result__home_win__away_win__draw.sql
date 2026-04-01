
    
    

with all_values as (

    select
        result as value_field,
        count(*) as n_records

    from `football-dashboard-490415`.`football_curated`.`stg_fixtures`
    group by result

)

select *
from all_values
where value_field not in (
    'home_win','away_win','draw'
)


