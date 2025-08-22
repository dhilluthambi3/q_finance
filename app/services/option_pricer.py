from math import log, sqrt, exp
from typing import Literal, Tuple, Dict
from scipy.stats import norm

import numpy as np
from typing import Literal, Tuple, Dict
from numpy.typing import NDArray

from qiskit.primitives import Sampler
from qiskit_finance.circuit.library import LogNormalDistribution
from qiskit_finance.applications.estimation import EuropeanCallPricing
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit_algorithms import EstimationProblem, IterativeAmplitudeEstimation


# --- Black–Scholes ---


def _d1(S0: float, K: float, r: float, sigma: float, T: float) -> float:
    return (log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))


def _d2(d1: float, sigma: float, T: float) -> float:
    return d1 - sigma * sqrt(T)


def black_scholes_price(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    opt_type: Literal["call", "put"],
) -> NDArray:
    d1 = _d1(S0, K, r, sigma, T)
    d2 = _d2(d1, sigma, T)
    if opt_type == "call":
        return S0 * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        return K * exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)


# TODO: complete the QAE call and put pricing methods
def quantum_price_stub(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    opt_type: Literal["call", "put"],
    num_qubits: int = 8,
) -> Tuple[float, Dict]:
    """
    Quantum Amplitude Estimation for European call/put pricing.
    Returns (price, meta) where meta holds algorithm diagnostics.
    """
    # Map problem to log-normal distribution
    mu = (r - 0.5 * sigma**2) * T + np.log(S0)
    sigma_t = sigma * np.sqrt(T)
    bounds = [0, 2 * S0]

    dist = LogNormalDistribution(num_qubits, mu=mu, sigma=sigma_t, bounds=bounds)

    sampler = Sampler()

    if opt_type == "call":
        raise NotImplementedError(
            "Quantum European Call Option pricing is not yet implemented."
        )
    else:
        raise NotImplementedError(
            "Only call options are supported in this quantum pricing method."
        )

    return 0.0, {"status": "not_implemented"}
