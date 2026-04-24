from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python", "java", "c++", "c", "sql", "mysql", "postgresql",
    "machine learning", "data science", "artificial intelligence", "nlp",
    "flask", "django", "html", "css", "javascript", "typescript",
    "react", "node", "git", "docker", "kubernetes", "aws", "azure"
]

def extract_skills(text):
    found_skills = []
    text_lower = text.lower()
    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill)
    return set(found_skills)

def calculate_skill_match(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    if len(job_skills) == 0:
        return 0

    matched = resume_skills.intersection(job_skills)
    return (len(matched) / len(job_skills)) * 100

def calculate_text_match(resume_text, job_text):
    if not resume_text.strip() or not job_text.strip():
        return 0.0
    
    vectorizer = TfidfVectorizer()
    # Adding a safety check in case the text is extremely short and has no valid vocabulary
    try:
        matrix = vectorizer.fit_transform([resume_text, job_text])
        similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return similarity * 100
    except ValueError:
        return 0.0

def calculate_match(resume_text, job_text):
    text_score = calculate_text_match(resume_text, job_text)
    skill_score = calculate_skill_match(resume_text, job_text)

    # If job text has no specific skills found from our list, rely purely on TFIDF
    job_skills = extract_skills(job_text)
    if len(job_skills) == 0:
        return round(text_score, 2)

    # Weighted score
    return round((0.4 * text_score) + (0.6 * skill_score), 2)