import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Load Files
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("models/churn_prediction_model.pkl")


@st.cache_data
def load_data():
    return pd.read_csv("data/customer_churn_processed.csv")


@st.cache_data
def load_importance():
    return pd.read_csv("data/feature_importance.csv")


@st.cache_data
def load_metrics():
    return pd.read_csv("data/model_performance.csv")


model = load_model()
df = load_data()
feature_importance = load_importance()
metrics = load_metrics()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 Customer Churn Prediction & Retention Analytics")

st.write(
    "Machine Learning system for identifying customers "
    "at risk of churn and generating retention insights."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Churn Prediction",
        "Model Performance",
        "Customer Insights"
    ]
)


# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    st.header("📈 Customer Churn Dashboard")

    total_customers = len(df)

    churned_customers = int(df["Churn"].sum())

    churn_rate = (
        churned_customers / total_customers * 100
    )

    avg_monthly_charges = df["MonthlyCharges"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Customers",
        total_customers
    )

    col2.metric(
        "Churned Customers",
        churned_customers
    )

    col3.metric(
        "Churn Rate",
        f"{churn_rate:.1f}%"
    )

    col4.metric(
        "Avg Monthly Charges",
        f"${avg_monthly_charges:.2f}"
    )

    st.divider()

    # Churn distribution

    st.subheader("Customer Churn Distribution")

    churn_counts = df["Churn"].value_counts()

    churn_labels = ["Active", "Churned"]

    churn_values = [
        churn_counts.get(0, 0),
        churn_counts.get(1, 0)
    ]

    fig, ax = plt.subplots()

    ax.bar(
        churn_labels,
        churn_values
    )

    ax.set_ylabel("Number of Customers")
    ax.set_title("Churn Distribution")

    st.pyplot(fig)


# ==================================================
# CHURN PREDICTION
# ==================================================

elif page == "Churn Prediction":

    st.header("🔮 Customer Churn Prediction")

    st.write(
        "Enter customer information to estimate churn risk."
    )

    col1, col2 = st.columns(2)

    with col1:

        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        senior_citizen = st.selectbox(
            "Senior Citizen",
            [0, 1]
        )

        partner = st.selectbox(
            "Partner",
            ["Yes", "No"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"]
        )

        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=72,
            value=12
        )

        phone_service = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["Yes", "No", "No phone service"]
        )

        internet_service = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

        online_security = st.selectbox(
            "Online Security",
            ["Yes", "No", "No internet service"]
        )

        online_backup = st.selectbox(
            "Online Backup",
            ["Yes", "No", "No internet service"]
        )

    with col2:

        device_protection = st.selectbox(
            "Device Protection",
            ["Yes", "No", "No internet service"]
        )

        tech_support = st.selectbox(
            "Tech Support",
            ["Yes", "No", "No internet service"]
        )

        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No", "No internet service"]
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No", "No internet service"]
        )

        contract = st.selectbox(
            "Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )

        paperless_billing = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=70.0
        )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=monthly_charges * tenure
        )

    # --------------------------------------------------
    # Feature Engineering
    # --------------------------------------------------

    if tenure <= 12:
        tenure_segment = "New Customer"
    elif tenure <= 48:
        tenure_segment = "Regular Customer"
    else:
        tenure_segment = "Loyal Customer"

    if monthly_charges <= df["MonthlyCharges"].quantile(0.33):
        monthly_category = "Low Spend"
    elif monthly_charges <= df["MonthlyCharges"].quantile(0.66):
        monthly_category = "Medium Spend"
    else:
        monthly_category = "High Spend"

    total_revenue = monthly_charges * tenure

    service_values = [
        phone_service,
        multiple_lines,
        internet_service,
        online_security,
        online_backup,
        device_protection,
        tech_support,
        streaming_tv,
        streaming_movies
    ]

    service_count = sum(
        value in ["Yes", "DSL", "Fiber optic"]
        for value in service_values
    )

    contract_risk = {
        "Month-to-month": 3,
        "One year": 2,
        "Two year": 1
    }

    contract_risk_score = contract_risk[contract]

    # --------------------------------------------------
    # Create Input DataFrame
    # --------------------------------------------------

    input_data = pd.DataFrame({
        "gender": [gender],
        "SeniorCitizen": [senior_citizen],
        "Partner": [partner],
        "Dependents": [dependents],
        "tenure": [tenure],
        "PhoneService": [phone_service],
        "MultipleLines": [multiple_lines],
        "InternetService": [internet_service],
        "OnlineSecurity": [online_security],
        "OnlineBackup": [online_backup],
        "DeviceProtection": [device_protection],
        "TechSupport": [tech_support],
        "StreamingTV": [streaming_tv],
        "StreamingMovies": [streaming_movies],
        "Contract": [contract],
        "PaperlessBilling": [paperless_billing],
        "PaymentMethod": [payment_method],
        "MonthlyCharges": [monthly_charges],
        "TotalCharges": [total_charges],
        "TenureSegment": [tenure_segment],
        "MonthlyChargesCategory": [monthly_category],
        "TotalRevenue": [total_revenue],
        "ServiceCount": [service_count],
        "ContractRiskScore": [contract_risk_score]
    })

    st.divider()

    if st.button(
        "🔮 Predict Churn",
        type="primary"
    ):

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(
            input_data
        )[0][1]

        st.subheader("Prediction Result")

        if prediction == 1:

            st.error(
                f"⚠️ High Churn Risk — "
                f"{probability * 100:.1f}% probability"
            )

            st.warning(
                "Retention Action: Contact the customer, "
                "offer a suitable contract upgrade or "
                "personalized retention incentive."
            )

        else:

            st.success(
                f"✅ Low Churn Risk — "
                f"{(1 - probability) * 100:.1f}% retention probability"
            )

            st.info(
                "Customer appears relatively stable. "
                "Continue engagement and service monitoring."
            )


# ==================================================
# MODEL PERFORMANCE
# ==================================================

elif page == "Model Performance":

    st.header("🤖 Machine Learning Model Performance")

    st.dataframe(
        metrics.round(4),
        use_container_width=True
    )

    st.subheader("Performance Comparison")

    chart_data = metrics.set_index("Model")[
        [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC-AUC"
        ]
    ]

    st.bar_chart(chart_data)


# ==================================================
# CUSTOMER INSIGHTS
# ==================================================

elif page == "Customer Insights":

    st.header("💡 Customer Churn Insights")

    st.subheader("Top Factors Influencing Churn")

    top_features = feature_importance.head(10)

    st.dataframe(
        top_features,
        use_container_width=True
    )

    st.subheader("Feature Importance")

    plot_data = top_features.sort_values(
        "Importance"
    )

    fig, ax = plt.subplots()

    ax.barh(
        plot_data["Feature"],
        plot_data["Importance"]
    )

    ax.set_xlabel("Importance")
    ax.set_title(
        "Top 10 Features Influencing Customer Churn"
    )

    st.pyplot(fig)

    st.subheader("Retention Recommendations")

    st.markdown(
        """
        **1. Focus on month-to-month customers**

        Customers with flexible contracts generally require
        stronger retention engagement.

        **2. Monitor high monthly charges**

        High spending customers should receive personalized
        offers and loyalty benefits.

        **3. Encourage longer contracts**

        One-year and two-year contracts can improve customer
        retention.

        **4. Monitor service usage**

        Customers using fewer services may have greater
        opportunities for engagement and targeted offers.

        **5. Prioritize high-risk customers**

        Customers with high predicted churn probability
        should receive proactive retention campaigns.
        """
    )