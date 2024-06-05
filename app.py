import streamlit as st
import pandas as pd
from datetime import datetime

# Load your data with the appropriate keys
sla_df = pd.read_hdf('sla_metrics.h5', key='period_sla')
satisfaction_df = pd.read_hdf('satisfaction_ratings.h5', key='period_satisfaction')
overall_sla_df = pd.read_hdf('sla_metrics.h5', key='overall_sla')
overall_satisfaction_df = pd.read_hdf('satisfaction_ratings.h5', key='overall_satisfaction')

# Load platform ratings data from Google Sheets
platform_ratings_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHFbcm6Ko-BkEplJ4qubN6QhJqPWp5BAZwrq6X080P-XV1yutazCOVirzHBl6PimOusdbP0ZkJ1J6H/pub?output=xlsx"
platform_ratings_df = pd.read_excel(platform_ratings_url, sheet_name='platform_ratings')

# Convert period to datetime for easier handling
sla_df['period'] = pd.to_datetime(sla_df['period'])
satisfaction_df['period'] = pd.to_datetime(satisfaction_df['period'])

# Add the month column to the dataframes
sla_df['month'] = sla_df['period'].dt.strftime('%B %Y')
satisfaction_df['month'] = satisfaction_df['period'].dt.strftime('%B %Y')

# Define all months for the table
all_months = ['May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April']
current_year = datetime.now().year

# Ensure all months have a year suffix for this year
all_months_year = [f"{month} {current_year}" for month in all_months]

# Filter overall data for periods
period_satisfaction_overall = satisfaction_df[satisfaction_df['agent'] == 'overall'].pivot_table(index='agent', columns='month', values='satisfaction', aggfunc='mean', fill_value=None)
period_sla_overall = sla_df[sla_df['agent'] == 'overall'].pivot_table(index='agent', columns='month', values='sla', aggfunc='mean', fill_value=None)

# Convert decimals to percentages
period_satisfaction_overall = period_satisfaction_overall.applymap(lambda x: f"{x * 100:.2f}%" if pd.notnull(x) else None)
period_sla_overall = period_sla_overall.applymap(lambda x: f"{x * 100:.2f}%" if pd.notnull(x) else None)

# Ensure all months are included in the pivot tables
period_satisfaction_overall = period_satisfaction_overall.reindex(columns=all_months_year)
period_sla_overall = period_sla_overall.reindex(columns=all_months_year)

st.title('Customer Relations Dashboard')

st.header('Satisfaction Rating')
overall_satisfaction = overall_satisfaction_df.iloc[0]['overall_satisfaction'] * 100
st.subheader(f'Overall: {overall_satisfaction:.2f}%')
st.write(period_satisfaction_overall)

st.header('SLA')
overall_sla = overall_sla_df.iloc[0]['overall_sla'] * 100
st.subheader(f'Overall: {overall_sla:.2f}%')
st.write(period_sla_overall)

st.header('Platform Ratings')
st.write(platform_ratings_df)
