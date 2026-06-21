# dashboard.py — Amazon Wishlist Analyzer
# Day 2 of 100 Days — @thekunal.build
# Run: streamlit run dashboard.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime

# ─── PAGE CONFIG ──────────────────────────────────────────
st.set_page_config(
    page_title="Amazon Wishlist Analyzer",
    page_icon="🛒",
    layout="wide"
)

# ─── GLOBAL STYLES ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

* { font-family: 'JetBrains Mono', monospace !important; }

[data-testid="stAppViewContainer"] {
    background: #080808;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #0d0d0d; border-right: 1px solid #1a1a1a; }

.block-container { padding: 2rem 3rem; }

/* Product cards */
.prod-card {
    background: #0f0f0f;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 16px;
    border: 0.5px solid #1e1e1e;
    transition: border-color 0.3s;
}

/* Metric cards */
.metric-box {
    background: #0f0f0f;
    border: 0.5px solid #1e1e1e;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.metric-val {
    font-size: 24px;
    font-weight: 600;
    color: #fff;
}
.metric-label {
    font-size: 11px;
    color: #444;
    margin-top: 4px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Recommendation pill */
.rec-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.05em;
}

/* Day badges */
.day-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
    margin: 2px;
}

/* Terminal header */
.terminal-header {
    background: #0f0f0f;
    border: 0.5px solid #1e1e1e;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 24px;
}

.blink {
    animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }

