"""
Healthcare Dashboard Screenshot & Asset Generator
Author: Divya Bansal
Description: Generates high-resolution visualization previews for project documentation.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

os.makedirs('screenshots', exist_ok=True)

df = pd.read_csv('patient_data.csv')
monthly = pd.read_csv('monthly_trends.csv')

# 1: Dashboard Overview
readmission_pct = df['readmitted'].mean() * 100
fig = go.Figure()
fig.add_trace(go.Indicator(mode='number', value=len(df), title={'text': 'Total Admissions'}, domain={'x': [0, 0.25], 'y': [0, 1]}))
fig.add_trace(go.Indicator(mode='number', value=round(df['length_of_stay'].mean(), 1), title={'text': 'Avg Stay (days)'}, domain={'x': [0.25, 0.5], 'y': [0, 1]}))
fig.add_trace(go.Indicator(mode='number', value=round(readmission_pct, 1), title={'text': 'Readmission %'}, domain={'x': [0.5, 0.75], 'y': [0, 1]}))
fig.add_trace(go.Indicator(mode='number', value=round(df['satisfaction_score'].mean(), 1), title={'text': 'Avg Satisfaction'}, domain={'x': [0.75, 1], 'y': [0, 1]}))
fig.update_layout(title='Healthcare Analytics Dashboard - Key Metrics | Divya Bansal', height=300, template='plotly_dark')
try:
    fig.write_image('screenshots/01_dashboard_overview.png', width=1200, height=300)
    print('Screenshot 1 done')
except Exception as e:
    print(f"Screenshot 1 export skipped (requires kaleido): {e}")

# 2: Disease Prevalence
disease_counts = df['disease'].value_counts()
fig2 = px.bar(x=disease_counts.index, y=disease_counts.values, title='Disease Prevalence by Patient Volume', labels={'x': 'Clinical Condition', 'y': 'Patient Count'}, color=disease_counts.values, color_continuous_scale='viridis')
fig2.update_layout(template='plotly_dark', height=500)
try:
    fig2.write_image('screenshots/02_disease_prevalence.png', width=1200, height=500)
    print('Screenshot 2 done')
except Exception as e:
    print(f"Screenshot 2 export skipped: {e}")

# 3: Age Group Analysis
age_counts = df['age_group'].value_counts().sort_index()
age_stay = df.groupby('age_group')['length_of_stay'].mean()
fig3 = make_subplots(rows=1, cols=2, subplot_titles=('Patient Distribution by Age Cohort', 'Avg Hospital Stay by Age (Days)'))
fig3.add_trace(go.Bar(x=age_counts.index, y=age_counts.values, name='Patients', marker_color='#58a6ff'), row=1, col=1)
fig3.add_trace(go.Bar(x=age_stay.index, y=age_stay.values, name='Avg Stay', marker_color='#f97316'), row=1, col=2)
fig3.update_layout(title='Demographic & Length of Stay Analysis', template='plotly_dark', height=400, showlegend=False)
try:
    fig3.write_image('screenshots/03_age_group_analysis.png', width=1200, height=400)
    print('Screenshot 3 done')
except Exception as e:
    print(f"Screenshot 3 export skipped: {e}")

# 4: Risk Factor Donut
risk_counts = df['risk_factor'].value_counts()
fig4 = px.pie(values=risk_counts.values, names=risk_counts.index, title='Risk Factor Distribution', hole=0.4)
fig4.update_layout(template='plotly_dark', height=500)
try:
    fig4.write_image('screenshots/04_risk_factors.png', width=1200, height=500)
    print('Screenshot 4 done')
except Exception as e:
    print(f"Screenshot 4 export skipped: {e}")

# 5: Correlation Heatmap (Plotly)
corr_cols = ['age', 'length_of_stay', 'total_charges', 'daily_cost', 'readmitted', 'satisfaction_score']
corr = df[corr_cols].corr()
fig5 = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title='Clinical & Financial Correlation Heatmap - Divya Bansal')
fig5.update_layout(template='plotly_dark', height=500)
try:
    fig5.write_image('screenshots/05_correlation_heatmap.png', width=1200, height=500)
    print('Screenshot 5 done')
except Exception as e:
    print(f"Screenshot 5 export skipped: {e}")

print('All screenshot tasks completed!')
