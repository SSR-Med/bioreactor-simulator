# 🧫 Biorreactor Fed-Batch Simulator

Simulador numérico de un biorreactor fed-batch usando arquitectura **hexagonal** (ports & adapters) con patrón **CQRS**.

## Arquitectura

```
bioreactor/
├── config.json                          ← Condiciones iniciales + ecuaciones
│
├── Core/
│   └── DTOs/
│       └── simulation_dtos.py           ← Objetos de transferencia de datos
│
├── Infrastructure/
│   └── Services/
│       └── config_service.py            ← Lee secretos/config del JSON
│
├── Application/
│   └── Features/
│       └── Equations/
│           └── SolveEquations/
│               ├── query.py             ← CQRS Query (inmutable)
│               └── query_handler.py     ← CQRS Handler (SciPy RK45)
│
└── Api/
    └── Controllers/
        └── simulation_controller.py     ← Streamlit UI
```

## Instalación y ejecución

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Lanzar la aplicación
streamlit run Api/Controllers/simulation_controller.py
```

## Sistema de ecuaciones

| Variable | Ecuación |
|----------|----------|
| V(t)     | V₀ + F·t |
| dX/dt    | µ·X − (F/V)·X |
| dS/dt    | (F/V)·(Sₓ − S) − Y_PS·µ·X |
| dP/dt    | Y_PX·µ·X − (F/V)·P |

donde **µ = µ_max · S / (K_s + S)** (cinética de Monod)

## Parametrización

Todos los parámetros, condiciones iniciales y límites de tiempo se controlan
desde `config.json` — **sin tocar el código**.
