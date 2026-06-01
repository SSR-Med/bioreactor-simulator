import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st

from Infrastructure.Services import ConfigService
from Application.Features.Equations.SolveEquations import (
    SolveEquationsQuery,
    SolveEquationsQueryHandler,
)
from Api.Controllers.atoms import render_status_badge
from Api.Controllers.simulations.molecules import (
    render_sidebar,
    render_results_metrics,
    render_plots,
    render_data_table,
)

st.set_page_config(
    page_title="Biorreactor Simulator",
    page_icon=os.path.join(ROOT, "Api", "static", "favicon.svg"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

      #MainMenu, footer, header { visibility: hidden; }
      .stDeployButton { display: none; }

      .main .block-container {
          padding-top: 2.5rem;
          padding-left: 2rem;
          padding-right: 2rem;
      }

      .hero-title {
          font-family: 'Space Mono', monospace;
          font-size: 2.5rem;
          font-weight: 700;
          letter-spacing: -0.03em;
          line-height: 1.2;
          margin-bottom: 0.3rem;
      }
      .hero-sub {
          font-size: 1rem;
          color: #8b949e;
          margin-bottom: 2rem;
      }

      .section-title {
          font-family: 'Space Mono', monospace;
          font-size: 0.8rem;
          color: #58a6ff;
          text-transform: uppercase;
          letter-spacing: 0.12em;
          margin-bottom: 0.8rem;
          border-bottom: 1px solid #30363d;
          padding-bottom: 0.5rem;
      }

      .metric-card {
          border: 1px solid #30363d;
          border-radius: 12px;
          padding: 1.2rem 1.5rem;
          margin-bottom: 0.6rem;
          transition: border-color 0.2s;
      }
      .metric-card:hover { border-color: #58a6ff; }
      .metric-label {
          font-family: 'Space Mono', monospace;
          font-size: 0.75rem;
          color: #8b949e;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          margin-bottom: 0.3rem;
      }
      .metric-value {
          font-family: 'Space Mono', monospace;
          font-size: 1.8rem;
          font-weight: 700;
      }
      .metric-unit {
          font-size: 0.85rem;
          color: #8b949e;
          margin-left: 0.3rem;
      }
      .metric-desc {
          font-size: 0.8rem;
          color: #8b949e;
          margin-top: 0.25rem;
      }

      .status-ok {
          display: inline-block;
          background: #1a3a2a;
          color: #3fb950;
          border: 1px solid #238636;
          border-radius: 20px;
          padding: 0.15rem 0.7rem;
          font-size: 0.75rem;
          font-family: 'Space Mono', monospace;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_config():
    svc = ConfigService()
    return svc.load()


cfg = load_config()

t_end = render_sidebar(cfg)


@st.cache_data(show_spinner=False)
def run_simulation(t_end: float):
    query = SolveEquationsQuery(t_end=t_end, config=cfg)
    handler = SolveEquationsQueryHandler()
    return handler.handle(query)


with st.spinner("Integrando sistema de EDOs\u2026"):
    result = run_simulation(t_end)

st.markdown(
    '<div class="hero-title">Biorreactor</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="hero-sub">t \u2208 [0, {t_end:.1f}] {cfg["time"]["unit"]}</div>',
    unsafe_allow_html=True,
)

if not result.success:
    st.error(f"Error en la simulaci\u00f3n: {result.message}")
    st.stop()

render_results_metrics(result, t_end, cfg)

st.markdown("---")

render_plots(result, cfg)

render_data_table(result, result.t)
