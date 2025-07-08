#!/usr/bin/env python3
"""
Test script for flight price web scraping using Playwright
Tests the scraping logic without Dagster integration
"""

import asyncio
import datetime
import random
import pandas as pd
from playwright.async_api import async_playwright
from fake_useragent import UserAgent

# Test configuration - replace with real proxies if available
PROXIES = [
    {"server": None, "region": "Local"},
    # {"server": "http://user:pass@nz-proxy.com:8080", "region": "NZ"},
    # {"server": "http://user:pass@au-proxy.com:8080", "region": "AU"},
    # {"server": "http://user:pass@sg-proxy.com:8080", "region": "SG"},
]

# Test routes - AU/NZ destinations
ROUTES = [
    {"origin": "ZQN", "destination": "SYD"},  # Queenstown to Sydney
    {"origin": "CHC", "destination": "MEL"},  # Christchurch to Melbourne
    {"origin": "AKL", "destination": "BNE"},  # Auckland to Brisbane
    {"origin": "WLG", "destination": "SYD"},  # Wellington to Sydney
]

DATE_OFFSET_DAYS = 21  # Days in the future for the flight


async def scrape_price(page, origin, destination, departure_date, debug=False):
    """
    Scrape flight price from Google Flights

    Args:
        page: Playwright page object
        origin: Origin airport code
        destination: Destination airport code  
        departure_date: Departure date in YYYY-MM-DD format
        debug: Print debug information

    Returns:
        dict: Price data or None if failed
    """
    url = f"https://www.google.com/travel/flights?q=Flights%20from%20{origin}%20to%20{destination}%20on%20{departure_date}"

    if debug:
        print(f"Scraping URL: {url}")

    try:
        await page.goto(url, timeout=60000)

        # Wait for page to load
        await page.wait_for_timeout(8000)

        # Try multiple selectors for price elements
        price_selectors = [
            "span[aria-label*='$']",
            "div[data-ved] span:has-text('$')",
            "[role='button'] span:text-matches('\\$\\d+')",
            ".YMlIz span:has-text('$')",
            "span[jsaction] span:has-text('$')"
        ]

        price = None
        price_text = None

        for selector in price_selectors:
            try:
                price_element = page.locator(selector).first
                if await price_element.count() > 0:
                    price_text = await price_element.inner_text()
                    if '$' in price_text:
                        # Extract numeric price
                        price_clean = price_text.replace(
                            '$', '').replace(',', '').strip()
                        # Extract first number found
                        import re
                        numbers = re.findall(r'\d+', price_clean)
                        if numbers:
                            price = float(numbers[0])
                            if debug:
                                print(f"Found price: {price_text} -> {price}")
                            break
            except Exception as e:
                if debug:
                    print(f"Selector {selector} failed: {e}")
                continue

        if price is None and debug:
            print("No price found with any selector")
            # Save screenshot for debugging
            await page.screenshot(path=f"debug_{origin}_{destination}.png")

        return {
            "price": price,
            "price_text": price_text,
            "url": url
        }

    except Exception as e:
        if debug:
            print(f"Error loading page: {e}")
        return {
            "price": None,
            "price_text": None,
            "url": url,
            "error": str(e)
        }


