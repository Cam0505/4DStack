SELECT "airline id"::int as airline_id, name as airline_name, 
NULLIF(TRIM(REPLACE(icao, '\n', '')), '') as icao,
NULLIF(TRIM(REPLACE(callsign, '\n', '')), '') as callsign,
NULLIF(TRIM(REPLACE(country, '\n', '')), '') as country,
active
FROM {{ source("openflights", "airlines_asset") }}
where "airline id" != '-1'