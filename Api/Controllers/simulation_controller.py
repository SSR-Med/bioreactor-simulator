import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from Infrastructure.Services import ConfigService
from Application.Features.Equations.SolveEquations import (
    SolveEquationsQuery,
    SolveEquationsQueryHandler,
)

st.set_page_config(
    page_title="Biorreactor Simulator",
    page_icon="🧫",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

      html, body, [class*="css"] {
          font-family: 'DM Sans', sans-serif;
      }

      [data-testid="stSidebar"] {
          background: #0d1117;
          border-right: 1px solid #21262d;
      }
      [data-testid="stSidebar"] * { color: #c9d1d9 !important; }

      .main .block-container {
          background: #0d1117;
          padding-top: 2rem;
      }

      .metric-card {
          background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
          border: 1px solid #30363d;
          border-radius: 12px;
          padding: 1.2rem 1.5rem;
          margin-bottom: 0.5rem;
          transition: border-color 0.2s;
      }
      .metric-card:hover { border-color: #58a6ff; }
      .metric-label {
          font-family: 'Space Mono', monospace;
          font-size: 0.72rem;
          color: #8b949e;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          margin-bottom: 0.3rem;
      }
      .metric-value {
          font-family: 'Space Mono', monospace;
          font-size: 1.6rem;
          font-weight: 700;
          color: #58a6ff;
      }
      .metric-unit {
          font-size: 0.8rem;
          color: #8b949e;
          margin-left: 0.3rem;
      }
      .metric-desc {
          font-size: 0.75rem;
          color: #6e7681;
          margin-top: 0.25rem;
      }

      .hero-title {
          font-family: 'Space Mono', monospace;
          font-size: 2rem;
          font-weight: 700;
          color: #e6edf3;
          letter-spacing: -0.02em;
      }
      .hero-sub {
          font-size: 0.9rem;
          color: #8b949e;
          margin-top: -0.3rem;
          margin-bottom: 1.5rem;
      }
      .section-title {
          font-family: 'Space Mono', monospace;
          font-size: 0.8rem;
          color: #58a6ff;
          text-transform: uppercase;
          letter-spacing: 0.12em;
          margin-bottom: 0.8rem;
          border-bottom: 1px solid #21262d;
          padding-bottom: 0.4rem;
      }

      .status-ok {
          display: inline-block;
          background: #1a3a2a;
          color: #3fb950;
          border: 1px solid #238636;
          border-radius: 20px;
          padding: 0.15rem 0.7rem;
          font-size: 0.72rem;
          font-family: 'Space Mono', monospace;
      }

      #MainMenu, footer, header { visibility: hidden; }
      .stDeployButton { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_config():
    svc = ConfigService()
    return svc.load()


cfg = load_config()
time_cfg = cfg["time"]
variables_cfg = cfg["variables"]
equations = cfg["equations"]
ic = cfg["initial_conditions"]

with st.sidebar:
    st.markdown('<p class="section-title">⚙ Parámetros de simulación</p>', unsafe_allow_html=True)

    t_slider = st.slider(
        "Tiempo final (horas)",
        min_value=float(time_cfg["min"]),
        max_value=float(time_cfg["max"]),
        value=float(time_cfg["default"]),
        step=float(time_cfg["step"]),
        key="t_slider",
    )
    t_number = st.number_input(
        "Valor exacto",
        min_value=float(time_cfg["min"]),
        max_value=float(time_cfg["max"]),
        value=float(t_slider),
        step=float(time_cfg["step"]),
        key="t_number",
        format="%.2f",
    )

    t_end = t_number if t_number != t_slider else t_slider

    st.markdown("---")
    st.markdown('<p class="section-title">📋 Condiciones iniciales</p>', unsafe_allow_html=True)
    for var_name in variables_cfg:
        info = variables_cfg[var_name]
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">{var_name}(0)</div>'
            f'<div class="metric-value">{ic[var_name]}<span class="metric-unit">{info["unit"]}</span></div>'
            f'<div class="metric-desc">{info["description"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown('<p class="section-title">🔬 Ecuaciones del modelo</p>', unsafe_allow_html=True)
    for name, expr in equations.items():
        with st.expander(f"{name}"):
            st.code(expr, language="python")


@st.cache_data(show_spinner=False)
def run_simulation(t_end: float):
    query = SolveEquationsQuery(t_end=t_end, config=cfg)
    handler = SolveEquationsQueryHandler()
    return handler.handle(query)


with st.spinner("Integrando sistema de EDOs…"):
    result = run_simulation(t_end)

st.markdown('<div class="hero-title">🧫 Biorreactor Fed-Batch</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hero-sub">Simulación numérica (RK45) &nbsp;·&nbsp; '
    f't ∈ [0, {t_end:.1f}] {time_cfg["unit"]} &nbsp;·&nbsp; '
    f'<span class="status-ok">✓ {result.message}</span></div>',
    unsafe_allow_html=True,
)

if not result.success:
    st.error(f"Error en la simulación: {result.message}")
    st.stop()

VAR_COLORS = {
    "X": "#58a6ff",
    "S": "#3fb950",
    "P": "#f78166",
    "V": "#d2a8ff",
}
VAR_NAMES = {
    "X": "Biomasa X",
    "S": "Sustrato S",
    "P": "Producto P",
    "V": "Volumen V",
}

st.markdown(f'<p class="section-title">Valores en t = {t_end:.2f} h</p>', unsafe_allow_html=True)

cols = st.columns(4)
for i, (var_name, var_res) in enumerate(result.variables.items()):
    with cols[i]:
        color = VAR_COLORS[var_name]
        st.markdown(
            f'<div class="metric-card" style="border-color:{color}33">'
            f'<div class="metric-label" style="color:{color}">{VAR_NAMES[var_name]}</div>'
            f'<div class="metric-value" style="color:{color}">{var_res.value_at_t:.4f}'
            f'<span class="metric-unit">{var_res.unit}</span></div>'
            f'<div class="metric-desc">{var_res.description}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

st.markdown('<p class="section-title">📈 Perfiles temporales</p>', unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(family="DM Sans", color="#c9d1d9", size=12),
    xaxis=dict(
        gridcolor="#21262d",
        linecolor="#30363d",
        tickcolor="#30363d",
        title_font=dict(family="Space Mono", size=11),
        tickfont=dict(family="Space Mono", size=10),
        title="Tiempo (h)",
    ),
    yaxis=dict(
        gridcolor="#21262d",
        linecolor="#30363d",
        tickcolor="#30363d",
        title_font=dict(family="Space Mono", size=11),
        tickfont=dict(family="Space Mono", size=10),
    ),
    margin=dict(l=60, r=20, t=50, b=50),
    hovermode="x unified",
    legend=dict(
        bgcolor="#161b22",
        bordercolor="#30363d",
        borderwidth=1,
        font=dict(family="Space Mono", size=10),
    ),
)

t = result.t

row1_cols = st.columns(2)
row2_cols = st.columns(2)
grid = [row1_cols[0], row1_cols[1], row2_cols[0], row2_cols[1]]

for i, (var_name, var_res) in enumerate(result.variables.items()):
    color = VAR_COLORS[var_name]
    values = var_res.values

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=t,
            y=values,
            fill="tozeroy",
            fillcolor=f"{color}18",
            line=dict(color=color, width=2.5),
            mode="lines",
            name=f"{var_name} ({var_res.unit})",
            hovertemplate=f"<b>t</b>: %{{x:.2f}} h<br><b>{var_name}</b>: %{{y:.4f}} {var_res.unit}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[t[-1]],
            y=[var_res.value_at_t],
            mode="markers+text",
            marker=dict(color=color, size=9, line=dict(color="#0d1117", width=2)),
            text=[f"  {var_res.value_at_t:.3f}"],
            textposition="middle right",
            textfont=dict(family="Space Mono", size=10, color=color),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    layout = dict(
        **PLOT_LAYOUT,
        title=dict(
            text=f"<b>{VAR_NAMES[var_name]}</b>",
            font=dict(family="Space Mono", size=14, color=color),
            x=0.04,
        ),
    )
    layout["yaxis"] = {**PLOT_LAYOUT["yaxis"], "title": f"{var_name} ({var_res.unit})"}
    fig.update_layout(**layout)

    grid[i].plotly_chart(fig, use_container_width=True)

st.markdown('<p class="section-title">🔀 Vista combinada (normalizada)</p>', unsafe_allow_html=True)

fig_all = go.Figure()
for var_name, var_res in result.variables.items():
    color = VAR_COLORS[var_name]
    values = var_res.values
    vmax = np.max(np.abs(values))
    norm = values / vmax if vmax > 0 else values

    fig_all.add_trace(
        go.Scatter(
            x=t,
            y=norm,
            line=dict(color=color, width=2),
            mode="lines",
            name=f"{var_name} / {var_name}_max",
            hovertemplate=f"<b>t</b>: %{{x:.2f}} h<br><b>{var_name}</b>: %{{customdata:.4f}} {var_res.unit}<extra></extra>",
            customdata=values,
        )
    )

combined_layout = dict(
    **PLOT_LAYOUT,
    title=dict(
        text="<b>Variables normalizadas</b>",
        font=dict(family="Space Mono", size=14, color="#e6edf3"),
        x=0.02,
    ),
)
combined_layout["yaxis"] = {**PLOT_LAYOUT["yaxis"], "title": "Valor normalizado (−)"}
fig_all.update_layout(**combined_layout)
st.plotly_chart(fig_all, use_container_width=True)

with st.expander("📊 Tabla de resultados numéricos"):
    import pandas as pd

    df = pd.DataFrame({"t (h)": t})
    for var_name, var_res in result.variables.items():
        df[f"{var_name} ({var_res.unit})"] = var_res.values

    st.dataframe(
        df.style.format("{:.4f}"),
        use_container_width=True,
        height=300,
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Descargar CSV", csv, "simulacion_biorreactor.csv", "text/csv")
