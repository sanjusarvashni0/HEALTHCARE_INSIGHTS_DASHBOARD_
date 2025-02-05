import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Database Connection
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/healthcare_data')

# Navigation
option = st.sidebar.radio('Select one', ['Home', 'Business cases'])

#Homepage
if option == 'Home':
    st.title("HEALTHCARE DATA ANALYSIS")
    st.write(
        'In modern healthcare, data is critical for improving patient care and operational efficiency. However, analyzing large volumes of patient and treatment data remains challenging. This project aims to build an interactive analytics dashboard using Python, SQL, and Streamlit, providing insights into patient demographics, treatment patterns, and facility utilization.')
    
    st.markdown('''
    **Patient Demographics Analysis**:  
    - Analyze the distribution of patients by age, gender, and location.  
    - Identify trends and patterns in patient demographics.

    **Treatment and Service Trends**:  
    - Understand the frequency and popularity of treatments or procedures.  
    - Identify peak times for patient visits to optimize resource allocation.

   **Healthcare Facility Utilization**:  
   - Measure admission and discharge trends over time.  
   - Monitor facility usage to prevent overcrowding and ensure efficient operations.

   **Data-Driven Decision Making**:  
   - Support hospital administrators in planning based on patient trends and service usage.  
   - Provide actionable insights to improve healthcare delivery.
   ''')


