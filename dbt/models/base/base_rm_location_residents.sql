
-- ------------------------------------------------------------------------------
-- Model: base_rm_location_residents
-- Description: Base Table for ricky and morty residents within a location from API
-- ------------------------------------------------------------------------------
-- Change Log:
-- Date       | Author   | Description
-- -----------|----------|-------------------------------------------------------
-- 2025-05-16 | Cam      | Initial creation
-- YYYY-MM-DD | NAME     | [Add future changes here]
-- ------------------------------------------------------------------------------


SELECT
  _dlt_root_id AS location_dlt_id,
  CAST(regexp_replace(value, '.*/(\d+)$', '\1') AS INTEGER) AS character_id
FROM {{ source("rick_and_morty", "location__residents") }}