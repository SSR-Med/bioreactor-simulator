import pandas as pd
import streamlit as st


def render_data_table(result, t, cfg):
    with st.expander("Tabla de resultados num\u00e9ricos"):
        df = pd.DataFrame({cfg["time"]["axis_label"]: t})
        for var_name, var_res in result.variables.items():
            info = cfg["variables"][var_name]
            df[f"{info['label']} ({var_res.unit})"] = var_res.values

        st.dataframe(
            df.style.format("{:.4f}"),
            width="stretch",
            height=300,
        )
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descargar CSV",
            csv,
            "simulacion_biorreactor.csv",
            "text/csv",
        )
