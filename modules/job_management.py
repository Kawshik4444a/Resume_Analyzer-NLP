import streamlit as st
import sqlite3

# Function to create the jobs table in the database
def create_jobs_table():
    """
    Creates the `jobs` table in `jobs.db` if it doesn't exist.
    """
    conn = sqlite3.connect('data/jobs.db')
    cursor = conn.cursor()
    
    # Create the jobs table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            job_title TEXT NOT NULL,
            required_skills TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a job into the jobs table
def insert_job(job_title, required_skills):
    """
    Inserts a new job with its required skills into the `jobs` table.
    """
    conn = sqlite3.connect('data/jobs.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO jobs (job_title, required_skills) VALUES (?, ?)', (job_title, required_skills))
    conn.commit()
    conn.close()

# Function to display the existing jobs
def display_jobs():
    """
    Fetches and displays all jobs stored in the `jobs` table.
    """
    conn = sqlite3.connect('data/jobs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT job_title, required_skills FROM jobs')
    jobs = cursor.fetchall()
    conn.close()

    if jobs:
        st.header("Existing Jobs")
        for job in jobs:
            st.write(f"**Job Title:** {job[0]}")
            st.write(f"**Required Skills:** {job[1]}")
            st.markdown("---")
    else:
        st.write("No jobs available yet. Please add some jobs!")

# Function to handle the recruiter interface
def process_recruiters_mode():
    """
    Handles the recruiter mode in Streamlit.
    Allows recruiters to add new jobs and view existing jobs.
    """
    create_jobs_table()  # Ensure the jobs table exists

    st.title("Recruiter Portal")
    st.header("Add a New Job")

    job_title = st.text_input("Job Title")
    required_skills = st.text_area("Required Skills (comma-separated)")

    if st.button("Add Job"):
        if job_title and required_skills:
            insert_job(job_title, required_skills)
            st.success("Job added successfully!")
        else:
            st.error("Please fill in both fields.")

    # Display existing jobs from the database
    display_jobs()

if __name__ == "__main__":
    process_recruiters_mode()
