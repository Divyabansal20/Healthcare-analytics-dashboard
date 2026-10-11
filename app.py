"""
Healthcare Clinical & Operational Analytics Dashboard
Author: Divya Bansal
Description: An interactive, production-grade Streamlit healthcare analytics platform 
featuring clinical KPI tracking, epidemiological cohort analysis, financial performance 
metrics, interactive patient risk simulation, and registry exploration.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime
from generate_data import generate_hospital_data, generate_monthly_trends

# Optional statsmodels support for Plotly OLS
try:
    import statsmodels
    has_statsmodels = True
except ImportError:
    has_statsmodels = False

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Healthcare Analytics Dashboard | Divya Bansal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Healthcare Analytics Design System
st.markdown("""
<style>
    /* Global Typography & Layout */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Top Header Banner */
    .dashboard-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0D9488 100%);
        padding: 24px 28px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.12);
    }
    .dashboard-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
        color: #F8FAFC;
    }
    .dashboard-subtitle {
        font-size: 0.98rem;
        color: #94A3B8;
        margin-top: 6px;
        font-weight: 400;
    }
    .author-badge {
        display: inline-block;
        background: rgba(13, 148, 136, 0.25);
        border: 1px solid rgba(13, 148, 136, 0.5);
        color: #5EEAD4;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* KPI Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.07);
    }
    .metric-title {
        color: #64748B;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #0F172A;
        font-size: 1.85rem;
        font-weight: 700;
        margin: 6px 0 2px 0;
    }
    .metric-sub {
        font-size: 0.80rem;
        color: #64748B;
    }
    
    /* Dynamic Insight Callout */
    .insight-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
        border-left: 4px solid #10B981;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: #065F46;
        font-size: 0.92rem;
    }
    
    /* Sidebar styling */
    .sidebar-author-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DATA PIPELINE & CACHING
# ==========================================
@st.cache_data
def load_healthcare_data():
    """Loads and formats patient records with fallback generator."""
    patient_file = 'patient_data.csv'
    if os.path.exists(patient_file):
        df = pd.read_csv(patient_file)
    else:
        df = generate_hospital_data(n_patients=1200)
        df.to_csv(patient_file, index=False)
        
    df['admission_date'] = pd.to_datetime(df['admission_date'])
    return df

patient_df = load_healthcare_data()