div[data-testid="metric-container"] {
    background: #0f0f0f;
    border: 0.5px solid #1e1e1e;
    border-radius: 10px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA ─────────────────────────────────────────────────
PRODUCTS = [
    {"name": "boAt Airdopes 141",      "emoji": "🎧", "base": 4999,  "color": "#7F77DD"},
    {"name": "Noise ColorFit Pro 4",   "emoji": "⌚", "base": 3999,  "color": "#1D9E75"},
    {"name": "Ambrane 20000mAh",       "emoji": "🔋", "base": 1299,  "color": "#E4A500"},
    {"name": "Logitech M235 Mouse",    "emoji": "🖱️",  "base": 1595,  "color": "#E24B4A"},
    {"name": "Kindle Paperwhite",      "emoji": "📖", "base": 13999, "color": "#378ADD"},
]

DAY_MULTIPLIERS = {
    "Monday":    1.05,
    "Tuesday":   1.02,
    "Wednesday": 0.91,
    "Thursday":  1.00,
    "Friday":    0.95,
    "Saturday":  1.09,
    "Sunday":    1.07,
}

DAYS = list(DAY_MULTIPLIERS.keys())

# ─── ANALYSIS ─────────────────────────────────────────────
@st.cache_data
def analyze_all():
    results = []
    for p in PRODUCTS:
        base = p["base"]
        avg_by_day = {}
        for day, mult in DAY_MULTIPLIERS.items():
            prices = [round(base * (mult + random.uniform(-0.02, 0.02)), -1) for _ in range(4)]
            avg_by_day[day] = sum(prices) / len(prices)

        best_day  = min(avg_by_day, key=avg_by_day.get)
        worst_day = max(avg_by_day, key=avg_by_day.get)
        current   = round(base * (DAY_MULTIPLIERS.get(datetime.now().strftime("%A"), 1.0) + random.uniform(-0.02, 0.02)), -1)
        lowest    = round(min(avg_by_day.values()), -1)
        highest   = round(max(avg_by_day.values()), -1)
        avg       = round(sum(avg_by_day.values()) / 7, -1)
        saving    = round(avg - lowest, -1)
        pct       = ((current - avg) / avg) * 100

        if pct <= -3:
            rec, rec_color, rec_bg, rec_icon = "BUY NOW", "#1D9E75", "#0d1f17", "✅"
        elif pct <= 3:
            rec, rec_color, rec_bg, rec_icon = "DECENT TIME", "#E4A500", "#1f1800", "🟡"
        else:
            rec, rec_color, rec_bg, rec_icon = f"WAIT → {best_day[:3].upper()}", "#E24B4A", "#1f0d0d", "⏳"

        results.append({
            **p,
            "avg_by_day": avg_by_day,
            "best_day":   best_day,
            "worst_day":  worst_day,
            "current":    current,
            "lowest":     lowest,
            "highest":    highest,
            "avg":        avg,
            "saving":     saving,
            "pct":        pct,
            "rec":        rec,
            "rec_color":  rec_color,
            "rec_bg":     rec_bg,
            "rec_icon":   rec_icon,
        })
    return results

# ─── HEADER ───────────────────────────────────────────────
st.markdown("""
<div class="terminal-header">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
        <span style="width:12px;height:12px;border-radius:50%;background:#E24B4A;display:inline-block"></span>
        <span style="width:12px;height:12px;border-radius:50%;background:#E4A500;display:inline-block"></span>
        <span style="width:12px;height:12px;border-radius:50%;background:#1D9E75;display:inline-block"></span>
        <span style="color:#333;font-size:12px;margin-left:8px">amazon-wishlist-analyzer — dashboard.py</span>
    </div>
    <div style="font-size:22px;font-weight:600;color:#fff;margin-bottom:4px">
        🛒 Amazon Wishlist Analyzer
    </div>
    <div style="font-size:12px;color:#444">
        Day 2 of 100 &nbsp;·&nbsp; @thekunal.build &nbsp;·&nbsp; github.com/Givhel
        <span style="color:#7F77DD;margin-left:8px">█</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ────────────────────────────────────────────
with st.spinner("Fetching price history..."):
    results = analyze_all()

# ─── SUMMARY METRICS ──────────────────────────────────────
buy_now  = [r for r in results if "BUY" in r["rec"]]
wait     = [r for r in results if "WAIT" in r["rec"]]
decent   = [r for r in results if "DECENT" in r["rec"]]
total_saving = sum(r["saving"] for r in results)
best_deal    = min(results, key=lambda r: r["pct"])

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Products", len(results), "in wishlist")
with col2:
    st.metric("Buy Now", len(buy_now), "at good price")
with col3:
    st.metric("Wait", len(wait), "overpriced now")
with col4:
    st.metric("Monthly Saving", f"₹{total_saving:,.0f}", "if timed right")
with col5:
    st.metric("Best Deal", best_deal["emoji"] + " " + best_deal["name"].split()[0], f"{abs(best_deal['pct']):.1f}% below avg")

st.markdown("<br>", unsafe_allow_html=True)

# ─── PRODUCT CARDS ────────────────────────────────────────
st.markdown(f"### 📊 Product Analysis")
st.markdown("<br>", unsafe_allow_html=True)

for r in results:
    color = r["color"]

    # Card container with left color border
    st.markdown(f"""
    <div style="
        border-left: 3px solid {color};
        background: #0f0f0f;
        border-radius: 0 12px 12px 0;
        padding: 20px 24px;
        margin-bottom: 20px;
        border-top: 0.5px solid #1a1a1a;
        border-right: 0.5px solid #1a1a1a;
        border-bottom: 0.5px solid #1a1a1a;
    ">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
            <div>
                <span style="font-size:20px">{r['emoji']}</span>
                <span style="font-size:16px;font-weight:600;color:#fff;margin-left:10px">{r['name']}</span>
            </div>
            <div style="background:{r['rec_bg']};border:0.5px solid {r['rec_color']};
                        border-radius:20px;padding:6px 16px;
                        color:{r['rec_color']};font-size:13px;font-weight:600">
                {r['rec_icon']} {r['rec']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        # Price metrics
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Current", f"₹{r['current']:,.0f}")
            st.metric("Lowest", f"₹{r['lowest']:,.0f}")
        with m2:
            st.metric("Average", f"₹{r['avg']:,.0f}")
            st.metric("You Save", f"₹{r['saving']:,.0f}")

        # Best / worst day badges
        st.markdown(f"""
        <div style="margin-top:12px">
            <span style="font-size:11px;color:#444;text-transform:uppercase;letter-spacing:0.08em">Best day</span><br>
            <span style="background:{color}22;border:0.5px solid {color};
                         color:{color};padding:4px 12px;border-radius:6px;
                         font-size:13px;font-weight:500">{r['best_day']}</span>
            &nbsp;
            <span style="background:#E24B4A22;border:0.5px solid #E24B4A;
                         color:#E24B4A;padding:4px 12px;border-radius:6px;
                         font-size:13px;font-weight:500">Avoid {r['worst_day']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Day by day bar chart
        days_list  = list(r["avg_by_day"].keys())
        prices     = list(r["avg_by_day"].values())
        bar_colors = []
        for d in days_list:
            if d == r["best_day"]:
                bar_colors.append(color)
            elif d == r["worst_day"]:
                bar_colors.append("#E24B4A")
            else:
                bar_colors.append("#1e1e1e")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=days_list,
            y=prices,
            marker_color=bar_colors,
            marker_line_width=0,
            text=[f"₹{p:,.0f}" for p in prices],
            textposition="outside",
            textfont=dict(color="#666", size=10),
        ))

        # Highlight best day
        fig.add_annotation(
            x=r["best_day"],
            y=max(prices) * 1.12,
            text="CHEAPEST",
            showarrow=False,
            font=dict(color=color, size=10, family="JetBrains Mono"),
        )

        fig.update_layout(
            paper_bgcolor="#0f0f0f",
            plot_bgcolor="#0f0f0f",
            height=200,
            margin=dict(l=0, r=0, t=20, b=0),
            showlegend=False,
            xaxis=dict(
                tickfont=dict(color="#555", size=11),
                gridcolor="#151515",
                linecolor="#1a1a1a"
            ),
            yaxis=dict(visible=False),
            bargap=0.3,
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<hr style='border-color:#151515;margin:8px 0 24px'>", unsafe_allow_html=True)

# ─── COMPARISON CHART ─────────────────────────────────────
st.markdown("### 💰 Saving Potential Comparison")
st.markdown("<br>", unsafe_allow_html=True)

names   = [r["emoji"] + " " + r["name"].split()[0] for r in results]
savings = [r["saving"] for r in results]
colors  = [r["color"] for r in results]

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=names,
    y=savings,
    marker_color=colors,
    marker_line_width=0,
    text=[f"₹{s:,.0f}" for s in savings],
    textposition="outside",
    textfont=dict(color="#888", size=12),
))

fig2.update_layout(
    paper_bgcolor="#0f0f0f",
    plot_bgcolor="#0f0f0f",
    height=280,
    margin=dict(l=0, r=0, t=20, b=0),
    showlegend=False,
    xaxis=dict(
        tickfont=dict(color="#666", size=12),
        gridcolor="#111",
        linecolor="#1a1a1a"
    ),
    yaxis=dict(
        tickfont=dict(color="#444", size=10),
        gridcolor="#111",
        tickprefix="₹"
    ),
    bargap=0.35,
)

st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ─── FOOTER ───────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;padding:16px;border-top:0.5px solid #1a1a1a;color:#333;font-size:12px">
    Built with Python + Pandas + Plotly + Streamlit &nbsp;·&nbsp;
    Day 2 of 100 Days &nbsp;·&nbsp;
    <span style="color:#7F77DD">@thekunal.build</span> &nbsp;·&nbsp;
    github.com/Givhel
</div>
""", unsafe_allow_html=True)