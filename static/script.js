// Find the college search input.
const collegeSearchInput = document.getElementById("college-search-input");

// Find the search-results dropdown.
const searchResults = document.getElementById("search-results");

// Find the selected-college chip container.
const selectedCollegesContainer = document.getElementById("selected-colleges");

// Find the main calculate button.
const calculateButton = document.getElementById("calculate-button");

// Find the loading message.
const loading = document.getElementById("loading");

// Find the result-content wrapper.
const resultsContent = document.getElementById("results-content");

// Find the activities container.
const activitiesContainer = document.getElementById("activities-container");

// Find the awards container.
const awardsContainer = document.getElementById("awards-container");

// Find the add-activity button.
const addActivityButton = document.getElementById("add-activity-button");

// Find the add-award button.
const addAwardButton = document.getElementById("add-award-button");

// Store the names of colleges selected by the student.
let selectedColleges = [];

// Track the next activity number.
let activityCounter = 0;

// Track the next award number.
let awardCounter = 0;


/**
 * Create one extracurricular activity card.
 */
function addActivityCard() {
    // Increase the unique activity number.
    activityCounter += 1;

    // Create a new article element.
    const card = document.createElement("article");

    // Give the article styling and a unique data attribute.
    card.className = "repeatable-card activity-card";
    card.dataset.activityId = activityCounter;

    // Fill the card with activity form fields.
    card.innerHTML = `
        <div class="repeatable-header">
            <div>
                <span class="item-number">Activity ${activityCounter}</span>
                <h3>Describe your involvement</h3>
            </div>

            <button
                class="remove-button remove-activity"
                type="button"
                aria-label="Remove activity"
            >
                Remove
            </button>
        </div>

        <div class="form-grid">
            <label>
                Activity name
                <input
                    class="activity-name"
                    type="text"
                    placeholder="Robotics Club"
                >
            </label>

            <label>
                Role or position
                <input
                    class="activity-role"
                    type="text"
                    placeholder="Programming Lead"
                >
            </label>

            <label>
                Years involved
                <input
                    class="activity-years"
                    type="number"
                    min="0"
                    max="10"
                    step="0.5"
                    placeholder="2"
                >
            </label>

            <label>
                Hours per week
                <input
                    class="activity-hours"
                    type="number"
                    min="0"
                    max="80"
                    step="0.5"
                    placeholder="4"
                >
            </label>

            <label>
                Weeks per year
                <input
                    class="activity-weeks"
                    type="number"
                    min="0"
                    max="52"
                    placeholder="30"
                >
            </label>

            <label class="checkbox-label">
                <input
                    class="activity-leadership"
                    type="checkbox"
                >
                I held a leadership role
            </label>

            <label class="full-width">
                Description and impact
                <textarea
                    class="activity-description"
                    rows="5"
                    placeholder="What did you do? What did you create, lead, improve, learn, or accomplish? Include numbers when possible."
                ></textarea>

                <small>
                    Example: Led five students in building a recycling app,
                    organized three workshops, and increased club membership by 30%.
                </small>
            </label>
        </div>
    `;

    // Find the remove button inside this new card.
    const removeButton = card.querySelector(".remove-activity");

    // Remove the card when the student clicks Remove.
    removeButton.addEventListener("click", () => {
        card.remove();

        // Make sure at least one activity card remains.
        if (activitiesContainer.children.length === 0) {
            addActivityCard();
        }
    });

    // Add the completed card to the page.
    activitiesContainer.appendChild(card);
}


/**
 * Create one award or honor card.
 */
