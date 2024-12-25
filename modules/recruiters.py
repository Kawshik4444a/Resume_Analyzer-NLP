import streamlit as st
import pandas as pd
from resume_parser import extract_skills,extract_resume_info_from_pdf  # Assuming this function is already defined in your resume_parser module

# Function to load job listings from a CSV file
def load_job_listings(file_path):
    job_listings = pd.read_csv(file_path)
    return job_listings

# Function to display job listings
def display_job_listings(job_listings):
    st.header("Available Job Listings")
    for index, row in job_listings.iterrows():
        st.subheader(f"Job Title: {row['job_title']}")
        st.write(f"Required Skills: {row['required_skills']}")
        st.markdown('<hr>', unsafe_allow_html=True)

# Function to process the recruiters' mode
def process_recruiters_mode():
    st.title("Recruiters Section")

    # Load job listings
    job_listings = load_job_listings('data/job_posting.csv')  # Adjust the path as necessary
    display_job_listings(job_listings)

    # Section to upload resumes for skill extraction
    uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf")

    if uploaded_file:
        st.write("File uploaded successfully!")

        # Extract skills from the uploaded resume
        pdf_text = extract_resume_info_from_pdf(uploaded_file)  # Assuming this function is defined
        skills = extract_skills(pdf_text)  # Extract skills using the existing function

        st.header("Extracted Skills from Resume:")
        st.write(', '.join(skills) if skills else "No skills extracted.")

        # Compare extracted skills with job requirements
        for index, row in job_listings.iterrows():
            required_skills = set(row['required_skills'].split(','))  # Assuming skills are comma-separated
            matched_skills = required_skills.intersection(set(skills))

            if matched_skills:
                st.write(f"Matched Skills for {row['job_title']}: {', '.join(matched_skills)}")
            else:
                st.write(f"No matched skills for {row['job_title']}.")

if __name__ == '__main__':
    process_recruiters_mode()
