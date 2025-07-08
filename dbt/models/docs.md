# A
# B
{% docs base_geo_description %}
    The `base_geo` model contains foundational geographic data that can be used to enrich other datasets with location context. It includes information like city name, country, coordinates, and region grouping.

    This model is useful for joining geographic metadata into analytical datasets.
{% enddocs %}

{% docs base_weather_description %}
    The `base_weather` model contains weather-related data for various locations. It includes metrics like temperature, humidity, precipitation, and wind speed, useful for analyzing and predicting weather patterns and environmental conditions.

    This model can be useful in a variety of analytical contexts, including climate modeling, forecasting, and geospatial analysis.
{% enddocs %}

# C
{% docs city %}
The name of the city. This field is typically used as a primary identifier for a location in the dataset.
{% enddocs %}

{% docs country %}
The country where the city is located. Useful for aggregating or filtering by national boundaries.
{% enddocs %}

{% docs continent %}
The continent where the city is located. This field helps in broader geographic aggregations and global segmentation.
{% enddocs %}
# D
{% docs dim_date_description %}
    Comprehensive date dimension table for flight price analysis across Australia and New Zealand. 
    
    Includes standard date attributes, public holiday flags by AU state and NZ, school holiday periods, 
    weekend indicators, and travel-specific flags for peak seasons and long weekends. 
    
    This table spans from 2000 to one year ahead and is designed to support pricing analysis by 
    identifying seasonal patterns, holiday impacts, and booking trends.
{% enddocs %}

{% docs date_col %}
    The primary date field in YYYY-MM-DD format. Used as the unique key for joining with other tables.
{% enddocs %}

{% docs day_of_week %}
    Numeric day of the week where Monday=0 through Sunday=6. Useful for identifying weekday patterns in travel demand.
{% enddocs %}

{% docs days_to_next_major_holiday %}
    Number of days until the next major holiday (Australian national holidays, NZ holidays, or Christmas). 
    Useful for analyzing booking lead times and pricing patterns before holidays.
{% enddocs %}
# E
# F
# G
# H
{% docs humidity %}
    The relative humidity of the air at a given location, measured as a percentage (%). High humidity levels can affect comfort and play a role in weather events like precipitation.
{% enddocs %}

{% docs holiday_name_au_state %}
    The name of the Australian state/territory public holiday, if the date is a holiday. NULL if not a holiday.
{% enddocs %}

{% docs holiday_name_nz %}
    The name of the New Zealand public holiday, if the date is a holiday. NULL if not a holiday.
{% enddocs %}
# I
{% docs is_holiday_au_national %}
    Boolean flag indicating if the date is a national Australian public holiday (observed across all states/territories).
{% enddocs %}

{% docs is_holiday_au_state %}
    Boolean flag indicating if the date is a public holiday in the specific Australian state or territory.
{% enddocs %}

{% docs is_holiday_nz %}
    Boolean flag indicating if the date is a public holiday in New Zealand.
{% enddocs %}

{% docs is_long_weekend %}
    Boolean flag identifying long weekends (3+ day weekends that include public holidays). 
    Important for travel demand analysis as these periods typically see increased domestic travel.
{% enddocs %}

{% docs is_peak_travel %}
    Boolean flag identifying peak travel periods including Christmas/New Year, Easter weekends, 
    winter holidays, and Melbourne Cup weekend. These periods typically have higher flight prices.
{% enddocs %}

{% docs is_school_holiday_au_state %}
    Boolean flag indicating if the date falls within school holiday periods for the specific Australian state or territory. 
    Based on typical school calendar patterns and includes summer, autumn, winter, and spring breaks.
{% enddocs %}

{% docs is_school_holiday_nz %}
    Boolean flag indicating if the date falls within New Zealand school holiday periods. 
    Based on the 4-term system with breaks between terms and summer holidays.
{% enddocs %}

{% docs is_school_holiday_period %}
    Boolean flag indicating if the date is a school holiday in ANY region (Australia or New Zealand). 
    Useful for identifying periods of increased family travel demand.
{% enddocs %}

{% docs is_weekend %}
    Boolean flag identifying Saturday and Sunday. Weekend travel patterns often differ significantly from weekday patterns.
{% enddocs %}
# J
# K
# L
{% docs latitude %}
The latitude coordinate of the city in decimal degrees. Positive values indicate locations north of the equator.
{% enddocs %}

{% docs longitude %}
    The longitude coordinate of the city in decimal degrees. Positive values indicate locations east of the Prime Meridian.
{% enddocs %}
# M
{% docs month_name %}
    Full month name (e.g., "January", "February"). Useful for reporting and human-readable date displays.
{% enddocs %}
# N
# O
{% docs ozone %}
    The concentration of ozone in the atmosphere, typically measured in Dobson Units (DU). Ozone plays a key role in absorbing UV radiation, and its concentration can influence the level of UV exposure.
{% enddocs %}
# P
{% docs precipitation_sum %}
    The total amount of precipitation (rain, snow, etc.) that has fallen over a given period, measured in millimeters (mm) or inches (in). This value helps to track overall rainfall or snowfall accumulation, which is important for understanding seasonal or long-term trends in precipitation.
{% enddocs %}

# Q
# R
{% docs region %}
    A higher-level geographic grouping, such as a continent or internal administrative region. Optional but useful for rollups and segmentation.
{% enddocs %}
# S
{% docs season %}
    Seasonal classification based on Australian/Southern Hemisphere seasons: Summer (Dec-Feb), 
    Autumn (Mar-May), Winter (Jun-Aug), Spring (Sep-Nov). Important for identifying seasonal travel patterns.
{% enddocs %}

{% docs sunshine_duration %}
    The total duration of sunshine at a given location over a specific period, typically measured in hours. This metric is important for assessing how much sunlight an area receives, which can affect agriculture, energy production, and climate conditions.
{% enddocs %}
# T
{% docs temperature_mean %}
    The mean temperature at a given location, averaged over a specific period (e.g., daily, weekly). This value helps in assessing general weather conditions and trends over time, providing a more stable representation of temperature compared to single-point measurements.
{% enddocs %}

{% docs temperature_max %}
    The maximum temperature at a given location, typically measured during a specific time frame (e.g., daily or hourly). This value represents the highest temperature recorded and is often used to analyze extreme weather conditions or heat events.
{% enddocs %}
# U
# V
# W
{% docs weekday_name %}
    Full weekday name (e.g., "Monday", "Tuesday"). Useful for reporting and analyzing day-of-week travel patterns.
{% enddocs %}

{% docs wind_speed %}
    The speed of wind at a given location, typically measured in kilometers per hour (km/h) or miles per hour (mph). This value is crucial for forecasting storm conditions and understanding general weather dynamics.
{% enddocs %}

{% docs windgusts_max %}
The maximum wind gust recorded at a given location during a specific time period. Wind gusts are short bursts of high-speed wind and can be important indicators of severe weather events such as storms or tornadoes.
{% enddocs %}
# X
# Y
# Z