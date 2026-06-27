# ============================================================
# resume_scorer.py
# Scores a resume out of 100 based on multiple factors.
# ============================================================


def score_resume(resume_text, found_skills, found_categories):
    """
    Analyzes the resume text and skills to give a score out of 100.
    Also returns specific feedback for each category.

    Scoring breakdown:
    - Skills variety:    30 points
    - Resume keywords:   25 points
    - Skill categories:  20 points
    - Resume length:     15 points
    - Bonus signals:     10 points
    """

    score = 0
    feedback = []  # Tips to improve the score
    breakdown = {} # Score for each category

    resume_lower = resume_text.lower()

    # ---- CATEGORY 1: Skills variety (max 30 points) ----
    num_skills = len(found_skills)
    if num_skills >= 15:
        skills_score = 30
    elif num_skills >= 10:
        skills_score = 22
    elif num_skills >= 6:
        skills_score = 15
    elif num_skills >= 3:
        skills_score = 8
    else:
        skills_score = 3

    score += skills_score
    breakdown["Skills (30pts)"] = skills_score

    if num_skills < 10:
        feedback.append(f"💡 You have {num_skills} skills detected. Adding more technical skills (target 10+) will improve your score.")


    # ---- CATEGORY 2: Important resume keywords (max 25 points) ----
    important_keywords = [
        "project", "experience", "education", "university",
        "developed", "built", "analyzed", "managed",
        "achieved", "improved", "designed", "implemented",
        "intern", "certif", "award", "publication"
    ]

    # Count how many of these keywords appear in the resume
    keywords_found = sum(1 for kw in important_keywords if kw in resume_lower)
    keywords_score = min(25, keywords_found * 2)  # 2 points per keyword, max 25

    score += keywords_score
    breakdown["Keywords (25pts)"] = keywords_score

    if keywords_found < 8:
        feedback.append("💡 Use strong action verbs: 'developed', 'analyzed', 'implemented', 'achieved'. They make your resume stronger.")


    # ---- CATEGORY 3: Skill category diversity (max 20 points) ----
    num_categories = len(found_categories)
    if num_categories >= 4:
        category_score = 20
    elif num_categories >= 3:
        category_score = 15
    elif num_categories >= 2:
        category_score = 10
    else:
        category_score = 5

    score += category_score
    breakdown["Category diversity (20pts)"] = category_score

    if num_categories < 3:
        feedback.append("💡 Your skills span fewer than 3 categories. Try to add skills from different areas like cloud, data tools, and soft skills.")


    # ---- CATEGORY 4: Resume length/content (max 15 points) ----
    word_count = len(resume_text.split())
    if word_count >= 400:
        length_score = 15
    elif word_count >= 250:
        length_score = 10
    elif word_count >= 150:
        length_score = 6
    else:
        length_score = 2

    score += length_score
    breakdown["Content richness (15pts)"] = length_score

    if word_count < 300:
        feedback.append(f"💡 Your resume is {word_count} words. Aim for 300-600 words. Add more detail to your experience and projects.")


    # ---- CATEGORY 5: Bonus signals (max 10 points) ----
    bonus_score = 0

    if any(word in resume_lower for word in ["github", "linkedin", "portfolio"]):
        bonus_score += 3
    else:
        feedback.append("💡 Add your GitHub and LinkedIn profile links to your resume.")

    if any(word in resume_lower for word in ["project", "built", "developed", "created"]):
        bonus_score += 4
    else:
        feedback.append("💡 Add a 'Projects' section. Even academic projects count — describe what you built and what tech you used.")

    if any(word in resume_lower for word in ["intern", "internship", "experience"]):
        bonus_score += 3

    score += bonus_score
    breakdown["Bonus signals (10pts)"] = bonus_score


    # ---- Determine grade ----
    if score >= 80:
        grade = "A — Excellent"
        grade_color = "green"
    elif score >= 65:
        grade = "B — Good"
        grade_color = "blue"
    elif score >= 50:
        grade = "C — Average"
        grade_color = "orange"
    else:
        grade = "D — Needs Work"
        grade_color = "red"

    return {
        "total_score": score,
        "grade": grade,
        "grade_color": grade_color,
        "breakdown": breakdown,
        "feedback": feedback,
        "word_count": word_count
    }