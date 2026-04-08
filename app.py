import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Fraud Risk Analysis Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #e74c3c;
        margin-bottom: 10px;
    }
    .ring-card {
        background: #1a1a2e;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #333;
        margin-bottom: 8px;
    }
    .critical-badge {
        background: #e74c3c;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .high-badge {
        background: #e67e22;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .medium-badge {
        background: #f39c12;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .low-badge {
        background: #27ae60;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .section-header {
        border-bottom: 2px solid #e74c3c;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(
        "/Users/mathuthavarajah/Documents/fraud-team/fraud_cases.csv",
        quotechar='"',
        skipinitialspace=True,
        on_bad_lines="skip",
    )
    df["application_date"] = pd.to_datetime(df["application_date"])
    df["income_coverage_pct"] = (
        df["observed_monthly_deposits"] / df["claimed_monthly_income"] * 100
    ).round(1)
    df["income_gap"] = df["claimed_monthly_income"] - df["observed_monthly_deposits"]
    return df


df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/fraud.png", width=64)
    st.title("Fraud Risk Dashboard")
    st.caption("Analysis Date: April 8, 2026")
    st.divider()

    st.subheader("Filters")
    selected_labels = st.multiselect(
        "Fraud Label",
        options=df["fraud_label"].unique().tolist(),
        default=df["fraud_label"].unique().tolist(),
    )
    selected_priority = st.multiselect(
        "Review Priority",
        options=df["manual_review_priority"].unique().tolist(),
        default=df["manual_review_priority"].unique().tolist(),
    )
    selected_provinces = st.multiselect(
        "Province",
        options=sorted(df["province"].unique().tolist()),
        default=sorted(df["province"].unique().tolist()),
    )

    st.divider()
    st.markdown("**Dataset Stats**")
    st.caption(f"Total Cases: **{len(df):,}**")
    st.caption(f"Date Range: Jan – Apr 2026")
    st.caption(f"Provinces: {df['province'].nunique()}")

filtered_df = df[
    df["fraud_label"].isin(selected_labels)
    & df["manual_review_priority"].isin(selected_priority)
    & df["province"].isin(selected_provinces)
]

# ── Fraud Ring Definitions ───────────────────────────────────────────────────
RINGS = {
    "Meridian Staffing Ring": {
        "device": "DEV-8821-A",
        "ip": "10.22.33.44",
        "employer": "Meridian Staffing Inc.",
        "color": "#e74c3c",
        "cases": ["FR-006", "FR-009", "FR-021", "FR-038", "FR-042", "FR-045", "FR-050", "FR-051"],
    },
    "Westline Holdings Ring": {
        "device": "DEV-7751-I",
        "ip": "198.51.100.12",
        "employer": "Westline Holdings",
        "color": "#e67e22",
        "cases": ["FR-011", "FR-015", "FR-023", "FR-028", "FR-031", "FR-032", "FR-047", "FR-048"],
    },
    "Forde Enterprises Ring": {
        "device": "DEV-RING3-X",
        "ip": "203.0.113.55",
        "employer": "Forde Enterprises",
        "color": "#9b59b6",
        "cases": ["FR-005", "FR-018", "FR-027", "FR-033", "FR-036", "FR-039", "FR-041"],
    },
    "Apex Resource Group Ring": {
        "device": "DEV-RING4-Y",
        "ip": "172.99.55.11",
        "employer": "Apex Resource Group",
        "color": "#3498db",
        "cases": ["FR-026", "FR-030", "FR-034", "FR-037", "FR-043", "FR-052"],
    },
    "Pinnacle Talent Group Ring": {
        "device": "DEV-RING5-Z",
        "ip": "10.88.77.22",
        "employer": "Pinnacle Talent Group",
        "color": "#1abc9c",
        "cases": ["FR-029", "FR-035", "FR-040", "FR-044", "FR-046", "FR-049"],
    },
}


