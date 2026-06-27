# ============================================================
# job_matcher.py
# Compares user skills vs job requirements.
# Returns match %, matched skills, and missing skills.
# ============================================================


# This is your job requirements database.
# Each job title maps to a list of skills companies look for.
# You can add more jobs or more skills to any job anytime!

JOB_DATABASE = {
    "Data Analyst": {
        "required_skills": [
            "python", "sql", "excel", "tableau", "statistics",
            "data analysis", "data visualization", "pandas"
        ],
        "description": "Analyze data to find business insights",
        "avg_salary": "PKR 80,000 - 150,000/month",
        "icon": "📊"
    },

    "Data Scientist": {
        "required_skills": [
            "python", "machine learning", "statistics", "tensorflow",
            "pandas", "numpy", "sql", "deep learning", "scikit-learn"
        ],
        "description": "Build predictive models and AI solutions",
        "avg_salary": "PKR 120,000 - 250,000/month",
        "icon": "🧬"
    },

    "Software Engineer": {
        "required_skills": [
            "python", "java", "git", "github", "rest api",
            "docker", "linux", "problem solving"
        ],
        "description": "Build and maintain software systems",
        "avg_salary": "PKR 100,000 - 200,000/month",
        "icon": "💻"
    },

    "Business Analyst": {
        "required_skills": [
            "excel", "sql", "tableau", "power bi",
            "data analysis", "communication", "project management"
        ],
        "description": "Bridge between business needs and technical solutions",
        "avg_salary": "PKR 70,000 - 130,000/month",
        "icon": "📈"
    },

    "Machine Learning Engineer": {
        "required_skills": [
            "python", "machine learning", "deep learning", "tensorflow",
            "pytorch", "scikit-learn", "docker", "aws", "sql"
        ],
        "description": "Deploy ML models into production systems",
        "avg_salary": "PKR 150,000 - 300,000/month",
        "icon": "🤖"
    },

    "Web Developer": {
        "required_skills": [
            "html", "css", "javascript", "react",
            "git", "rest api", "django", "flask"
        ],
        "description": "Build websites and web applications",
        "avg_salary": "PKR 60,000 - 130,000/month",
        "icon": "🌐"
    },
}


def match_all_jobs(user_skills):
    """
    Compares user skills against every job in the database.
    Returns a sorted list of results (best match first).
    """

    results = []  # We'll store each job's result here

    for job_title, job_info in JOB_DATABASE.items():
        required = job_info["required_skills"]  # What the job needs

        # Find which required skills the user HAS
        # This is Python "set" math — super clean
        matched = [skill for skill in required if skill in user_skills]

        # Find which required skills the user is MISSING
        missing = [skill for skill in required if skill not in user_skills]

        # Calculate match percentage
        # Example: matched 4 out of 8 skills = 50%
        score = round((len(matched) / len(required)) * 100)

        results.append({
            "job": job_title,
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "description": job_info["description"],
            "avg_salary": job_info["avg_salary"],
            "icon": job_info["icon"],
            "total_required": len(required),
            "total_matched": len(matched),
        })

    # Sort by score — highest match at the top
    results.sort(key=lambda x: x["score"], reverse=True)

    return results


def get_top_match(results):
    """Returns just the #1 best matching job."""
    if results:
        return results[0]
    return None


def get_gap_analysis(results, target_job_title):
    """
    Gets the gap analysis for a specific job the user is targeting.
    Example: "I want to be a Data Scientist — what am I missing?"
    """
    for result in results:
        if result["job"] == target_job_title:
            return result["missing_skills"]
    return []