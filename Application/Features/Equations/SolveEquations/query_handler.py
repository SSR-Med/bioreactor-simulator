from Core.DTOs import SimulationResult
from Infrastructure.Services import EquationSolver
from .query import SolveEquationsQuery


class SolveEquationsQueryHandler:

    def handle(self, query: SolveEquationsQuery) -> SimulationResult:
        solver = EquationSolver(query.config)
        return solver.solve(query.t_end)
