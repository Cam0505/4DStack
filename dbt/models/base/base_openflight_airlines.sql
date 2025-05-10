SELECT airline_id::int as airline_id, name as airline_name, 
NULLIF(TRIM(REPLACE(icao, '\n', '')), '') as icao,
NULLIF(TRIM(REPLACE(callsign, '\n', '')), '') as callsign,
NULLIF(TRIM(REPLACE(country, '\n', '')), '') as country,
active
<<<<<<< HEAD
<<<<<<< HEAD
FROM {{ source("openflights", "airlines_asset") }}
where "airline id" != '-1'
=======
SELECT airline_id, name, icao, callsign, country, active
FROM {{ source("openflights", "airlines") }}
>>>>>>> fe81082 (New Data Source and improved DLT code for existing pipelines)
=======
FROM {{ source("openflights", "airlines") }}
where airline_id != '-1'
>>>>>>> e329922 (Fixing model)
=======
FROM {{ source("openflights", "airlines_asset") }}
where airline_id != '-1'