function addAwardCard() {
    // Increase the unique award number.
    awardCounter += 1;

    // Create a new article element.
    const card = document.createElement("article");

    // Give the card styling and a unique identifier.
    card.className = "repeatable-card award-card";
    card.dataset.awardId = awardCounter;

    // Fill the card with award fields.
    card.innerHTML = `
        <div class="repeatable-header">
            <div>
                <span class="item-number">Award ${awardCounter}</span>
                <h3>Describe the recognition</h3>
            </div>

            <button
                class="remove-button remove-award"
                type="button"
                aria-label="Remove award"
            >
                Remove
            </button>
        </div>

        <div class="form-grid">
            <label>
                Award or honor name
                <input
                    class="award-name"
                    type="text"
                    placeholder="Congressional App Challenge Finalist"
                >
            </label>

            <label>
                Year received
                <input
                    class="award-year"
                    type="number"
                    min="2000"
                    max="2040"
                    placeholder="2026"
                >
            </label>

            <label>
                Recognition level
                <select class="award-level">
                    <option value="school">School</option>
                    <option value="local">Local</option>
                    <option value="regional">Regional</option>
                    <option value="state">State</option>
                    <option value="national">National</option>
                    <option value="international">International</option>
                </select>
            </label>

            <label>
                Recognition type
                <select class="award-recognition-type">
                    <option value="recognition">Recognition</option>
                    <option value="selection">Selected participant</option>
                    <option value="placement">Placed</option>
                    <option value="finalist">Finalist</option>
                    <option value="winner">Winner</option>
                    <option value="participation">Participation</option>
                </select>
            </label>

            <label class="full-width">
                Description
                <textarea
                    class="award-description"
                    rows="5"
                    placeholder="Explain what the award recognizes, how competitive it was, what you did to earn it, and any measurable result."
                ></textarea>
            </label>
        </div>
    `;

    // Find the remove button inside this new card.
    const removeButton = card.querySelector(".remove-award");

    // Remove the award card when clicked.
    removeButton.addEventListener("click", () => {
        card.remove();

        // Keep at least one award card visible.
        if (awardsContainer.children.length === 0) {
            addAwardCard();
        }
    });

    // Add the card to the awards section.
    awardsContainer.appendChild(card);
}


/**
 * Read all extracurricular cards and turn them into JavaScript objects.
 */
function collectExtracurriculars() {
    // Find every activity card currently on the page.
    const cards = document.querySelectorAll(".activity-card");

    // Convert each card into a structured object.
    return Array.from(cards).map(card => ({
        // Read the activity name.
        name: card.querySelector(".activity-name").value.trim(),

        // Read the student's role.
        role: card.querySelector(".activity-role").value.trim(),

        // Read the number of years.
        years: card.querySelector(".activity-years").value,

        // Read the weekly time commitment.
        hours_per_week: card.querySelector(".activity-hours").value,

        // Read the yearly time commitment.
        weeks_per_year: card.querySelector(".activity-weeks").value,

        // Read whether leadership is selected.
        leadership: card.querySelector(".activity-leadership").checked,

        // Read the detailed activity description.
        description: card.querySelector(".activity-description").value.trim()
    }));
}


/**
 * Read all award cards and turn them into JavaScript objects.
 */
function collectAwards() {
    // Find every award card currently on the page.
    const cards = document.querySelectorAll(".award-card");

    // Convert each award card into a structured object.
    return Array.from(cards).map(card => ({
        // Read the award name.
        name: card.querySelector(".award-name").value.trim(),

        // Read the year received.
        year: card.querySelector(".award-year").value,

        // Read the recognition level.
        level: card.querySelector(".award-level").value,

        // Read the recognition type.
        recognition_type: card.querySelector(
            ".award-recognition-type"
        ).value,

        // Read the full award description.
        description: card.querySelector(".award-description").value.trim()
    }));
}


/**
 * Search colleges whenever the student types.
 */
collegeSearchInput.addEventListener("input", async () => {
    // Remove extra spaces from the search text.
    const query = collegeSearchInput.value.trim();

    // Clear results when the input is empty.
    if (!query) {
        searchResults.innerHTML = "";
        return;
    }

    try {
        // Ask the Flask backend for matching colleges.
        const response = await fetch(
            `/api/colleges?q=${encodeURIComponent(query)}`
        );

        // Convert the JSON response into a JavaScript array.
        const colleges = await response.json();

        // Create up to six search-result buttons.
        searchResults.innerHTML = colleges.slice(0, 6).map(college => `
            <button
                class="search-result"
                type="button"
                data-name="${college.name}"
            >
                <span>${college.name}</span>
                <strong>${college.acceptance_rate}% sample admit rate</strong>
            </button>
        `).join("");

        // Find every newly created search button.
        document.querySelectorAll(".search-result").forEach(button => {
            // Add the college when its result is clicked.
            button.addEventListener("click", () => {
                addCollege(button.dataset.name);
            });
        });
    } catch (error) {
        // Print technical details in the browser console.
        console.error("College search failed:", error);

        // Show a readable error in the dropdown.
        searchResults.innerHTML = `
            <p class="search-error">College search is temporarily unavailable.</p>
        `;
    }
});


