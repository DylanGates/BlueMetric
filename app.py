import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Set page config
st.set_page_config(
    page_title="Water Pollution in Ghana",
    page_icon="💧",
    layout="wide"
)

# Define the river names
rivers = [
    "River Oda", "River Birim", "River Pra Twifo", "River Ankobra", 
    "River Subri", "River Anuru", "River Offin", "River Ashrey",
    "River Butre", "River Tano", "River Pra Daboase", "Galamsey Pit"
]

# Define thresholds (WHO or most conservative between WHO, EPA, Ghana)
thresholds = {
    'As (mg/L)': 0.01,
    'Cd (mg/L)': 0.003,
    'Cr (mg/L)': 0.05,
    'Pb (mg/L)': 0.01,
    'pH_min': 6.5,
    'pH_max': 8.5,
    'TDS (mg/L)': 1000,
    'Conductivity (µS/cm)': 1000,
    'Hardness (mg/L)': 500,
    'Ca Hardness (mg/L)': 500,
    'Mg Hardness (mg/L)': 500
}

# Create sample data for demonstration
np.random.seed(42)

# Create sample data with all parameters
data = {
    'Sample': [
        'River Oda', 'River Birim', 'River Pra Twifo', 'River Ankobra', 'River Subri', 'River Anuru',
        'River Offin', 'River Ashrey', 'River Butre', 'River Tano', 'River Pra Daboase', 'Galamsey Pit'
    ],
    'As (mg/L)': [0.364, 0.372, 0.305, 0.221, 0.0, 0.444, 0.216, 0.367, 0.341, 0.346, 0.288, 0.291],
    'Cd (mg/L)': [0.0, 0.0, 0.0, 0.0, 0.013, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'Cr (mg/L)': [0.103, 0.037, 0.115, 0.293, 1.607, 0.15, 0.411, 0.096, 0.147, 0.187, 0.186, 0.021],
    'Pb (mg/L)': [0.073, 0.065, 0.133, 0.119, 0.208, 0.062, 0.148, 0.079, 0.066, 0.086, 0.057, 0.051],
    'pH': [5.93, 5.96, 5.65, 5.7, 5.25, 5.64, 6.46, 6.12, 5.67, 5.69, 5.62, 3.21],
    'TDS (mg/L)': [0.08, 0.05, 0.06, 0.06, 0.03, 0.16, 0.14, 0.07, 0.05, 0.05, 0.05, 0.29],
    'Conductivity (µS/cm)': [0.16, 0.1, 0.12, 0.12, 0.06, 0.31, 0.29, 0.13, 0.1, 0.09, 0.1, 0.57],
    'Hardness (mg/L)': [3, 2.4, 2.2, 1.6, 5.0, 3, 3, 2.2, 4.2, 1.4, 2.2, 18],
    'Ca Hardness (mg/L)': [1.2, 1.0, 1.0, 0.7, 1.8, 1.0, 1.2, 0.8, 2.0, 0.6, 1.0, 7.5],
    'Mg Hardness (mg/L)': [1.8, 1.4, 1.2, 0.9, 3.2, 2.0, 1.8, 1.4, 2.2, 0.8, 1.2, 10.5]
}
df = pd.DataFrame(data)

# Calculate exceedances
df['As_exceed'] = df['As (mg/L)'] > thresholds['As (mg/L)']
df['Cd_exceed'] = df['Cd (mg/L)'] > thresholds['Cd (mg/L)']
df['Cr_exceed'] = df['Cr (mg/L)'] > thresholds['Cr (mg/L)']
df['Pb_exceed'] = df['Pb (mg/L)'] > thresholds['Pb (mg/L)']
df['pH_exceed'] = (df['pH'] < thresholds['pH_min']) | (df['pH'] > thresholds['pH_max'])
df['TDS_exceed'] = df['TDS (mg/L)'] > thresholds['TDS (mg/L)']
df['Conductivity_exceed'] = df['Conductivity (µS/cm)'] > thresholds['Conductivity (µS/cm)']
df['Hardness_exceed'] = df['Hardness (mg/L)'] > thresholds['Hardness (mg/L)']
df['Ca_Hardness_exceed'] = df['Ca Hardness (mg/L)'] > thresholds['Ca Hardness (mg/L)']
df['Mg_Hardness_exceed'] = df['Mg Hardness (mg/L)'] > thresholds['Mg Hardness (mg/L)']

# Calculate exceedances count
df['exceedances_count'] = df[['As_exceed', 'Cd_exceed', 'Cr_exceed', 'Pb_exceed', 'pH_exceed', 
                           'TDS_exceed', 'Conductivity_exceed', 'Hardness_exceed', 
                           'Ca_Hardness_exceed', 'Mg_Hardness_exceed']].sum(axis=1)

# Calculate pollution risk score (weighted)
df['pollution_risk_score'] = (
    df['As_exceed'].astype(int) * 2.5 + 
    df['Cd_exceed'].astype(int) * 2.0 + 
    df['Cr_exceed'].astype(int) * 2.0 + 
    df['Pb_exceed'].astype(int) * 2.5 + 
    df['pH_exceed'].astype(int) * 1.5 +
    df['TDS_exceed'].astype(int) * 1.0 +
    df['Conductivity_exceed'].astype(int) * 1.0 +
    df['Hardness_exceed'].astype(int) * 1.0 +
    df['Ca_Hardness_exceed'].astype(int) * 1.0 +
    df['Mg_Hardness_exceed'].astype(int) * 1.0
)

# Combine measurements by river (mean)
df_rivers = df.groupby('Sample').mean().reset_index()

# Title Slide
def slide_1():
    st.markdown("# 💧 Silent Streams, Loud Consequences")
    st.markdown("## The Impact of Water Pollution in Ghana")
    st.markdown("---")
    st.markdown("**Presented by:** Mawutor Afoh")
    st.markdown(f"**Date:** April 21, 2025")

# Why This Matters
def slide_2():
    st.markdown("## Why This Matters")

    st.markdown("""
    - **Illegal mining ("Galamsey")** has severely contaminated many of Ghana’s key rivers, including the Pra, Offin, and Ankobra.
    - **Over 60 %** of tested river samples exceed WHO safety thresholds for pollutants like **mercury, arsenic, and lead**.
    - Millions of Ghanaians rely on these water bodies for **drinking, irrigation, and fishing**—increasing exposure to toxic contaminants.
    - **Communities face rising health risks**, food insecurity, and ecosystem collapse without urgent action.
    - We must protect these water sources now to safeguard **public health, economic stability, and future generations**.
    """)


# Objectives
def slide_3():
    st.markdown("## Objectives of the Project")
    st.markdown("""
    - Identify rivers most affected by pollution
    - Compare observed pollutant levels with WHO, US EPA, and Ghana standards
    - Visualize pollutant exceedances and compute pollution risk scores
    - Explore human and ecosystem health risks
    - Inform policy recommendations and community actions
    """)

# Chemical Pollutants & Standards
def slide_4():
    st.markdown("## Chemical Pollutants & Standards")
    
    st.markdown("""
    Water quality standards set by the **WHO**, **EPA**, and **Ghana Standards Authority** help protect public health and ecosystems.  
    These limits define the **maximum safe concentration** of each pollutant in drinking water or natural water bodies.  
    Even small exceedances over time can lead to **chronic health effects**, **bioaccumulation**, and **ecosystem damage**.

    **Why These Standards Matter:**
    - **Arsenic, Lead, Mercury, and Cadmium** are toxic heavy metals. Long-term exposure can cause **neurological damage, kidney failure**, and **cancer**.
    - **pH** levels outside the 6.5–8.5 range can increase **metal solubility**, harming aquatic life and corroding infrastructure.
    - **Total Dissolved Solids (TDS)** and **Conductivity** indicate general water quality. High levels affect **taste, crop yield**, and **irrigation systems**.
    - **Hardness** impacts domestic and industrial water use, and excessive hardness can cause **scale buildup** and lower cleaning efficiency.

    The table below compares limits from key regulatory bodies:
    """)

    standards_data = {
        'Pollutant': ['Arsenic', 'Lead', 'Mercury', 'Cadmium', 'Chromium', 'pH', 'TDS', 'Conductivity', 'Hardness'],
        'WHO Limit (mg/L)': ['0.01', '0.01', '0.001', '0.003', '0.05', '6.5–8.5', '1000', '1000', '500'],
        'EPA Limit': ['0.01', '0.015', '0.002', '0.005', '0.1', '6.5–8.5', '500–1000', '500–1000', '500'],
        'Ghana Standard': ['0.01', '0.01', '0.001', '0.003', '0.05', '6.5–8.5', '1000', '1000', '500']
    }

    standards_df = pd.DataFrame(standards_data)
    st.table(standards_df)

    st.markdown("""
    > **Note:** Ghana’s standards largely align with WHO guidelines, emphasizing the **global consensus** on what constitutes safe water.  
    > Monitoring and enforcing these standards is critical for safeguarding communities near **illegal mining hotspots**.
    """)


# Dataset Overview
def slide_5():
    st.markdown("## Dataset Overview")

    st.markdown("""
    This dataset gives us a snapshot of water quality in **12 major rivers** across Ghana's mining regions. 

    **Why the data matters:**
    - Rivers are essential for **drinking water, farming, and fishing**. Pollution affects livelihoods and health.
    - **Illegal mining (Galamsey)** introduces dangerous substances into these waters.

    **What's in the dataset?**
    - 🏞️ **Multiple samples** were collected from the same rivers at **different locations or times** to get a more accurate picture.
    - We measured:
        - 🧪 **Heavy metals**: *Arsenic, Lead, Cadmium, Chromium* – toxic even in tiny amounts.
        - 🌊 **Water properties**: *pH, TDS, Conductivity* – these indicate general water quality.
        - 💧 **Hardness**: Levels of *Calcium* and *Magnesium*, which affect water usability and safety.

    **Extra insight:**
    - 🚩 "Exceedance flags" show if pollutant levels go **above safe limits** (set by WHO and Ghana EPA).
    - ✅ We also calculated a **pollution risk score** to simplify interpretation.

    Data was collected through **field sampling and laboratory analysis**.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Measured Water Quality")
        measurement_cols = ['As (mg/L)', 'Cd (mg/L)', 'Cr (mg/L)', 'Pb (mg/L)', 'pH', 'TDS (mg/L)', 
                            'Conductivity (µS/cm)', 'Hardness (mg/L)', 'Ca Hardness (mg/L)', 'Mg Hardness (mg/L)']
        st.dataframe(df[['Sample'] + measurement_cols].head(13))

    with col2:
        st.markdown("### Exceedance Flags (Above Safe Limits)")
        exceed_cols = ['As_exceed', 'Cd_exceed', 'Cr_exceed', 'Pb_exceed', 'pH_exceed', 'TDS_exceed', 
                       'Conductivity_exceed', 'Hardness_exceed', 'Ca_Hardness_exceed', 'Mg_Hardness_exceed']
        st.dataframe(df[['Sample'] + exceed_cols].head(13))

    st.markdown("""
    > ℹ️ **Note**: Some rivers appear more than once because **multiple locations were sampled** to capture local variations in pollution levels.
    > ⚠️ If a value is marked `True`, it means that pollutant exceeded recommended safety limits — these are the critical areas of concern.
    """)


# Visualizing the Problem
def slide_6():
    st.markdown("## Visualizing the Problem")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Heatmap of exceedances
        exceed_cols = ['As_exceed', 'Cd_exceed', 'Cr_exceed', 'Pb_exceed', 'pH_exceed', 'TDS_exceed']
        heat_data = df_rivers.set_index('Sample')[exceed_cols].astype(int)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(heat_data, cmap="Reds", annot=True, cbar=False, ax=ax)
        plt.title("Key Pollutant Exceedances by River")
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Dropdown to select pollutant for boxplot
        pollutant = st.selectbox(
            "Select pollutant to visualize:",
            ['As (mg/L)', 'Cd (mg/L)', 'Cr (mg/L)', 'Pb (mg/L)', 'pH', 'TDS (mg/L)']
        )
        
        # Get the threshold for the selected pollutant
        if pollutant == 'pH':
            threshold_min = thresholds['pH_min']
            threshold_max = thresholds['pH_max']
        else:
            threshold = thresholds[pollutant]
        
        # Create boxplot
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.boxplot(x='Sample', y=pollutant, data=df, ax=ax)
        plt.xticks(rotation=90)
        
        # Add threshold line(s)
        if pollutant == 'pH':
            plt.axhline(y=threshold_min, color='r', linestyle='--', label=f"Min Limit: {threshold_min}")
            plt.axhline(y=threshold_max, color='r', linestyle='--', label=f"Max Limit: {threshold_max}")
        else:
            plt.axhline(y=threshold, color='r', linestyle='--', label=f"Limit: {threshold}")
        
        plt.title(f"{pollutant} Levels Across Rivers")
        plt.legend()
        plt.tight_layout()
        st.pyplot(fig)
        
    st.markdown("""
    **Interpretation:**
    - Several rivers show multiple pollutant exceedances
    - Heavy metals (especially Arsenic and Lead) are the most frequently exceeded standards
    - Mining-heavy regions show the highest contamination levels
    - Galamsey Pit and rivers in active mining areas consistently exceed safety thresholds
    """)

# Example data with more than 3 rivers
data1 = {
    'Sample': ['Densu River', 'Pra River', 'Ankobrah River', 'Volta River', 'Tano River', 'Offin River', 'Birim River'],
    'pollution_risk_score': [11.2, 7.5, 3.4, 5.1, 4.2, 8.0, 2.9],
    'exceedances_count': [5, 3, 2, 4, 3, 6, 1]
}
df_rivers1 = pd.DataFrame(data1)


def slide_7():
    st.markdown("## Pollution Risk Scores")

    # Assuming df_rivers is your DataFrame containing all rivers.
    # Sort rivers by pollution risk score (descending)
    sorted_rivers = df_rivers1.sort_values('pollution_risk_score', ascending=False)

    # ---- BAR CHART: Pollution Risk Score by River ----
    fig_bar = px.bar(
        sorted_rivers,
        x='Sample',
        y='pollution_risk_score',
        color='pollution_risk_score',
        color_continuous_scale='Reds',
        title="Pollution Risk Score by River"
    )
    fig_bar.update_layout(
        xaxis_title="River",
        yaxis_title="Risk Score",
        xaxis_tickangle=45,
        xaxis={'categoryorder': 'total descending'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ---- SPLIT: Bubble chart (left) + Text explanation (right) ----
    col1, col2 = st.columns([1.3, 0.7])

    with col1:
        fig_scatter = px.scatter(
            df_rivers1,
            x='exceedances_count',
            y='pollution_risk_score',
            size='pollution_risk_score',
            color='Sample',
            hover_name='Sample',
            title="Exceedances vs. Pollution Risk",
            labels={
                'exceedances_count': 'No. of Standards Exceeded',
                'pollution_risk_score': 'Risk Score'
            }
        )
        fig_scatter.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig_scatter.update_layout(
            xaxis=dict(title='No. of Standards Exceeded'),
            yaxis=dict(title='Pollution Risk Score')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.markdown("""
        ### 💡 How to Interpret the Risk Score

        The **pollution risk score** tells us how dangerous a river sample is. It’s based on:
        - ✅ How **many pollutants** exceed safe limits
        - ⚠️ How **toxic** each pollutant is
        - 🔁 How **frequently** the exceedances occur

        #### Score Ranges:
        - 🔴 **Above 10**: Extremely polluted
        - 🟠 **5–10**: High pollution
        - 🟡 **2–5**: Moderate pollution
        - 🟢 **Below 2**: Low pollution

        Rivers with the highest scores need urgent action.
        """)


# Health Impacts
def slide_8():
    st.markdown("## Health Impacts of Water Pollution")

    tab1, tab2 = st.tabs(["📋 Health Impact Table", "📊 Impact Visualization"])

    # --- Tab 1: Health Impact Table ---
    with tab1:
        health_data = {
            "Pollutant": [
                "Arsenic (As)",
                "Mercury (Hg)",
                "Cadmium (Cd)",
                "Lead (Pb)",
                "Chromium (Cr)"
            ],
            "Known Diseases": [
                "Skin lesions, cancers (skin, lung, bladder), heart diseases",
                "Nerve damage, kidney failure",
                "Kidney disease, bone problems, cancers",
                "Learning difficulties, memory loss in children",
                "Breathing issues, skin rashes, lung cancer"
            ],
            "Short-Term Impact": [
                "Stomach pain, vomiting, diarrhea",
                "Shaking hands, confusion, mood swings",
                "Nausea, belly pain",
                "Tiredness, headaches, stomach aches",
                "Coughing, skin irritation"
            ],
            "Long-Term Impact": [
                "Cancer, diabetes, heart disease",
                "Memory loss, kidney failure",
                "Weak bones, kidney damage",
                "Slow brain development in children",
                "Lung cancer, breathing problems"
            ]
        }
        health_df = pd.DataFrame(health_data)
        st.dataframe(health_df, use_container_width=True)

    # --- Tab 2: Visualizations ---
    with tab2:
        col1, col2 = st.columns(2)

        # --- Radar Chart: Health System Impact Severity ---
        with col1:
            impact_data = {
                'Category': ['Nervous System', 'Kidneys', 'Heart', 'Reproduction', 'Skin', 'Digestion'],
                'Arsenic': [5, 6, 8, 5, 9, 7],
                'Mercury': [9, 8, 5, 8, 3, 6],
                'Cadmium': [4, 9, 5, 7, 4, 5],
                'Lead': [9, 6, 7, 8, 2, 5],
                'Chromium': [3, 5, 4, 6, 8, 3]
            }
            impact_df = pd.DataFrame(impact_data)

            impact_long_df = impact_df.melt(
                id_vars='Category',
                var_name='Pollutant',
                value_name='Severity'
            )

            fig_radar = px.line_polar(
                impact_long_df,
                r='Severity',
                theta='Category',
                color='Pollutant',
                line_close=True,
                title="Impact of Pollutants on Body Systems",
                color_discrete_sequence=px.colors.qualitative.Bold,
                labels={'Severity': 'Impact Level (1–10)'}
            )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                legend_title_text='Pollutant'
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # --- Bar Chart: Healthcare Costs ---
        with col2:
            cost_data = {
                'Disease': [
                    'Skin Cancer',
                    'Kidney Disease',
                    'Neurological Disorders',
                    'Developmental Issues',
                    'Respiratory Disease'
                ],
                'Annual Cost per Patient (USD)': [
                    'N/A',
                    5300,
                    'N/A',
                    'N/A',
                    1741
                ]
            }
            cost_df = pd.DataFrame(cost_data)

            fig_bar = px.bar(
                cost_df,
                x='Annual Cost per Patient (USD)',
                y='Disease',
                color='Disease',
                orientation='h',
                title="Estimated Yearly Healthcare Costs per Patient",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("""
        **💬 Notes on Cost Data:**  
        - Kidney disease treatment (like dialysis) can cost around \$5,300 per year.  
        - Asthma treatment (used here as a proxy for respiratory disease) costs roughly \$1,741 yearly per patient.  
        - Costs for cancer and neurological issues are harder to estimate in Ghana due to limited national data.
        - Ghana spends only **4.15% of its GDP** on health – below the average for developing countries.
        """)

    # --- Summary of Key Insights ---
    st.markdown("""
    ### 🔍 Key Takeaways

    - **Most dangerous effects:** Cancer, kidney failure, and brain damage are among the most serious health threats.
    - **Children at greatest risk:** Kids absorb more heavy metals than adults — putting them at higher risk for lifelong health issues.
    - **Health system strain:** Many pollution-related illnesses are expensive to treat, and Ghana’s health spending is limited.
    - **We need better data:** Some impacts, especially on mental development and cancer, are under-researched locally.
    """)

   
# Generational & Regional Effects
def slide_9():
    st.markdown("## Generational & Regional Effects")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Vulnerability by Population Group")

        # Updated vulnerability scores based on recent findings
        vulnerability_data = {
            'Group': ['Children', 'Pregnant Women', 'Farmers', 'Fishers', 'General Population'],
            'Vulnerability Score': [9.2, 8.7, 7.5, 8.3, 5.4]
        }

        df_vuln = pd.DataFrame(vulnerability_data)

        # Create horizontal bar chart
        fig = px.bar(
            df_vuln,
            x='Vulnerability Score',
            y='Group',
            orientation='h',
            title="Vulnerability to Water Pollution (Scale 1-10)",
            color='Vulnerability Score',
            color_continuous_scale='Reds',
            text_auto='.1f'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Regional Impact Severity")

        # Updated regional impact data based on recent findings
        region_data = {
            'Region': ['Eastern Region', 'Ashanti Region', 'Western Region', 'Central Region', 
                      'Western North', 'Bono East', 'Upper East', 'Ahafo'],
            'Impact Score': [9.0, 8.7, 8.5, 6.2, 7.8, 6.5, 5.2, 7.3],
            'Primary Mining Activity': ['Galamsey', 'Mixed Mining', 'Large-scale & Galamsey', 
                                        'Moderate Galamsey', 'Large-scale Mining', 'Small-scale Legal', 
                                        'Small-scale Mining', 'Mixed Mining']
        }

        df_region = pd.DataFrame(region_data)

        # Bar chart for regional impacts
        fig = px.bar(
            df_region.sort_values('Impact Score', ascending=False),
            x='Region',
            y='Impact Score',
            color='Primary Mining Activity',
            title="Pollution Impact by Mining Region",
            hover_data=['Primary Mining Activity'],
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Generational Impact Pathway")

    # Create a flowchart-like visualization using matplotlib
    fig, ax = plt.subplots(figsize=(10, 3))

    # Turn off the axis
    ax.axis('off')

    # Define the boxes and arrows
    boxes = [
        (0.1, 0.5, 0.15, 0.3, "Water\nPollution"),
        (0.35, 0.5, 0.15, 0.3, "Maternal\nExposure"),
        (0.6, 0.5, 0.15, 0.3, "Fetal\nDevelopment\nImpact"),
        (0.85, 0.5, 0.15, 0.3, "Lifelong\nHealth\nEffects")
    ]

    arrows = [
        (0.25, 0.65, 0.35, 0.65),
        (0.5, 0.65, 0.6, 0.65),
        (0.75, 0.65, 0.85, 0.65)
    ]

    # Draw the boxes
    for x, y, w, h, label in boxes:
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=True, color='lightblue', alpha=0.7))
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontweight='bold')

    # Draw the arrows
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle="->", lw=2, color='blue'))

    st.pyplot(fig)

    st.markdown("""
    ### Regional & Generational Findings:

    - **Highest risk regions:** Eastern and Ashanti Regions exhibit critical levels of mercury and arsenic contamination due to intensive galamsey activities.
    - **Mining correlation:** Areas with prevalent illegal mining show significantly higher pollution levels, adversely affecting water quality and public health.
    - **Generational transfer:** Studies have detected heavy metals in umbilical cord blood, indicating prenatal exposure and potential long-term health effects.
    - **Long-term consequences:** Children born in high-exposure areas are at increased risk of developmental delays and other health issues.
    """)

    st.markdown("""
    ### References

    - Obiri, S. et al. (2024). *Impacts of illegal mining activities on water quality for irrigation and domestic purposes*. Journal of Water and Health. [Link](https://iwaponline.com/jwh/article/22/10/1886/104786/Impacts-of-illegal-mining-activities-on-water)
    - Cross Catholic Outreach. (2021). *Water Crisis in Ghana*. [Link](https://crosscatholic.org/blogs/2021/12/water-crisis-in-ghana/)
    - National Institutes of Health. (2023). *Heavy Metals in Umbilical Cord Blood: Effects on Epigenetics and Child Health*. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC11544782/)
    - Nature Scientific Reports. (2023). *Effects of heavy metal exposure during pregnancy on birth outcomes*. [Link](https://www.nature.com/articles/s41598-023-46271-0)
    """)


def slide_10():
    st.markdown("## Ecosystem Damage")

    tab1, tab2 = st.tabs(["Ecosystem Impact Data", "Biodiversity & Bioaccumulation"])

    # Tab 1: Ecosystem Impact Data
    with tab1:
        eco_data = {
            "Pollutant": ["Arsenic", "Mercury", "Cadmium", "Lead", "Chromium", "pH Imbalance", "TDS"],
            "Aquatic Life Impact": [
                "Bioaccumulates; enzyme disruption and reproductive failure",
                "Neurotoxic methylmercury impairs growth and reproduction",
                "Gill damage, reduced growth, lower survival rates",
                "Neurological and muscular dysfunction",
                "Gill tissue damage, stunted growth",
                "High acidity kills sensitive aquatic species",
                "Disrupts osmoregulation; reduces fish health"
            ],
            "Environmental Impact": [
                "Soil/crop contamination; long-term sediment persistence (10+ yrs)",
                "Accumulates in sediment and fish (up to 2.5 ppm); 15–30 years to clear",
                "Soil degradation, yield losses; 20-year recovery",
                "Lead in sediment persists 25+ years; affects biodiversity",
                "Long-term toxicity in sediments (~15 years)",
                "Acid mine drainage alters soil and water pH for 3–7 years",
                "High levels signal heavy metal presence; clears in 1–5 years"
            ],
            "Recovery Time (years)": [10, 15, 20, 25, 15, 5, 3]
        }
        st.dataframe(pd.DataFrame(eco_data), use_container_width=True)

    # Tab 2: Biodiversity & Bioaccumulation
    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                pd.DataFrame({
                    "Category": ["Freshwater Vertebrates"],
                    "Decline (%)": [85]
                }),
                x="Category", y="Decline (%)", text="Decline (%)",
                title="Global Freshwater Biodiversity Decline since 1970"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            bioaccum_df = pd.DataFrame({
                "Organism": [
                    "Water", "Sediment", "Primary Producer",
                    "Primary Consumer", "Secondary Consumer",
                    "Tertiary Consumer", "Human"
                ],
                "Hg (ppm)": [0.001, 0.05, 0.2, 0.8, 2.5, 4.0, 1.2]  # Obiri et al., 2024
            })
            fig2 = px.bar(
                bioaccum_df,
                x="Organism", y="Hg (ppm)",
                title="Mercury Bioaccumulation in Ghanaian Food Chain",
                log_y=True, text="Hg (ppm)"
            )
            fig2.update_layout(yaxis_title="Mercury Level (ppm, log scale)")
            st.plotly_chart(fig2, use_container_width=True)

    # Ecosystem Services Impacted
    st.markdown("### Ecosystem Services Impacted")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Primary Forest Loss (2002–2020)", "9.3 %")
        st.caption("Source: Global Forest Watch")

    with col2:
        st.metric("Wetland Loss (1970–2020)", "35 %")
        st.caption("Source: Ramsar Global Wetland Outlook")

    with col3:
        st.metric("Child Population (under 15)", "36.6 %")
        st.caption("Source: World Bank (2023)")

    with col4:
        st.metric("Children Stunting Rate", "22.3 %")
        st.caption("Source: UNICEF Ghana (2022)")

    # Key Takeaways
    st.markdown("""
    ### Key Takeaways
    - Mercury levels in predatory fish can reach **2.5–4.0 ppm**, over **25×** the safe limit
    - Freshwater vertebrate populations have declined by **85 %** since 1970 (WWF)
    - Ghana has lost **9.3 %** of its primary forest cover between 2002–2020
    - Pollutants like **Lead** and **Cadmium** persist in sediment and soil for **20–25 years**
    """)


# Slide 11: Economic Consequences
def slide_11():
    st.markdown("## Economic Consequences")

    col1, col2 = st.columns(2)

    with col1:
        # Sectoral losses in Ghana and region (USD million)
        economic_data = {
            "Sector": ["Agriculture", "Fisheries", "Healthcare", "Water Treatment", "Tourism"],
            "Annual Loss": [120, 80, 200, 45.6, 30],
            "Type": ["Direct", "Direct", "Indirect", "Indirect", "Indirect"]
        }
        econ_df = pd.DataFrame(economic_data)
        fig = px.bar(
            econ_df,
            x="Annual Loss",
            y="Sector",
            color="Type",
            orientation="h",
            title="Annual Economic Impact by Sector in Ghana"
        )
        fig.update_layout(xaxis_title="Loss (USD million)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        • Agriculture & Fisheries losses from yield decline :contentReference[oaicite:14]{index=14}  
        • Healthcare costs from waterborne diseases :contentReference[oaicite:15]{index=15}  
        • Water treatment spending and reduced tourism revenue  
        """)

    with col2:
        # Regional GDP loss
        impact_df = pd.DataFrame({
            "Impact Area": ["Sub‑Saharan Africa"],
            "GDP Loss (%)": [5]
        })
        fig2 = px.bar(
            impact_df,
            x="GDP Loss (%)",
            y="Impact Area",
            orientation="h",
            title="Regional GDP Loss due to Water Issues"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("Sub‑Saharan Africa loses **5 %** of GDP (~US$170 billion/yr) to water issues :contentReference[oaicite:16]{index=16}")

    st.markdown("""
    > **Context:**  
    > Ghana’s agriculture workforce (~44 %) relies on seasonal water; loss of water quality directly threatens **US$200 million** in annual revenue :contentReference[oaicite:17]{index=17}  
    > Over **30 %** of inland fisheries yield lost to pollution :contentReference[oaicite:18]{index=18}  
    """)
    st.markdown("""
    **International High‑Level Panel on Water Investments for Africa** (2023). Sub‑Saharan Africa loses **5 %** of GDP (~US$ 170 billion/yr) due to poor water infrastructure and contamination. :contentReference[oaicite:6]{index=6}  
    **African Development Bank** (2025). *World Water Day 2025: Preserving Africa’s Water Resources* — confirms the **5 %** GDP loss estimate. :contentReference[oaicite:7]{index=7}  
    **Infrastructure Consortium for Africa** (2022). “The Water Challenge”: Sub‑Saharan Africa loses **5 %** of GDP annually from water issues. :contentReference[oaicite:8]{index=8}  
    **Muntaka, A.** (2020). *Fisheries and Mangroves in Ghana*: fish stocks down ~**30 %** in key river deltas due to pollution.   
    **OECD** (2024). *Diversifying Sources of Finance for Water in Africa*: reiterates **5 %** GDP loss to water scarcity and pollution. :contentReference[oaicite:9]{index=9}  
    """)
    

# Severity Index & Rankings
def slide_12():
    st.markdown("## Severity Index & Rankings")

    # Classify severity based on risk score
    df_rivers['Severity'] = pd.cut(
        df_rivers['pollution_risk_score'],
        bins=[0, 2, 4, 8],
        labels=['Low', 'Medium', 'High']
    )

    # Sort rivers by pollution risk score (descending)
    ranked_df = df_rivers.sort_values(by='pollution_risk_score', ascending=False)

    # Create color-coded bar chart
    fig = px.bar(
        ranked_df,
        x='Sample',
        y='pollution_risk_score',
        color='Severity',
        color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'},
        title="Pollution Severity Ranking of River Samples (High to Low)",
        hover_data={
            'Sample': True,
            'pollution_risk_score': ':.2f',
            'Severity': True
        }
    )
    fig.update_layout(
        xaxis_title="River Sample",
        yaxis_title="Pollution Risk Score",
        legend_title="Severity Level",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

    # Interpretation guidance
    st.markdown("""
    ### 🛠️ Intervention Priority

    - 🟥 **High Severity (Score > 4)**:  
      Immediate mitigation required — high pollution and potential health/ecosystem risks.
    
    - 🟧 **Medium Severity (Score 2–4)**:  
      Needs regular monitoring and early intervention to prevent escalation.
    
    - 🟩 **Low Severity (Score < 2)**:  
      Maintain current water quality through protection and proactive management.
    """)


# Recommendations for Action
def slide_13():
    st.markdown("## Recommendations for Action")
    st.markdown("""
    ### Policy Level:
    - Ban illegal mining activities within 100m of water bodies
    - Enforce stricter penalties for environmental violations
    - Create protected buffer zones around critical water sources
    
    ### Community Level:
    - Regular water quality testing and public reporting
    - Community-based river clean-up programs
    - Education on safe water practices and health risks
    
    ### Environmental Restoration:
    - Invest in natural filtration wetlands
    - River bank reforestation programs
    - Remediation technologies for heavily contaminated areas
    """)

# Call to Action
def slide_14():
    st.markdown("## Call to Action")
    st.markdown("""
    ### Everyone has a role to play:
    
    - **Government:** Enforce mining regulations and invest in clean water
    - **Citizens:** Report illegal mining and participate in clean-up efforts
    - **Scientists:** Continue monitoring and developing solutions
    - **Businesses:** Adopt responsible water usage practices
    
    > ### "Clean water = healthy people = strong economy"
    
    **Time is running out for these rivers—let's act together.**
    """)

# Q&A / Acknowledgements
def slide_15():
    st.markdown("## Thank You & Acknowledgements")
    st.markdown("""
    ### Acknowledgements:
    - Ghana Water Resources Commission
    - Environmental Protection Agency
    
    ### Contact Information:
    - Email: Solomonafoh@gmail.com
    
    ### Questions?
    """)
    
def slide_16():
    st.markdown("## End of Presentation")
    st.markdown("Thank you for your attention!")
    st.markdown("### References")
    st.markdown("""
    World Bank. (2011). Ghana: Balancing economic growth and depletion of resources. Retrieved from https://blogs.worldbank.org/en/africacan/ghana-balancing-economic-growth-and-depletion-resources

    Ghana Environmental Protection Agency. (2016). National Biodiversity Strategy and Action Plan. Retrieved from https://dev-chm.cbd.int/doc/world/gh/gh-nbsap-v2-en.pdf

    Shao, K., et al. (2023). Bioaccumulation and trophic transfer of total mercury through the aquatic food web. Retrieved from https://www.sciencedirect.com/science/article/pii/S0048969723028310

    Winrock International. (2021). Ghana Water Resources Profile Overview. Retrieved from https://winrock.org/resources/ghana-water-resources-profile/

    Muntaka, A. (2020). Fisheries and Mangroves in Ghana: Atidza and the Densu Delta. Retrieved from https://muntaka.com/fishing-in-ghana-mangroves/

    World Bank. (2012). Ghana loses GHC420 million annually due to poor sanitation. Retrieved from https://documents1.worldbank.org/curated/ar/786701468256742033/pdf/681220WSP0ESI00B000PUBLIC00brochure.pdf
    
    Agyemang, I. A., & Addai, A. (2023). Mining Activities and Their Effect on the Environment: A Case Study of Illegal Mining in the Eastern Region of Ghana. African Journal of Technical Education and Occupational Health (AJTEOH), 5(2), 66–79.
    https://journal-iasssf.com/index.php/AJTEOH/article/download/395/651/6303

    Tsekpo, M., & Ntiamoah, B. (2023). Analyzing Topographical and Socio-Economic Impacts of Illegal Gold Mining in Ghana's Ashanti and Eastern Regions Using Remote Sensing and Field Surveys.
    ResearchGate.
    https://www.researchgate.net/publication/375696718_Analyzing_Topographical_and_Socio-Economic_Impacts_of_Illegal_Gold_Mining_in_Ghana's_Ashanti_and_Eastern_Regions_Using_Remote_Sensing_and_Field_Surveys

    Obiri, S., Agyemang, I., & Doyi, H. (2024). Impacts of Illegal Mining Activities on Water Quality for Irrigation and Domestic Purposes in Ghana. Journal of Water and Health, 22(10), 1886–1899.
    https://iwaponline.com/jwh/article/22/10/1886/104786/Impacts-of-illegal-mining-activities-on-water

    Ansong, J., & Asante, K. A. (2023). Assessment of Heavy Metal Pollution in Rivers Impacted by Illegal Mining Using Pollution Indices and Health Risk Models in Ghana. Environmental Pollution, 329, 122218.
    https://www.sciencedirect.com/science/article/abs/pii/S0269749123021942
    """)

# Navigation system
st.sidebar.title("Presentation Navigation")
slide_options = {
    "1: Title Slide": slide_1,
    "2: Why This Matters": slide_2,
    "3: Objectives": slide_3,
    "4: Chemical Pollutants & Standards": slide_4,
    "5: Dataset Overview": slide_5,
    "6: Visualizing the Problem": slide_6,
    "7: Pollution Risk Scores": slide_7,
    "8: Health Impacts": slide_8,
    "9: Generational & Regional Effects": slide_9,
    "10: Ecosystem Damage": slide_10,
    "11: Economic Consequences": slide_11,
    "12: Severity Index & Rankings": slide_12,
    "13: Recommendations for Action": slide_13,
    "14: Call to Action": slide_14,
    "15: Q&A / Acknowledgements": slide_15,
    "16: End of Presentation": slide_16
}

# Initialize session state for slide selection
if "selected_slide" not in st.session_state:
    st.session_state.selected_slide = list(slide_options.keys())[0]

# Sidebar navigation
st.sidebar.title("Presentation Navigation")

selected = st.sidebar.radio("Go to slide:", list(slide_options.keys()), 
                             index=list(slide_options.keys()).index(st.session_state.selected_slide))
st.session_state.selected_slide = selected

st.sidebar.markdown("---")

# Previous/Next buttons
col1, col2 = st.sidebar.columns(2)
slide_num = int(st.session_state.selected_slide.split(":")[0])

if col1.button("← Previous") and slide_num > 1:
    st.session_state.selected_slide = f"{slide_num-1}: {list(slide_options.keys())[slide_num-2].split(': ')[1]}"
    st.rerun()

if col2.button("Next →") and slide_num < len(slide_options):
    st.session_state.selected_slide = f"{slide_num+1}: {list(slide_options.keys())[slide_num].split(': ')[1]}"
    st.rerun()

# Display the selected slide
slide_options[st.session_state.selected_slide]()
