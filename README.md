# Biorreactor Simulator

Simulador de un biorreactor fed-batch con Streamlit. Toda la configuracion
(iniciales, ecuaciones, parametros de tiempo) se maneja desde `config.json`,
sin tocar codigo.

## Que usa

- **Streamlit** para la interfaz
- **scipy** (`solve_ivp` con RK45) para integrar las EDOs
- **plotly** para las graficas
- La arquitectura esta partida en capas: `Api/`, `Application/`, `Core/`, `Infrastructure/`
  con CQRS bien separado (queries y handlers).

## Estructura

```
bioreactor/
├── config.json
├── Core/DTOs/                  → simulation_dtos.py
├── Infrastructure/Services/    → config_service.py, equation_solver.py
├── Application/Features/
│   └── Equations/SolveEquations/ → query.py, query_handler.py
└── Api/Controllers/
    ├── atoms/                  → metric_card, section_title, status_badge
    ├── molecules/              → time_control
    └── simulations/
        ├── simulation_controller.py
        └── molecules/          → sidebar, results_metrics, plots, data_table
```

## Como correrlo

```bash
pip install -r requirements.txt
streamlit run Api/Controllers/simulations/simulation_controller.py
```

## Modelo

Las ecuaciones estan en `config.json` y se resuelven numericamente.

| Variable | Expresion |
|----------|-----------|
| V(t)     | V₀ + F·t |
| dX/dt    | µ·X − (F/V)·X |
| dS/dt    | (F/V)·(Sₓ − S) − Y_PS·µ·X |
| dP/dt    | Y_PX·µ·X − (F/V)·P |

con µ = µ_max · S / (K_s + S) (Monod).

## Notas

- No hardcodees nada en la UI, todo sale de `config.json`.
- Los numbers inputs son number_input, no slider.
- Los colores, unidades, labels de cada variable se definen ahi tambien.