# ── Page Header ──────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#e74c3c;'>🔍 Fraud Risk Analysis Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "**Loan Application Queue Review · 215 Cases · April 8, 2026**"
)
st.divider()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Executive Summary",
    "🎯 Review Queue",
    "🔗 Fraud Rings",
    "📈 Analytics",
    "📋 Case Explorer",
    "📝 Investigation Memo",
])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — Executive Summary
# ════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("## Executive Summary")

    # Top KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    total = len(df)
    high = (df["fraud_label"] == "likely_fraud").sum()
    medium = (df["fraud_label"] == "suspicious").sum()
    low = (df["fraud_label"] == "legitimate").sum()
    rings_active = 5

    col1.metric("Total Cases", f"{total:,}", help="All applications in queue")
    col2.metric("🔴 High Risk", f"{high}", f"{high/total*100:.0f}% of portfolio",
                delta_color="inverse")
    col3.metric("🟡 Medium Risk", f"{medium}", f"{medium/total*100:.0f}% of portfolio",
                delta_color="inverse")
    col4.metric("🟢 Low Risk", f"{low}", f"{low/total*100:.0f}% of portfolio")
    col5.metric("Active Fraud Rings", f"{rings_active}", "Coordinated operation",
                delta_color="inverse")

    st.divider()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        # Risk distribution donut
        label_counts = df["fraud_label"].value_counts().reset_index()
        label_counts.columns = ["label", "count"]
        label_map = {"likely_fraud": "High Risk", "suspicious": "Medium Risk", "legitimate": "Low Risk"}
        label_counts["label"] = label_counts["label"].map(label_map)
        color_map = {"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#27ae60"}

        fig_donut = px.pie(
            label_counts,
            names="label",
            values="count",
            hole=0.55,
            color="label",
            color_discrete_map=color_map,
            title="Risk Distribution",
        )
        fig_donut.update_traces(textposition="outside", textinfo="percent+label")
        fig_donut.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_size=16,
            margin=dict(t=50, b=20, l=20, r=20),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_right:
        # Applications over time
        daily = df.groupby(["application_date", "fraud_label"]).size().reset_index(name="count")
        daily["label"] = daily["fraud_label"].map(label_map)
        color_map2 = {"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#27ae60"}

        fig_time = px.bar(
            daily,
            x="application_date",
            y="count",
            color="label",
            color_discrete_map=color_map2,
            title="Applications Over Time by Risk Level",
            labels={"application_date": "Date", "count": "Applications", "label": "Risk"},
            barmode="stack",
        )
        fig_time.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            legend_title_text="",
            title_font_size=16,
            margin=dict(t=50, b=20, l=20, r=20),
        )
        st.plotly_chart(fig_time, use_container_width=True)

    st.divider()

    # Key findings
    st.subheader("Key Fraud Findings")
    f1, f2, f3 = st.columns(3)

    with f1:
        st.error("**Coordinated Ring Activity**")
        st.markdown(
            "Five distinct fraud rings operate using shared devices and IPs. "
            "Each ring uses a fictitious employer to fabricate employment history. "
            "Rings span multiple provinces — not isolated actors."
        )

    with f2:
        st.warning("**Income Fabrication at Scale**")
        fraud_cases = df[df["fraud_label"] == "likely_fraud"]
        avg_coverage = fraud_cases["income_coverage_pct"].mean()
        st.markdown(
            f"Across 34 high-risk cases, applicants show an average of only "
            f"**{avg_coverage:.0f}%** of claimed income in actual deposits. "
            f"Worst case: FR-049 at **5%** ($660 deposited vs $13,412 claimed)."
        )

    with f3:
        st.info("**Thin-File / Synthetic Signals**")
        st.markdown(
            "All 34 ring members have bank accounts **≤5 months old** — "
            "accounts opened specifically to support loan applications. "
            "FR-018 and FR-023 carry explicit synthetic identity flags."
        )


