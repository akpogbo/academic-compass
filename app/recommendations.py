
def generate_advice(profile, pathway):
    if pathway == "academic_support":
        return {
            "explanation": (
                "Your profile suggests focusing on academic consistency "
                "and strengthening your study habits first."
            ),
            "strengths": [
                "You have a starting point for tracking your progress.",
                "Your academic profile can help identify areas to improve.",
            ],
            "next_steps": [
                "Create a weekly study timetable.",
                "Seek help with difficult courses.",
                "Track attendance and review your CGPA each semester.",
            ],
        }

    if pathway == "software_engineering":
        return {
            "explanation": (
                "Your profile suggests exploring software development "
                "and building practical programming experience."
            ),
            "strengths": [
                "Potential interest in software development.",
                "Opportunity to practise problem-solving through projects.",
            ],
            "next_steps": [
                "Build and publish a small software application.",
                "Practise data structures and algorithms.",
                "Learn Git, testing, and clean coding practices.",
            ],
        }

    if pathway == "data_science":
        return {
            "explanation": (
                "Your profile suggests exploring data analysis and "
                "data science, combining programming with mathematics."
            ),
            "strengths": [
                "Interest in data-related work.",
                "Opportunity to combine analytical and programming skills.",
            ],
            "next_steps": [
                "Practise Python and SQL.",
                "Analyse a dataset and communicate your findings.",
                "Learn statistics and introductory machine learning.",
            ],
        }

    return {
        "explanation": (
            "Your profile suggests exploring artificial intelligence "
            "and machine learning."
        ),
        "strengths": [
            "Interest in AI-related work.",
            "Opportunity to combine programming and mathematics.",
        ],
        "next_steps": [
            "Study machine learning fundamentals.",
            "Train and evaluate a small classification model.",
            "Build a practical AI project and document its limitations.",
        ],
    }
