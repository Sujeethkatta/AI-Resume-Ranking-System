import os
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils import preprocess_text

vectorizer = joblib.load("model/vectorizer.pkl")

SKILLS = [
    "python", "java", "machine learning", "deep learning",
    "flask", "django", "react", "sql", "mysql",
    "tensorflow", "pytorch", "nlp"
]

def extract_skills(text):
    found_skills = []
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)
    return found_skills

def rank_resumes(job_description, resumes):
    job_description = preprocess_text(job_description)

    results = []

    for name, text in resumes:
        processed_resume = preprocess_text(text)

        vectors = vectorizer.transform([processed_resume, job_description])
        similarity = cosine_similarity(vectors[0], vectors[1])
        score = round(float(similarity[0][0]) * 100, 2)

        matched_skills = extract_skills(processed_resume)

        results.append((name, score, matched_skills))

    ranked = sorted(results, key=lambda x: x[1], reverse=True)

    # ✅ CREATE UPLOADS FOLDER IF NOT EXISTS
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    df = pd.DataFrame(
        [(r[0], r[1]) for r in ranked],
        columns=["Resume", "Score (%)"]
    )

    df.to_csv("uploads/ranked_results.csv", index=False)

    return ranked