/**
 * Add one college to the selected list.
 */
function addCollege(name) {
    // Only add a college when it is not already selected.
    if (!selectedColleges.includes(name)) {
        selectedColleges.push(name);
    }

    // Clear the search field.
    collegeSearchInput.value = "";

    // Hide the search results.
    searchResults.innerHTML = "";

    // Redraw the selected-college chips.
    renderSelectedColleges();
}


/**
 * Remove one college from the selected list.
 */
function removeCollege(name) {
    // Keep every college except the one being removed.
    selectedColleges = selectedColleges.filter(
        college => college !== name
    );

    // Redraw the selected-college chips.
    renderSelectedColleges();
}


/**
 * Display selected colleges as removable chips.
 */
function renderSelectedColleges() {
    // Show an empty message when no college is selected.
    if (selectedColleges.length === 0) {
        selectedCollegesContainer.innerHTML = `
            <p class="empty-state">No colleges selected yet.</p>
        `;
        return;
    }

    // Create one chip for each selected college.
    selectedCollegesContainer.innerHTML = selectedColleges.map(name => `
        <span class="college-chip">
            ${name}

            <button
                type="button"
                aria-label="Remove ${name}"
                data-name="${name}"
            >
                ×
            </button>
        </span>
    `).join("");

    // Add removal behavior to every chip button.
    document.querySelectorAll(".college-chip button").forEach(button => {
        button.addEventListener("click", () => {
            removeCollege(button.dataset.name);
        });
    });
}


/**
 * Collect every section of the student profile.
 */
function collectProfile() {
    // Return one complete profile object.
    return {
        // Read the student's basic information.
        student_name: document.getElementById("student_name").value.trim(),
        grade_level: document.getElementById("grade_level").value,
        graduation_year: document.getElementById("graduation_year").value,

        // Read academic information.
        gpa: document.getElementById("gpa").value,
        test_score: document.getElementById("test_score").value,
        course_rigor: document.getElementById("course_rigor").value,

        // Read all dynamic extracurricular cards.
        extracurriculars: collectExtracurriculars(),

        // Read all dynamic award cards.
        awards: collectAwards(),

        // Read major, minor, and career-interest information.
        intended_major: document.getElementById("intended_major").value.trim(),
        second_major: document.getElementById("second_major").value.trim(),
        intended_minor: document.getElementById("intended_minor").value.trim(),
        career_interests: document.getElementById("career_interests").value.trim(),
        interest_statement: document.getElementById(
            "interest_statement"
        ).value.trim(),

        // Read the student's longer profile statement.
        essay: document.getElementById("essay").value.trim()
    };
}


/**
 * Send the student profile to Flask when Calculate is clicked.
 */
calculateButton.addEventListener("click", async () => {
    // Read the GPA field.
    const gpa = document.getElementById("gpa").value;

    // Require a GPA before calculation.
    if (!gpa) {
        alert("Please enter a GPA first.");
        return;
    }

    // Require at least one selected college.
    if (selectedColleges.length === 0) {
        alert("Please add at least one college.");
        return;
    }

    // Gather the full student profile.
    const profile = collectProfile();

    // Show the loading text.
    loading.classList.remove("hidden");

    // Hide old results while a new result is loading.
    resultsContent.classList.add("hidden");

    try {
        // Send profile data to the Flask score route.
        const response = await fetch("/api/score", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                profile: profile,
                colleges: selectedColleges
            })
        });

        // Stop and show an error when the server response is unsuccessful.
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        // Convert the server JSON into a JavaScript object.
        const data = await response.json();

        // Draw the score, recommendations, and comparisons.
        renderResults(data, profile);
    } catch (error) {
        // Print the technical error for debugging.
        console.error("Score calculation failed:", error);

        // Show a readable message to the student.
        alert(
            "Something went wrong while calculating the score. " +
            "Check that the Flask server is still running."
        );
    } finally {
        // Hide the loading text whether the request passed or failed.
        loading.classList.add("hidden");
    }
});


