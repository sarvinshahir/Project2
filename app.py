import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Apply Seaborn theme
sns.set_theme(style="whitegrid")

# Load the dataset
data = pd.read_csv("new_df.csv")  # Update with your dataset file path

# Title and Description
st.title("Employee Well-being and Workplace Insights Dashboard")
st.markdown("""
This **interactive dashboard** provides an in-depth look at employee well-being, workplace trends, and productivity factors. 
Explore insights across regions, job roles, work locations, and more using the filters in the sidebar.
""")


# Dataset Description
st.markdown("""
### 📄 Dataset Description
The dataset used in this dashboard contains information about employees' experiences with remote work, 
their mental health, work-life balance, and related factors. It includes data on:
- **Demographics** (e.g., age, gender, region)
- **Job-related factors** (e.g., job role, work location, years of experience)
- **Health factors** (e.g., stress level, mental health condition, sleep quality)
- **Work-related outcomes** (e.g., productivity change, work-life balance rating)

The dataset aims to provide insights into how remote work impacts various aspects of employees' professional and personal lives.
""")

# Variable Descriptions
st.markdown("""
### 🔍 Variable Descriptions
Here’s a brief overview of the key variables used in the dashboard:
- **Region:** Geographic location of the employee (e.g., North America, Asia).
- **Work Location:** Current work setup (e.g., Remote, Hybrid, Onsite).
- **Job Role:** The role or position held by the employee (e.g., Data Scientist, HR, Software Engineer).
- **Gender:** Gender of the employee (e.g., Male, Female, Non-binary).
- **Age:** Age of the employee.
- **Stress Level:** Self-reported stress level (Low, Medium, High).
- **Mental Health Condition:** Reported mental health issues (e.g., Depression, Anxiety, Burnout).
- **Sleep Quality:** Self-assessed sleep quality (Good, Average, Poor).
- **Work-Life Balance Rating:** Rating of work-life balance on a numerical scale.
- **Hours Worked Per Week:** Average hours worked by the employee per week.
- **Years of Experience:** Total professional experience of the employee in years.
""")

# Sidebar for filtering
st.sidebar.header("🎚️ Filter Options")

# Add "All" to Region options
region_options = ["All"] + list(data['Region'].unique())
selected_region = st.sidebar.selectbox("🌍 Select Region", region_options, index=0)

# Add "All" to Work Location options
work_location_options = ["All"] + list(data['Work_Location'].unique())
selected_work_location = st.sidebar.radio("🏢 Select Work Location", work_location_options, index=0)

# Add "All" to Gender options
gender_options = ["All"] + list(data['Gender'].unique())
selected_gender = st.sidebar.radio("🚻 Select Gender", gender_options, index=0)

selected_age_range = st.sidebar.slider("👩‍💼 Select Age Range", 
                                        int(data['Age'].min()), 
                                        int(data['Age'].max()), 
                                        (20, 50))

# Modify filtering logic for Region, Work Location, and Gender
filtered_data = data[data['Age'].between(selected_age_range[0], selected_age_range[1])]

if selected_region != "All":
    filtered_data = filtered_data[filtered_data['Region'] == selected_region]

if selected_work_location != "All":
    filtered_data = filtered_data[filtered_data['Work_Location'] == selected_work_location]

if selected_gender != "All":
    filtered_data = filtered_data[filtered_data['Gender'] == selected_gender]

# Show filtered data
st.markdown(f"### 📋 Filtered Data: **{len(filtered_data)} Employees**")
st.dataframe(filtered_data)

# Visualization 1: Horizontal Bar Chart - Job Role Distribution
st.markdown("### 📊 Job Role Distribution")
job_role_counts = filtered_data['Job_Role'].value_counts()
fig1, ax1 = plt.subplots()
ax1.barh(job_role_counts.index, job_role_counts.values, color="skyblue")
ax1.set_title("Job Role Distribution", fontsize=16, fontweight="bold")
ax1.set_xlabel("Number of Employees", fontsize=12)
ax1.set_ylabel("Job Role", fontsize=12)
ax1.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig1)

# Visualization 2: Heatmap - Work Location vs. Job Role
st.markdown("### 🌡️ Work Location vs. Job Role (Heatmap)")
pivot_data = filtered_data.pivot_table(index='Job_Role', columns='Work_Location', aggfunc='size', fill_value=0)
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.heatmap(pivot_data, annot=True, fmt="d", cmap="coolwarm", ax=ax2, cbar_kws={'label': 'Number of Employees'})
ax2.set_title("Work Location by Job Role", fontsize=16, fontweight="bold")
ax2.set_xlabel("Work Location", fontsize=12)
ax2.set_ylabel("Job Role", fontsize=12)
st.pyplot(fig2)

# Visualization 3: Histogram with KDE - Hours Worked Per Week
st.markdown("### ⏱️ Distribution of Hours Worked Per Week")
fig3, ax3 = plt.subplots()
sns.histplot(data=filtered_data, x='Hours_Worked_Per_Week', kde=True, bins=20, ax=ax3, color='purple')
ax3.set_title("Hours Worked Per Week", fontsize=16, fontweight="bold")
ax3.set_xlabel("Hours", fontsize=12)
ax3.set_ylabel("Frequency", fontsize=12)
st.pyplot(fig3)

# Visualization 4: Boxplot - Work Life Balance Rating by Region
st.markdown("### 📦 Work Life Balance Rating by Region")
fig4, ax4 = plt.subplots()
sns.boxplot(data=filtered_data, x='Region', y='Work_Life_Balance_Rating', palette="Set2", ax=ax4)
ax4.set_title("Work Life Balance Rating by Region", fontsize=16, fontweight="bold")
ax4.set_xlabel("Region", fontsize=12)
ax4.set_ylabel("Work Life Balance Rating", fontsize=12)
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha='right')  # Rotate x-axis labels
st.pyplot(fig4)

