from typing import Optional
import yfinance as yf


def get_spot_price(ticker: str) -> Optional[float]:
    """Fetch the latest close as spot proxy. In production use a real-time feed."""
    try:
        data = yf.Ticker(ticker).history(period="1d")
        if not data.empty:
            return float(data["Close"].iloc[-1])
    except Exception:
        return None
    return None