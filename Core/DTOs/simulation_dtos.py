from dataclasses import dataclass
from typing import Dict
import numpy as np


@dataclass
class VariableResult:
    name: str
    values: np.ndarray
    unit: str
    description: str
    value_at_t: float


@dataclass
class SimulationResult:
    t: np.ndarray
    variables: Dict[str, VariableResult]
    success: bool
    message: str = ""
