import streamlit as st


def render_time_control(time_cfg):
    return st.number_input(
        time_cfg["input_label"],
        min_value=float(time_cfg["min"]),
        max_value=float(time_cfg["max"]),
        value=float(time_cfg["default"]),
        step=float(time_cfg["step"]),
        key="t_number",
        format="%.2f",
    )
