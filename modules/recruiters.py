import streamlit as st
import pandas as pd
from resume_parser import extract_skills, extract_resume_info_from_pdf  # Assuming this function is already defined in your resume_parser module

# Function to load job listings from a CSV file
def load_job_listings(file_path):
    job_listings = pd.read_csv(file_path)
    return job_listings

# Function to display job listings
def display_job_listings(job_listings):
    st.markdown('<h2 style="color: #FF6347;">Available Job Listings</h2>', unsafe_allow_html=True)
    for index, row in job_listings.iterrows():
        st.markdown(f"""
        <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <h4 style="color: #4CAF50;">Job Title: {row['job_title']}</h4>
            <p><strong>Required Skills:</strong> {row['required_skills']}</p>
        </div>
        """, unsafe_allow_html=True)

# Function to process the recruiters' mode
def process_recruiters_mode():
    # Page title and custom header
    st.markdown('<h1 style="text-align: center; color: #4682B4;">Recruiters Section</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #808080;">Upload resumes to check job compatibility</p>', unsafe_allow_html=True)
    
    # Load job listings
    job_listings = load_job_listings('data/job_posting.csv')  # Adjust the path as necessary
    display_job_listings(job_listings)

    # Section to upload resumes for skill extraction
    uploaded_file = st.file_uploader(
        label="Upload a PDF Resume", 
        type="pdf", 
        label_visibility="visible",
        help="Upload a PDF resume to analyze and match with job listings."
    )

    if uploaded_file:
        st.success("File uploaded successfully! Processing resume...")
        
        # Extract skills from the uploaded resume
        pdf_text = extract_resume_info_from_pdf(uploaded_file)  # Assuming this function is defined
        skills = extract_skills(pdf_text)  # Extract skills using the existing function

        st.markdown('<h3 style="color: #FF8C00;">Extracted Skills from Resume:</h3>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: #F0FFF0; padding: 10px; border-radius: 5px;">
            {', '.join(skills) if skills else "<em>No skills extracted.</em>"}
        </div>
        """, unsafe_allow_html=True)

        # Check if resume matches all required skills for any job
        matching_jobs = []
        for index, row in job_listings.iterrows():
            required_skills = set(row['required_skills'].split(','))  # Assuming skills are comma-separated
            missing_skills = required_skills - set(skills)  # Skills that are required but not in the resume

            if not missing_skills:  # If there are no missing skills, the resume is a match
                matching_jobs.append(row)

        if matching_jobs:
            st.markdown('<h3 style="color: #2E8B57;">Jobs You Can Apply To:</h3>', unsafe_allow_html=True)
            for job in matching_jobs:
                st.markdown(f"""
                <div style="background-color: #FFFACD; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <h4>{job['job_title']}</h4>
                    <p><strong>Required Skills:</strong> {job['required_skills']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<h3 style="color: #FF4500;">No Jobs Match Your Resume</h3>', unsafe_allow_html=True)
            st.info("Your resume doesn't meet the required skills for any job listings.")

if __name__ == '__main__':
    process_recruiters_mode()
