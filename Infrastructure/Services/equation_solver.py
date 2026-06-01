import numpy as np
from scipy.integrate import solve_ivp

from Core.DTOs import SimulationResult, VariableResult


class EquationSolver:

    def __init__(self, config: dict):
        self._config = config

    def solve(self, t_end: float) -> SimulationResult:
        cfg = self._config
        equations = cfg["equations"]
        ic = cfg["initial_conditions"]
        time_cfg = cfg["time"]
        variables_cfg = cfg["variables"]

        state_vars = self._identify_state_vars(equations)
        y0 = [ic[v]["value"] for v in state_vars]

        t_span = (time_cfg["min"], t_end)
        t_eval = np.arange(time_cfg["min"], t_end + time_cfg["step"], time_cfg["step"])

        try:
            sol = solve_ivp(
                fun=lambda t, y: self._odes(t, y, equations, state_vars),
                t_span=t_span,
                y0=y0,
                t_eval=t_eval,
                method="RK45",
                rtol=1e-6,
                atol=1e-9,
            )

            if not sol.success:
                return SimulationResult(
                    t=np.array([]),
                    variables={},
                    success=False,
                    message=f"El integrador falló: {sol.message}",
                )

            t_out = sol.t
            state_results = {name: sol.y[i] for i, name in enumerate(state_vars)}
            all_results = self._compute_all_variables(
                t_out, state_results, equations, state_vars
            )

            variables = {}
            for var_name in variables_cfg:
                if var_name in all_results:
                    v = all_results[var_name]
                    variables[var_name] = VariableResult(
                        name=var_name,
                        values=v,
                        unit=variables_cfg[var_name]["unit"],
                        description=variables_cfg[var_name]["description"],
                        value_at_t=float(v[-1]),
                    )

            return SimulationResult(
                t=t_out,
                variables=variables,
                success=True,
                message="Simulación completada exitosamente.",
            )

        except Exception as exc:
            return SimulationResult(
                t=np.array([]),
                variables={},
                success=False,
                message=str(exc),
            )

    @staticmethod
    def _identify_state_vars(equations: dict) -> list:
        return [name[1:-3] for name in equations
                if name.startswith("d") and name.endswith("_dt")]

    @staticmethod
    def _odes(t, y, equations, state_vars):
        namespace = {"t": t, "np": np}
        for i, name in enumerate(state_vars):
            namespace[name] = max(y[i], 0.0)

        for name, expr in equations.items():
            if not (name.startswith("d") and name.endswith("_dt")):
                namespace[name] = eval(expr, {"__builtins__": {}}, namespace)

        return [
            eval(equations[f"d{name}_dt"], {"__builtins__": {}}, namespace)
            for name in state_vars
        ]

    @staticmethod
    def _compute_all_variables(t, state_results, equations, state_vars):
        namespace = {"t": t, "np": np}
        for name in state_vars:
            namespace[name] = state_results[name]

        result = dict(state_results)
        for name, expr in equations.items():
            if name.startswith("d") and name.endswith("_dt"):
                continue
            result[name] = eval(expr, {"__builtins__": {}}, namespace)

        return result
