import os
import json
import requests
import yfinance as yf
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


def test_fred():
    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": "GDP",
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "limit": 1,
        "sort_order": "desc"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    observation = data["observations"][0]

    return {
        "source": "FRED",
        "status": "success",
        "series": "GDP",
        "date": observation["date"],
        "value": observation["value"]
    }


def test_yahoo_finance():
    ticker = yf.Ticker("AAPL")
    history = ticker.history(period="5d")

    if history.empty:
        raise RuntimeError("Yahoo Finance returned no data.")

    latest_row = history.iloc[-1]

    return {
        "source": "Yahoo Finance",
        "status": "success",
        "ticker": "AAPL",
        "latest_close": round(float(latest_row["Close"]), 2)
    }


def test_alpha_vantage():
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": "IBM",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    quote = data.get("Global Quote", {})

    if not quote:
        raise RuntimeError(
            "Alpha Vantage returned no quote data: "
            + json.dumps(data)
        )

    return {
        "source": "Alpha Vantage",
        "status": "success",
        "symbol": quote.get("01. symbol"),
        "price": quote.get("05. price"),
        "latest_trading_day": quote.get("07. latest trading day")
    }


def run_test(name, test_function):
    try:
        return test_function()
    except Exception as error:
        return {
            "source": name,
            "status": "failed",
            "error": str(error)
        }


def main():
    results = {
        "project": "Finance API Environment Test",
        "environment": "Python virtual environment (venv)",
        "results": {
            "fred": run_test("FRED", test_fred),
            "yahoo_finance": run_test(
                "Yahoo Finance",
                test_yahoo_finance
            ),
            "alpha_vantage": run_test(
                "Alpha Vantage",
                test_alpha_vantage
            )
        }
    }

    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()