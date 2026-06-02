import numpy as np
import plotly.graph_objects as go
import streamlit as st

from Api.Controllers.atoms import render_section_title


def _hex_to_rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _build_plot_layout(axis_label):
    return dict(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#c9d1d9", size=12),
        xaxis=dict(
            gridcolor="#21262d",
            linecolor="#30363d",
            tickcolor="#30363d",
            title_font=dict(family="Space Mono", size=11),
            tickfont=dict(family="Space Mono", size=10),
            title=axis_label,
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


def _build_single_plot(t, var_name, var_res, color, var_label, axis_label):
    values = var_res.values
    plot_layout = _build_plot_layout(axis_label)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=t,
            y=values,
            fill="tozeroy",
            fillcolor=_hex_to_rgba(color, 0.1),
            line=dict(color=color, width=2.5),
            mode="lines",
            name=f"{var_name} ({var_res.unit})",
            hovertemplate=(
                f"<b>{axis_label}</b>: %{{x:.2f}}<br>"
                f"<b>{var_name}</b>: %{{y:.4f}} {var_res.unit}<extra></extra>"
            ),
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
        **plot_layout,
        title=dict(
            text=f"<b>{var_label}</b>",
            font=dict(family="Space Mono", size=14, color=color),
            x=0.04,
        ),
    )
    layout["yaxis"] = {
        **plot_layout["yaxis"],
        "title": f"{var_name} ({var_res.unit})",
    }
    fig.update_layout(**layout)

    return fig


def render_plots(result, cfg):
    t = result.t
    variables_cfg = cfg["variables"]
    axis_label = cfg["time"]["axis_label"]
    n_vars = len(result.variables)

    render_section_title("Perfiles temporales")

    cols = st.columns(n_vars)

    for i, (var_name, var_res) in enumerate(result.variables.items()):
        info = variables_cfg[var_name]
        fig = _build_single_plot(
            t, var_name, var_res, info["color"], info["label"], axis_label
        )
        cols[i].plotly_chart(fig, width="stretch")
