import re

# ✅ Extract relevant skills from a job description using a keyword list
def extract_skills_from_job(job_description):
    skill_keywords = [
        "python", "sql", "excel", "tableau", "power bi", "numpy", "pandas",
        "scikit-learn", "tensorflow", "keras", "flask", "django", "nlp",
        "data visualization", "machine learning", "deep learning",
        "matplotlib", "seaborn", "api", "git", "linux"
    ]

    found_skills = []
    description_lower = job_description.lower()

    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', description_lower):
            found_skills.append(skill)

    return found_skills

# ✅ Compare job-required skills with resume skills
def find_skill_gap(resume_skills, job_required_skills):
    resume_skills_lower = [skill.lower() for skill in resume_skills]
    missing = list(set(job_required_skills) - set(resume_skills_lower))
    return missing
