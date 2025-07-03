from flask import Flask, request, render_template
import os
import spacy
from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx
from parser.nlp_parser import parse_resume
from matcher.job_matcher import load_job_descriptions, match_jobs
from matcher.skill_gap import extract_skills_from_job, find_skill_gap
from matcher.learning_path import get_learning_resources

# ✅ Ensure Spacy model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# ✅ Flask App Config
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files.get('resume_file')
    if not file:
        return "No file uploaded", 400

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # ✅ Extract text
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        return "Unsupported file format. Only PDF and DOCX allowed.", 400

    # ✅ Parse resume and get matches
    parsed_data = parse_resume(text)
    resume_blob = " ".join(parsed_data["skills"] + parsed_data["experience"] + parsed_data["projects"])
    job_data = load_job_descriptions()
    matched_jobs = match_jobs(resume_blob, job_data)

    # ✅ Build HTML response
    html = """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <title>Smart Career Advisor | Results</title>
        <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'>
        <style>
            body { background-color: #f5f9fc; font-family: 'Segoe UI', sans-serif; }
            .card { margin-bottom: 20px; border-radius: 15px; box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
    <div class='container mt-5'>
        <h2 class='mb-4 text-center'>🔍 Top Job Matches</h2>
    """

    for job in matched_jobs[:5]:
        job_skills = extract_skills_from_job(job["description"])
        skill_gap = find_skill_gap(parsed_data["skills"], job_skills)
        learning_path = get_learning_resources(skill_gap)

        html += "<div class='card p-4'>"
        html += f"<h4>{job['title']} <small class='text-muted'>at {job['company']}</small></h4>"
        html += f"<p><b>Match Score:</b> {job['score']}%</p>"
        html += f"<p>{job['description']}</p>"

        if skill_gap:
            html += f"<p><b class='text-danger'>Skill Gap:</b> "
            html += " ".join([f"<span class='badge bg-danger'>{skill}</span>" for skill in skill_gap])
            html += "</p>"

            if learning_path:
                html += f"<p><b class='text-primary'>Suggested Learning Resources:</b></p><ul>"
                for skill, link in learning_path.items():
                    html += f"<li><a href='{link}' target='_blank'>{skill.title()}</a></li>"
                html += "</ul>"
        else:
            html += "<p class='text-success'><b>You meet all required skills!</b></p>"

        html += "</div>"

    html += """
        <div class='text-center mt-4'>
            <a href='/' class='btn btn-secondary'>🔙 Upload Another Resume</a>
        </div>
    </div>
    </body>
    </html>
    """

    return html

# ✅ Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
