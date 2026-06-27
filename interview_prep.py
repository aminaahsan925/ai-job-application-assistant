# ============================================================
# interview_prep.py
# Generates interview questions based on detected skills.
# ============================================================


# For each skill, here are real interview questions.
# The questions go from easier to harder within each skill.

QUESTION_BANK = {
    "python": [
        "What is the difference between a list and a tuple in Python?",
        "What is a list comprehension? Give an example.",
        "How does Python handle memory management?",
        "What is the difference between '==' and 'is' in Python?",
        "Explain what a decorator is in Python.",
    ],
    "sql": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "What is a primary key? What is a foreign key?",
        "How do you find duplicate rows in a table?",
        "What is the difference between WHERE and HAVING?",
        "Explain the difference between DELETE, TRUNCATE, and DROP.",
    ],
    "excel": [
        "What is a VLOOKUP and when would you use it?",
        "How do you create a Pivot Table?",
        "What is the difference between absolute and relative cell references?",
        "How would you find the average of only the values above a certain threshold?",
        "What are some common Excel functions you use for data cleaning?",
    ],
    "machine learning": [
        "What is the difference between supervised and unsupervised learning?",
        "What is overfitting and how do you prevent it?",
        "Explain bias-variance tradeoff.",
        "What is cross-validation and why is it used?",
        "What is the difference between classification and regression?",
    ],
    "data analysis": [
        "Walk me through how you would clean a messy dataset.",
        "How do you handle missing values in a dataset?",
        "What is the difference between mean, median, and mode? When would you use each?",
        "How would you detect outliers in data?",
        "Explain what a correlation matrix tells you.",
    ],
    "pandas": [
        "What is a DataFrame in pandas?",
        "How do you select specific columns from a DataFrame?",
        "What is the difference between .loc and .iloc?",
        "How do you group data and compute aggregates in pandas?",
        "How would you merge two DataFrames?",
    ],
    "statistics": [
        "What is the Central Limit Theorem?",
        "What is the difference between Type I and Type II errors?",
        "Explain what a p-value means.",
        "What is the difference between correlation and causation?",
        "What is a normal distribution?",
    ],
    "tableau": [
        "What is a dimension vs a measure in Tableau?",
        "How do you create a calculated field?",
        "What is the difference between a join and a blend in Tableau?",
        "How would you show year-over-year growth in Tableau?",
        "What is a LOD (Level of Detail) expression?",
    ],
    "git": [
        "What is the difference between git pull and git fetch?",
        "How do you resolve a merge conflict?",
        "What is a branch and why do we use them?",
        "What does git rebase do?",
        "How do you undo the last commit without losing your changes?",
    ],
    "power bi": [
        "What is DAX and when is it used?",
        "What is the difference between Power BI Desktop and Power BI Service?",
        "How do you create a relationship between two tables?",
        "What is a slicer in Power BI?",
        "How do you publish a report in Power BI?",
    ],
}

# Generic questions asked for almost any tech role
GENERAL_QUESTIONS = [
    "Tell me about yourself and your background.",
    "Why are you interested in this role?",
    "Describe a challenging project you worked on and how you handled it.",
    "Where do you see yourself in 5 years?",
    "What is your greatest strength? What is your greatest weakness?",
    "How do you stay updated with new technologies?",
    "Describe a time you had to learn something quickly.",
]


def generate_interview_questions(user_skills, max_per_skill=3):
    """
    Given a list of user skills, picks the most relevant
    interview questions from the question bank.
    Returns a dict of {skill: [questions]}
    """

    questions = {}

    # Add general questions first — everyone gets these
    questions["General"] = GENERAL_QUESTIONS

    # For each skill the user has, add questions if we have them
    for skill in user_skills:
        if skill in QUESTION_BANK:
            # Take only the first N questions (don't overwhelm them)
            questions[skill] = QUESTION_BANK[skill][:max_per_skill]

    return questions


def get_total_question_count(questions_dict):
    """Counts total number of questions generated."""
    return sum(len(q) for q in questions_dict.values())