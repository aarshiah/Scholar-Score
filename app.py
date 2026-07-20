# Import Flask tools for creating pages and API routes.
from flask import Flask, render_template, request, jsonify

# Import Path so file locations work on Mac and Windows.
from pathlib import Path

# Import JSON so Python can read the college data file.
import json


# Create the Flask application.
app = Flask(__name__)


# Find the folder containing this app.py file.
BASE_DIR = Path(__file__).resolve().parent

# Build the path to the local college JSON file.
COLLEGE_DATA_PATH = BASE_DIR / "data" / "colleges.json"


def load_colleges():
    """Read and return all college records from colleges.json."""

    # Open the JSON file using UTF-8 text encoding.
    with open(COLLEGE_DATA_PATH, "r", encoding="utf-8") as file:
        # Convert the JSON text into Python lists and dictionaries.
        return json.load(file)


def clamp(value, minimum=0, maximum=100):
    """Keep a number between a minimum and maximum value."""

    # Return the value, but never lower than minimum or higher than maximum.
    return max(minimum, min(maximum, value))


def safe_float(value, default=0):
    """Convert a value to a decimal number without crashing."""

    try:
        # Try converting the incoming value into a float.
        return float(value or default)
    except (TypeError, ValueError):
        # Return the default value when the conversion is unsuccessful.
        return float(default)


def safe_int(value, default=0):
    """Convert a value to a whole number without crashing."""

    try:
        # Convert through float first so values such as "3.0" still work.
        return int(float(value or default))
    except (TypeError, ValueError):
        # Return the default value when the conversion is unsuccessful.
        return int(default)


def text_quality_score(text, target_words=80):
    """
    Create a basic NLP-style score for a written description.

    This is not a large language model. It is an explainable classroom
    demonstration that checks detail, action words, and measurable impact.
    """

    # Remove extra spaces from the beginning and end.
    cleaned_text = (text or "").strip()

    # Split the description into individual words.
    words = cleaned_text.split()

    # Count how many words the student wrote.
    word_count = len(words)

    # Convert the text to lowercase so keyword matching is easier.
    lower_text = cleaned_text.lower()

    # These words often describe initiative, leadership, and accomplishments.
    action_words = [
        "built", "created", "developed", "designed", "organized", "led",
        "managed", "improved", "increased", "started", "founded", "researched",
        "taught", "mentored", "volunteered", "raised", "won", "earned",
        "published", "presented", "coordinated", "helped", "solved"
    ]

    # Count how many different action words appear in the description.
    action_hits = sum(1 for word in action_words if word in lower_text)

    # Count digits because numbers often show measurable impact.
    number_hits = sum(1 for character in cleaned_text if character.isdigit())

    # Give up to 65 points for writing enough detail.
    detail_points = clamp((word_count / target_words) * 65, 0, 65)

    # Give up to 25 points for using strong action language.
    action_points = clamp(action_hits * 5, 0, 25)

    # Give up to 10 points for including measurable results.
    measurement_points = clamp(number_hits * 2, 0, 10)

    # Add all parts together and keep the result between 0 and 100.
    total_score = clamp(detail_points + action_points + measurement_points)

    # Return the rounded score and useful explanation data.
    return round(total_score), {
        "word_count": word_count,
        "action_hits": action_hits,
        "number_hits": number_hits
    }


