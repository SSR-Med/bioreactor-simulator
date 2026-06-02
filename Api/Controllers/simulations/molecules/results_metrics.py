import streamlit as st

from Api.Controllers.atoms import render_metric_card, render_section_title


def render_results_metrics(result, t_end, cfg):
    variables_cfg = cfg["variables"]
    time_unit = cfg["time"]["unit"]

    render_section_title(f"Valores en t = {t_end:.2f} {time_unit}")

    cols = st.columns(len(result.variables))
    for i, (var_name, var_res) in enumerate(result.variables.items()):
        with cols[i]:
            info = variables_cfg[var_name]
            html = render_metric_card(
                info["label"],
                f"{var_res.value_at_t:.4f}",
                var_res.unit,
                var_res.description,
                color=info["color"],
            )
            st.markdown(html, unsafe_allow_html=True)
