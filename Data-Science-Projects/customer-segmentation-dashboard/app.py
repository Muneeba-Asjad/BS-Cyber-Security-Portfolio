import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import (
    KMeans,
    DBSCAN,
    AgglomerativeClustering
)
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #f6f8fc;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */

.hero {
    background: linear-gradient(135deg, #172554, #1e3a8a);
    padding: 35px 40px;
    border-radius: 22px;
    margin-bottom: 28px;
    color: white;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 17px;
    opacity: 0.88;
}

/* KPI Cards */

[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
}

/* Section */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #172033;
    margin-top: 10px;
    margin-bottom: 18px;
}

/* Cards */

.info-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    margin-bottom: 15px;
}

.info-card h3 {
    margin-top: 0;
    color: #172033;
}

.info-card p {
    color: #64748b;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #f1f5f9;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #172033;
}

/* Upload */

[data-testid="stFileUploader"] {
    background: white;
    border-radius: 14px;
    padding: 10px;
    border: 1px solid #e5e7eb;
}

/* Tables */

[data-testid="stDataFrame"] {
    border-radius: 14px;
}

/* Buttons */

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 650;
    min-height: 42px;
}

/* Alerts */

.stAlert {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
📊 Customer Segmentation & Behavioral Analytics
</div>

<div class="hero-subtitle">
AI-powered customer insights using RFM analysis, dimensionality
reduction and unsupervised machine learning
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SAMPLE DATA
# =========================================================

@st.cache_data
def load_sample_data():

    return pd.read_csv("data/customers.csv")


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 📂 Customer Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload Customer CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.sidebar.success(
        "✅ Uploaded dataset loaded"
    )

else:

    df = load_sample_data()

    st.sidebar.info(
        "Using built-in sample dataset"
    )


st.sidebar.metric(
    "Customers",
    f"{len(df):,}"
)


st.sidebar.markdown("---")

st.sidebar.markdown("## 🧭 Navigation")

page = st.sidebar.radio(
    "Select Dashboard Section",
    [
        "Overview",
        "EDA",
        "RFM Analysis",
        "Customer Segmentation",
        "Algorithm Comparison",
        "Customer Profiles",
        "Business Insights"
    ]
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [
    "CustomerID",
    "Age",
    "Income",
    "Total_Purchases",
    "Total_Spend",
    "Website_Visits",
    "Email_Interactions",
    "Days_Since_Last_Purchase",
    "Avg_Order_Value",
    "Category"
]


missing_columns = [
    col for col in required_columns
    if col not in df.columns
]


if missing_columns:

    st.error(
        "❌ Dataset is missing these required columns:"
    )

    st.write(missing_columns)

    st.stop()


# =========================================================
# PREPROCESSING
# =========================================================

numeric_columns = [
    "Age",
    "Income",
    "Total_Purchases",
    "Total_Spend",
    "Website_Visits",
    "Email_Interactions",
    "Days_Since_Last_Purchase",
    "Avg_Order_Value"
]


for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# Missing values

missing_before = df[numeric_columns].isna().sum().sum()

df[numeric_columns] = df[numeric_columns].fillna(
    df[numeric_columns].median()
)


# Remove duplicates

duplicates = df.duplicated().sum()

df = df.drop_duplicates()


# =========================================================
# OUTLIER TREATMENT USING IQR
# =========================================================

for col in numeric_columns:

    q1 = df[col].quantile(0.25)

    q3 = df[col].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr

    df[col] = df[col].clip(
        lower=lower,
        upper=upper
    )


# =========================================================
# RFM FEATURES
# =========================================================

df["Recency"] = df[
    "Days_Since_Last_Purchase"
]

df["Frequency"] = df[
    "Total_Purchases"
]

df["Monetary"] = df[
    "Total_Spend"
]


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.markdown(
        '<div class="section-title">📌 Business Overview</div>',
        unsafe_allow_html=True
    )

    # KPI cards

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Total Customers",
            f"{len(df):,}"
        )

    with col2:

        st.metric(
            "💰 Total Revenue",
            f"${df['Total_Spend'].sum():,.0f}"
        )

    with col3:

        st.metric(
            "🛒 Average Spend",
            f"${df['Total_Spend'].mean():,.2f}"
        )

    with col4:

        st.metric(
            "🔄 Avg Purchases",
            f"{df['Total_Purchases'].mean():.1f}"
        )


    st.markdown("---")


    # Dataset information

    st.markdown(
        '<div class="section-title">📋 Dataset Preview</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df.head(100),
        use_container_width=True,
        height=380
    )


    st.markdown(
        '<div class="section-title">📈 Customer Behavior</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        fig = px.histogram(
            df,
            x="Total_Spend",
            nbins=35,
            title="Customer Spending Distribution"
        )

        fig.update_layout(
            template="plotly_white",
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.histogram(
            df,
            x="Total_Purchases",
            nbins=30,
            title="Purchase Frequency Distribution"
        )

        fig.update_layout(
            template="plotly_white",
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# EDA
# =========================================================

elif page == "EDA":

    st.markdown(
        '<div class="section-title">🔍 Exploratory Data Analysis</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Missing Values Handled",
            missing_before
        )


    with col2:

        st.metric(
            "Duplicate Rows Removed",
            duplicates
        )


    with col3:

        st.metric(
            "Final Records",
            f"{len(df):,}"
        )


    st.markdown("### 📊 Statistical Summary")

    st.dataframe(
        df[numeric_columns]
        .describe()
        .round(2),
        use_container_width=True
    )


    col1, col2 = st.columns(2)


    with col1:

        fig = px.histogram(
            df,
            x="Age",
            nbins=30,
            title="Customer Age Distribution"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        color_column = (
            "Gender"
            if "Gender" in df.columns
            else None
        )

        fig = px.scatter(
            df,
            x="Income",
            y="Total_Spend",
            color=color_column,
            hover_data=["CustomerID"],
            title="Income vs Total Spending"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Category analysis

    category_spend = (
        df.groupby("Category")["Total_Spend"]
        .sum()
        .reset_index()
        .sort_values(
            "Total_Spend",
            ascending=False
        )
    )


    fig = px.bar(
        category_spend,
        x="Category",
        y="Total_Spend",
        title="Revenue by Product Category"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Correlation

    st.markdown("### 🔗 Correlation Analysis")

    correlation = df[
        numeric_columns
    ].corr()


    fig = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="Feature Correlation Heatmap"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# RFM ANALYSIS
# =========================================================

elif page == "RFM Analysis":

    st.markdown(
        '<div class="section-title">📈 RFM Customer Analysis</div>',
        unsafe_allow_html=True
    )


    st.info(
        "RFM analysis evaluates customers using "
        "Recency, Frequency and Monetary value."
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "📅 Avg Recency",
            f"{df['Recency'].mean():.1f} days"
        )


    with col2:

        st.metric(
            "🛍 Avg Frequency",
            f"{df['Frequency'].mean():.1f}"
        )


    with col3:

        st.metric(
            "💵 Avg Monetary",
            f"${df['Monetary'].mean():,.2f}"
        )


    st.markdown("### 🎯 Customer RFM Behavior")


    sample = df.sample(
        min(1500, len(df)),
        random_state=42
    )


    fig = px.scatter_3d(
        sample,
        x="Recency",
        y="Frequency",
        z="Monetary",
        color="Category",
        hover_data=["CustomerID"],
        title="3D RFM Customer Behavior"
    )

    fig.update_layout(
        height=650
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.markdown("### 📋 RFM Customer Table")


    rfm_table = df[
        [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary"
        ]
    ]


    st.dataframe(
        rfm_table.head(100),
        use_container_width=True
    )


# =========================================================
# CUSTOMER SEGMENTATION
# =========================================================

elif page == "Customer Segmentation":

    st.markdown(
        '<div class="section-title">🤖 Customer Segmentation</div>',
        unsafe_allow_html=True
    )


    features = [
        "Recency",
        "Frequency",
        "Monetary",
        "Website_Visits",
        "Email_Interactions"
    ]


    X = df[features]


    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    # -----------------------------------------------------
    # ELBOW METHOD
    # -----------------------------------------------------

    st.markdown("### 📉 Elbow Method")


    inertias = []


    for k in range(2, 9):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X_scaled)

        inertias.append(
            model.inertia_
        )


    elbow_df = pd.DataFrame({
        "Clusters": range(2, 9),
        "Inertia": inertias
    })


    fig = px.line(
        elbow_df,
        x="Clusters",
        y="Inertia",
        markers=True,
        title="K-Means Elbow Curve"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # CLUSTER SELECTION
    # -----------------------------------------------------

    k = st.slider(
        "🎯 Select Number of Customer Segments",
        min_value=2,
        max_value=8,
        value=4
    )


    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )


    df["Cluster"] = kmeans.fit_predict(
        X_scaled
    )


    # -----------------------------------------------------
    # PCA
    # -----------------------------------------------------

    pca = PCA(
        n_components=2
    )


    pca_result = pca.fit_transform(
        X_scaled
    )


    pca_df = pd.DataFrame({
        "PC1": pca_result[:, 0],
        "PC2": pca_result[:, 1],
        "Cluster": df["Cluster"].astype(str)
    })


    st.markdown("### 🎯 PCA Cluster Visualization")


    fig = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        color="Cluster",
        title="Customer Segments using PCA"
    )


    fig.update_layout(
        template="plotly_white",
        height=550
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # EVALUATION
    # -----------------------------------------------------

    silhouette = silhouette_score(
        X_scaled,
        df["Cluster"]
    )


    db_score = davies_bouldin_score(
        X_scaled,
        df["Cluster"]
    )


    ch_score = calinski_harabasz_score(
        X_scaled,
        df["Cluster"]
    )


    st.markdown("### 📊 Cluster Evaluation")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Silhouette Score",
            f"{silhouette:.3f}"
        )


    with col2:

        st.metric(
            "Davies-Bouldin Index",
            f"{db_score:.3f}"
        )


    with col3:

        st.metric(
            "Calinski-Harabasz",
            f"{ch_score:.1f}"
        )


    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    st.markdown("### 👥 Segment Profile")


    profile = (
        df.groupby("Cluster")[features]
        .mean()
        .round(2)
    )


    st.dataframe(
        profile,
        use_container_width=True
    )


    # -----------------------------------------------------
    # EXPORT
    # -----------------------------------------------------

    st.markdown("### 📥 Export Segmentation Results")


    csv = df.to_csv(
        index=False
    )


    st.download_button(
        "⬇️ Download Segmented Customers",
        data=csv,
        file_name="segmented_customers.csv",
        mime="text/csv"
    )


# =========================================================
# ALGORITHM COMPARISON
# =========================================================

elif page == "Algorithm Comparison":

    st.markdown(
        '<div class="section-title">⚖️ Clustering Algorithm Comparison</div>',
        unsafe_allow_html=True
    )


    features = [
        "Recency",
        "Frequency",
        "Monetary",
        "Website_Visits",
        "Email_Interactions"
    ]


    X_scaled = StandardScaler().fit_transform(
        df[features]
    )


    results = []


    # -----------------------------------------------------
    # K-MEANS
    # -----------------------------------------------------

    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )


    labels = kmeans.fit_predict(
        X_scaled
    )


    results.append([
        "K-Means",
        silhouette_score(
            X_scaled,
            labels
        ),
        davies_bouldin_score(
            X_scaled,
            labels
        ),
        calinski_harabasz_score(
            X_scaled,
            labels
        )
    ])


    # -----------------------------------------------------
    # HIERARCHICAL
    # -----------------------------------------------------

    hierarchical = AgglomerativeClustering(
        n_clusters=4
    )


    labels = hierarchical.fit_predict(
        X_scaled
    )


    results.append([
        "Hierarchical",
        silhouette_score(
            X_scaled,
            labels
        ),
        davies_bouldin_score(
            X_scaled,
            labels
        ),
        calinski_harabasz_score(
            X_scaled,
            labels
        )
    ])


    # -----------------------------------------------------
    # DBSCAN
    # -----------------------------------------------------

    dbscan = DBSCAN(
        eps=0.7,
        min_samples=10
    )


    labels = dbscan.fit_predict(
        X_scaled
    )


    valid = labels != -1


    unique_clusters = set(
        labels[valid]
    )


    if (
        valid.sum() > 0
        and len(unique_clusters) >= 2
    ):

        results.append([
            "DBSCAN",
            silhouette_score(
                X_scaled[valid],
                labels[valid]
            ),
            davies_bouldin_score(
                X_scaled[valid],
                labels[valid]
            ),
            calinski_harabasz_score(
                X_scaled[valid],
                labels[valid]
            )
        ])


    # -----------------------------------------------------
    # GAUSSIAN MIXTURE MODEL
    # -----------------------------------------------------

    gmm = GaussianMixture(
        n_components=4,
        random_state=42
    )


    labels = gmm.fit_predict(
        X_scaled
    )


    results.append([
        "Gaussian Mixture",
        silhouette_score(
            X_scaled,
            labels
        ),
        davies_bouldin_score(
            X_scaled,
            labels
        ),
        calinski_harabasz_score(
            X_scaled,
            labels
        )
    ])


    comparison = pd.DataFrame(
        results,
        columns=[
            "Algorithm",
            "Silhouette Score",
            "Davies-Bouldin Index",
            "Calinski-Harabasz Index"
        ]
    )


    st.markdown("### 📊 Performance Comparison")


    st.dataframe(
        comparison.round(3),
        use_container_width=True
    )


    st.markdown("### 🏆 Silhouette Score Comparison")


    fig = px.bar(
        comparison,
        x="Algorithm",
        y="Silhouette Score",
        title="Clustering Quality"
    )


    fig.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CUSTOMER PROFILES
# =========================================================

elif page == "Customer Profiles":

    st.markdown(
        '<div class="section-title">👥 Customer Segment Profiles</div>',
        unsafe_allow_html=True
    )


    features = [
        "Recency",
        "Frequency",
        "Monetary",
        "Website_Visits",
        "Email_Interactions"
    ]


    X_scaled = StandardScaler().fit_transform(
        df[features]
    )


    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )


    df["Cluster"] = model.fit_predict(
        X_scaled
    )


    profile = (
        df.groupby("Cluster")
        .agg(
            Customers=("CustomerID", "count"),
            Recency=("Recency", "mean"),
            Frequency=("Frequency", "mean"),
            Monetary=("Monetary", "mean"),
            Website_Visits=("Website_Visits", "mean"),
            Email_Interactions=("Email_Interactions", "mean")
        )
        .round(2)
    )


    st.markdown("### 📋 Segment Characteristics")


    st.dataframe(
        profile,
        use_container_width=True
    )


    st.markdown("### 👥 Customer Distribution")


    fig = px.bar(
        profile.reset_index(),
        x="Cluster",
        y="Customers",
        title="Customers per Segment"
    )


    fig.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.markdown("### 💰 Monetary Value by Segment")


    fig = px.bar(
        profile.reset_index(),
        x="Cluster",
        y="Monetary",
        title="Average Monetary Value"
    )


    fig.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "Business Insights":

    st.markdown(
        '<div class="section-title">💡 Business Insights & Recommendations</div>',
        unsafe_allow_html=True
    )


    features = [
        "Recency",
        "Frequency",
        "Monetary",
        "Website_Visits",
        "Email_Interactions"
    ]


    X_scaled = StandardScaler().fit_transform(
        df[features]
    )


    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )


    df["Cluster"] = model.fit_predict(
        X_scaled
    )


    profile = df.groupby(
        "Cluster"
    )[features].mean()


    avg_monetary = profile[
        "Monetary"
    ].mean()


    avg_frequency = profile[
        "Frequency"
    ].mean()


    avg_recency = profile[
        "Recency"
    ].mean()


    st.info(
        "The system automatically analyzes each segment "
        "and generates business recommendations."
    )


    for cluster in profile.index:

        row = profile.loc[cluster]


        # High value

        if (
            row["Monetary"] > avg_monetary
            and row["Frequency"] > avg_frequency
        ):

            st.success(
                f"""
### 🟢 Segment {cluster} — High Value Customers

**Customer Characteristics**
- Higher spending
- Frequent purchases
- Strong customer value

**Recommended Actions**
- Loyalty rewards
- Premium product offers
- Personalized marketing
- VIP membership
"""
            )


        # At risk

        elif row["Recency"] > avg_recency:

            st.warning(
                f"""
### 🟠 Segment {cluster} — At Risk Customers

**Customer Characteristics**
- Longer time since last purchase
- Potential churn risk

**Recommended Actions**
- Re-engagement campaigns
- Limited-time discounts
- Personalized emails
- Churn prevention
"""
            )


        # Regular

        elif row["Frequency"] > avg_frequency:

            st.info(
                f"""
### 🔵 Segment {cluster} — Regular Customers

**Customer Characteristics**
- Frequent purchasing behavior
- Good engagement

**Recommended Actions**
- Cross-selling
- Product recommendations
- Membership programs
- Bundle offers
"""
            )


        # Low engagement

        else:

            st.markdown(
                f"""
<div class="info-card">

<h3>⚪ Segment {cluster} — Low Engagement Customers</h3>

<p><b>Recommended Actions</b></p>

<ul>
<li>Introductory offers</li>
<li>Engagement campaigns</li>
<li>Personalized promotions</li>
<li>Product discovery campaigns</li>
</ul>

</div>
""",
                unsafe_allow_html=True
            )


    st.markdown("### 📊 Segment Summary")


    st.dataframe(
        profile.round(2),
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
<div style="text-align:center; color:#64748b; padding:15px;">
<b>Customer Segmentation & Behavioral Analytics Dashboard</b><br>
Unsupervised Machine Learning • RFM Analytics • Business Intelligence
</div>
""",
    unsafe_allow_html=True
)