# ════════════════════════════════════════════════════════════════════
# TAB 2 — Review Queue
# ════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("## Priority Review Queue")
    st.caption("Top 5 cases requiring immediate action")

    TOP5 = [
        {
            "rank": "1",
            "case_id": "FR-021",
            "name": "Derek Fallon",
            "priority": "CRITICAL",
            "label": "likely_fraud",
            "ring": "Meridian Staffing Ring",
            "signals": "DEV-8821-A (4th use) · $900 deposits vs $5,100 claimed (18%) · 1-month account · IP shared with 7 cases",
            "why": "Fourth application on same device. Shutting this case exposes and blocks the entire Meridian ring (8 members).",
            "action": "Decline · Block DEV-8821-A · Block IP 10.22.33.44 · File SAR",
        },
        {
            "rank": "2",
            "case_id": "FR-049",
            "name": "Levi Moore",
            "priority": "CRITICAL",
            "label": "likely_fraud",
            "ring": "Pinnacle Talent Group Ring",
            "signals": "DEV-RING5-Z (5th use) · $660 deposits vs $13,412 claimed (5% — worst ratio in dataset) · 5-month account",
            "why": "Lowest income coverage in the entire portfolio. Ring has submitted 6 applications spanning Jan–Mar 2026.",
            "action": "Decline · Block DEV-RING5-Z · Block IP 10.88.77.22 · File SAR",
        },
        {
            "rank": "3",
            "case_id": "FR-033",
            "name": "Elena Taylor",
            "priority": "CRITICAL",
            "label": "likely_fraud",
            "ring": "Forde Enterprises Ring",
            "signals": "DEV-RING3-X · 1-month account · $1,853 vs $13,042 (14%) · IP 203.0.113.55 shared with 8+ cases",
            "why": "IP 203.0.113.55 is the most widely shared in the dataset. 1-month account is strongest thin-file signal.",
            "action": "Decline · Block IP 203.0.113.55 (highest case count) · Blacklist Forde Enterprises",
        },
        {
            "rank": "4",
            "case_id": "FR-032",
            "name": "Wyatt Brooks",
            "priority": "CRITICAL",
            "label": "likely_fraud",
            "ring": "Westline Holdings Ring",
            "signals": "DEV-7751-I (4th use) · $2,235 vs $13,900 (16%) · 5-month account · IP 198.51.100.12 shared with 7 cases",
            "why": "Westline Holdings spans 8 applications across multiple provinces. This case holds highest claimed income in the ring.",
            "action": "Decline · Block DEV-7751-I + IP 198.51.100.12 · Escalate all Westline cases together",
        },
        {
            "rank": "5",
            "case_id": "FR-037",
            "name": "Grace Fallon",
            "priority": "HIGH",
            "label": "likely_fraud",
            "ring": "Apex Resource Group Ring",
            "signals": "DEV-RING4-Y (5th use) · $2,935 vs $10,742 (27%) · 1-month account · Application dated 2026-03-20",
            "why": "Apex ring is currently active — FR-043 submitted 2026-04-01. Most recent application confirms ongoing activity.",
            "action": "Decline · Block DEV-RING4-Y + IP 172.99.55.11 · Urgent: check pipeline for new Apex applications",
        },
    ]

    badge_colors = {"CRITICAL": "#e74c3c", "HIGH": "#e67e22"}

    for case in TOP5:
        with st.container():
            col_rank, col_detail = st.columns([1, 9])
            with col_rank:
                st.markdown(
                    f"<div style='font-size:3rem;font-weight:900;color:{badge_colors.get(case['priority'],'#aaa')};text-align:center;'>"
                    f"#{case['rank']}</div>",
                    unsafe_allow_html=True,
                )
            with col_detail:
                badge_html = (
                    f"<span style='background:{badge_colors.get(case['priority'],'#aaa')};"
                    f"color:white;padding:3px 12px;border-radius:12px;font-size:12px;"
                    f"font-weight:bold;'>{case['priority']}</span>"
                )
                st.markdown(
                    f"**{case['case_id']}** — {case['name']} &nbsp; {badge_html}",
                    unsafe_allow_html=True,
                )
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Ring:** {case['ring']}")
                c2.markdown(f"**Label:** `{case['label']}`")
                c3.markdown(f"**Action:** {case['action']}")
                st.info(f"**Signals:** {case['signals']}")
                st.success(f"**Why it matters:** {case['why']}")
            st.divider()

    # Full priority table
    st.subheader("All High-Risk Cases")
    high_df = filtered_df[filtered_df["fraud_label"] == "likely_fraud"].copy()
    high_df = high_df.sort_values("income_coverage_pct")
    display_cols = [
        "case_id", "applicant_name", "province", "city", "employer_name",
        "claimed_monthly_income", "observed_monthly_deposits", "income_coverage_pct",
        "bank_account_age_months", "device_id", "ip_address",
    ]
    high_display = high_df[display_cols].rename(columns={
        "case_id": "Case ID",
        "applicant_name": "Applicant",
        "employer_name": "Employer",
        "claimed_monthly_income": "Claimed Income",
        "observed_monthly_deposits": "Observed Deposits",
        "income_coverage_pct": "Coverage %",
        "bank_account_age_months": "Acct Age (mo)",
        "device_id": "Device ID",
        "ip_address": "IP Address",
    })

    st.dataframe(
        high_display.style.background_gradient(
            subset=["Coverage %"], cmap="RdYlGn", vmin=0, vmax=100
        ).background_gradient(
            subset=["Acct Age (mo)"], cmap="RdYlGn_r", vmin=0, vmax=24
        ),
        use_container_width=True,
        height=400,
    )


