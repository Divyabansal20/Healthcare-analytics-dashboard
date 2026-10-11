# Healthcare Clinical and Operational Analytics Dashboard

An enterprise-grade hospital intelligence and clinical data analytics application built with Python, Streamlit, Pandas, and Plotly. Designed to evaluate inpatient capacity, track clinical quality benchmarks, identify financial cost drivers, and simulate 30-day patient readmission risk.

---

## Executive Summary

Hospital administrators, clinical department chairs, and healthcare operations directors face significant pressure to balance patient care quality with operational efficiency and financial sustainability. Key challenges include:

- Inefficient inpatient bed utilization and extended length of stay (LOS).
- Unfavorable 30-day patient readmission rates leading to Centers for Medicare & Medicaid Services (CMS) quality penalties.
- High-cost variance across clinical departments and lack of visibility into daily cost drivers.
- Absence of real-time clinical decision support tools to stratify patient risk before hospital discharge.

This project delivers an interactive, centralized business intelligence platform that synthesizes 1,200 multi-variable inpatient admission records across 10 major disease classifications and 7 specialized hospital departments. It translates raw operational and clinical datasets into quantifiable metrics and actionable strategies.

---

## Core Analytical Modules

The dashboard is structured into five focused analytical modules:

### 1. Executive KPI and Operational Overview
- **Clinical Benchmarking:** Real-time tracking of Total Inpatient Admissions, Average Length of Stay (monitored against an operational target of 4.5 days), 30-Day Readmission Rate (evaluated against the national 12.0% quality threshold), Total Billed Expenditure, and Average Daily Cost per Patient.
- **Dynamic Executive Takeaways:** Automated insight synthesis engine that computes predominant conditions, primary departmental cost drivers, and quality threshold alerts for any filtered cohort.
- **Longitudinal Trend Tracking:** Dynamically aggregated monthly trends tracking admission volume, length of stay, readmission rate, and billed revenue over time.

### 2. Clinical Epidemiology and Cohort Profiling
- **Disease Prevalence Mapping:** Comparative distribution of admissions across 10 critical conditions (Heart Disease, Hypertension, Stroke, Cancer, Asthma, COPD, Kidney Disease, Arthritis, Diabetes, and Obesity).
- **Outlier Stay Detection:** Boxplot distributions highlighting condition-level median stay, interquartile ranges, and extreme length-of-stay outliers for capacity planning.
- **Demographic and Risk Factor Matrices:** Cross-tabulation heatmaps exploring condition prevalence across age cohorts (18-25 through 65+) and primary lifestyle risk factors.

### 3. Financial Performance and Departmental Utilization
- **Revenue Allocation:** Comparative billing breakdown across 7 departments (Cardiology, Neurology, Oncology, Pulmonology, Nephrology, Orthopedics, General).
- **Regression Analysis:** Scatter plot evaluating the empirical relationship between Length of Stay and Total Billed Charges, featuring Ordinary Least Squares (OLS) regression lines and bubble sizing weighted by daily inpatient cost.
- **Payer Mix Breakdown:** Revenue and patient volume distributions across payer types (Medicare, Medicaid, Private Insurance, Self-Pay).
- **Statistical Correlation Matrix:** Pearson correlation coefficients computed across continuous numerical metrics (Age, Length of Stay, Total Charges, Daily Cost, Readmission, and Satisfaction Score).

### 4. Predictive 30-Day Readmission Risk Simulator
- **Interactive Risk Calculation Engine:** Allows healthcare providers to input individual patient parameters (Age, Primary Condition, Admission Type, Length of Stay, and Comorbid Risk Factors) to compute estimated readmission probability using an empirical multi-factor risk model.
- **Visual Risk Stratification:** Plotly gauge indicator categorizing patient profiles into Low Risk (under 15%), Moderate Risk (15% to 28%), and High Risk (over 28%).
- **Targeted Clinical Interventions:** Automated care management recommendations corresponding to predicted risk tiers (such as 48-hour telehealth check-ins, pharmacist medication reconciliation, or home health referrals).

### 5. Patient Registry Explorer and Data Extraction
- **Searchable Patient Registry:** Dynamic text search filtering by Patient ID, Disease, or Department.
- **Custom View Configuration:** Interactive column selector and descriptive summary statistics generator (mean, median, standard deviation, interquartile ranges).
- **One-Click Data Export:** Direct CSV export functionality for reporting and downstream analyses.

---

## Data Schema and Feature Dictionary

The underlying dataset comprises 1,200 patient records structured across 15 clinical and administrative features:

