"""
Healthcare Data Generation Engine
Author: Divya Bansal
Description: Generates clinically coherent synthetic patient records and aggregated 
monthly operational metrics for healthcare data analytics.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_hospital_data(n_patients=1200, seed=42):
    """
    Generates realistic patient admission records with clinical relationships
    between demographics, chronic conditions, length of stay, and hospital charges.
    """
    np.random.seed(seed)
    
    disease_dept_map = {
        'Heart Disease': 'Cardiology',
        'Hypertension': 'Cardiology',
        'Stroke': 'Neurology',
        'Cancer': 'Oncology',
        'Asthma': 'Pulmonology',
        'COPD': 'Pulmonology',
        'Kidney Disease': 'Nephrology',
        'Arthritis': 'Orthopedics',
        'Diabetes': 'General',
        'Obesity': 'General'
    }
    
    diseases = list(disease_dept_map.keys())
    disease_weights = [0.14, 0.16, 0.08, 0.10, 0.09, 0.09, 0.07, 0.09, 0.12, 0.06]
    
    age_groups = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    age_weights = [0.08, 0.14, 0.18, 0.24, 0.22, 0.14]
    
    risk_factors = ['Smoking', 'Obesity', 'Sedentary Lifestyle', 'Poor Diet', 
                    'Alcohol', 'Stress', 'Genetics', 'None']
    risk_weights = [0.18, 0.15, 0.16, 0.14, 0.10, 0.11, 0.08, 0.08]
    
    insurance_types = ['Medicare', 'Private', 'Medicaid', 'Self-Pay']
    admission_types = ['Emergency', 'Elective', 'Urgent']
    
    # 1. Base demographics & conditions
    selected_diseases = np.random.choice(diseases, n_patients, p=disease_weights)
    selected_depts = [disease_dept_map[d] for d in selected_diseases]
    selected_age_groups = np.random.choice(age_groups, n_patients, p=age_weights)
    genders = np.random.choice(['Male', 'Female'], n_patients, p=[0.49, 0.51])
    selected_risks = np.random.choice(risk_factors, n_patients, p=risk_weights)
    
    # Age group to numeric proxy for statistical correlation
    age_proxy_map = {
        '18-25': 22, '26-35': 30, '36-45': 40, 
        '46-55': 50, '56-65': 60, '65+': 72
    }
    approx_ages = np.array([age_proxy_map[ag] + np.random.randint(-3, 4) for ag in selected_age_groups])
    
    # Insurance type probability depends on age
    insurances = []
    for ag in selected_age_groups:
        if ag == '65+':
            ins = np.random.choice(insurance_types, p=[0.72, 0.18, 0.08, 0.02])
        elif ag in ['18-25', '26-35']:
            ins = np.random.choice(insurance_types, p=[0.02, 0.60, 0.28, 0.10])
        else:
            ins = np.random.choice(insurance_types, p=[0.10, 0.65, 0.18, 0.07])
        insurances.append(ins)
        
    admission_choices = np.random.choice(admission_types, n_patients, p=[0.48, 0.32, 0.20])
    
    # Admission dates spread across 2024
    base_date = datetime(2024, 1, 1)
    admission_dates = [(base_date + timedelta(days=int(d))).strftime('%Y-%m-%d') 
                       for d in np.random.uniform(0, 365, n_patients)]
    
    # 2. Clinically coherent Length of Stay (LOS)
    los_base_map = {
        'Cancer': 7.8, 'Stroke': 8.2, 'Heart Disease': 6.5,
        'Kidney Disease': 5.8, 'COPD': 5.2, 'Diabetes': 4.1,
        'Hypertension': 3.4, 'Arthritis': 3.6, 'Asthma': 3.0, 'Obesity': 3.5
    }
    
    lengths_of_stay = []
    for d, ag, adm in zip(selected_diseases, selected_age_groups, admission_choices):
        mean_stay = los_base_map[d]
        if ag in ['56-65', '65+']:
            mean_stay += 1.2
        if adm == 'Emergency':
            mean_stay += 0.8
        stay = max(1, int(np.random.exponential(mean_stay)))
        lengths_of_stay.append(stay)
    lengths_of_stay = np.array(lengths_of_stay)
    
    # 3. Clinically coherent Financial Charges
    procedure_surcharge_map = {
        'Cancer': 16000, 'Stroke': 14000, 'Heart Disease': 12000,
        'Kidney Disease': 8500, 'Arthritis': 5500, 'COPD': 4500,
        'Diabetes': 3500, 'Hypertension': 2800, 'Asthma': 2200, 'Obesity': 2500
    }
    
    total_charges = []
    for d, stay, adm in zip(selected_diseases, lengths_of_stay, admission_choices):
        daily_room_rate = 1200 + np.random.normal(0, 100)
        surcharge = procedure_surcharge_map[d]
        if adm == 'Emergency':
            surcharge += 2500
        noise = np.random.normal(0, 1200)
        cost = max(950.0, (stay * daily_room_rate) + surcharge + noise)
        total_charges.append(round(cost, 2))
    total_charges = np.array(total_charges)
    daily_cost = np.round(total_charges / lengths_of_stay, 2)
    
    # 4. Realistic 30-day Readmission probability
    readmissions = []
    for d, ag, rf, stay in zip(selected_diseases, selected_age_groups, selected_risks, lengths_of_stay):
        prob = 0.08  # Baseline probability
        if d in ['Heart Disease', 'Stroke', 'Kidney Disease', 'COPD']:
            prob += 0.08
        if ag in ['56-65', '65+']:
            prob += 0.06
        if rf in ['Smoking', 'Obesity', 'Sedentary Lifestyle']:
            prob += 0.04
        if stay > 7:
            prob += 0.05
        prob = min(prob, 0.45)
        readmitted = 1 if np.random.rand() < prob else 0
        readmissions.append(readmitted)
        
    # 5. Satisfaction score (1 to 5)
    satisfactions = []
    for stay, readm in zip(lengths_of_stay, readmissions):
        base_sat = 4.2
        if stay > 10:
            base_sat -= 0.8
        if readm == 1:
            base_sat -= 0.7
        score = int(np.clip(np.random.normal(base_sat, 0.9), 1, 5))
        satisfactions.append(score)
        
    data = {
        'patient_id': range(1001, 1001 + n_patients),
        'age': approx_ages,
        'age_group': selected_age_groups,
        'gender': genders,
        'disease': selected_diseases,
        'department': selected_depts,
        'risk_factor': selected_risks,
        'admission_type': admission_choices,
        'insurance_type': insurances,
        'admission_date': admission_dates,
        'length_of_stay': lengths_of_stay,
        'total_charges': total_charges,
        'daily_cost': daily_cost,
        'readmitted': readmissions,
        'satisfaction_score': satisfactions
    }
    
    return pd.DataFrame(data).sort_values('admission_date').reset_index(drop=True)

def generate_monthly_trends(patient_df=None):
    """
    Computes monthly operational metrics directly aggregated from patient records,
    ensuring statistical consistency across the analytics pipeline.
    """
    if patient_df is None or len(patient_df) == 0:
        patient_df = generate_hospital_data()
        
    df = patient_df.copy()
    df['month'] = pd.to_datetime(df['admission_date']).dt.strftime('%Y-%m')
    
    monthly_summary = df.groupby('month').agg(
        admissions=('patient_id', 'count'),
        average_stay=('length_of_stay', 'mean'),
        readmission_rate=('readmitted', 'mean'),
        total_charges=('total_charges', 'sum')
    ).reset_index()
    
    monthly_summary['average_stay'] = monthly_summary['average_stay'].round(1)
    monthly_summary['readmission_rate'] = monthly_summary['readmission_rate'].round(3)
    monthly_summary['total_charges'] = monthly_summary['total_charges'].round(2)
    
    return monthly_summary

if __name__ == '__main__':
    print("Generating comprehensive healthcare dataset by Divya Bansal...")
    patients = generate_hospital_data(n_patients=1200)
    monthly = generate_monthly_trends(patients)
    
    patients.to_csv('patient_data.csv', index=False)
    monthly.to_csv('monthly_trends.csv', index=False)
    
    print("Dataset generated successfully!")
    print(f"Total Patient Records: {len(patients)}")
    print(f"Monthly Periods Tracked: {len(monthly)}")
    print(f"Average Length of Stay: {patients['length_of_stay'].mean():.2f} days")
    print(f"Readmission Rate: {patients['readmitted'].mean()*100:.2f}%")
    print(f"Average Hospital Charge: ${patients['total_charges'].mean():,.2f}")
