import spacy
import re
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

# Example skills list (you can expand this)
SKILLS_DB = [
    "python", "java", "c++", "machine learning", "data analysis", "deep learning",
    "nlp", "sql", "flask", "django", "pandas", "numpy", "excel", "javascript"
]

def extract_name(resume_text):
    doc = nlp(resume_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return ""

def extract_skills(resume_text):
    skills = []
    resume_text = resume_text.lower()
    for skill in SKILLS_DB:
        if skill.lower() in resume_text and skill not in skills:
            skills.append(skill)
    return skills

def extract_education(resume_text):
    education_keywords = ['btech', 'b.e', 'mtech', 'msc', 'b.sc', 'mca', 'phd']
    education = []
    lines = resume_text.lower().split("\n")
    for line in lines:
        if any(edu in line for edu in education_keywords):
            education.append(line.strip())
    return education

def extract_experience(resume_text):
    experience = []
    experience_keywords = ["experience", "worked", "internship", "role", "company"]
    lines = resume_text.lower().split("\n")
    for line in lines:
        if any(word in line for word in experience_keywords):
            experience.append(line.strip())
    return experience

def extract_projects(resume_text):
    projects = []
    lines = resume_text.split("\n")
    for line in lines:
        if "project" in line.lower():
            projects.append(line.strip())
    return projects

def parse_resume(resume_text):
    return {
        "name": extract_name(resume_text),
        "skills": extract_skills(resume_text),
        "education": extract_education(resume_text),
        "experience": extract_experience(resume_text),
        "projects": extract_projects(resume_text)
    }