def score_extracurricular(activity):
    """Score one extracurricular activity using commitment and impact."""

    # Read the number of years the student participated.
    years = safe_float(activity.get("years"), 0)

    # Read the average number of hours spent each week.
    hours_per_week = safe_float(activity.get("hours_per_week"), 0)

    # Read the number of weeks spent each year.
    weeks_per_year = safe_float(activity.get("weeks_per_year"), 0)

    # Read whether the student held a leadership position.
    leadership = bool(activity.get("leadership", False))

    # Read the activity description.
    description = activity.get("description", "")

    # Score the quality of the written description.
    description_score, _ = text_quality_score(description, target_words=60)

    # Reward long-term commitment, up to four years.
    years_score = clamp((years / 4) * 100)

    # Reward weekly commitment, with ten hours reaching the maximum.
    weekly_score = clamp((hours_per_week / 10) * 100)

    # Reward year-round participation, with forty weeks reaching the maximum.
    yearly_score = clamp((weeks_per_year / 40) * 100)

    # Give a leadership bonus when the checkbox is selected.
    leadership_score = 100 if leadership else 35

    # Combine commitment, leadership, and description quality.
    activity_score = (
        years_score * 0.20
        + weekly_score * 0.15
        + yearly_score * 0.10
        + leadership_score * 0.20
        + description_score * 0.35
    )

    # Return a rounded score from 0 through 100.
    return round(clamp(activity_score))


def score_award(award):
    """Score one award using level, placement, and description quality."""

    # Translate award levels into numeric values.
    level_points = {
        "school": 45,
        "local": 55,
        "regional": 68,
        "state": 78,
        "national": 90,
        "international": 100
    }

    # Read the selected award level.
    award_level = (award.get("level") or "school").lower()

    # Look up the score for the selected level.
    level_score = level_points.get(award_level, 45)

    # Read and score the award description.
    description_score, _ = text_quality_score(
        award.get("description", ""),
        target_words=45
    )

    # Read whether the student won, placed, or was recognized.
    recognition_type = (award.get("recognition_type") or "recognition").lower()

    # Give different values for different types of recognition.
    recognition_points = {
        "winner": 100,
        "finalist": 85,
        "placement": 78,
        "selection": 68,
        "recognition": 60,
        "participation": 35
    }

    # Find the recognition score or use 60 as a safe default.
    recognition_score = recognition_points.get(recognition_type, 60)

    # Combine the level, recognition, and written description.
    award_score = (
        level_score * 0.45
        + recognition_score * 0.25
        + description_score * 0.30
    )

    # Return the final award score.
    return round(clamp(award_score))


def calculate_academic_score(profile):
    """Calculate the academic portion of the student score."""

    # Read the student's GPA on a 4.0 scale.
    gpa = safe_float(profile.get("gpa"), 0)

    # Read the student's SAT score.
    test_score = safe_float(profile.get("test_score"), 0)

    # Read the student's course rigor rating from 1 through 5.
    course_rigor = safe_float(profile.get("course_rigor"), 1)

    # Convert GPA into a percentage score.
    gpa_score = clamp((gpa / 4.0) * 100)

    # Convert SAT into a percentage score.
    sat_score = clamp((test_score / 1600) * 100)

    # Convert course rigor into a percentage score.
    rigor_score = clamp((course_rigor / 5) * 100)

    # Give GPA the greatest weight.
    academic_score = (
        gpa_score * 0.55
        + sat_score * 0.25
        + rigor_score * 0.20
    )

    # Return both the total and its components.
    return round(clamp(academic_score)), {
        "gpa": round(gpa_score),
        "testing": round(sat_score),
        "rigor": round(rigor_score)
    }


def calculate_extracurricular_score(profile):
    """Calculate the score for all extracurricular activities."""

    # Read the array of activities sent by JavaScript.
    activities = profile.get("extracurriculars", [])

    # Remove empty activity rows.
    completed_activities = [
        activity for activity in activities
        if (activity.get("name") or "").strip()
    ]

    # Return zero when no activities were added.
    if not completed_activities:
        return 0, []

    # Score each completed activity.
    individual_scores = [
        score_extracurricular(activity)
        for activity in completed_activities
    ]

    # Sort scores from strongest to weakest.
    sorted_scores = sorted(individual_scores, reverse=True)

    # Weight the student's strongest activities more heavily.
    weights = [0.35, 0.25, 0.18, 0.12, 0.10]

    # Start the total at zero.
    weighted_total = 0

    # Start the used-weight total at zero.
    used_weight = 0

    # Score up to five activities.
    for index, score in enumerate(sorted_scores[:5]):
        # Use the matching position weight.
        weight = weights[index]

        # Add the weighted score.
        weighted_total += score * weight

        # Track how much weight was used.
        used_weight += weight

    # Normalize the result when fewer than five activities were entered.
    normalized_score = weighted_total / used_weight if used_weight else 0

    # Add a small breadth bonus for having multiple meaningful activities.
    breadth_bonus = clamp((len(completed_activities) - 1) * 3, 0, 12)

    # Combine depth and breadth.
    final_score = clamp(normalized_score + breadth_bonus)

    # Return the overall score and individual activity scores.
    return round(final_score), individual_scores