#business cases    
elif option == 'Business cases':
    query_dict = {
        "Trends in Admission Over Time": "SELECT DATE_FORMAT(Admit_Date, '%Y-%m') AS Month, COUNT(*) AS Total_Admissions FROM patients_data GROUP BY Month ORDER BY Month;",
        "Diagnosis Frequency Analysis": "SELECT Diagnosis, COUNT(*) AS Diagnosis_Count FROM patients_data GROUP BY Diagnosis ORDER BY Diagnosis_Count DESC LIMIT 5;",
        "Bed Occupancy Analysis": "SELECT Bed_Occupancy, COUNT(*) AS Total_Admissions FROM patients_data GROUP BY Bed_Occupancy ORDER BY Total_Admissions DESC;",
        "Length of Stay Distribution": "SELECT DATEDIFF(Discharge_Date, Admit_Date) AS Length_Of_Stay FROM patients_data;",
        "Seasonal Admission Patterns": "SELECT MONTH(Admit_Date) AS Month, COUNT(*) AS Total_Admissions FROM patients_data GROUP BY Month ORDER BY Total_Admissions DESC;",
        "Doctor Workload Analysis": "SELECT Doctor, COUNT(*) AS Total_Patients FROM patients_data GROUP BY Doctor ORDER BY Total_Patients DESC;",
        "Revenue Analysis": "SELECT SUM(`Billing Amount`) AS Total_Revenue, SUM(`Health Insurance Amount`) AS Total_Insurance_Covered, SUM(`Billing Amount` - `Health Insurance Amount`) AS Out_Of_Pocket_Payments FROM patients_data;",
        "Most Expensive Diagnoses": "SELECT Diagnosis, AVG(`Billing Amount`) AS Avg_Billing_Amount FROM patients_data GROUP BY Diagnosis ORDER BY Avg_Billing_Amount DESC LIMIT 5;",
        "Most Common Tests Ordered": "SELECT Test, COUNT(*) AS Test_Count FROM patients_data GROUP BY Test ORDER BY Test_Count DESC LIMIT 5;",
        "Follow-up Rate by Diagnosis": "SELECT Diagnosis, COUNT(`Followup Date`) AS Total_Followups, COUNT(*) AS Total_Cases, (COUNT(`Followup Date`) / COUNT(*)) * 100 AS Followup_Rate FROM patients_data GROUP BY Diagnosis ORDER BY Followup_Rate DESC;",
        "Insurance Coverage Analysis": "SELECT (SUM(`Health Insurance Amount`) / SUM(`Billing Amount`)) * 100 AS Insurance_Coverage_Percentage FROM patients_data;",
        "Fastest Discharges (Shortest Stay)": "SELECT Diagnosis, MIN(DATEDIFF(Discharge_Date, Admit_Date)) AS Min_Stay FROM patients_data GROUP BY Diagnosis ORDER BY Min_Stay ASC LIMIT 5;",
        "Patient Satisfaction Analysis": "SELECT Doctor, AVG(Feedback) AS Avg_Feedback FROM patients_data GROUP BY Doctor ORDER BY Avg_Feedback DESC;",
        "Readmission Analysis": "SELECT COUNT(DISTINCT Patient_ID) AS Total_Patients, COUNT(*) AS Total_Admissions, (COUNT(*) - COUNT(DISTINCT Patient_ID)) AS Readmissions FROM patients_data;",
        "High-Risk Patients (Long Stays & High Bills)": "SELECT Patient_ID, Diagnosis, DATEDIFF(Discharge_Date, Admit_Date) AS Length_Of_Stay, `Billing Amount` FROM patients_data WHERE DATEDIFF(Discharge_Date, Admit_Date) > (SELECT AVG(DATEDIFF(Discharge_Date, Admit_Date)) FROM patients_data) AND `Billing Amount` > (SELECT AVG(`Billing Amount`) FROM patients_data) ORDER BY `Billing Amount` DESC;"
    }
    
    query = st.sidebar.selectbox("Select a business case", list(query_dict.keys()))
    df = pd.read_sql(query_dict[query], con=engine)
    st.title(query)

    # Display DataFrame at the top
    st.write("### Data Table")
    st.dataframe(df)
    
    # Visualization below the DataFrame
    st.write("### Visualization")
    fig, ax = plt.subplots(figsize=(12, 8))  # Increased figure size for better fit
    
    # Visualization of business cases
    if query == "Trends in Admission Over Time":
        sns.lineplot(x='Month', y='Total_Admissions', data=df, marker='o', ax=ax)
        ax.set_title("Trends in Admission Over Time", fontsize=16)
        ax.set_xlabel("Month", fontsize=14)
        ax.set_ylabel("Total Admissions", fontsize=14)
    
    elif query == "Diagnosis Frequency Analysis":
        sns.barplot(x='Diagnosis', y='Diagnosis_Count', data=df, ax=ax)
        ax.set_title("Top 5 Diagnoses")
    
    elif query == "Bed Occupancy Analysis":
        df.set_index("Bed_Occupancy").plot.pie(y="Total_Admissions", autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        ax.set_title("Bed Occupancy Distribution")
    
    elif query == "Length of Stay Distribution":
        sns.boxplot(y=df["Length_Of_Stay"], ax=ax)
        ax.set_title("Length of Stay Distribution")
    
    elif query == "Seasonal Admission Patterns":
        sns.barplot(x='Month', y='Total_Admissions', data=df, ax=ax)
        ax.set_title("Monthly Admission Patterns")
    
    elif query == "Doctor Workload Analysis":
        sns.barplot(x='Doctor', y='Total_Patients', data=df, ax=ax)
        ax.set_title("Doctor Workload Analysis")
    
    elif query == "Revenue Analysis":
        df_series = df.iloc[0]  # Extract first row as a Series
        df_series.plot.pie(autopct='%1.1f%%', labels=['Total Revenue', 'Insurance Covered', 'Out of Pocket Payments'], ax=ax)
        ax.set_ylabel('')
        ax.set_title("Revenue Breakdown")
    
    elif query == "Most Expensive Diagnoses":
        sns.barplot(x='Diagnosis', y='Avg_Billing_Amount', data=df, ax=ax)
        ax.set_title("Most Expensive Diagnoses")
    
    elif query == "Most Common Tests Ordered":
        sns.barplot(x='Test', y='Test_Count', data=df, ax=ax)
        ax.set_title("Most Common Tests Ordered")
    
    elif query == "Follow-up Rate by Diagnosis":
        sns.barplot(x='Diagnosis', y='Followup_Rate', data=df, ax=ax)
        ax.set_title("Follow-up Rate by Diagnosis")
    
    elif query == "Insurance Coverage Analysis":
        df.plot.pie(y='Insurance_Coverage_Percentage', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        ax.set_title("Insurance Coverage Analysis")
    
    elif query == "Fastest Discharges (Shortest Stay)":
        sns.barplot(x='Diagnosis', y='Min_Stay', data=df, ax=ax)
        ax.set_title("Fastest Discharges")
    
    elif query == "Patient Satisfaction Analysis":
        sns.barplot(x='Doctor', y='Avg_Feedback', data=df, ax=ax)
        ax.set_title("Patient Satisfaction Analysis")
    
    elif query == "Readmission Analysis":
        sns.barplot(x=['Total_Patients', 'Readmissions'], y=[df['Total_Patients'][0], df['Readmissions'][0]], ax=ax)
        ax.set_title("Readmission Analysis")
    
    elif query == "High-Risk Patients (Long Stays & High Bills)":
        sns.scatterplot(x='Length_Of_Stay', y='Billing Amount', data=df, ax=ax)
        ax.set_title("High-Risk Patients Analysis")
    
    st.pyplot(fig)

st.sidebar.info('Select a business case to view insights')