# ==========================================
# 3. SIDEBAR CONTROLS & FILTERS
# ==========================================
with st.sidebar:
    st.markdown("## Filter Control Panel")
    st.caption("Customize cohort parameters for real-time analysis")
    
    # Date Range Filter
    min_date = patient_df['admission_date'].min().date()
    max_date = patient_df['admission_date'].max().date()
    selected_date_range = st.date_input(
        "Admission Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Handle single date vs range tuple safely
    if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
    else:
        start_date, end_date = min_date, max_date
        
    # Department Multiselect
    all_depts = sorted(patient_df['department'].unique().tolist())
    selected_depts = st.multiselect("Hospital Department", all_depts, default=all_depts)
    
    # Disease Multiselect
    all_diseases = sorted(patient_df['disease'].unique().tolist())
    selected_diseases = st.multiselect("Clinical Condition", all_diseases, default=all_diseases)
    
    # Age Group Multiselect
    all_age_groups = sorted(patient_df['age_group'].unique().tolist())
    selected_age_groups = st.multiselect("Age Demographics", all_age_groups, default=all_age_groups)
    
    # Admission Type & Insurance
    all_admissions = sorted(patient_df['admission_type'].unique().tolist())
    selected_admissions = st.multiselect("Admission Type", all_admissions, default=all_admissions)
    
    all_insurances = sorted(patient_df['insurance_type'].unique().tolist())
    selected_insurances = st.multiselect("Insurance Payer", all_insurances, default=all_insurances)
    
    st.markdown("---")
    
    # Author Profile Section
    st.markdown("""
    <div class="sidebar-author-card">
        <strong style="color: #0F172A; font-size: 0.95rem;">Divya Bansal</strong><br>
        <span style="color: #64748B; font-size: 0.82rem;">Lead Developer & Healthcare Data Analyst</span>
        <hr style="margin: 8px 0; border: none; border-top: 1px solid #E2E8F0;">
        <span style="font-size: 0.78rem; color: #475569;">
            Focusing on clinical cohort discovery, hospital operational optimization, 
            predictive risk modeling, and business intelligence.
        </span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. FILTER EXECUTION & EMPTY STATE HANDLING
# ==========================================
filtered_df = patient_df[
    (patient_df['admission_date'].dt.date >= start_date) &
    (patient_df['admission_date'].dt.date <= end_date) &
    (patient_df['department'].isin(selected_depts)) &
    (patient_df['disease'].isin(selected_diseases)) &
    (patient_df['age_group'].isin(selected_age_groups)) &
    (patient_df['admission_type'].isin(selected_admissions)) &
    (patient_df['insurance_type'].isin(selected_insurances))
]

# Top Header Presentation
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">Healthcare Clinical & Operational Analytics</h1>
    <div class="dashboard-subtitle">
        Enterprise Hospital Intelligence Platform | Operational Benchmarks | Readmission Risk Modeling
    </div>
    <div class="author-badge">
        Author & Data Analyst: Divya Bansal
    </div>
</div>
""", unsafe_allow_html=True)

# Guard against empty filtered state
if filtered_df.empty:
    st.warning("Notice: No patient records match the currently selected filter criteria. Please expand your selections in the sidebar (for example, select more departments, conditions, or broaden the date range).")
    st.stop()


# ==========================================
# 5. DYNAMIC EXECUTIVE INSIGHTS GENERATION
# ==========================================
total_pts = len(filtered_df)
avg_los = filtered_df['length_of_stay'].mean()
readm_rate = filtered_df['readmitted'].mean() * 100
total_revenue = filtered_df['total_charges'].sum()
avg_charge = filtered_df['total_charges'].mean()
avg_daily_cost = (filtered_df['total_charges'] / filtered_df['length_of_stay']).mean()

# Identify analytical highlights dynamically
top_disease = filtered_df['disease'].value_counts().index[0]
top_disease_pct = (filtered_df['disease'].value_counts().iloc[0] / total_pts) * 100
top_cost_dept = filtered_df.groupby('department')['total_charges'].sum().idxmax()
dept_cost_share = (filtered_df.groupby('department')['total_charges'].sum().max() / total_revenue) * 100

insight_html = f"""
<div class="insight-card">
    <strong>Key Executive Takeaways ({total_pts:,} Filtered Inpatient Records):</strong><br>
    - <strong>Prevalent Condition:</strong> <em>{top_disease}</em> represents <strong>{top_disease_pct:.1f}%</strong> of total admissions in this cohort.<br>
    - <strong>Financial Driver:</strong> <em>{top_cost_dept}</em> accounts for <strong>{dept_cost_share:.1f}%</strong> of total billed hospital expenditure (${total_revenue:,.0f}).<br>
    - <strong>Quality Benchmark:</strong> 30-Day Readmission rate is <strong>{readm_rate:.1f}%</strong> 
    {'(Exceeds national 12.0% benchmark threshold)' if readm_rate > 12.0 else '(Within acceptable quality benchmark range)'}.
</div>
"""
st.markdown(insight_html, unsafe_allow_html=True)


# ==========================================
# 6. TABBED DASHBOARD ARCHITECTURE
# ==========================================
tab_exec, tab_clinical, tab_financial, tab_predict, tab_registry = st.tabs([
    "Executive KPI Overview",
    "Clinical & Demographics",
    "Financial & Departmental",
    "Readmission Risk Simulator",
    "Patient Registry & Export"
])


# ------------------------------------------
# TAB 1: EXECUTIVE KPI OVERVIEW
# ------------------------------------------
with tab_exec:
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Admissions</div>
            <div class="metric-value">{total_pts:,}</div>
            <div class="metric-sub">Active Inpatient Cohort</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        los_delta = avg_los - 4.5
        delta_symbol = "+" if los_delta > 0 else "-"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Length of Stay</div>
            <div class="metric-value">{avg_los:.1f} <span style="font-size:1rem;color:#64748B;">days</span></div>
            <div class="metric-sub">{delta_symbol} {abs(los_delta):.1f} vs Target (4.5d)</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        readm_delta = readm_rate - 12.0
        delta_symbol = "+" if readm_delta > 0 else "-"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">30-Day Readmission</div>
            <div class="metric-value">{readm_rate:.1f}%</div>
            <div class="metric-sub">{delta_symbol} {abs(readm_delta):.1f}% vs Benchmark (12.0%)</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Billed Charges</div>
            <div class="metric-value">${total_revenue/1e6:.2f}M</div>
            <div class="metric-sub">Avg ${avg_charge:,.0f} / patient</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Cost Per Day</div>
            <div class="metric-value">${avg_daily_cost:,.0f}</div>
            <div class="metric-sub">Operational Daily Cost</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Hospital Operational Trends Over Time")
    
    cohort_monthly = filtered_df.copy()
    cohort_monthly['month'] = cohort_monthly['admission_date'].dt.strftime('%Y-%m')
    monthly_stats = cohort_monthly.groupby('month').agg(
        admissions=('patient_id', 'count'),
        avg_stay=('length_of_stay', 'mean'),
        readm_rate=('readmitted', lambda x: x.mean() * 100),
        total_charges=('total_charges', lambda x: x.sum() / 1e6)
    ).reset_index().sort_values('month')
    
    fig_trends = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Monthly Patient Admissions', 
            'Average Length of Stay (Days)',
            '30-Day Readmission Rate (%)', 
            'Total Billed Revenue ($ Millions)'
        ),
        vertical_spacing=0.14
    )
    
    fig_trends.add_trace(go.Scatter(
        x=monthly_stats['month'], y=monthly_stats['admissions'],
        mode='lines+markers', name='Admissions', line=dict(color='#0284C7', width=3),
        marker=dict(size=7)
    ), row=1, col=1)
    
    fig_trends.add_trace(go.Scatter(
        x=monthly_stats['month'], y=monthly_stats['avg_stay'],
        mode='lines+markers', name='Avg Stay', line=dict(color='#F97316', width=3),
        marker=dict(size=7)
    ), row=1, col=2)
    
    fig_trends.add_trace(go.Scatter(
        x=monthly_stats['month'], y=monthly_stats['readm_rate'],
        mode='lines+markers', name='Readmission %', line=dict(color='#10B981', width=3),
        marker=dict(size=7)
    ), row=2, col=1)
    
    fig_trends.add_trace(go.Scatter(
        x=monthly_stats['month'], y=monthly_stats['total_charges'],
        mode='lines+markers', name='Charges ($M)', line=dict(color='#8B5CF6', width=3),
        marker=dict(size=7)
    ), row=2, col=2)
    
    fig_trends.update_layout(
        height=520, 
        showlegend=False, 
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_trends, use_container_width=True)