def calculate_award_score(profile):
    """Calculate the score for the student's awards and honors."""

    # Read all awards submitted by JavaScript.
    awards = profile.get("awards", [])

    # Keep only rows with an award name.
    completed_awards = [
        award for award in awards
        if (award.get("name") or "").strip()
    ]

    # Return zero if no awards were entered.
    if not completed_awards:
        return 0, []

    # Score every award.
    individual_scores = [score_award(award) for award in completed_awards]

    # Sort awards from strongest to weakest.
    sorted_scores = sorted(individual_scores, reverse=True)

    # Use the strongest three awards for the main score.
    top_scores = sorted_scores[:3]

    # Calculate their average.
    average_score = sum(top_scores) / len(top_scores)

    # Add a small bonus for additional awards.
    breadth_bonus = clamp((len(completed_awards) - 1) * 2, 0, 8)

    # Return the final score and all individual scores.
    return round(clamp(average_score + breadth_bonus)), individual_scores


def calculate_interest_score(profile):
    """Score how clearly the student explains major and career interests."""

    # Read the student's primary intended major.
    intended_major = (profile.get("intended_major") or "").strip()

    # Read the student's possible second major.
    second_major = (profile.get("second_major") or "").strip()

    # Read the student's possible minor.
    intended_minor = (profile.get("intended_minor") or "").strip()

    # Read the student's career interests.
    career_interests = (profile.get("career_interests") or "").strip()

    # Read the explanation connecting interests to experiences.
    interest_statement = (profile.get("interest_statement") or "").strip()

    # Score the quality of the interest statement.
    statement_score, _ = text_quality_score(
        interest_statement,
        target_words=90
    )

    # Give points for completing important planning fields.
    completion_points = 0

    # Add points when a primary major is entered.
    if intended_major:
        completion_points += 35

    # Add optional points for a second major.
    if second_major:
        completion_points += 10

    # Add optional points for a minor.
    if intended_minor:
        completion_points += 10

    # Add points when career interests are explained.
    if career_interests:
        completion_points += 25

    # Add points when the student writes a detailed connection statement.
    if interest_statement:
        completion_points += 20

    # Keep completion points between 0 and 100.
    completion_score = clamp(completion_points)

    # Blend field completion with the quality of the written explanation.
    interest_score = completion_score * 0.45 + statement_score * 0.55

    # Return the final interest score.
    return round(clamp(interest_score))


def calculate_student_score(profile):
    """Calculate the complete ScholarScore and all category breakdowns."""

    # Calculate academics.
    academic_score, academic_details = calculate_academic_score(profile)

    # Calculate extracurricular depth and impact.
    extracurricular_score, activity_scores = calculate_extracurricular_score(profile)

    # Calculate awards and honors.
    award_score, award_scores = calculate_award_score(profile)

    # Score the main personal statement.
    essay_score, essay_details = text_quality_score(
        profile.get("essay", ""),
        target_words=180
    )

    # Calculate major, minor, and career-interest clarity.
    interest_score = calculate_interest_score(profile)

    # Combine all categories into one transparent score.
    total_score = (
        academic_score * 0.45
        + extracurricular_score * 0.23
        + award_score * 0.10
        + essay_score * 0.12
        + interest_score * 0.10
    )

    # Build a detailed category breakdown for the frontend.
    breakdown = {
        "academic": academic_score,
        "extracurriculars": extracurricular_score,
        "awards": award_score,
        "essay": essay_score,
        "interests": interest_score
    }

    # Build extra explanation information.
    details = {
        "academic_details": academic_details,
        "activity_scores": activity_scores,
        "award_scores": award_scores,
        "essay_details": essay_details
    }

    # Return the rounded total, breakdown, and details.
    return round(clamp(total_score)), breakdown, details


