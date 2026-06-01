from dataclasses import dataclass


@dataclass(frozen=True)
class SolveEquationsQuery:
    t_end: float
    config: dict
