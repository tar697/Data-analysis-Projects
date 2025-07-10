import streamlit as st
import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="📊 PhonePe Insights Dashboard", layout="wide")

st.title("📱 PhonePe Transaction Insights Dashboard")
st.markdown("Explore user engagement, transaction patterns, and growth trends using real PhonePe Pulse data.")

# Connect to DB
conn = sqlite3.connect("phonepe_pulse.db")

# Sidebar - Case Study Selector
case_study = st.sidebar.selectbox(
    "Select Case Study", 
    [
        "1️⃣ Transaction Trends by State & Category",
        "2️⃣ Device Dominance and Engagement",
        "4️⃣ Market Expansion (State-Level)",
        "5️⃣ User Engagement & Growth",
        "6️⃣ User Registration Trends"
    ]
)

# CASE STUDY 1
if case_study.startswith("1️⃣"):
    st.header("📈 Transaction Trends by Category and State")

    df = pd.read_sql("""
        SELECT year, quarter, transaction_type, SUM(transaction_amount) AS amount
        FROM aggregated_transaction
        GROUP BY year, quarter, transaction_type
    """, conn)

    df["period"] = df["year"].astype(str) + " Q" + df["quarter"].astype(str)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x="period", y="amount", hue="transaction_type", marker="o", ax=ax)
    plt.xticks(rotation=45)
    plt.title("Transaction Amount by Category Over Time")
    st.pyplot(fig)

# CASE STUDY 2: User Engagement State-wise (No Device Info)
elif case_study.startswith("2️⃣"):
    st.header("📱 User Engagement Across States")

    df = pd.read_sql("""
        SELECT state, 
               SUM(registered_users) AS total_users,
               SUM(app_opens) AS total_opens
        FROM aggregated_user
        GROUP BY state
        HAVING total_users > 0
        ORDER BY total_users DESC
    """, conn)

    df["engagement_ratio"] = df["total_opens"] / df["total_users"]

    # Plot 1: Top 10 states by app opens
    top_states = df.sort_values(by="total_opens", ascending=False).head(10)
    st.subheader("📲 Top 10 States by App Opens")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_states, x="total_opens", y="state", palette="Purples_r", ax=ax)
    ax.set_title("Top States by App Opens")
    st.pyplot(fig)

    # Plot 2: Engagement Ratio
    st.subheader("📊 Engagement Ratio by State (App Opens / Users)")

    top_ratio = df.sort_values(by="engagement_ratio", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_ratio, x="engagement_ratio", y="state", palette="coolwarm", ax=ax)
    ax.set_title("Top States by User Engagement Ratio")
    st.pyplot(fig)


# CASE STUDY 4
elif case_study.startswith("4️⃣"):
    st.header("🗺️ Market Expansion by State")
    df = pd.read_sql("""
        SELECT state, SUM(transaction_amount) AS total_amount
        FROM aggregated_transaction
        GROUP BY state
        ORDER BY total_amount DESC
        LIMIT 10;
    """, conn)

    st.subheader("Top 10 States by Transaction Value")
    st.dataframe(df)

    fig, ax = plt.subplots()
    sns.barplot(data=df, x="total_amount", y="state", palette="crest", ax=ax)
    ax.set_title("Top States by Transaction Volume")
    st.pyplot(fig)

# CASE STUDY 5
elif case_study.startswith("5️⃣"):
    st.header("📈 User Engagement Across States")
    df = pd.read_sql("""
        SELECT state, SUM(registered_users) AS users, SUM(app_opens) AS opens
        FROM aggregated_user
        GROUP BY state
        ORDER BY users DESC;
    """, conn)

    st.subheader("Top 10 States by Registered Users")
    top_states = df.head(10)
    fig, ax = plt.subplots()
    sns.barplot(data=top_states, x="users", y="state", palette="Blues", ax=ax)
    ax.set_title("Top States by Registered Users")
    st.pyplot(fig)

    st.subheader("Engagement Scatter: Users vs App Opens")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="users", y="opens", hue="state", legend=False, ax=ax)
    ax.set_title("App Opens vs Registered Users")
    st.pyplot(fig)

# CASE STUDY 6
elif case_study.startswith("6️⃣"):
    st.header("📊 User Registration Trends Over Time")
    df = pd.read_sql("""
        SELECT year, quarter, SUM(registered_users) AS total_users
        FROM aggregated_user
        GROUP BY year, quarter
    """, conn)

    df["period"] = df["year"].astype(str) + " Q" + df["quarter"].astype(str)
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="period", y="total_users", marker="o", color="green", ax=ax)
    ax.set_title("Quarterly User Registrations")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("© 2025 | Streamlit Dashboard for PhonePe Pulse Insights | Built by Taruna")