def calculate_major_alignment(profile, college):
    """Estimate whether a college offers fields related to the student's interests."""

    # Read the student's intended major.
    intended_major = (profile.get("intended_major") or "").strip().lower()

    # Read the student's second major.
    second_major = (profile.get("second_major") or "").strip().lower()

    # Read the student's possible minor.
    intended_minor = (profile.get("intended_minor") or "").strip().lower()

    # Read the college's sample list of strong academic areas.
    college_strengths = [
        subject.lower()
        for subject in college.get("major_strengths", [])
    ]

    # Combine the student's selected fields.
    student_fields = [
        field for field in [intended_major, second_major, intended_minor]
        if field
    ]

    # Return a neutral score if the student did not enter an academic field.
    if not student_fields:
        return 55, "Add an intended major to receive a stronger academic-interest comparison."

    # Start the number of matching fields at zero.
    matches = 0

    # Compare each student field with each college strength.
    for field in student_fields:
        for strength in college_strengths:
            # Count partial matches in either direction.
            if field in strength or strength in field:
                matches += 1
                break

    # Give a high score when at least one field matches.
    if matches >= 2:
        return 95, "This college has multiple sample strengths related to your interests."

    # Give a strong score when one field matches.
    if matches == 1:
        return 82, "This college has a sample academic strength related to your interests."

    # Give a moderate score when no direct sample match appears.
    return 58, "No direct match appears in this small sample list, so research the college's full program catalog."


def compare_to_college(student_score, profile, college):
    """
    Compare a student profile with one college benchmark.

    The result is a planning estimate and not an official acceptance chance.
    """

    # Read the college benchmark score.
    benchmark = safe_float(college.get("benchmark_score"), 70)

    # Find the difference between the student and college scores.
    score_gap = student_score - benchmark

    # Read the student's GPA.
    student_gpa = safe_float(profile.get("gpa"), 0)

    # Read the student's SAT score.
    student_test = safe_float(profile.get("test_score"), 0)

    # Calculate GPA alignment.
    gpa_alignment = clamp(
        100 - abs(student_gpa - safe_float(college.get("avg_gpa"), 0)) * 35
    )

    # Calculate SAT alignment.
    test_alignment = clamp(
        100 - abs(student_test - safe_float(college.get("avg_test_score"), 0)) / 4
    )

    # Convert the benchmark difference into a comparison score.
    profile_alignment = clamp(50 + score_gap * 3)

    # Calculate how well the student's interests align with sample strengths.
    major_alignment, major_message = calculate_major_alignment(profile, college)

    # Combine all comparison components.
    fit_score = round(
        profile_alignment * 0.42
        + gpa_alignment * 0.23
        + test_alignment * 0.15
        + major_alignment * 0.20
    )

    # Classify the college using the score gap.
    if score_gap >= 8:
        category = "Likely"

        # Explain the likely category.
        message = "Your ScholarScore is currently above this app's sample benchmark."

    elif score_gap >= -5:
        category = "Target"

        # Explain the target category.
        message = "Your ScholarScore is currently close to this app's sample benchmark."

    else:
        category = "Reach"

        # Explain the reach category.
        message = "Your ScholarScore is currently below this app's sample benchmark."

    # Return all information needed by JavaScript.
    return {
        "college": college["name"],
        "college_score": round(benchmark),
        "student_score": student_score,
        "fit_score": fit_score,
        "major_alignment": round(major_alignment),
        "major_message": major_message,
        "category": category,
        "message": message,
        "acceptance_rate": college["acceptance_rate"],
        "avg_gpa": college["avg_gpa"],
        "avg_test_score": college["avg_test_score"],
        "major_strengths": college.get("major_strengths", []),
        "disclaimer": (
            "This is an educational estimate based on sample historical data "
            "and a transparent scoring formula. It is not an official admission probability."
        )
    }


