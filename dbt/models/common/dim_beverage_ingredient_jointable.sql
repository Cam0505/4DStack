-- ------------------------------------------------------------------------------
-- Model: Dim_beverage_ingredient_jointable
-- Description: Join table for beverage ingredients
-- ------------------------------------------------------------------------------
-- Change Log:
-- Date       | Author   | Description
-- -----------|----------|-------------------------------------------------------
-- 2025-05-17 | Cam      | Initial creation
-- YYYY-MM-DD | NAME     | [Add future changes here]
-- ------------------------------------------------------------------------------
<<<<<<< HEAD
SELECT distinct idDrink as Beverage_ID
=======
SELECT distinct id_drink as Beverage_ID
>>>>>>> aae1518 (Done! Slim CI!)
    from {{ source("beverages", "ingredients_table") }} as it
    where idDrink is not null