# ------------------------------------------
# TAB 2: CLINICAL & DEMOGRAPHICS
# ------------------------------------------
with tab_clinical:
    st.subheader("Disease Burden & Demographics Analysis")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        disease_df = filtered_df['disease'].value_counts().reset_index()
        disease_df.columns = ['Disease', 'Patient Count']
        fig_dis = px.bar(
            disease_df, x='Disease', y='Patient Count',
            title="Admissions by Clinical Condition",
            color='Patient Count',
            color_continuous_scale='Blues',
            text='Patient Count'
        )
        fig_dis.update_traces(textposition='outside')
        fig_dis.update_layout(template='plotly_white', height=400, margin=dict(t=40, b=20))
        st.plotly_chart(fig_dis, use_container_width=True)
        
    with col_c2:
        risk_counts = filtered_df['risk_factor'].value_counts().reset_index()
        risk_counts.columns = ['Risk Factor', 'Count']
        fig_rf = px.pie(
            risk_counts, values='Count', names='Risk Factor',
            title="Distribution of Identified Risk Factors",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_rf.update_layout(template='plotly_white', height=400, margin=dict(t=40, b=20))
        st.plotly_chart(fig_rf, use_container_width=True)
        
    col_c3, col_c4 = st.columns(2)
    
    with col_c3:
        fig_box = px.box(
            filtered_df, x='disease', y='length_of_stay',
            title="Length of Stay Distribution & Outliers by Condition",
            color='disease',
            labels={'disease': 'Condition', 'length_of_stay': 'Stay Duration (Days)'}
        )
        fig_box.update_layout(template='plotly_white', showlegend=False, height=420, margin=dict(t=40, b=20))
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_c4:
        ct_data = pd.crosstab(filtered_df['disease'], filtered_df['age_group'])
        fig_ct = px.imshow(
            ct_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
            title="Patient Volume Matrix: Condition vs. Age Cohort",
            labels=dict(x="Age Cohort", y="Condition", color="Patient Volume")
        )
        fig_ct.update_layout(template='plotly_white', height=420, margin=dict(t=40, b=20))
        st.plotly_chart(fig_ct, use_container_width=True)


# ------------------------------------------
# TAB 3: FINANCIAL & DEPARTMENTAL PERFORMANCE
# ------------------------------------------
with tab_financial:
    st.subheader("Financial Utilization & Cost Efficiency")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        dept_summary = filtered_df.groupby('department').agg(
            patients=('patient_id', 'count'),
            total_revenue=('total_charges', lambda x: x.sum() / 1e6),
            avg_stay=('length_of_stay', 'mean')
        ).reset_index()
        
        fig_dept_rev = px.bar(
            dept_summary, x='department', y='total_revenue',
            title="Total Revenue Generated by Department ($ Millions)",
            color='total_revenue',
            color_continuous_scale='Teal',
            labels={'department': 'Department', 'total_revenue': 'Revenue ($M)'},
            text_auto='.2f'
        )
        fig_dept_rev.update_layout(template='plotly_white', height=400, margin=dict(t=40, b=20))
        st.plotly_chart(fig_dept_rev, use_container_width=True)
        
    with col_f2:
        payer_df = filtered_df.groupby('insurance_type').agg(
            patients=('patient_id', 'count'),
            total_cost=('total_charges', 'sum')
        ).reset_index()
        
        fig_payer = px.pie(
            payer_df, values='total_cost', names='insurance_type',
            title="Payer Mix: Revenue Contribution by Insurance",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_payer.update_layout(template='plotly_white', height=400, margin=dict(t=40, b=20))
        st.plotly_chart(fig_payer, use_container_width=True)
        
    st.markdown("#### Cost vs. Length of Stay Relationship (Regression Analysis)")
    fig_scatter = px.scatter(
        filtered_df, x='length_of_stay', y='total_charges',
        color='disease',
        size='daily_cost',
        hover_data=['patient_id', 'department', 'age', 'admission_type'],
        title="Patient Billing vs. Stay Duration (Bubble size reflects Daily Cost)",
        labels={'length_of_stay': 'Length of Stay (Days)', 'total_charges': 'Total Billed Charges ($)'},
        trendline="ols" if (has_statsmodels and len(filtered_df) > 10) else None
    )
    if not has_statsmodels and len(filtered_df) > 1:
        x_vals = np.array(filtered_df['length_of_stay'])
        y_vals = np.array(filtered_df['total_charges'])
        if len(x_vals) >= 2 and np.std(x_vals) > 0:
            m, b = np.polyfit(x_vals, y_vals, 1)
            x_line = np.linspace(x_vals.min(), x_vals.max(), 50)
            y_line = m * x_line + b
            fig_scatter.add_trace(go.Scatter(
                x=x_line, y=y_line,
                mode='lines',
                name=f'Trendline (${m:.0f}/day)',
                line=dict(color='#0F172A', dash='dash', width=2)
            ))
    fig_scatter.update_layout(template='plotly_white', height=480, margin=dict(t=40, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("#### Statistical Correlation Analysis (Continuous Clinical & Financial Metrics)")
    metric_cols = ['age', 'length_of_stay', 'total_charges', 'daily_cost', 'readmitted', 'satisfaction_score']
    corr_df = filtered_df[metric_cols].corr().round(2)
    
    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        title="Pearson Correlation Matrix (Clinical & Financial Factors)"
    )
    fig_corr.update_layout(template='plotly_white', height=400, margin=dict(t=40, b=20))
    st.plotly_chart(fig_corr, use_container_width=True)


# ------------------------------------------
# TAB 4: READMISSION RISK SIMULATOR
# ------------------------------------------
with tab_predict:
    st.subheader("Predictive 30-Day Readmission Risk Simulator")
    st.markdown("""
    Evaluate patient profiles and simulate readmission probability using an empirical multi-factor clinical risk model. 
    Use this interactive tool to demonstrate operational decision-support and proactive care intervention planning.
    """)
    
    sim_col1, sim_col2 = st.columns([1.1, 1])
    
    with sim_col1:
        st.markdown("##### Input Patient Clinical Parameters")
        sim_age = st.slider("Patient Age", min_value=18, max_value=95, value=58, step=1)
        sim_disease = st.selectbox("Primary Condition", all_diseases, index=0)
        sim_adm_type = st.selectbox("Admission Type", all_admissions, index=0)
        sim_los = st.slider("Hospital Length of Stay (Days)", min_value=1, max_value=30, value=6, step=1)
        sim_risks = st.multiselect(
            "Identified Comorbid Risk Factors", 
            ['Smoking', 'Obesity', 'Sedentary Lifestyle', 'Poor Diet', 'Alcohol', 'Stress', 'Genetics'],
            default=['Smoking']
        )
        
        # Empirical Risk Scoring Algorithm
        base_log_odds = -2.4
        
        cond_weights = {
            'Heart Disease': 0.75, 'Stroke': 0.85, 'Cancer': 0.65, 'Kidney Disease': 0.70,
            'COPD': 0.60, 'Diabetes': 0.40, 'Hypertension': 0.25, 'Arthritis': 0.15,
            'Asthma': 0.20, 'Obesity': 0.25
        }
        base_log_odds += cond_weights.get(sim_disease, 0.3)
        
        if sim_age >= 65:
            base_log_odds += 0.55
        elif sim_age >= 50:
            base_log_odds += 0.25
            
        if sim_adm_type == 'Emergency':
            base_log_odds += 0.45
            
        if sim_los > 7:
            base_log_odds += 0.40
            
        base_log_odds += len(sim_risks) * 0.18
        
        risk_probability = 1.0 / (1.0 + np.exp(-base_log_odds))
        risk_pct = round(risk_probability * 100, 1)
        
    with sim_col2:
        st.markdown("##### Predicted Risk Stratification")
        
        if risk_pct < 15.0:
            tier_color = "#10B981"
            tier_label = "LOW RISK"
        elif risk_pct <= 28.0:
            tier_color = "#F59E0B"
            tier_label = "MODERATE RISK"
        else:
            tier_color = "#EF4444"
            tier_label = "HIGH RISK"
            
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            title={'text': f"Predicted Readmission Risk: [{tier_label}]", 'font': {'size': 18}},
            number={'suffix': "%", 'font': {'size': 38, 'color': tier_color}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': tier_color, 'thickness': 0.3},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 15], 'color': '#ECFDF5'},
                    {'range': [15, 28], 'color': '#FFFBEB'},
                    {'range': [28, 100], 'color': '#FEF2F2'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': risk_pct
                }
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=30, r=30, t=50, b=20), template='plotly_white')
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown(f"**Recommended Actionable Interventions ({tier_label}):**")
        if tier_label == "HIGH RISK":
            st.error("""
            - Schedule dedicated 48-hour post-discharge nurse telehealth follow-up.  
            - Initiate comprehensive clinical medication reconciliation review.  
            - Refer patient for specialized home healthcare and chronic disease care management.
            """)
        elif tier_label == "MODERATE RISK":
            st.warning("""
            - Schedule primary care clinic consultation within 7 business days.  
            - Provide tailored discharge education on condition warning signs.  
            - Implement remote symptom check-in protocol at day 5 post-discharge.
            """)
        else:
            st.success("""
            - Standard routine discharge protocol with printed patient instructions.  
            - Routine primary care follow-up within 14 to 21 days.
            """)


# ------------------------------------------
# TAB 5: PATIENT REGISTRY & DATA EXPORT
# ------------------------------------------
with tab_registry:
    st.subheader("Patient Registry & Cohort Export")
    
    r_col1, r_col2 = st.columns([2, 1])
    with r_col1:
        search_query = st.text_input("Search Patient Records (by ID or Disease)", "")
    with r_col2:
        export_cols = st.multiselect(
            "Selected Columns to Display",
            list(filtered_df.columns),
            default=['patient_id', 'age', 'gender', 'disease', 'department', 'admission_type', 'length_of_stay', 'total_charges', 'readmitted']
        )
        
    display_df = filtered_df.copy()
    if search_query:
        display_df = display_df[
            display_df['patient_id'].astype(str).str.contains(search_query, case=False, na=False) |
            display_df['disease'].str.contains(search_query, case=False, na=False) |
            display_df['department'].str.contains(search_query, case=False, na=False)
        ]
        
    st.dataframe(
        display_df[export_cols].reset_index(drop=True),
        use_container_width=True,
        height=380
    )
    
    st.caption(f"Displaying {len(display_df):,} matching patient records.")
    
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Cohort Dataset (CSV)",
        data=csv_data,
        file_name=f"healthcare_patient_cohort_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    with st.expander("View Cohort Statistical Summary (Numeric Metrics)"):
        st.dataframe(filtered_df[['age', 'length_of_stay', 'total_charges', 'daily_cost', 'satisfaction_score']].describe().round(2))

# ==========================================
# 7. FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 12px 0;">
    <strong>Healthcare Clinical & Operational Analytics Dashboard</strong> | 
    Created & Maintained by <strong>Divya Bansal</strong> | 
    Built with Python, Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