def create_recommendations(breakdown):
    """Generate improvement recommendations from the lowest categories."""

    # Pair each category name with its score and recommendation.
    recommendation_map = {
        "academic": (
            breakdown["academic"],
            "Strengthen academics through course rigor, consistent grades, or test preparation."
        ),
        "extracurriculars": (
            breakdown["extracurriculars"],
            "Add deeper activity descriptions that show commitment, leadership, and measurable impact."
        ),
        "awards": (
            breakdown["awards"],
            "Include awards, certifications, competitions, publications, or meaningful recognitions."
        ),
        "essay": (
            breakdown["essay"],
            "Develop the personal statement with specific examples, action words, reflection, and results."
        ),
        "interests": (
            breakdown["interests"],
            "Explain how your intended major connects to your classes, projects, activities, and career goals."
        )
    }

    # Sort categories from lowest score to highest score.
    sorted_categories = sorted(
        recommendation_map.items(),
        key=lambda item: item[1][0]
    )

    # Return recommendations for the three lowest categories.
    return [
        {
            "category": category.replace("_", " ").title(),
            "score": score_and_message[0],
            "message": score_and_message[1]
        }
        for category, score_and_message in sorted_categories[:3]
    ]


@app.route("/")
def home():
    """Display the main ScholarScore page."""

    # Render the HTML template.
    return render_template("index.html")


@app.route("/api/colleges")
def colleges():
    """Return college search results as JSON."""

    # Read the search text from the URL.
    query = request.args.get("q", "").lower().strip()

    # Load every college.
    college_list = load_colleges()

    # Filter the college list when the user typed a query.
    if query:
        college_list = [
            college for college in college_list
            if query in college["name"].lower()
        ]

    # Send the matching colleges back to JavaScript.
    return jsonify(college_list)


@app.route("/api/score", methods=["POST"])
def score():
    """Receive a student profile and return ScholarScore results."""

    # Read the JSON body sent by JavaScript.
    payload = request.get_json() or {}

    # Get the student profile object.
    profile = payload.get("profile", {})

    # Get the selected college names.
    selected_colleges = payload.get("colleges", [])

    # Calculate the student's complete score.
    student_score, breakdown, details = calculate_student_score(profile)

    # Load all college records.
    all_colleges = load_colleges()

    # Create a dictionary for quickly finding a college by name.
    college_lookup = {
        college["name"]: college
        for college in all_colleges
    }

    # Start an empty comparison list.
    comparisons = []

    # Compare the student with each selected college.
    for college_name in selected_colleges:
        # Find the selected college.
        college = college_lookup.get(college_name)

        # Only compare when the college exists.
        if college:
            comparisons.append(
                compare_to_college(student_score, profile, college)
            )

    # Create personalized recommendations.
    recommendations = create_recommendations(breakdown)

    # Return the complete result as JSON.
    return jsonify({
        "student_score": student_score,
        "breakdown": breakdown,
        "details": details,
        "comparisons": comparisons,
        "recommendations": recommendations,
        "model_note": (
            "ScholarScore uses a transparent weighted scoring model and basic "
            "NLP-style text analysis. It does not replace an admissions counselor "
            "or predict an official admissions decision."
        )
    })


# Only start the development server when this file is run directly.
if __name__ == "__main__":
    # Turn on debug mode so code changes reload during development.
    app.run(debug=True)
