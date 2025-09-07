# create_jobs.py
from jobapp.models import CustomUser, Job, Application
from django.db import transaction
import os

# Create media folder if not exists
os.makedirs('media/resumes', exist_ok=True)

# Dummy resume
resume_path = 'media/resumes/sample_resume.pdf'
with open(resume_path, 'w') as f:
    f.write("This is a sample resume.")

# Start transaction
with transaction.atomic():
    # Delete old data
    Application.objects.all().delete()
    Job.objects.all().delete()
    CustomUser.objects.filter(username__in=['Nisha', 'Applicant1']).delete()

    # Create users
    employer = CustomUser.objects.create_user(
        username='Nisha',
        email='nisha@example.com',
        password='StrongPassword123',
        role='employer',
        is_staff=True
    )

    applicant = CustomUser.objects.create_user(
        username='Applicant1',
        email='applicant1@example.com',
        password='ApplicantPass123',
        role='applicant'
    )

    # Create jobs
    jobs_data = [
        {"title": "Backend Developer", "company": "TechCorp", "location": "Doha, Qatar",
         "description": "Develop APIs using Django and Python."},
        {"title": "Frontend Engineer", "company": "InnovateX", "location": "Doha, Qatar",
         "description": "Expert in React.js and modern frontend frameworks required."},
        {"title": "Data Analyst", "company": "DataSolutions", "location": "Doha, Qatar",
         "description": "Analyze and interpret complex datasets to help business decisions."},
    ]

    created_jobs = [Job.objects.create(**job, created_by=employer) for job in jobs_data]

    # Submit application for the first job
    application = Application.objects.create(
        job=created_jobs[0],
        applicant=applicant,
        resume='resumes/sample_resume.pdf',
        cover_letter='I am very interested in this position.'
    )

print("✅ Setup complete")
print("Jobs:", Job.objects.all())
print("Application:", application)
