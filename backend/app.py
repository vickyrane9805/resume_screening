from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from database import init_db, insert_candidate, fetch_candidates
from resume_processor import quick_sort, greedy_select
from skill_extractor import extract_text_from_pdf, extract_skills_from_text

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.config["UPLOAD_FOLDER"] = "../resumes"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

hr_prompt = ""

# Initialize database
init_db()

@app.route("/")
def index():
    global hr_prompt
    candidates = fetch_candidates()

    scores = [c["score"] for c in candidates]
    stats = {
        "total": len(candidates),
        "highest": max(scores) if scores else 0,
        "average": round(sum(scores)/len(scores), 2) if scores else 0,
        "shortlisted": len([c for c in candidates if hr_prompt.lower() in c["skills"].lower()]) if hr_prompt else 0
    }

    return render_template("index.html", stats=stats, candidates=candidates, hr_prompt=hr_prompt)

@app.route("/set_prompt", methods=["POST"])
def set_prompt():
    global hr_prompt
    hr_prompt = request.form.get("prompt", "")
    return redirect(url_for("index"))

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return "No file part"
    file = request.files["resume"]
    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Extract text & skills
    text = extract_text_from_pdf(filepath)
    skills = extract_skills_from_text(text)

    # Dummy values (replace with real logic)
    experience = 2
    education = "Unknown"
    score = experience * 2 + len(skills)

    insert_candidate(file.filename, ",".join(skills), experience, education, score)

    return redirect(url_for("index"))

@app.route("/view_resume/<filename>")
def view_resume(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/search")
def search():
    query = request.args.get("query", "").lower()
    filter_opt = request.args.get("filter", "top5")

    candidates = fetch_candidates()
    filtered = [c for c in candidates if query in c["name"].lower() or query in c["skills"].lower()]

    if filter_opt == "top5":
        filtered = sorted(filtered, key=lambda x: x["score"], reverse=True)[:5]
    elif filter_opt == "last5":
        filtered = sorted(filtered, key=lambda x: x["score"])[:5]
    elif filter_opt == "all":
        filtered = sorted(filtered, key=lambda x: x["score"], reverse=True)

    return render_template("results.html", candidates=filtered)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
