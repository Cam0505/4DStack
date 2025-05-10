-- ------------------------------------------------------------------------------
-- Model: Dim Country
<<<<<<< HEAD
-- Description: Dimension Table, country information (Test)
=======
-- Description: Dimension Table, country information
>>>>>>> aae1518 (Done! Slim CI!)
-- ------------------------------------------------------------------------------
-- Change Log:
-- Date       | Author   | Description
-- -----------|----------|-------------------------------------------------------
-- 2025-05-17 | Cam      | Initial creation
-- YYYY-MM-DD | NAME     | [Add future changes here]
-- ------------------------------------------------------------------------------
select country_code, country, Country_SK
from {{ref('staging_geo')}}
group by country_code, country, Country_SK