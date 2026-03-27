import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI ROI Calculator", layout="wide")

st.title("AI ROI Calculator Dashboard")
st.write("Adjust the inputs below to calculate the expected return on investment.")

# Sidebar for Interactive Inputs
st.sidebar.header("Input Parameters")

# General Inputs
st.sidebar.subheader("General")
num_locations = st.sidebar.number_input("Number of Locations", min_value=1, value=10)
ops_per_location = st.sidebar.number_input("Operatories per Location", min_value=1, value=6)
avg_rev = st.sidebar.number_input("Avg Revenue per Operatory per Day ($)", min_value=0, value=1200)

# Downtime
st.sidebar.subheader("Downtime")
downtime_days = st.sidebar.number_input("Current Downtime (days/year/operator)", min_value=0.0, value=5.0)
downtime_red = st.sidebar.slider("% Downtime Reduction", 0.0, 1.0, 0.3)

# Repairs
st.sidebar.subheader("Repairs")
repair_cost = st.sidebar.number_input("Annual Repair Cost per Location ($)", min_value=0, value=15000)
repair_red = st.sidebar.slider("% Repair Cost Reduction", 0.0, 1.0, 0.2)

# Admin
st.sidebar.subheader("Admin")
admin_hours = st.sidebar.number_input("Admin Hours per Month per Location", min_value=0, value=20)
admin_cost = st.sidebar.number_input("Hourly Admin Cost ($)", min_value=0, value=25)
admin_red = st.sidebar.slider("% Admin Time Reduction", 0.0, 1.0, 0.25)

# Compliance
st.sidebar.subheader("Compliance")
comp_cost = st.sidebar.number_input("Annual Compliance Cost per Location ($)", min_value=0, value=5000)
comp_red = st.sidebar.slider("% Compliance Cost Reduction", 0.0, 1.0, 0.5)

# Software
st.sidebar.subheader("Software")
software_cost_per_loc = st.sidebar.number_input("UptimeHealth Cost per Location ($)", min_value=0, value=3000)

# --- CALCULATIONS ---
downtime_rev_loss = avg_rev * ops_per_location * downtime_days
recovered_rev_per_loc = downtime_rev_loss * downtime_red
total_downtime_recovery = recovered_rev_per_loc * num_locations

repair_savings_per_loc = repair_cost * repair_red
total_repair_savings = repair_savings_per_loc * num_locations

annual_admin_cost_per_loc = admin_hours * 12 * admin_cost
admin_savings_per_loc = annual_admin_cost_per_loc * admin_red
total_admin_savings = admin_savings_per_loc * num_locations

comp_savings_per_loc = comp_cost * comp_red
total_comp_savings = comp_savings_per_loc * num_locations

total_software_cost = num_locations * software_cost_per_loc

# --- RESULTS ---
total_annual_benefit = total_downtime_recovery + total_repair_savings + total_admin_savings + total_comp_savings
net_benefit = total_annual_benefit - total_software_cost

roi_pct = (net_benefit / total_software_cost) * 100 if total_software_cost > 0 else 0
payback_months = (total_software_cost / total_annual_benefit) * 12 if total_annual_benefit > 0 else 0

# --- DASHBOARD DISPLAY ---
st.subheader("ROI Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Annual Benefit", f"${total_annual_benefit:,.0f}")
col2.metric("Net Benefit", f"${net_benefit:,.0f}")
col3.metric("ROI", f"{roi_pct:,.0f}%")
col4.metric("Payback (Months)", f"{payback_months:,.1f}")

st.divider()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Savings Breakdown")
    breakdown_data = pd.DataFrame({
        "Category": ["Downtime Recovery", "Repair Savings", "Admin Savings", "Compliance Savings"],
        "Amount ($)": [total_downtime_recovery, total_repair_savings, total_admin_savings, total_comp_savings]
    })
    st.bar_chart(breakdown_data.set_index("Category"))

with col_chart2:
    st.subheader("Costs vs Benefits")
    cost_benefit_data = pd.DataFrame({
        "Category": ["Total Software Cost", "Total Annual Benefit"],
        "Amount ($)": [total_software_cost, total_annual_benefit]
    })
    st.bar_chart(cost_benefit_data.set_index("Category"))