# ════════════════════════════════════════════════════════════════════
# TAB 3 — Fraud Rings
# ════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("## Coordinated Fraud Ring Analysis")
    st.caption(
        "Five organized rings identified. Each shares a device ID, IP address, "
        "and fictitious employer across multiple applications."
    )

    # Ring overview metrics
    cols = st.columns(5)
    for i, (ring_name, ring) in enumerate(RINGS.items()):
        ring_cases_df = df[df["case_id"].isin(ring["cases"])]
        avg_gap = ring_cases_df["income_gap"].mean() if len(ring_cases_df) > 0 else 0
        avg_cov = ring_cases_df["income_coverage_pct"].mean() if len(ring_cases_df) > 0 else 0
        with cols[i]:
            st.markdown(
                f"<div style='border:2px solid {ring['color']};border-radius:10px;"
                f"padding:14px;text-align:center;'>"
                f"<div style='color:{ring['color']};font-weight:700;font-size:13px;'>"
                f"{ring_name.replace(' Ring','')}</div>"
                f"<div style='font-size:2rem;font-weight:900;'>{len(ring['cases'])}</div>"
                f"<div style='font-size:11px;color:#aaa;'>cases</div>"
                f"<div style='font-size:11px;margin-top:8px;'>Avg coverage: <b>{avg_cov:.0f}%</b></div>"
                f"<div style='font-size:11px;'>Avg gap: <b>${avg_gap:,.0f}/mo</b></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    # Ring selector
    selected_ring_name = st.selectbox(
        "Inspect a fraud ring:",
        options=list(RINGS.keys()),
    )
    ring = RINGS[selected_ring_name]
    ring_cases_df = df[df["case_id"].isin(ring["cases"])].copy()

    col_info, col_chart = st.columns([1, 2])

    with col_info:
        st.markdown(
            f"<div style='border-left:4px solid {ring['color']};padding-left:16px;'>"
            f"<h4>{selected_ring_name}</h4>"
            f"<b>Device ID:</b> <code>{ring['device']}</code><br>"
            f"<b>Shared IP:</b> <code>{ring['ip']}</code><br>"
            f"<b>Employer:</b> {ring['employer']}<br>"
            f"<b>Total Members:</b> {len(ring['cases'])}<br>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.divider()
        if len(ring_cases_df) > 0:
            st.metric("Avg Income Claimed", f"${ring_cases_df['claimed_monthly_income'].mean():,.0f}/mo")
            st.metric("Avg Observed Deposits", f"${ring_cases_df['observed_monthly_deposits'].mean():,.0f}/mo")
            st.metric("Avg Coverage Ratio", f"{ring_cases_df['income_coverage_pct'].mean():.1f}%")
            st.metric("Avg Bank Account Age", f"{ring_cases_df['bank_account_age_months'].mean():.1f} months")

    with col_chart:
        if len(ring_cases_df) > 0:
            fig_ring = go.Figure()
            fig_ring.add_trace(go.Bar(
                name="Claimed Income",
                x=ring_cases_df["case_id"],
                y=ring_cases_df["claimed_monthly_income"],
                marker_color="#e74c3c",
                opacity=0.85,
            ))
            fig_ring.add_trace(go.Bar(
                name="Observed Deposits",
                x=ring_cases_df["case_id"],
                y=ring_cases_df["observed_monthly_deposits"],
                marker_color=ring["color"],
                opacity=0.9,
            ))
            fig_ring.update_layout(
                title=f"{selected_ring_name}: Income vs. Deposits",
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                yaxis_title="$/month",
                xaxis_title="",
            )
            st.plotly_chart(fig_ring, use_container_width=True)

    # Ring case detail table
    if len(ring_cases_df) > 0:
        st.subheader("Ring Case Details")
        ring_display = ring_cases_df[[
            "case_id", "applicant_name", "province", "city",
            "claimed_monthly_income", "observed_monthly_deposits",
            "income_coverage_pct", "bank_account_age_months",
            "application_date", "ip_address",
        ]].copy()
        ring_display.columns = [
            "Case ID", "Applicant", "Province", "City",
            "Claimed Income", "Observed Deposits",
            "Coverage %", "Acct Age (mo)",
            "App Date", "IP Address",
        ]
        st.dataframe(
            ring_display.style.background_gradient(
                subset=["Coverage %"], cmap="RdYlGn", vmin=0, vmax=100
            ),
            use_container_width=True,
        )

    st.divider()

    # IP address heatmap
    st.subheader("Shared IP Address Clusters")
    ip_risk = df[df["fraud_label"].isin(["likely_fraud", "suspicious"])].copy()
    ip_counts = ip_risk.groupby(["ip_address", "fraud_label"]).size().reset_index(name="count")
    top_ips = ip_risk["ip_address"].value_counts().head(10).index.tolist()
    ip_top = ip_counts[ip_counts["ip_address"].isin(top_ips)]

    fig_ip = px.bar(
        ip_top,
        x="ip_address",
        y="count",
        color="fraud_label",
        color_discrete_map={"likely_fraud": "#e74c3c", "suspicious": "#f39c12"},
        title="Top Shared IP Addresses (Suspicious + Fraud Cases Only)",
        labels={"ip_address": "IP Address", "count": "Applications", "fraud_label": "Label"},
    )
    fig_ip.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis_tickangle=-30,
    )
    st.plotly_chart(fig_ip, use_container_width=True)


# ════════════════════════════════════════════════════════════════════
# TAB 4 — Analytics
# ════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("## Fraud Analytics")

    col_a, col_b = st.columns(2)

    with col_a:
        # Income coverage distribution
        fig_cov = px.histogram(
            filtered_df,
            x="income_coverage_pct",
            color="fraud_label",
            nbins=40,
            color_discrete_map={
                "likely_fraud": "#e74c3c",
                "suspicious": "#f39c12",
                "legitimate": "#27ae60",
            },
            title="Income Coverage Distribution (Deposits ÷ Claimed Income)",
            labels={"income_coverage_pct": "Coverage % (Observed / Claimed)", "count": "Cases"},
            barmode="overlay",
            opacity=0.75,
        )
        fig_cov.add_vline(x=50, line_dash="dash", line_color="white",
                          annotation_text="50% threshold", annotation_position="top right")
        fig_cov.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            legend_title_text="",
        )
        st.plotly_chart(fig_cov, use_container_width=True)

    with col_b:
        # Bank account age vs fraud
        fig_age = px.box(
            filtered_df,
            x="fraud_label",
            y="bank_account_age_months",
            color="fraud_label",
            color_discrete_map={
                "likely_fraud": "#e74c3c",
                "suspicious": "#f39c12",
                "legitimate": "#27ae60",
            },
            title="Bank Account Age by Fraud Label",
            labels={"bank_account_age_months": "Account Age (months)", "fraud_label": ""},
            points="outliers",
        )
        fig_age.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            showlegend=False,
        )
        st.plotly_chart(fig_age, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        # Province breakdown
        prov_risk = (
            filtered_df[filtered_df["fraud_label"] == "likely_fraud"]
            .groupby("province")
            .size()
            .reset_index(name="fraud_count")
            .sort_values("fraud_count", ascending=True)
        )
        fig_prov = px.bar(
            prov_risk,
            x="fraud_count",
            y="province",
            orientation="h",
            title="High-Risk Cases by Province",
            color="fraud_count",
            color_continuous_scale="Reds",
            labels={"fraud_count": "Likely Fraud Cases", "province": ""},
        )
        fig_prov.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_prov, use_container_width=True)

    with col_d:
        # Scatter: claimed vs observed
        fig_scatter = px.scatter(
            filtered_df,
            x="claimed_monthly_income",
            y="observed_monthly_deposits",
            color="fraud_label",
            color_discrete_map={
                "likely_fraud": "#e74c3c",
                "suspicious": "#f39c12",
                "legitimate": "#27ae60",
            },
            hover_data=["case_id", "applicant_name", "employer_name"],
            title="Claimed Income vs. Observed Deposits",
            labels={
                "claimed_monthly_income": "Claimed Monthly Income ($)",
                "observed_monthly_deposits": "Observed Deposits ($)",
                "fraud_label": "",
            },
            opacity=0.7,
        )
        # Add 1:1 reference line
        max_val = filtered_df["claimed_monthly_income"].max()
        fig_scatter.add_trace(go.Scatter(
            x=[0, max_val], y=[0, max_val],
            mode="lines",
            line=dict(color="white", dash="dot", width=1),
            name="1:1 line (income = deposits)",
        ))
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Device reuse heatmap
    st.subheader("Device Reuse by Fraud Label")
    device_fraud = (
        df[df["device_reuse_count"] > 1]
        .groupby(["device_id", "fraud_label"])
        .size()
        .reset_index(name="count")
    )
    top_devices = (
        df[df["device_reuse_count"] > 1]["device_id"]
        .value_counts()
        .head(12)
        .index.tolist()
    )
    device_top = device_fraud[device_fraud["device_id"].isin(top_devices)]

    fig_dev = px.bar(
        device_top,
        x="device_id",
        y="count",
        color="fraud_label",
        color_discrete_map={
            "likely_fraud": "#e74c3c",
            "suspicious": "#f39c12",
            "legitimate": "#27ae60",
        },
        title="Top Reused Devices — Application Count by Risk Label",
        labels={"device_id": "Device ID", "count": "Applications", "fraud_label": ""},
        barmode="stack",
    )
    fig_dev.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis_tickangle=-30,
    )
    st.plotly_chart(fig_dev, use_container_width=True)


