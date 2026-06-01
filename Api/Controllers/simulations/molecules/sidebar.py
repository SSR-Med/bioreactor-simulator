import streamlit as st

from Api.Controllers.atoms import render_metric_card, render_section_title
from Api.Controllers.molecules import render_time_control


def render_sidebar(cfg):
    t_end = None
    with st.sidebar:
        render_section_title("Par\u00e1metros de simulaci\u00f3n")

        t_end = render_time_control(cfg["time"])

        st.markdown("---")
        render_section_title("Condiciones iniciales")
        for var_name in cfg["variables"]:
            info = cfg["variables"][var_name]
            ic = cfg["initial_conditions"][var_name]
            html = render_metric_card(
                ic["label"],
                ic["value"],
                info["unit"],
                info["description"],
            )
            st.markdown(html, unsafe_allow_html=True)

        st.markdown("---")
        render_section_title("Ecuaciones del modelo")
        for name, eq in cfg["equations"].items():
            with st.expander(name):
                st.latex(eq["latex"])

    return t_end
