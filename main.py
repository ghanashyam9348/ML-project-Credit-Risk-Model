import streamlit as st
from prediction_helper import predict

# Set the page config
st.set_page_config(page_title="CrediSure: Credit Risk Modeling", page_icon="📊", layout="wide")

# App title and subtitle
st.title("📊 CrediSure")
st.markdown("### Intelligent Credit Risk Modeling for Smarter Lending Decisions")

st.markdown("---")

# Input Section
st.header("📝 Applicant Financial Details")

# Input Columns
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("🎂 Age", min_value=18, max_value=100, step=1, value=28)
with col2:
    income = st.number_input("💼 Annual Income (₹)", min_value=0, value=1_200_000)
with col3:
    loan_amount = st.number_input("🏦 Loan Amount (₹)", min_value=0, value=2_560_000)

# Loan-to-Income Ratio
loan_to_income_ratio = loan_amount / income if income > 0 else 0
st.markdown("##### 💰 Loan to Income Ratio")
st.metric(label="LTI Ratio", value=f"{loan_to_income_ratio:.2f}")

# More Inputs
st.header("📊 Credit Behavior Metrics")

col4, col5, col6 = st.columns(3)

with col4:
    loan_tenure_months = st.number_input("⏳ Loan Tenure (months)", min_value=0, step=1, value=36)
with col5:
    avg_dpd_per_delinquency = st.number_input("📉 Avg Days Past Due (DPD)", min_value=0, value=20)
with col6:
    delinquency_ratio = st.number_input("📛 Delinquency Ratio (%)", min_value=0, max_value=100, step=1, value=30)

col7, col8, col9 = st.columns(3)

with col7:
    credit_utilization_ratio = st.number_input("📈 Credit Utilization Ratio (%)", min_value=0, max_value=100, step=1, value=30)
with col8:
    num_open_accounts = st.number_input("📂 Open Loan Accounts", min_value=1, max_value=4, step=1, value=2)
with col9:
    residence_type = st.selectbox("🏠 Residence Type", ['Owned', 'Rented', 'Mortgage'])

col10, col11, col12 = st.columns(3)

with col10:
    loan_purpose = st.selectbox("🎯 Loan Purpose", ['Education', 'Home', 'Auto', 'Personal'])
with col11:
    loan_type = st.selectbox("🔐 Loan Type", ['Unsecured', 'Secured'])

st.markdown("---")

# Predict Button
if st.button("🚀 Calculate Risk"):
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    st.success("✅ Prediction Completed!")

    colA, colB, colC = st.columns(3)
    with colA:
        st.metric(label="📉 Default Probability", value=f"{probability:.2%}")
    with colB:
        st.metric(label="💳 Credit Score", value=credit_score)
    with colC:
        st.metric(label="🏷️ Rating", value=rating)

# Optional Footer
st.markdown("---")
st.caption("🔍 Built with ❤️ using Streamlit and Machine Learning · Project: CrediSure")