async def test_single_scrape(debug=True):
    """Test scraping a single route"""
    print("Testing single route scraping...")

    route = ROUTES[0]  # Test first route
    departure_date = (datetime.date.today() +
                      datetime.timedelta(days=DATE_OFFSET_DAYS)).isoformat()

    ua = UserAgent()
    user_agent = ua.random

    playwright = await async_playwright().start()

    try:
        # Visible for debugging
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent=user_agent,
            locale="en-AU"
        )
        page = await context.new_page()

        print(f"Testing route: {route['origin']} → {route['destination']}")
        print(f"Departure date: {departure_date}")
        print(f"User agent: {user_agent[:50]}...")

        result = await scrape_price(
            page,
            route['origin'],
            route['destination'],
            departure_date,
            debug=debug
        )

        print(f"Result: {result}")

        # Keep browser open for manual inspection
        if debug:
            print("Browser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)

    finally:
        await browser.close()
        await playwright.stop()

    return result


async def scrape_all_routes(limit_routes=2, debug=False):
    """
    Scrape all configured routes with different proxy/locale combinations

    Args:
        limit_routes: Limit number of routes for testing
        debug: Enable debug output
    """
    print(f"Starting scrape of {min(limit_routes, len(ROUTES))} routes...")

    ua = UserAgent()
    results = []

    playwright = await async_playwright().start()

    test_routes = ROUTES[:limit_routes]

    for i, route in enumerate(test_routes):
        print(
            f"\n--- Route {i+1}/{len(test_routes)}: {route['origin']} → {route['destination']} ---")

        for j, proxy_config in enumerate(PROXIES):
            origin = route["origin"]
            destination = route["destination"]
            departure_date = (datetime.date.today(
            ) + datetime.timedelta(days=DATE_OFFSET_DAYS)).isoformat()

            proxy_server = proxy_config["server"]
            region = proxy_config["region"]
            user_agent = ua.random
            locale = random.choice(["en-US", "en-NZ", "en-AU"])

            print(f"  Proxy {j+1}: {region} | Locale: {locale}")

            # Browser configuration
            browser_args = {
                "headless": not debug,  # Visible if debug mode
            }

            if proxy_server:
                browser_args["proxy"] = {"server": proxy_server}

            browser = await playwright.chromium.launch(**browser_args)
            context = await browser.new_context(
                user_agent=user_agent,
                locale=locale
            )
            page = await context.new_page()

            try:
                scrape_result = await scrape_price(page, origin, destination, departure_date, debug=debug)

                result = {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "price": scrape_result.get("price"),
                    "price_text": scrape_result.get("price_text"),
                    "scrape_time": datetime.datetime.utcnow().isoformat(),
                    "proxy_used": proxy_server or "none",
                    "proxy_region": region,
                    "accept_language": locale,
                    "user_agent": user_agent[:50] + "..." if len(user_agent) > 50 else user_agent,
                    "url": scrape_result.get("url"),
                    "error": scrape_result.get("error")
                }

                results.append(result)

                if scrape_result.get("price"):
                    print(f"    ✓ Price found: {scrape_result['price_text']}")
                else:
                    print(f"    ✗ No price found")
                    if scrape_result.get("error"):
                        print(f"    Error: {scrape_result['error']}")

            except Exception as e:
                print(f"    ✗ Exception: {e}")
                results.append({
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "price": None,
                    "price_text": None,
                    "scrape_time": datetime.datetime.utcnow().isoformat(),
                    "proxy_used": proxy_server or "none",
                    "proxy_region": region,
                    "accept_language": locale,
                    "user_agent": user_agent[:50] + "..." if len(user_agent) > 50 else user_agent,
                    "error": str(e)
                })
            finally:
                await browser.close()

            # Add delay between requests
            await asyncio.sleep(random.uniform(2, 5))

    await playwright.stop()

    return pd.DataFrame(results)


async def main():
    """Main test function"""
    print("Flight Price Scraper Test")
    print("=" * 50)

    # Test 1: Single route with debugging
    print("\n1. Testing single route (visible browser)...")
    single_result = await test_single_scrape(debug=True)

    # Test 2: Multiple routes
    print("\n2. Testing multiple routes...")
    df_results = await scrape_all_routes(limit_routes=2, debug=False)

    print("\n" + "=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)

    if not df_results.empty:
        print(f"Total attempts: {len(df_results)}")
        print(
            f"Successful price extractions: {df_results['price'].notna().sum()}")
        print(f"Success rate: {df_results['price'].notna().mean():.1%}")

        print("\nSuccessful results:")
        successful = df_results[df_results['price'].notna()]
        for _, row in successful.iterrows():
            print(
                f"  {row['origin']} → {row['destination']}: {row['price_text']} ({row['proxy_region']})")

        print("\nFailed results:")
        failed = df_results[df_results['price'].isna()]
        for _, row in failed.iterrows():
            error_msg = row.get('error', 'Unknown error')
            print(
                f"  {row['origin']} → {row['destination']}: {error_msg[:100]}... ({row['proxy_region']})")

        # Save results to CSV
        output_file = f"flight_scrape_test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_results.to_csv(output_file, index=False)
        print(f"\nDetailed results saved to: {output_file}")
    else:
        print("No results collected")


if __name__ == "__main__":
    # Install required packages if not already installed
    try:
        import playwright
        import fake_useragent
        import pandas as pd
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Install with: pip install playwright fake-useragent pandas")
        print("Then run: playwright install chromium")
        exit(1)

    asyncio.run(main())
