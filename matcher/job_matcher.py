import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ This is the function your app is trying to import
def load_job_descriptions(path='jobs/jobs.json'):
    with open(path, 'r') as file:
        return json.load(file)

# ✅ This is the second function your app uses
def match_jobs(resume_text, job_descriptions):
    all_docs = [resume_text] + [job["description"] for job in job_descriptions]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_docs)

    resume_vec = tfidf_matrix[0]
    job_vecs = tfidf_matrix[1:]

    similarity_scores = cosine_similarity(resume_vec, job_vecs)[0]

    results = []
    for i, job in enumerate(job_descriptions):
        results.append({
            "title": job["title"],
            "company": job["company"],
            "score": round(similarity_scores[i] * 100, 2),
            "description": job["description"]
        })

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return sorted_results