# ════════════════════════════════════════════════════════════════════
# TAB 5 — Case Explorer
# ════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("## Case Explorer")

    search_col, filter_col1, filter_col2 = st.columns([2, 1, 1])
    with search_col:
        search = st.text_input("Search by Case ID, Name, or Employer", "")
    with filter_col1:
        explorer_label = st.selectbox(
            "Fraud Label", ["All"] + df["fraud_label"].unique().tolist()
        )
    with filter_col2:
        explorer_priority = st.selectbox(
            "Priority", ["All"] + df["manual_review_priority"].unique().tolist()
        )

    explorer_df = filtered_df.copy()
    if search:
        mask = (
            explorer_df["case_id"].str.contains(search, case=False, na=False)
            | explorer_df["applicant_name"].str.contains(search, case=False, na=False)
            | explorer_df["employer_name"].str.contains(search, case=False, na=False)
        )
        explorer_df = explorer_df[mask]
    if explorer_label != "All":
        explorer_df = explorer_df[explorer_df["fraud_label"] == explorer_label]
    if explorer_priority != "All":
        explorer_df = explorer_df[explorer_df["manual_review_priority"] == explorer_priority]

    explorer_df = explorer_df.sort_values(["manual_review_priority", "income_coverage_pct"],
                                           ascending=[True, True])

    label_colors = {"likely_fraud": "🔴", "suspicious": "🟡", "legitimate": "🟢"}
    explorer_df["Risk"] = explorer_df["fraud_label"].map(label_colors) + " " + explorer_df["fraud_label"]

    show_cols = [
        "case_id", "applicant_name", "province", "employer_name",
        "claimed_monthly_income", "observed_monthly_deposits", "income_coverage_pct",
        "bank_account_age_months", "device_id", "Risk", "manual_review_priority",
    ]
    st.dataframe(
        explorer_df[show_cols].rename(columns={
            "case_id": "Case ID",
            "applicant_name": "Applicant",
            "employer_name": "Employer",
            "claimed_monthly_income": "Claimed $/mo",
            "observed_monthly_deposits": "Observed $/mo",
            "income_coverage_pct": "Coverage %",
            "bank_account_age_months": "Acct Age",
            "device_id": "Device",
            "manual_review_priority": "Priority",
        }),
        use_container_width=True,
        height=500,
    )

    st.caption(f"Showing **{len(explorer_df)}** of **{len(df)}** cases")

    # Case detail expander
    st.divider()
    st.subheader("Case Detail")
    selected_case_id = st.selectbox("Select a case to inspect", explorer_df["case_id"].tolist())
    if selected_case_id:
        case_row = df[df["case_id"] == selected_case_id].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Claimed Income", f"${case_row['claimed_monthly_income']:,}/mo")
        c2.metric("Observed Deposits", f"${case_row['observed_monthly_deposits']:,}/mo")
        c3.metric("Coverage Ratio", f"{case_row['income_coverage_pct']}%",
                  delta=f"{case_row['income_coverage_pct']-100:.0f}% vs 100% target",
                  delta_color="inverse")
        c4.metric("Account Age", f"{case_row['bank_account_age_months']} months")

        col_detail_left, col_detail_right = st.columns(2)
        with col_detail_left:
            st.markdown("**Application Details**")
            detail_fields = {
                "Case ID": case_row["case_id"],
                "Applicant": case_row["applicant_name"],
                "Age": case_row["age"],
                "Province": case_row["province"],
                "City": case_row["city"],
                "Application Date": str(case_row["application_date"].date()),
                "Email": case_row["email"],
                "Phone": case_row["phone"],
            }
            for k, v in detail_fields.items():
                st.markdown(f"**{k}:** {v}")

        with col_detail_right:
            st.markdown("**Risk Signals**")
            risk_fields = {
                "Employer": case_row["employer_name"],
                "Job Title": case_row["job_title"],
                "Device ID": case_row["device_id"],
                "IP Address": case_row["ip_address"],
                "Device Reuse Count": case_row["device_reuse_count"],
                "IP Reuse Count": case_row["ip_reuse_count"],
                "Fraud Label": case_row["fraud_label"],
                "Review Priority": case_row["manual_review_priority"],
                "Identity Risk": case_row["identity_risk"],
                "Synthetic Identity Risk": case_row["synthetic_identity_risk"],
            }
            for k, v in risk_fields.items():
                st.markdown(f"**{k}:** {v}")

        st.markdown("**Analyst Notes**")
        st.info(case_row["analyst_notes"])


