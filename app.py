from flask import Flask, render_template, request
from resume_parser import read_pdf, read_docx, clean_text
from matcher import calculate_match

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/match", methods=["POST"])
def match():
    resume = request.files["resume"]
    job_desc = request.form["job_description"]

    if resume.filename.endswith(".pdf"):
        resume_text = read_pdf(resume)
    else:
        resume_text = read_docx(resume)

    resume_text = clean_text(resume_text)
    job_desc = clean_text(job_desc)

    score = calculate_match(resume_text, job_desc)

    # ✅ MATCH CATEGORY LOGIC
    if score >= 85:
        category = "Great Match"
    elif score >= 70:
        category = "Good Match"
    elif score >= 40:
        category = "Average Match"
    else:
        category = "Poor Match"

    return render_template(
        "index.html",
        score=score,
        category=category
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)