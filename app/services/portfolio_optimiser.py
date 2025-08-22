import numpy as np
import pandas as pd 

from qiskit import QuantumCircuit   
from qiskit.primitives import Sampler
from qiskit_finance.circuit.library import LogNormalDistribution
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit_algorithms import EstimationProblem, IterativeAmplitudeEstimation


class PortfolioOptimizer:
    def __init__(self, num_qubits: int = 8):
        self.num_qubits = num_qubits
        self.sampler = Sampler()