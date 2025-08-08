import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Cement Sector Climate Targets", layout="wide")

# ----------------------
# Data: real + placeholder
# ----------------------
data = [
    {"Company": "Holcim", "BaselineYear": 2018, "BaselineIntensity": 590, "CurrentYear": 2023, "CurrentIntensity": 420,
     "Target2030": 436, "Target2050": 30, "Source": "Holcim Climate Report 2023"},
    {"Company": "Heidelberg Materials", "BaselineYear": 2020, "BaselineIntensity": 580, "CurrentYear": 2023, "CurrentIntensity": 560,
     "Target2030": 425, "Target2050": 30, "Source": "Heidelberg Annual Report 2023"},
    {"Company": "CEMEX", "BaselineYear": 1990, "BaselineIntensity": 710, "CurrentYear": 2023, "CurrentIntensity": 475,
     "Target2030": 475, "Target2050": 0, "Source": "CEMEX Climate Position 2024"},
    {"Company": "CRH", "BaselineYear": 2021, "BaselineIntensity": 570, "CurrentYear": 2023, "CurrentIntensity": 550,
     "Target2030": 450, "Target2050": 30, "Source": "Placeholder"},
    {"Company": "UltraTech", "BaselineYear": 2017, "BaselineIntensity": 600, "CurrentYear": 2023, "CurrentIntensity": 520,
     "Target2030": 450, "Target2050": 30, "Source": "Placeholder"},
    {"Company": "Anhui Conch", "BaselineYear": 2019, "BaselineIntensity": 580, "CurrentYear": 2023, "CurrentIntensity": 540,
     "Target2030": 470, "Target2050": 30, "Source": "Placeholder"}
]
df = pd.DataFrame(data)

# ----------------------
# Normalize to 2019 = 100
# ----------------------
norm_df = df.copy()
norm_df["BaselineIndex"] = 100
norm_df["CurrentIndex"] = (norm_df["CurrentIntensity"] / norm_df["BaselineIntensity"]) * 100
norm_df["Target2030Index"] = (norm_df["Target2030"] / norm_df["BaselineIntensity"]) * 100
norm_df["Target2050Index"] = (norm_df["Target2050"] / norm_df["BaselineIntensity"]) * 100

# ----------------------
# Tabs
# ----------------------
tab1, tab2 = st.tabs(["2×2 Ambition Matrix", "Progress vs Targets"])

with tab1:
    st.subheader("2030 vs 2050 Target Ambition (Indexed to Baseline)")
    fig = px.scatter(
        norm_df,
        x="Target2030Index",
        y="Target2050Index",
        text="Company",
        hover_data=["Source"],
        size=[40]*len(norm_df),
        color="Company"
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(
        xaxis_title="2030 Target (2019=100)",
        yaxis_title="2050 Target (2019=100)",
        shapes=[
            dict(type="line", x0=100, x1=0, y0=50, y1=50, line=dict(dash="dot")),
            dict(type="line", x0=50, x1=50, y0=100, y1=0, line=dict(dash="dot"))
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Progress Over Time (Indexed to 2019 = 100)")
    all_years = list(range(2019, 2051))
    plot_data = []
    for _, row in norm_df.iterrows():
        start_idx = (2019 - row["BaselineYear"])
        start_val = 100
        curr_val = row["CurrentIndex"]
        t2030 = row["Target2030Index"]
        t2050 = row["Target2050Index"]
        
        # straight-line from current to 2030, then to 2050
        years1 = np.linspace(curr_val, t2030, 2030 - row["CurrentYear"] + 1)
        years2 = np.linspace(t2030, t2050, 2050 - 2030 + 1)[1:]
        proj = list(years1) + list(years2)
        proj_years = list(range(row["CurrentYear"], 2051))
        
        df_plot = pd.DataFrame({
            "Year": proj_years,
            "Index": proj,
            "Company": row["Company"]
        })
        plot_data.append(df_plot)
    plot_df = pd.concat(plot_data)

    fig2 = px.line(plot_df, x="Year", y="Index", color="Company")
    fig2.add_hline(y=100, line_dash="dot", annotation_text="2019 baseline", annotation_position="bottom right")
    st.plotly_chart(fig2, use_container_width=True)

st.caption("Sources: Holcim Climate Report 2023, Heidelberg AR 2023, CEMEX Climate Position 2024, plus placeholders for missing companies.")