/**
 * Draw all result sections using data from Flask.
 */
function renderResults(data, profile) {
    // Display the overall ScholarScore.
    document.getElementById("student-score").textContent =
        data.student_score;

    // Display the academic category score.
    document.getElementById("academic-score").textContent =
        data.breakdown.academic;

    // Display the activity category score.
    document.getElementById("extracurricular-score").textContent =
        data.breakdown.extracurriculars;

    // Display the awards category score.
    document.getElementById("award-score").textContent =
        data.breakdown.awards;

    // Display the student-story score.
    document.getElementById("essay-score").textContent =
        data.breakdown.essay;

    // Display the major-focus score.
    document.getElementById("interest-score").textContent =
        data.breakdown.interests;

    // Display the responsible-AI model note.
    document.getElementById("model-note").textContent =
        data.model_note;

    // Begin with a default result heading.
    let message = "Keep building your profile.";

    // Create a stronger message for high scores.
    if (data.student_score >= 85) {
        message = "You have a strong, detailed, and focused profile.";
    } else if (data.student_score >= 70) {
        // Create a balanced message for middle-high scores.
        message = "You have a solid profile with clear areas to strengthen.";
    } else if (data.student_score >= 55) {
        // Create an encouraging message for developing profiles.
        message = "Your profile has a foundation and needs more depth.";
    }

    // Add the student's name when it was provided.
    if (profile.student_name) {
        message = `${profile.student_name}, ${message.charAt(0).toLowerCase()}${message.slice(1)}`;
    }

    // Display the final score heading.
    document.getElementById("score-message").textContent = message;

    // Find the recommendation container.
    const recommendationContainer =
        document.getElementById("recommendations");

    // Create one recommendation card for each suggestion.
    recommendationContainer.innerHTML = data.recommendations.map(item => `
        <article class="recommendation-card card">
            <span class="recommendation-score">${item.score}</span>
            <div>
                <h3>${item.category}</h3>
                <p>${item.message}</p>
            </div>
        </article>
    `).join("");

    // Find the college comparison container.
    const comparisonContainer =
        document.getElementById("college-comparisons");

    // Create a comparison card for every selected college.
    comparisonContainer.innerHTML = data.comparisons.map(item => `
        <article class="comparison-card card">
            <div class="comparison-top">
                <div>
                    <span class="eyebrow">College match</span>
                    <h3>${item.college}</h3>
                </div>

                <span class="badge">${item.category}</span>
            </div>

            <div class="score-row">
                <div>
                    <span>Student score</span>
                    <strong>${item.student_score}</strong>
                </div>

                <div>
                    <span>College score</span>
                    <strong>${item.college_score}</strong>
                </div>

                <div>
                    <span>Overall fit</span>
                    <strong>${item.fit_score}</strong>
                </div>

                <div>
                    <span>Major match</span>
                    <strong>${item.major_alignment}</strong>
                </div>
            </div>

            <p>${item.message}</p>

            <p>${item.major_message}</p>

            <div class="strength-list">
                <span>Sample academic strengths:</span>

                ${item.major_strengths.map(strength => `
                    <small>${strength}</small>
                `).join("")}
            </div>

            <p>
                Sample profile: ${item.acceptance_rate}% acceptance rate,
                ${item.avg_gpa} average GPA, and
                ${item.avg_test_score} average SAT.
            </p>

            <p class="disclaimer">${item.disclaimer}</p>
        </article>
    `).join("");

    // Reveal the completed result section.
    resultsContent.classList.remove("hidden");

    // Smoothly move the browser to the results.
    document.getElementById("results").scrollIntoView({
        behavior: "smooth"
    });
}


// Add a new activity card when its button is clicked.
addActivityButton.addEventListener("click", addActivityCard);

// Add a new award card when its button is clicked.
addAwardButton.addEventListener("click", addAwardCard);

// Add the first activity card when the website loads.
addActivityCard();

// Add the first award card when the website loads.
addAwardCard();
