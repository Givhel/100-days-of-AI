# dashboard.py — Internshala Internship Tracker
# Day 3 of 100 Days — @thekunal.build
# Run: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random

st.set_page_config(
    page_title="Internship Tracker",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

* { font-family: 'JetBrains Mono', monospace !important; }

[data-testid="stAppViewContainer"] { background: #080808; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #0d0d0d; border-right: 1px solid #222; }
.block-container { padding: 2rem 3rem; }

/* Fix faded text */
p, span, label, div { color: #e0e0e0 !important; }
h1, h2, h3 { color: #ffffff !important; }

/* Metric cards */
div[data-testid="metric-container"] {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
div[data-testid="metric-container"] label {
    color: #888 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 28px !important;
    font-weight: 600 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #222 !important;
    border-radius: 10px !important;
}

/* Input */
[data-testid="stTextInput"] input {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    color: #fff !important;
    border-radius: 8px !important;
}

/* Selectbox */
[data-testid="stSelectbox"] select {
    background: #111 !important;
    color: #fff !important;
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: #7F77DD !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

/* Divider */
hr { border-color: #1a1a1a !important; }

/* Sidebar text */
[data-testid="stSidebar"] * { color: #ccc !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #fff !important; }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────
st.markdown("""
<div style="background:#111;border:1px solid #222;border-radius:14px;
            padding:24px 32px;margin-bottom:28px">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
        <span style="width:13px;height:13px;border-radius:50%;
                     background:#E24B4A;display:inline-block"></span>
        <span style="width:13px;height:13px;border-radius:50%;
                     background:#E4A500;display:inline-block"></span>
        <span style="width:13px;height:13px;border-radius:50%;
                     background:#1D9E75;display:inline-block"></span>
        <span style="color:#555;font-size:12px;margin-left:10px">
            internship-tracker — dashboard.py
        </span>
    </div>
    <div style="font-size:26px;font-weight:700;color:#ffffff;margin-bottom:6px">
        🔍 Internshala Internship Tracker
    </div>
    <div style="font-size:13px;color:#666">
        Day 3 of 100 &nbsp;·&nbsp;
        <span style="color:#7F77DD">@thekunal.build</span>
        &nbsp;·&nbsp; github.com/Givhel
    </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ────────────────────────────────────────────
try:
    df = pd.read_csv("internships.csv")
except FileNotFoundError:
    st.error("⚠️ Run python scraper.py first to generate internships.csv")
    st.stop()

# ─── SIDEBAR FILTERS ──────────────────────────────────────
st.sidebar.markdown("## 🎛️ Filters")
st.sidebar.markdown("---")

locations = ["All"] + sorted(df["location"].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("📍 Location", locations)

stipend_filter = st.sidebar.radio(
    "💰 Stipend",
    ["All", "Paid only", "Unpaid only"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:12px;color:#555;line-height:1.6">
    Built with<br>
    🐍 Python<br>
    🍜 BeautifulSoup<br>
    🐼 Pandas<br>
    📊 Plotly<br>
    🚀 Streamlit
</div>
""", unsafe_allow_html=True)

# Apply filters
df_filtered = df.copy()
if selected_location != "All":
    df_filtered = df_filtered[df_filtered["location"].str.contains(
        selected_location, na=False)]
if stipend_filter == "Paid only":
    df_filtered = df_filtered[df_filtered["stipend"] != "Unpaid"]
elif stipend_filter == "Unpaid only":
    df_filtered = df_filtered[df_filtered["stipend"] == "Unpaid"]

# ─── METRICS ──────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

paid   = len(df_filtered[df_filtered["stipend"] != "Unpaid"])
remote = len(df_filtered[df_filtered["location"].str.contains(
    "Work from Home|Remote|work from home", na=False, case=False)])
companies = df_filtered["company"].nunique()
unpaid = len(df_filtered) - paid

with col1:
    st.metric("🔎 Total Found", len(df_filtered))
with col2:
    st.metric("💰 Paid", paid)
with col3:
    st.metric("🏠 Remote", remote)
with col4:
    st.metric("🏢 Companies", companies)
with col5:
    st.metric("📋 Unpaid", unpaid)

st.markdown("<br>", unsafe_allow_html=True)

# ─── ROW 1: SKILLS BAR + LOCATION PIE ─────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### 📊 Top Skills Companies Are Demanding")

    common_skills = [
        "python", "machine learning", "data analysis", "sql", "excel",
        "javascript", "react", "django", "flask", "pandas", "numpy",
        "tensorflow", "pytorch", "nlp", "deep learning", "java",
        "tableau", "power bi", "aws", "docker", "git", "figma",
        "communication", "c++", "mongodb"
    ]

    skill_count = {}
    for skill in common_skills:
        count = df_filtered.apply(
            lambda row: skill.lower() in
            str(row.get("skills", "")).lower() + " " +
            str(row.get("title", "")).lower(),
            axis=1
        ).sum()
        if count > 0:
            skill_count[skill] = int(count)

    skill_count = dict(sorted(
        skill_count.items(), key=lambda x: x[1], reverse=True)[:10])

    bar_colors = [
        "#7F77DD", "#1D9E75", "#E4A500", "#E24B4A", "#378ADD",
        "#7F77DD", "#1D9E75", "#E4A500", "#E24B4A", "#378ADD"
    ]

    fig_skills = go.Figure()
    fig_skills.add_trace(go.Bar(
        x=list(skill_count.keys()),
        y=list(skill_count.values()),
        marker_color=bar_colors[:len(skill_count)],
        marker_line_width=0,
        text=list(skill_count.values()),
        textposition="outside",
        textfont=dict(color="#ccc", size=12, family="JetBrains Mono"),
    ))

    fig_skills.update_layout(
        paper_bgcolor="#111",
        plot_bgcolor="#111",
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        xaxis=dict(
            tickfont=dict(color="#ccc", size=11,
                          family="JetBrains Mono"),
            gridcolor="#1a1a1a",
            linecolor="#222"
        ),
        yaxis=dict(
            tickfont=dict(color="#888", size=10),
            gridcolor="#1a1a1a",
            linecolor="#222"
        ),
        bargap=0.3,
    )
    st.plotly_chart(fig_skills, use_container_width=True,
                    config={"displayModeBar": False})

with col_right:
    st.markdown("### 🥧 Paid vs Unpaid")

    pie_labels = ["Paid", "Unpaid"]
    pie_values = [paid, unpaid]
    pie_colors = ["#1D9E75", "#E24B4A"]

    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=pie_labels,
        values=pie_values,
        marker=dict(
            colors=pie_colors,
            line=dict(color="#080808", width=3)
        ),
        textfont=dict(color="#fff", size=13,
                      family="JetBrains Mono"),
        hole=0.5,
        textinfo="label+percent"
    ))

    fig_pie.update_layout(
        paper_bgcolor="#111",
        plot_bgcolor="#111",
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        annotations=[dict(
            text=f"{paid}<br><span style='font-size:10px'>paid</span>",
            x=0.5, y=0.5,
            font=dict(color="#fff", size=18,
                      family="JetBrains Mono"),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True,
                    config={"displayModeBar": False})

st.markdown("<br>", unsafe_allow_html=True)

# ─── ROW 2: LOCATION BAR + REMOTE PIE ─────────────────────
col_left2, col_right2 = st.columns([3, 2])

with col_left2:
    st.markdown("### 📍 Internships by Location")

    loc_counts = df_filtered["location"].value_counts().head(8)

    fig_loc = go.Figure()
    fig_loc.add_trace(go.Bar(
        x=loc_counts.index.tolist(),
        y=loc_counts.values.tolist(),
        marker_color="#7F77DD",
        marker_line_width=0,
        text=loc_counts.values.tolist(),
        textposition="outside",
        textfont=dict(color="#ccc", size=11,
                      family="JetBrains Mono"),
    ))

    fig_loc.update_layout(
        paper_bgcolor="#111",
        plot_bgcolor="#111",
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        xaxis=dict(
            tickfont=dict(color="#ccc", size=10,
                          family="JetBrains Mono"),
            gridcolor="#1a1a1a",
            linecolor="#222"
        ),
        yaxis=dict(
            tickfont=dict(color="#888", size=10),
            gridcolor="#1a1a1a",
            linecolor="#222"
        ),
        bargap=0.3,
    )
    st.plotly_chart(fig_loc, use_container_width=True,
                    config={"displayModeBar": False})

with col_right2:
    st.markdown("### 🏠 Remote vs Onsite")

    onsite = len(df_filtered) - remote
    fig_pie2 = go.Figure()
    fig_pie2.add_trace(go.Pie(
        labels=["Remote", "Onsite"],
        values=[remote, onsite],
        marker=dict(
            colors=["#378ADD", "#E4A500"],
            line=dict(color="#080808", width=3)
        ),
        textfont=dict(color="#fff", size=13,
                      family="JetBrains Mono"),
        hole=0.5,
        textinfo="label+percent"
    ))

    fig_pie2.update_layout(
        paper_bgcolor="#111",
        plot_bgcolor="#111",
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        annotations=[dict(
            text=f"{remote}<br><span>remote</span>",
            x=0.5, y=0.5,
            font=dict(color="#fff", size=18,
                      family="JetBrains Mono"),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_pie2, use_container_width=True,
                    config={"displayModeBar": False})

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABLE ────────────────────────────────────────────────
st.markdown("### 📋 All Internships")

search = st.text_input("🔎 Search company or title", "")

if search:
    df_show = df_filtered[
        df_filtered["company"].str.contains(search, case=False, na=False) |
        df_filtered["title"].str.contains(search, case=False, na=False)
    ]
else:
    df_show = df_filtered

st.dataframe(
    df_show[["title", "company", "stipend", "duration", "location"]].reset_index(drop=True),
    use_container_width=True,
    height=380
)

col_dl1, col_dl2 = st.columns([1, 4])
with col_dl1:
    csv = df_show.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="internships.csv",
        mime="text/csv"
    )

# ─── FOOTER ───────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:20px;
            border-top:1px solid #1a1a1a;
            color:#444;font-size:12px">
    Built with Python + BeautifulSoup + Pandas + Plotly + Streamlit
    &nbsp;·&nbsp; Day 3 of 100
    &nbsp;·&nbsp;
    <span style="color:#7F77DD">@thekunal.build</span>
    &nbsp;·&nbsp; github.com/Givhel
</div>
""", unsafe_allow_html=True)