# Visualization 5: Pie Chart - Mental Health Conditions
st.markdown("### 🧠 Distribution of Mental Health Conditions")
mental_health_counts = filtered_data['Mental_Health_Condition'].value_counts()
fig5, ax5 = plt.subplots()
ax5.pie(mental_health_counts, labels=mental_health_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
ax5.set_title("Distribution of Mental Health Conditions", fontsize=16, fontweight="bold")
st.pyplot(fig5)

# Visualization 6: Bar Chart - Stress Level by Job Role
st.markdown("### 😟 Stress Level by Job Role")
stress_job_data = (
    filtered_data.groupby(['Job_Role', 'Stress_Level'])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=["Low", "Medium", "High"])  # Reorder columns
)

# Define custom colors for Low, Medium, High
custom_colors = ["green", "yellow", "red"]

fig6, ax6 = plt.subplots(figsize=(10, 6))
bars = stress_job_data.plot(kind='bar', stacked=True, ax=ax6, color=custom_colors)
ax6.set_title("Stress Level by Job Role", fontsize=16, fontweight="bold")
ax6.set_xlabel("Job Role", fontsize=12)
ax6.set_ylabel("Number of Employees", fontsize=12)
ax6.legend(title="Stress Level", loc='upper right')

# Add annotations
for container in bars.containers:
    ax6.bar_label(container, label_type='center', fmt='%d', fontsize=10, color='black')

st.pyplot(fig6)


# Visualization 7: Stacked Bar Chart - Sleep Quality by Work Location
st.markdown("### 🛌 Sleep Quality by Work Location")
sleep_work_data = (
    filtered_data.groupby(['Work_Location', 'Sleep_Quality'])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=["Poor", "Average", "Good"])  # Reorder columns
)
fig7, ax7 = plt.subplots(figsize=(10, 6))
bars = sleep_work_data.plot(kind='bar', stacked=True, ax=ax7, color=sns.color_palette("viridis"))
ax7.set_title("Sleep Quality by Work Location", fontsize=16, fontweight="bold")
ax7.set_xlabel("Work Location", fontsize=12)
ax7.set_ylabel("Number of Employees", fontsize=12)
ax7.legend(title="Sleep Quality", loc='upper right')

# Add annotations
for container in bars.containers:
    ax7.bar_label(container, label_type='center', fmt='%d', fontsize=10, color='white')

st.pyplot(fig7)


# Insights Section
st.markdown("""
### 📊 Insights from the Dashboard

1. **Job Role Distribution Across Regions and Genders:**
   - Globally, **Project Managers** represent the highest number of employees in the dataset across all genders aged 20 to 60.
   - Regional trends:
     - **Europe:** HR professionals dominate.
     - **Asia:** Data Scientists are the most prevalent.
     - **North America:** HR professionals are the highest.
     - **Africa:** Project Managers lead in numbers.
     - **Oceania & South America:** Designers are the most common role.
   - Gender-specific trends:
     - Among females worldwide, **Data Scientist** is the most common job role.
     - Among males, **Project Manager** leads globally.

2. **Work Location and Job Role:**
   - **Hybrid workers** are predominantly **Project Managers.**
   - **Onsite workers** are mostly **Software Engineers.**
   - **Remote workers** are primarily **Data Scientists.**

3. **Distribution of Hours Worked Per Week:**
   - **Males:** Higher frequency of working **above 40 hours per week.**
   - **Females:** Tend to work **less than 40 hours per week**, showing a higher frequency in this range.
   - **Non-binary:** Hours worked are more evenly distributed, with no strong concentration in any range.

4. **Work-Life Balance Trends:**
   - **Females in North America** report the **highest work-life balance.**
   - **Males in Africa** report the **lowest work-life balance.**
   - Across all genders, work-life balance is **very low** for employees working **hybrid setups** in **South America** and **Africa.**

5. **Mental Health Insights:**
   - **Anxiety** is consistently high in proportion across different genders, regions, and work locations, suggesting it’s a widespread mental health challenge.

6. **Stress Levels by Job Role:**
   - Employees in **Designer** roles report **lower stress levels.**
   - **Project Managers** experience **higher stress levels**, with significant proportions reporting high stress.

7. **Sleep Quality Insights:**
   - Employees working **remotely** report **better sleep quality** compared to those in hybrid setups.
   - **Hybrid workers** report poorer sleep quality overall.
   - Gender-specific trends:
     - **Females** report better sleep quality compared to males.

---

### Key Takeaways
These insights emphasize:
1. The importance of regional and gender-specific interventions to improve job satisfaction and work-life balance.
2. The need for targeted support in roles with high stress levels, such as Project Managers.
3. A focus on promoting flexible work arrangements, like remote setups, to enhance sleep quality and reduce stress.
""")



# Footer
st.markdown("---")
st.markdown("""
### 🌟 Thank You for Exploring the Dashboard!
This dashboard was developed to provide actionable insights into the impact of remote work on mental health. 

#### 📬 Feedback
We value your feedback! If you have suggestions or comments, feel free to reach out.

#### 📊 Dashboard Highlights
- Interactive filters for tailored insights.
- Data-driven visualizations for better understanding.
- Focused on improving workplace wellness and productivity.

---

**Developed by Sarvin Shahir**  
📧 Contact: alizadshahir.s@northeastern.edu  
📍 Location: Vancouver, BC
""")