| Column Name | Data Type | Description | Values / Range |
| :--- | :--- | :--- | :--- |
| `patient_id` | Integer | Unique identifier assigned to each inpatient record | 1001 to 2200 |
| `age` | Integer | Patient age in years | 18 to 95 |
| `age_group` | Categorical | Demographic bracket | 18-25, 26-35, 36-45, 46-55, 56-65, 65+ |
| `gender` | Categorical | Patient gender | Male, Female |
| `disease` | Categorical | Primary diagnosis | 10 clinical conditions |
| `department` | Categorical | Treating hospital department | 7 specialized departments |
| `risk_factor` | Categorical | Primary identified lifestyle or clinical risk | Smoking, Obesity, Alcohol, Sedentary, etc. |
| `admission_type` | Categorical | Inpatient admission category | Emergency, Elective, Urgent |
| `insurance_type` | Categorical | Primary insurance carrier classification | Medicare, Private, Medicaid, Self-Pay |
| `admission_date` | Date | Date of hospital admission | Calendar year 2024 |
| `length_of_stay` | Integer | Total duration of inpatient hospitalization | 1 to 30 days |
| `total_charges` | Float | Total billed cost in USD | Scaled by stay duration and diagnosis |
| `daily_cost` | Float | Effective cost per inpatient day in USD | Calculated as Total Charges / Length of Stay |
| `readmitted` | Binary | 30-Day readmission flag | 0 = No, 1 = Yes |
| `satisfaction_score` | Integer | Post-discharge patient satisfaction score | 1 (Lowest) to 5 (Highest) |

---

## Resume Highlights and Professional Talking Points

For data analyst and business intelligence roles, this project exemplifies the following competencies:

- **End-to-End Data Pipeline Architecture:** Developed an interactive analytics platform in Python (Streamlit, Plotly, Pandas) analyzing 1,200 multi-variable patient records across 10 disease categories and 7 hospital departments.
- **Operational and Quality KPI Tracking:** Designed executive metric cards with benchmark comparisons (Length of Stay against a 4.5-day target; Readmission against a 12.0% national threshold) and dynamic natural-language executive takeaways.
- **Predictive Risk Stratification:** Engineered an empirical 30-day readmission risk simulator featuring multi-factor scoring algorithms and visual gauge indicators to support proactive discharge planning.
- **Statistical and Financial Regression:** Executed Ordinary Least Squares (OLS) trendline analysis and Pearson correlation matrices to identify departmental cost variances and inpatient stay outliers.
- **Production-Ready Web Deployment:** Configured modular application architecture, optimized caching with Streamlit cache decorators, and implemented robust empty-state error handling.

---

## Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Programming Language** | Python 3.9+ | Data manipulation, statistical computations, and logic |
| **Web Application Framework** | Streamlit 1.32+ | Interactive front-end layout, filters, and state management |
| **Data Processing & Analytics** | Pandas 2.0+, NumPy 1.24+ | Data ingestion, cohort filtering, aggregation, and matrices |
| **Interactive Visualization** | Plotly 5.18+ (Express & Graph Objects) | Responsive charts, heatmaps, boxplots, and gauge indicators |
| **Statistical Modeling** | Statsmodels / NumPy Linear Fits | Ordinary Least Squares regression and correlation analysis |
| **Configuration** | TOML | Streamlit runtime configuration and theme tokens |

---

## Project Structure

```
healthcare-dashboard/
├── .streamlit/
│   └── config.toml             # Streamlit server and theme configurations
├── app.py                      # Main Streamlit dashboard application
├── generate_data.py            # Clinical and financial data generation engine
├── requirements.txt            # Python dependencies for local and cloud execution
├── patient_data.csv            # Generated dataset of 1,200 patient records
├── monthly_trends.csv          # Longitudinal monthly operational records
├── take_screenshots.py         # Visual documentation asset generation script
├── screenshots/                # Application preview assets
├── CONTRIBUTING.md             # Contributor guidelines
├── LICENSE                     # MIT License
└── README.md                   # Project documentation
```

---

## Local Setup and Installation

### Prerequisites
- Python 3.9 or higher
- Git version control
- pip package manager

### 1. Clone the Repository
```bash
git clone https://github.com/divyabansal/healthcare-dashboard.git
cd healthcare-dashboard
```

### 2. Create and Activate a Virtual Environment
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Regenerate Synthetic Clinical Data (Optional)
```bash
python generate_data.py
```

### 5. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
The application will launch automatically in your web browser at `http://localhost:8501`.
---

## Author

**Divya Bansal**  
*Healthcare Data Analyst* 
- **Email:** bansaldivya20082005@gmail.com  

---

## License

This project is distributed under the MIT License. Refer to the [LICENSE](LICENSE) file for complete details.  
Copyright (c) 2026 Divya Bansal.
