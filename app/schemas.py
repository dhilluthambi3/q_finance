from pydantic import BaseModel, Field
from typing import Literal, Optional


class SpotQuery(BaseModel):
    ticker: str = Field(..., pattern=r"^[A-Za-z.\-]{1,12}$")


class OptionPriceRequest(BaseModel):
    ticker: str = Field(..., pattern=r"^[A-Za-z.\-]{1,12}$")
    K: float = Field(..., gt=0, description="Strike price")
    r: float = Field(..., ge=0, le=1, description="Risk-free rate (annualized)")
    sigma: float = Field(..., gt=0, le=5, description="Volatility (stdev, annualized)")
    T: float = Field(..., gt=0, le=10, description="Time to expiry in years")
    type: Literal["call", "put"]
    method: Literal["black_scholes", "quantum"] = "black_scholes"
    S0: Optional[float] = Field(None, gt=0, description="Override spot price")


class OptionPriceResponse(BaseModel):
    ticker: str
    method: str
    type: str
    S0: float
    K: float
    r: float
    sigma: float
    T: float
    price: float
    meta: dict
