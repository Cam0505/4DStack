SELECT "airport id", name, city, country, 
case when iata = '\N' then NULL else iata end as iata, 
case when icao = '\N' then NULL else icao end as icao, 
latitude::DOUBLE as latitude, 
longitude::DOUBLE as longitude, altitude::INT as altitude, 
case when timezone = '\N' then NULL else timezone end as timezone,
case when dst = '\N' then NULL else dst end as dst, 
<<<<<<< HEAD
case when "Tz database time zone" = '\N' then NULL else "Tz database time zone" end as database_time_zone
FROM {{ source("openflights", "airports_asset") }}
=======
case when tz_database_time_zone = '\N' then NULL else tz_database_time_zone end as database_time_zone
<<<<<<< HEAD
FROM {{ source("openflights", "airports") }}
>>>>>>> e329922 (Fixing model)
=======
FROM {{ source("openflights", "airports_asset") }}
>>>>>>> 1fa9733 (Switching another asset over)
