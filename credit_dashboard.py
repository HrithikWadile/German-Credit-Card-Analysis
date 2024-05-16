import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set page configuration
st.set_page_config(page_title="German Credit Analysis", layout="wide", page_icon="💳")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data(file_path):
    """Load and prepare the credit data"""
    try:
        df = pd.read_csv(file_path, index_col=0)
        # Clean column names
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.info("german_credit_data.csv")
        return None

# Main title
st.title("🏦 German Credit Data Analytics Dashboard")
st.markdown("### Comprehensive Analysis of Credit Risk Patterns and Customer Demographics")

# Load data
data_file = "german_credit_data.csv"
df = load_data(data_file)

if df is not None:
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    # Age filter
    age_range = st.sidebar.slider(
        "Age Range",
        int(df['Age'].min()),
        int(df['Age'].max()),
        (int(df['Age'].min()), int(df['Age'].max()))
    )
    
    # Gender filter
    gender_filter = st.sidebar.multiselect(
        "Gender",
        options=df['Sex'].unique(),
        default=df['Sex'].unique()
    )
    
    # Housing filter
    housing_filter = st.sidebar.multiselect(
        "Housing Type",
        options=df['Housing'].unique(),
        default=df['Housing'].unique()
    )
    
    # Purpose filter
    purpose_filter = st.sidebar.multiselect(
        "Credit Purpose",
        options=df['Purpose'].unique(),
        default=df['Purpose'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['Age'] >= age_range[0]) &
        (df['Age'] <= age_range[1]) &
        (df['Sex'].isin(gender_filter)) &
        (df['Housing'].isin(housing_filter)) &
        (df['Purpose'].isin(purpose_filter))
    ]
    
    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Records", len(filtered_df))
    
    with col2:
        st.metric("Average Age", f"{filtered_df['Age'].mean():.1f}")
    
    with col3:
        st.metric("Avg Credit Amount", f"€{filtered_df['Credit amount'].mean():.0f}")
    
    with col4:
        st.metric("Avg Duration", f"{filtered_df['Duration'].mean():.1f} mo")
    
    with col5:
        st.metric("Total Credit", f"€{filtered_df['Credit amount'].sum()/1000:.0f}K")
    
    # Analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "👥 Demographics", 
        "💰 Credit Analysis", 
        "🎯 Purpose Analysis",
        "📋 Data Table"
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header("Overview Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Age Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            age_bins = [0, 25, 35, 45, 55, 65, 100]
            age_labels = ['<25', '25-35', '35-45', '45-55', '55-65', '65+']
            filtered_df['Age_Group'] = pd.cut(filtered_df['Age'], bins=age_bins, labels=age_labels)
            age_counts = filtered_df['Age_Group'].value_counts().sort_index()
            ax.bar(age_counts.index, age_counts.values, color='#1f77b4', alpha=0.8)
            ax.set_xlabel('Age Group', fontsize=12)
            ax.set_ylabel('Count', fontsize=12)
            ax.set_title('Distribution of Applicants by Age', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.subheader("Gender Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            gender_counts = filtered_df['Sex'].value_counts()
            colors = ['#ff7f0e', '#2ca02c']
            ax.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90)
            ax.set_title('Gender Distribution', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Housing Type Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            housing_counts = filtered_df['Housing'].value_counts()
            ax.bar(housing_counts.index, housing_counts.values, color='#2ca02c', alpha=0.8)
            ax.set_xlabel('Housing Type', fontsize=12)
            ax.set_ylabel('Count', fontsize=12)
            ax.set_title('Housing Type Distribution', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close()
        
        with col4:
            st.subheader("Job Category Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            job_counts = filtered_df['Job'].value_counts().sort_index()
            ax.bar(job_counts.index, job_counts.values, color='#d62728', alpha=0.8)
            ax.set_xlabel('Job Category', fontsize=12)
            ax.set_ylabel('Count', fontsize=12)
            ax.set_title('Job Category Distribution', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            plt.close()
    
    # Tab 2: Demographics
    with tab2:
        st.header("Demographic Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Age by Gender")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.boxplot(column='Age', by='Sex', ax=ax)
            ax.set_xlabel('Gender', fontsize=12)
            ax.set_ylabel('Age', fontsize=12)
            ax.set_title('Age Distribution by Gender', fontsize=14, fontweight='bold')
            plt.suptitle('')
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.subheader("Saving Accounts Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            saving_counts = filtered_df['Saving accounts'].value_counts()
            colors = plt.cm.Set3(range(len(saving_counts)))
            ax.pie(saving_counts.values, labels=saving_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90)
            ax.set_title('Saving Accounts Status', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Checking Account Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            checking_counts = filtered_df['Checking account'].value_counts()
            ax.bar(checking_counts.index, checking_counts.values, color='#9467bd', alpha=0.8)
            ax.set_xlabel('Checking Account Status', fontsize=12)
            ax.set_ylabel('Count', fontsize=12)
            ax.set_title('Checking Account Distribution', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close()
        
        with col4:
            st.subheader("Housing by Gender")
            fig, ax = plt.subplots(figsize=(10, 6))
            housing_gender = pd.crosstab(filtered_df['Housing'], filtered_df['Sex'])
            housing_gender.plot(kind='bar', ax=ax, color=['#ff7f0e', '#2ca02c'])
            ax.set_xlabel('Housing Type', fontsize=12)
            ax.set_ylabel('Count', fontsize=12)
            ax.set_title('Housing Type by Gender', fontsize=14, fontweight='bold')
            ax.legend(title='Gender')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close()
    
    # Tab 3: Credit Analysis
    with tab3:
        st.header("Credit Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Credit Amount Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(filtered_df['Credit amount'], bins=30, color='#1f77b4', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Credit Amount (€)', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Credit Amounts', fontsize=14, fontweight='bold')
            ax.axvline(filtered_df['Credit amount'].mean(), color='red', 
                      linestyle='--', label=f'Mean: €{filtered_df["Credit amount"].mean():.0f}')
            ax.legend()
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.subheader("Duration Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(filtered_df['Duration'], bins=20, color='#ff7f0e', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Duration (months)', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Credit Duration', fontsize=14, fontweight='bold')
            ax.axvline(filtered_df['Duration'].mean(), color='red', 
                      linestyle='--', label=f'Mean: {filtered_df["Duration"].mean():.1f} months')
            ax.legend()
            st.pyplot(fig)
            plt.close()
        
        st.subheader("Credit Amount vs Duration")
        fig, ax = plt.subplots(figsize=(12, 6))
        scatter = ax.scatter(filtered_df['Duration'], filtered_df['Credit amount'], 
                           alpha=0.5, c=filtered_df['Age'], cmap='viridis', s=50)
        ax.set_xlabel('Duration (months)', fontsize=12)
        ax.set_ylabel('Credit Amount (€)', fontsize=12)
        ax.set_title('Credit Amount vs Duration (colored by Age)', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, label='Age', ax=ax)
        st.pyplot(fig)
        plt.close()
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Average Credit by Housing Type")
            fig, ax = plt.subplots(figsize=(10, 6))
            avg_credit_housing = filtered_df.groupby('Housing')['Credit amount'].mean().sort_values(ascending=False)
            ax.barh(avg_credit_housing.index, avg_credit_housing.values, color='#2ca02c', alpha=0.8)
            ax.set_xlabel('Average Credit Amount (€)', fontsize=12)
            ax.set_ylabel('Housing Type', fontsize=12)
            ax.set_title('Average Credit by Housing Type', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        
        with col4:
            st.subheader("Credit Amount by Gender")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.boxplot(column='Credit amount', by='Sex', ax=ax)
            ax.set_xlabel('Gender', fontsize=12)
            ax.set_ylabel('Credit Amount (€)', fontsize=12)
            ax.set_title('Credit Amount Distribution by Gender', fontsize=14, fontweight='bold')
            plt.suptitle('')
            st.pyplot(fig)
            plt.close()
    
    # Tab 4: Purpose Analysis
    with tab4:
        st.header("Credit Purpose Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Purpose Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            purpose_counts = filtered_df['Purpose'].value_counts()
            ax.barh(purpose_counts.index, purpose_counts.values, color='#d62728', alpha=0.8)
            ax.set_xlabel('Count', fontsize=12)
            ax.set_ylabel('Purpose', fontsize=12)
            ax.set_title('Credit Purpose Distribution', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.subheader("Purpose Percentage")
            fig, ax = plt.subplots(figsize=(10, 6))
            purpose_counts = filtered_df['Purpose'].value_counts()
            colors = plt.cm.Set3(range(len(purpose_counts)))
            wedges, texts, autotexts = ax.pie(purpose_counts.values, labels=purpose_counts.index, 
                                               autopct='%1.1f%%', colors=colors, startangle=90)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            ax.set_title('Purpose Distribution (%)', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        
        st.subheader("Average Credit Amount by Purpose")
        fig, ax = plt.subplots(figsize=(12, 6))
        avg_credit_purpose = filtered_df.groupby('Purpose')['Credit amount'].mean().sort_values(ascending=False)
        ax.bar(avg_credit_purpose.index, avg_credit_purpose.values, color='#8c564b', alpha=0.8)
        ax.set_xlabel('Purpose', fontsize=12)
        ax.set_ylabel('Average Credit Amount (€)', fontsize=12)
        ax.set_title('Average Credit Amount by Purpose', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        plt.close()
        
        st.subheader("Duration by Purpose")
        fig, ax = plt.subplots(figsize=(12, 6))
        filtered_df.boxplot(column='Duration', by='Purpose', ax=ax)
        ax.set_xlabel('Purpose', fontsize=12)
        ax.set_ylabel('Duration (months)', fontsize=12)
        ax.set_title('Credit Duration by Purpose', fontsize=14, fontweight='bold')
        plt.suptitle('')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        plt.close()
    
    # Tab 5: Data Table
    with tab5:
        st.header("Data Explorer")
        
        # Statistical summary
        st.subheader("Statistical Summary")
        st.dataframe(filtered_df.describe())
        
        # Show raw data
        st.subheader("Raw Data")
        st.dataframe(filtered_df)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_credit_data.csv",
            mime="text/csv"
        )
    
    # Key Findings
    st.header("🔍 Key Findings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **👥 Customer Profile**
        - Average age: {filtered_df['Age'].mean():.1f} years
        - Male: {(filtered_df['Sex']=='male').sum()} ({(filtered_df['Sex']=='male').sum()/len(filtered_df)*100:.1f}%)
        - Female: {(filtered_df['Sex']=='female').sum()} ({(filtered_df['Sex']=='female').sum()/len(filtered_df)*100:.1f}%)
        - Most common housing: {filtered_df['Housing'].mode()[0]}
        """)
    
    with col2:
        st.success(f"""
        **💰 Credit Patterns**
        - Average credit: €{filtered_df['Credit amount'].mean():.0f}
        - Median credit: €{filtered_df['Credit amount'].median():.0f}
        - Average duration: {filtered_df['Duration'].mean():.1f} months
        - Most common purpose: {filtered_df['Purpose'].mode()[0]}
        """)
    
    with col3:
        st.warning(f"""
        **📊 Risk Indicators**
        - Applicants with savings: {(filtered_df['Saving accounts']!='NA').sum()}
        - Applicants with checking: {(filtered_df['Checking account']!='NA').sum()}
        - Own housing: {(filtered_df['Housing']=='own').sum()} ({(filtered_df['Housing']=='own').sum()/len(filtered_df)*100:.1f}%)
        """)

else:
    st.error("⚠️ Unable to load data. Please ensure 'german_credit_data.csv' is in the same directory.")
    st.info("""
    **How to use this dashboard:**
    1. Save your CSV file as 'german_credit_data.csv'
    2. Place it in the same folder as this Python script
    3. Run: `streamlit run credit_dashboard.py`
    """)