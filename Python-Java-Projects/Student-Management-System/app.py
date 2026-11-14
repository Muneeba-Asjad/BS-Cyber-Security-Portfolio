import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"


def get_connection():
    return sqlite3.connect(DB_PATH)


# --------------------------------------------------
# Database Helper Functions
# --------------------------------------------------

def get_count(table_name):
    try:
        conn = get_connection()

        query = f"SELECT COUNT(*) AS count FROM {table_name}"
        result = pd.read_sql_query(query, conn)

        conn.close()

        return int(result["count"].iloc[0])

    except Exception:
        return 0


def get_data(table_name):
    try:
        conn = get_connection()

        df = pd.read_sql_query(
            f"SELECT * FROM {table_name}",
            conn
        )

        conn.close()

        return df

    except Exception as e:
        st.error(f"Unable to load data: {e}")
        return pd.DataFrame()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🎓 Student Management System")
st.write("Welcome to the Student Management System")

st.divider()


# --------------------------------------------------
# Dashboard Statistics
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👨‍🎓 Students",
        get_count("students_student")
    )

with col2:
    st.metric(
        "👨‍🏫 Teachers",
        get_count("students_teacher")
    )

with col3:
    st.metric(
        "📚 Courses",
        get_count("students_course")
    )

with col4:
    st.metric(
        "📋 Attendance Records",
        get_count("students_attendance")
    )


st.divider()


# --------------------------------------------------
# Quick Access
# --------------------------------------------------

st.subheader("📊 Quick Access")

option = st.selectbox(
    "Select a section",
    [
        "Dashboard",
        "Students",
        "Teachers",
        "Courses",
        "Attendance",
        "Academic Results"
    ]
)


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

if option == "Dashboard":

    st.info(
        "Select a section from the dropdown above "
        "to view the records."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 System Overview")

        st.write(
            f"Total Students: **{get_count('students_student')}**"
        )

        st.write(
            f"Total Teachers: **{get_count('students_teacher')}**"
        )

        st.write(
            f"Total Courses: **{get_count('students_course')}**"
        )

    with col2:
        st.subheader("📋 Academic Information")

        st.write(
            f"Attendance Records: **{get_count('students_attendance')}**"
        )

        st.write(
            f"Academic Results: **{get_count('students_result')}**"
        )


# --------------------------------------------------
# Students
# --------------------------------------------------

elif option == "Students":

    st.subheader("👨‍🎓 Students")

    df = get_data("students_student")

    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No student records found.")


# --------------------------------------------------
# Teachers
# --------------------------------------------------

elif option == "Teachers":

    st.subheader("👨‍🏫 Teachers")

    df = get_data("students_teacher")

    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No teacher records found.")


# --------------------------------------------------
# Courses
# --------------------------------------------------

elif option == "Courses":

    st.subheader("📚 Courses")

    df = get_data("students_course")

    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No course records found.")


# --------------------------------------------------
# Attendance
# --------------------------------------------------

elif option == "Attendance":

    st.subheader("📋 Attendance Records")

    df = get_data("students_attendance")

    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No attendance records found.")


# --------------------------------------------------
# Academic Results
# --------------------------------------------------

elif option == "Academic Results":

    st.subheader("🎓 Academic Results")

    df = get_data("students_result")

    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No academic results found.")


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption("Student Management System | Django + SQLite + Streamlit")