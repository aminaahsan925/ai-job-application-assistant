# ============================================================
# skills_extractor.py
# Scans resume text and finds which skills are mentioned.
# ============================================================


# This is your master skills database.
# The KEY is the skill name we search for in the text.
# The VALUE is the category it belongs to.
# You can add more skills here anytime!

SKILLS_DATABASE = {
    # --- Programming Languages ---
    "python": "Programming",
    "java": "Programming",
    "javascript": "Programming",
    "c++": "Programming",
    "r": "Programming",
    "scala": "Programming",
    "matlab": "Programming",

    # --- Data & Analytics ---
    "sql": "Data & Analytics",
    "mysql": "Data & Analytics",
    "postgresql": "Data & Analytics",
    "mongodb": "Data & Analytics",
    "excel": "Data & Analytics",
    "tableau": "Data & Analytics",
    "power bi": "Data & Analytics",
    "pandas": "Data & Analytics",
    "numpy": "Data & Analytics",
    "matplotlib": "Data & Analytics",
    "seaborn": "Data & Analytics",
    "data analysis": "Data & Analytics",
    "data visualization": "Data & Analytics",
    "statistics": "Data & Analytics",
    "microsoft excel": "Data & Analytics",

    # --- Machine Learning & AI ---
    "machine learning": "Machine Learning",
    "deep learning": "Machine Learning",
    "tensorflow": "Machine Learning",
    "keras": "Machine Learning",
    "pytorch": "Machine Learning",
    "scikit-learn": "Machine Learning",
    "natural language processing": "Machine Learning",
    "nlp": "Machine Learning",
    "computer vision": "Machine Learning",
    "neural network": "Machine Learning",

    # --- Web Development ---
    "html": "Web Development",
    "css": "Web Development",
    "react": "Web Development",
    "django": "Web Development",
    "flask": "Web Development",
    "fastapi": "Web Development",
    "node.js": "Web Development",
    "rest api": "Web Development",

    # --- Cloud & DevOps ---
    "aws": "Cloud & DevOps",
    "azure": "Cloud & DevOps",
    "google cloud": "Cloud & DevOps",
    "docker": "Cloud & DevOps",
    "kubernetes": "Cloud & DevOps",
    "git": "Cloud & DevOps",
    "github": "Cloud & DevOps",
    "linux": "Cloud & DevOps",

    # --- Soft Skills (yes, these count!) ---
    "communication": "Soft Skills",
    "leadership": "Soft Skills",
    "teamwork": "Soft Skills",
    "problem solving": "Soft Skills",
    "project management": "Soft Skills",
}


def extract_skills(resume_text):
    """
    Looks through resume text and returns a list of skills found.
    We convert everything to lowercase so 'Python' and 'python' both match.
    """

    # Convert the entire resume text to lowercase for easy matching
    resume_lower = resume_text.lower()

    found_skills = []   # Skills we discover in the resume
    found_categories = {}  # Which categories we found skills in

    # Loop through every skill in our database
    for skill, category in SKILLS_DATABASE.items():

        # Check if this skill appears anywhere in the resume text
        if skill in resume_lower:
            found_skills.append(skill)  # Add to our found list

            # Also track which categories are represented
            if category not in found_categories:
                found_categories[category] = []
            found_categories[category].append(skill)

    return found_skills, found_categories


def get_skill_summary(found_categories):
    """
    Creates a human-readable summary of the skills found.
    Example output: "Found 12 skills across 4 categories"
    """
    total_skills = sum(len(skills) for skills in found_categories.values())
    num_categories = len(found_categories)
    return f"Found {total_skills} skills across {num_categories} categories"