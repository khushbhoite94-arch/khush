"""
AEGIS AI
Main Entry Point
"""

import time

from app.automation.browser import BrowserManager
from app.automation.chart_reader import ChartReader


def main():

    print("=" * 60)
    print("               AEGIS AI")
    print("=" * 60)

    browser = BrowserManager()

    try:

        # ----------------------------------------
        # Connect Browser
        # ----------------------------------------

        browser.connect()

        print()
        print("[AEGIS] Browser Connected")

        # ----------------------------------------
        # Chart Reader
        # ----------------------------------------

        reader = ChartReader(browser.page)

        reader.wait_ready()

        print("[AEGIS] Chart Reader Ready")
        print()

        # ----------------------------------------
        # Main Loop
        # ----------------------------------------

        while True:

            candle = reader.current_candle()

            if candle:

                print("=" * 50)

                print("Symbol     :", candle["symbol"])

                print("Timeframe  :", candle["timeframe"])

                print("Open       :", candle["open"])

                print("High       :", candle["high"])

                print("Low        :", candle["low"])

                print("Close      :", candle["close"])

                print("Timestamp  :", candle["timestamp"])

            else:

                print("[AEGIS] Waiting for chart data...")

            time.sleep(1)

    except KeyboardInterrupt:

        print()

        print("[AEGIS] Shutdown Requested")

    except Exception as e:

        print()

        print("[AEGIS] ERROR")

        print(e)

    finally:

        browser.stop()

        print()

        print("[AEGIS] System Stopped")


if __name__ == "__main__":

    main()