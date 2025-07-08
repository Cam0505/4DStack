# ------------------------------------------------------------------------------
# Model: Dim Date
# Description: Dimension Table with date information and public holidays for AU/NZ
# ------------------------------------------------------------------------------
# Change Log:
# Date       | Author   | Description
# -----------|----------|-------------------------------------------------------
# 2025-07-08 | Cam      | Initial creation
# -----------|----------|-------------------------------------------------------

import pandas as pd
from datetime import datetime, timedelta
import holidays
from typing import Any


def model(dbt: Any, session: Any):
    """
    Generate a comprehensive date dimension table with public holiday flags
    for flight price analysis across Australia and New Zealand.

    Includes:
    - Standard date attributes
    - Public holiday flags by AU state and NZ
    - Weekend/weekday indicators
    - Season indicators for travel analysis
    """

    dbt.config(
        materialized="table",
        unique_key="date_col"
    )

    # Set dynamic date range
    today = datetime.now().date()
    start_date = datetime(2000, 1, 1)
    end_date = datetime(today.year + 1, today.month,
                        today.day)  # One year from today

    # Get the date range for years to include in holiday calculations
    start_year = start_date.year
    end_year = end_date.year

    # Create date series
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    df = pd.DataFrame({'date_col': date_range})

    # Basic date attributes
    df['year'] = df['date_col'].dt.year
    df['month'] = df['date_col'].dt.month
    df['day'] = df['date_col'].dt.day
    df['month_name'] = df['date_col'].dt.strftime('%B')
    df['weekday_name'] = df['date_col'].dt.strftime('%A')
    df['day_of_week'] = df['date_col'].dt.dayofweek  # Monday=0, Sunday=6
    df['is_weekend'] = df['day_of_week'].isin([5, 6])  # Saturday=5, Sunday=6
    df['day_of_year'] = df['date_col'].dt.dayofyear
    df['week_of_year'] = df['date_col'].dt.isocalendar().week
    df['quarter'] = df['date_col'].dt.quarter

    # Season indicators (useful for travel patterns)
    df['season'] = df['month'].map({
        12: 'Summer', 1: 'Summer', 2: 'Summer',
        3: 'Autumn', 4: 'Autumn', 5: 'Autumn',
        6: 'Winter', 7: 'Winter', 8: 'Winter',
        9: 'Spring', 10: 'Spring', 11: 'Spring'
    })

    # Initialize holiday libraries for each region using dynamic year range
    # Australia by state
    au_holidays = {
        'NSW': holidays.country_holidays('AU', state='NSW', years=range(start_year, end_year + 1)),
        'VIC': holidays.country_holidays('AU', state='VIC', years=range(start_year, end_year + 1)),
        'QLD': holidays.country_holidays('AU', state='QLD', years=range(start_year, end_year + 1)),
        'WA': holidays.country_holidays('AU', state='WA', years=range(start_year, end_year + 1)),
        'SA': holidays.country_holidays('AU', state='SA', years=range(start_year, end_year + 1)),
        'TAS': holidays.country_holidays('AU', state='TAS', years=range(start_year, end_year + 1)),
        'ACT': holidays.country_holidays('AU', state='ACT', years=range(start_year, end_year + 1)),
        'NT': holidays.country_holidays('AU', state='NT', years=range(start_year, end_year + 1))
    }

    # New Zealand
    nz_holidays = holidays.country_holidays(
        'NZ', years=range(start_year, end_year + 1))

    # Add Australian state holiday flags
    for state, holiday_obj in au_holidays.items():
        df[f'is_holiday_au_{state.lower()}'] = df['date_col'].dt.date.apply(
            lambda x: x in holiday_obj
        )
        # Get holiday name for debugging/analysis
        df[f'holiday_name_au_{state.lower()}'] = df['date_col'].dt.date.apply(
            lambda x: holiday_obj.get(x, None)
        )

    # Add New Zealand holiday flags
    df['is_holiday_nz'] = df['date_col'].dt.date.apply(
        lambda x: x in nz_holidays)
    df['holiday_name_nz'] = df['date_col'].dt.date.apply(
        lambda x: nz_holidays.get(x, None)
    )

    # Add national Australian holidays (common across all states)
    au_national = holidays.country_holidays(
        'AU', years=range(start_year, end_year + 1))
    df['is_holiday_au_national'] = df['date_col'].dt.date.apply(
        lambda x: x in au_national
    )

    # Travel-specific indicators - School holidays by state/country
    # Using approximate school holiday periods based on typical patterns
    def get_school_holidays():
        """
        Returns approximate school holiday periods by state/territory.
        Each entry contains: name, start_date, end_date for better readability
        """
        return {
            # New South Wales
            'au_nsw': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-15", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "01-31"},
                {"name": "Autumn/Easter Holidays",
                    "start": "04-10", "end": "04-24"},
                {"name": "Winter Holidays", "start": "07-04", "end": "07-18"},
                {"name": "Spring Holidays", "start": "09-25", "end": "10-09"}
            ],

            # Victoria
            'au_vic': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-18", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "01-28"},
                {"name": "Autumn/Easter Holidays",
                    "start": "03-28", "end": "04-14"},
                {"name": "Winter Holidays", "start": "06-26", "end": "07-11"},
                {"name": "Spring Holidays", "start": "09-18", "end": "10-03"}
            ],

            # Queensland (earlier summer break due to heat)
            'au_qld': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-11", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "01-25"},
                {"name": "Autumn/Easter Holidays",
                    "start": "03-28", "end": "04-12"},
                {"name": "Winter Holidays", "start": "06-26", "end": "07-11"},
                {"name": "Spring Holidays", "start": "09-18", "end": "10-03"}
            ],

            # Western Australia (longer summer break)
            'au_wa': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-18", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "02-05"},
                {"name": "Autumn/Easter Holidays",
                    "start": "04-11", "end": "04-25"},
                {"name": "Winter Holidays", "start": "07-04", "end": "07-18"},
                {"name": "Spring Holidays", "start": "09-25", "end": "10-09"}
            ],

            # South Australia
            'au_sa': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-18", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "01-28"},
                {"name": "Autumn/Easter Holidays",
                    "start": "04-11", "end": "04-25"},
                {"name": "Winter Holidays", "start": "07-04", "end": "07-18"},
                {"name": "Spring Holidays", "start": "09-25", "end": "10-09"}
            ],

            # Tasmania (longer summer, earlier autumn break)
            'au_tas': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-18", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "02-08"},
                {"name": "Autumn/Easter Holidays",
                    "start": "04-06", "end": "04-20"},
                {"name": "Winter Holidays", "start": "07-04", "end": "07-18"},
                {"name": "Spring Holidays", "start": "09-25", "end": "10-09"}
            ],

            # Australian Capital Territory (follows NSW pattern)
            'au_act': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-15", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "01-31"},
                {"name": "Autumn/Easter Holidays",
                    "start": "04-10", "end": "04-24"},
                {"name": "Winter Holidays", "start": "07-04", "end": "07-18"},
                {"name": "Spring Holidays", "start": "09-25", "end": "10-09"}
            ],

            # Northern Territory (earlier due to tropical climate)
            'au_nt': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-11", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "01-28"},
                {"name": "Dry Season Break", "start": "04-04", "end": "04-18"},
                {"name": "Cooler Dry Season", "start": "06-26", "end": "07-11"},
                {"name": "Spring Holidays", "start": "09-25", "end": "10-09"}
            ],

            # New Zealand (4 terms system)
            'nz': [
                {"name": "Summer Holidays (Part 1)",
                 "start": "12-18", "end": "12-31"},
                {"name": "Summer Holidays (Part 2)",
                 "start": "01-01", "end": "02-05"},
                {"name": "Term 1/2 Break (Autumn)",
                 "start": "04-09", "end": "04-27"},
                {"name": "Term 2/3 Break (Winter)",
                 "start": "07-04", "end": "07-19"},
                {"name": "Term 3/4 Break (Spring)",
                 "start": "09-26", "end": "10-11"}
            ]
        }

    school_holidays = get_school_holidays()

    # Initialize all school holiday columns to False
    for region in school_holidays.keys():
        df[f'is_school_holiday_{region}'] = False

    # Use vectorized operations for much better performance
    for region, periods in school_holidays.items():
        holiday_column = f'is_school_holiday_{region}'

        for period in periods:
            # Create date ranges for each year in our dataset
            for year in range(df['year'].min(), df['year'].max() + 1):
                try:
                    # Parse MM-DD format and create full dates
                    start_month, start_day = map(
                        int, period["start"].split('-'))
                    end_month, end_day = map(int, period["end"].split('-'))

                    # Handle year boundary crossings (e.g., Dec 15 - Jan 31)
                    if start_month > end_month:
                        # Split into two periods: Dec start to Dec 31, and Jan 1 to end
                        start_date1 = pd.Timestamp(
                            year, start_month, start_day)
                        end_date1 = pd.Timestamp(year, 12, 31)
                        start_date2 = pd.Timestamp(year + 1, 1, 1)
                        end_date2 = pd.Timestamp(year + 1, end_month, end_day)

                        # Apply to both periods
                        mask1 = (df['date_col'] >= start_date1) & (
                            df['date_col'] <= end_date1)
                        mask2 = (df['date_col'] >= start_date2) & (
                            df['date_col'] <= end_date2)
                        df.loc[mask1 | mask2, holiday_column] = True
                    else:
                        # Normal case: within same year
                        start_date = pd.Timestamp(year, start_month, start_day)
                        end_date = pd.Timestamp(year, end_month, end_day)

                        mask = (df['date_col'] >= start_date) & (
                            df['date_col'] <= end_date)
                        df.loc[mask, holiday_column] = True

                except ValueError:
                    # Skip invalid dates (e.g., Feb 29 in non-leap years)
                    continue

    # General school holiday indicator (any region)
    school_holiday_cols = [
        col for col in df.columns if col.startswith('is_school_holiday_')]
    df['is_school_holiday_period'] = df[school_holiday_cols].any(axis=1)

    # Peak travel seasons (for pricing analysis)
    df['is_peak_travel'] = df.apply(lambda row:
                                    # Christmas/New Year
                                    (row['month'] == 12 and row['day'] >= 20) or
                                    (row['month'] == 1 and row['day'] <= 10) or
                                    # Easter period
                                    (row['month'] in [3, 4] and row['is_weekend']) or
                                    # Winter holidays
                                    (row['month'] == 7) or
                                    # Melbourne Cup weekend (first Tuesday in November)
                                    (row['month'] == 11 and 1 <= row['day'] <=
                                        7 and row['weekday_name'] in ['Monday', 'Tuesday']),
                                    axis=1
                                    )

    # Add days until next major holiday (useful for booking analysis)
    major_holidays = df[
        (df['is_holiday_au_national']) |
        (df['is_holiday_nz']) |
        ((df['month'] == 12) & (df['day'] == 25))  # Christmas
    ]['date_col'].tolist()

    def days_to_next_holiday(date):
        future_holidays = [h for h in major_holidays if h > date]
        if future_holidays:
            return (min(future_holidays) - date).days
        return None

    df['days_to_next_major_holiday'] = df['date_col'].apply(
        days_to_next_holiday)

    # Add is_long_weekend flag (useful for travel demand)
    df['is_long_weekend'] = df.apply(lambda row:
                                     # Check if it's a Friday/Monday and there's a holiday nearby
                                     (row['weekday_name'] in ['Friday', 'Monday'] and
                                      (row['is_holiday_au_national'] or row['is_holiday_nz'])) or
                                     # Or if it's part of a weekend with holidays
                                     (row['is_weekend'] and
                                         any([row[col] for col in df.columns if col.startswith('is_holiday_') and 'au_' in col])),
                                     axis=1
                                     )

    # Convert date_col to string for database compatibility
    df['date_col'] = df['date_col'].dt.date

    # Select final columns for the model
    final_columns = [
        'date_col', 'year', 'month', 'day', 'month_name', 'weekday_name',
        'day_of_week', 'is_weekend', 'day_of_year', 'week_of_year', 'quarter',
        'season', 'is_school_holiday_period', 'is_peak_travel',
        'days_to_next_major_holiday', 'is_long_weekend',
        'is_holiday_nz', 'holiday_name_nz', 'is_holiday_au_national'
    ]

    # Add all AU state holiday columns
    for state in ['nsw', 'vic', 'qld', 'wa', 'sa', 'tas', 'act', 'nt']:
        final_columns.extend(
            [f'is_holiday_au_{state}', f'holiday_name_au_{state}'])

    # Add all school holiday columns that were created
    school_holiday_cols = [col for col in df.columns if col.startswith(
        'is_school_holiday_') and col != 'is_school_holiday_period']
    final_columns.extend(school_holiday_cols)

    return df[final_columns]