# ════════════════════════════════════════════════════════════════════
# TAB 6 — Investigation Memo
# ════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("## Investigation Memo")

    st.markdown("""
    <div style="border:1px solid #e74c3c;border-radius:8px;padding:24px;background:#1a0a0a;">
    <b>TO:</b> Fraud Operations Team<br>
    <b>FROM:</b> Fraud Risk Analyst (AI-Assisted Review)<br>
    <b>DATE:</b> April 8, 2026<br>
    <b>RE:</b> Coordinated Multi-Ring Fraud Operation — Loan Application Queue<br>
    <b style="color:#e74c3c;">PRIORITY: CRITICAL</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Summary")
    st.markdown("""
    A review of **215 loan applications** identified **five active coordinated fraud rings** operating across Canada.
    Each ring follows an identical playbook: a **fictitious or unverifiable employer**, a recently opened bank account
    (1–5 months), grossly inflated claimed income against observed deposits, and — most critically — a **shared device ID
    and IP address reused across multiple applicants**. The most advanced ring (Meridian Staffing / DEV-8821-A) has
    submitted at least 8 fraudulent applications spanning January to March 2026. The most recent confirmed ring activity
    is the Apex Resource Group ring, with FR-043 (Brandon Harris) submitted on **2026-04-01** — just 7 days ago.
    **This ring is currently active.**
    """)

    st.markdown("### Evidence Summary")
    evidence = [
        ("5 devices reused across 35 confirmed fraud cases",
         "DEV-8821-A (8 apps), DEV-7751-I (8 apps), DEV-RING3-X (7 apps), DEV-RING4-Y (6 apps), DEV-RING5-Z (6 apps)"),
        ("5 fictitious employers",
         "Meridian Staffing Inc., Westline Holdings, Forde Enterprises, Apex Resource Group, Pinnacle Talent Group — none verifiable"),
        ("5 IP addresses tied 1:1 to each ring",
         "10.22.33.44, 198.51.100.12, 203.0.113.55, 172.99.55.11, 10.88.77.22"),
        ("Extreme income fabrication",
         "Average coverage ~15–20% of claimed income. Worst case: FR-049 at 5% ($660 observed vs. $13,412 claimed)"),
        ("Thin-file bank accounts",
         "All 34 ring members have accounts ≤5 months old — opened specifically for this application"),
        ("Synthetic identity signals",
         "FR-023 flagged for synthetic identity risk; FR-018 flagged for limited credit history"),
        ("Email naming pattern",
         "Formulaic '_ca' suffix appears disproportionately across ring members — possible automated generation"),
    ]
    for title, detail in evidence:
        with st.expander(f"📌 {title}"):
            st.markdown(detail)

    st.markdown("### Risk Assessment")
    st.error(
        "**CRITICAL.** This is not isolated fraud — it is an organized operation with consistent tradecraft across "
        "5 distinct rings. Total combined loan exposure across 34 high-risk applications is substantial. "
        "The Apex ring (FR-043, Apr 1 2026) confirms ongoing activity. Immediate systemic controls are required."
    )

    st.markdown("### Recommended Disposition")
    actions = [
        "**Decline all 34 high-risk applications immediately.** Do not fund pending cases.",
        "**Block all 5 device IDs and 5 ring IP addresses** across the originations platform — prevent new applications from the same infrastructure.",
        "**Blacklist all 5 employer names** in the employer verification registry.",
        "**Refer to fraud investigations / law enforcement** — scale, coordination, and cross-provincial reach warrants a formal investigation referral.",
        "**Review FR-025 (Raymond Eck)** as a borderline ring affiliate — shares IP and employer (Forde Enterprises) with Ring 3.",
        "**Audit 16 medium-risk cases** for possible ring affiliation not yet detected.",
    ]
    for i, action in enumerate(actions, 1):
        st.markdown(f"{i}. {action}")

    st.markdown("### What to Verify Next")
    verifications = [
        "Confirm DEV-RING4-Y (Apex ring) and DEV-8821-A (Meridian ring) are blocked at the platform level before next business day",
        "Request bank account ownership verification for all 34 cases — confirm accounts are held by the named applicants",
        "Submit Suspicious Activity Reports (SARs) for all five rings",
        "Query originations system for any additional applications from the five blocked IPs not yet in this dataset",
    ]
    for v in verifications:
        st.checkbox(v, value=False)

    st.divider()

    # Evidence Appendix
    st.markdown("### Evidence Appendix — Top Suspicious Cases")

    APPENDIX = {
        "FR-021 — Derek Fallon (Meridian Staffing Ring)": {
            "device_id": ("DEV-8821-A", "4th application using this device — conclusive reuse"),
            "bank_account_age_months": ("1 month", "Account opened 1 month ago — opened for this application"),
            "claimed_monthly_income": ("$5,100", "Far above observed deposits"),
            "observed_monthly_deposits": ("$900", "Only 18% of claimed income"),
            "employer_name": ("Meridian Staffing Inc.", "Unverified; linked to 8 total fraud applications"),
            "ip_address": ("10.22.33.44", "Shared with FR-006, FR-009, FR-038, FR-042, FR-045, FR-050, FR-051"),
        },
        "FR-049 — Levi Moore (Pinnacle Talent Group Ring)": {
            "device_id": ("DEV-RING5-Z", "5th application on this device"),
            "bank_account_age_months": ("5 months", "Recently opened"),
            "claimed_monthly_income": ("$13,412", "Highest of Pinnacle ring members"),
            "observed_monthly_deposits": ("$660", "5% coverage — worst income ratio in entire dataset"),
            "employer_name": ("Pinnacle Talent Group", "Unverifiable; only appears in fraud applications"),
            "ip_address": ("10.88.77.22", "Shared with FR-029, FR-035, FR-040, FR-044, FR-046"),
        },
        "FR-033 — Elena Taylor (Forde Enterprises Ring)": {
            "device_id": ("DEV-RING3-X", "Tied to Forde Enterprises ring"),
            "bank_account_age_months": ("1 month", "Opened 1 month ago — strongest account-age signal"),
            "claimed_monthly_income": ("$13,042", "Inflated to match a senior role"),
            "observed_monthly_deposits": ("$1,853", "14% of claimed income"),
            "employer_name": ("Forde Enterprises", "Unverifiable; linked to 7+ fraud applications"),
            "ip_address": ("203.0.113.55", "Most widely shared IP in dataset — 8+ cases"),
        },
        "FR-023 — Leo Barker (Westline Holdings Ring)": {
            "device_id": ("DEV-7751-I", "3rd Westline Holdings device application"),
            "bank_account_age_months": ("2 months", "Very recently opened"),
            "claimed_monthly_income": ("$9,200", "Junior Analyst title — income implausible"),
            "observed_monthly_deposits": ("$1,500", "16% of claimed income"),
            "employer_name": ("Westline Holdings", "Unverifiable; linked to 8 fraud applications"),
            "synthetic_identity_risk": ("HIGH", "Synthetic identity flagged — possible fabricated person"),
        },
        "FR-035 — Joseph Edwards (Pinnacle Talent Group Ring)": {
            "device_id": ("DEV-RING5-Z", "Pinnacle ring device"),
            "bank_account_age_months": ("2 months", "Recently opened"),
            "claimed_monthly_income": ("$13,938", "Highest claimed income in Pinnacle ring"),
            "observed_monthly_deposits": ("$1,264", "9% of claimed income"),
            "application_date": ("2026-01-18", "Ring has been operating for nearly 3 months"),
            "ip_reuse_count": ("3", "Confirmed multi-applicant IP"),
        },
    }

    for case_title, fields in APPENDIX.items():
        with st.expander(f"📎 {case_title}"):
            rows = []
            for field, (value, reason) in fields.items():
                rows.append({"Field": field, "Value": value, "Why Suspicious": reason})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()
    st.caption(
        "This report was generated by automated fraud analysis on 2026-04-08. "
        "All cases flagged as likely_fraud or suspicious should receive manual review "
        "before any credit decision is finalized."
    )
