import os
from flask import Flask, render_template_string, request
from openai import OpenAI

app = Flask(__name__)

# Sample opportunities for students
opportunities = [
    {
        "title": "Python Developer Intern",
        "degree": "B.Tech",
        "category": "Internship",
        "description": "Learn Python programming and software development.",
        "skills": "Python, Programming"
    },
    {
        "title": "Graduate Engineer Trainee",
        "degree": "B.Tech",
        "category": "Job",
        "description": "Explore entry-level engineering career opportunities.",
        "skills": "Problem Solving, Technical Skills"
    },
    {
        "title": "Merit Scholarship",
        "degree": "Any Degree",
        "category": "Scholarship",
        "description": "Explore scholarships based on merit and eligibility.",
        "skills": "Academic Performance"
    },
    {
        "title": "Business Operations Intern",
        "degree": "B.Com",
        "category": "Internship",
        "description": "Gain experience in business and finance.",
        "skills": "Communication, Excel"
    },
    {
        "title": "Content Writing Intern",
        "degree": "BA",
        "category": "Internship",
        "description": "Explore writing, editing and communication work.",
        "skills": "Writing, Communication"
    },
    {
        "title": "Science Research Intern",
        "degree": "B.Sc",
        "category": "Internship",
        "description": "Explore science and research-related experience.",
        "skills": "Research, Analytical Thinking"
    },
    {
        "title": "Data Analytics Intern",
        "degree": "Any Degree",
        "category": "Internship",
        "description": "Develop data analysis and visualization skills.",
        "skills": "Python, Excel, Data Analysis"
    }
]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">
    <title>GradPath AI</title>

    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f3f6fc;
            color: #202b45;
        }

        header {
            background: linear-gradient(120deg, #173b70, #3769bd);
            color: white;
            padding: 30px 8%;
        }

        header h1 { margin: 0 0 10px; font-size: 32px; }
        header p { margin: 0; }

        main {
            max-width: 1050px;
            margin: 35px auto;
            padding: 0 20px;
        }

        .search-box, .ai-box {
            background: white;
            padding: 25px;
            border-radius: 14px;
            box-shadow: 0 4px 16px #00000010;
            margin-bottom: 24px;
        }

        label {
            display: block;
            margin: 12px 0 7px;
            font-weight: bold;
        }

        select, input, textarea, button {
            padding: 12px;
            border-radius: 7px;
            font-size: 15px;
            margin: 5px 5px 5px 0;
        }

        select, input, textarea {
            border: 1px solid #cbd5e1;
            width: 100%;
            max-width: 100%;
        }

        select { max-width: 300px; }
        textarea { min-height: 120px; resize: vertical; }

        button {
            border: none;
            background: #245bc4;
            color: white;
            cursor: pointer;
        }

        button:hover { background: #173b70; }

        .cards, .ai-grid {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-top: 22px;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0 4px 16px #0000000c;
        }

        .tag {
            display: inline-block;
            background: #e5edff;
            color: #245bc4;
            padding: 6px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }

        .card h3 { margin-bottom: 10px; }
        .skills, .count { color: #52627b; font-size: 14px; }

        .result {
            background: #f0f5ff;
            padding: 18px;
            border-radius: 9px;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            line-height: 1.6;
        }

        .error {
            color: #a12626;
            background: #fff0f0;
            padding: 14px;
            border-radius: 8px;
        }

        footer {
            text-align: center;
            padding: 25px;
            color: #667085;
        }
    </style>
</head>

<body>
<header>
    <h1>GradPath AI</h1>
    <p>Your pathway to scholarships, internships and jobs.</p>
</header>

<main>
    <section class="search-box">
        <h2>Find your opportunities</h2>
        <p>Select your degree to explore relevant opportunities.</p>

        <form method="GET" action="/">
            <label for="degree">Choose your degree</label>
            <select name="degree" id="degree">
                <option value="All"
                    {% if selected == 'All' %}selected{% endif %}>
                    All Degrees
                </option>
                <option value="B.Tech"
                    {% if selected == 'B.Tech' %}selected{% endif %}>
                    B.Tech
                </option>
                <option value="B.Com"
                    {% if selected == 'B.Com' %}selected{% endif %}>
                    B.Com
                </option>
                <option value="BA"
                    {% if selected == 'BA' %}selected{% endif %}>
                    BA
                </option>
                <option value="B.Sc"
                    {% if selected == 'B.Sc' %}selected{% endif %}>
                    B.Sc
                </option>
            </select>
            <button type="submit">Find Opportunities</button>
        </form>
    </section>

    <h2>Available Opportunities</h2>
    <p class="count">{{ results|length }} opportunities found</p>

    <section class="cards">
        {% for item in results %}
        <article class="card">
            <span class="tag">{{ item.category }}</span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
            <p class="skills"><strong>Degree:</strong> {{ item.degree }}</p>
            <p class="skills"><strong>Skills:</strong> {{ item.skills }}</p>
        </article>
        {% else %}
        <p>No opportunities match your selection.</p>
        {% endfor %}
    </section>

    <h2>AI Career Tools</h2>
    <p>Get personalized suggestions to help plan your next steps.</p>

    <section class="ai-grid">
        <article class="ai-box">
            <h3>AI Internship Recommendations</h3>
            <p>Find opportunities that match your skills and interests.</p>
            <form method="POST" action="/ai">
                <input type="hidden" name="feature"
                       value="recommendations">

                <label for="rec_degree">Your degree</label>
                <select id="rec_degree" name="degree" required>
                    <option value="">Select degree</option>
                    <option>B.Tech</option>
                    <option>B.Com</option>
                    <option>BA</option>
                    <option>B.Sc</option>
                    <option>Other</option>
                </select>

                <label for="rec_skills">Your skills</label>
                <textarea id="rec_skills" name="skills"
                    maxlength="1000" required
                    placeholder="e.g. Python, Excel, communication"></textarea>

                <label for="rec_interests">Your interests</label>
                <textarea id="rec_interests" name="interests"
                    maxlength="1000" required
                    placeholder="e.g. software, finance, research"></textarea>

                <button type="submit">Get Recommendations</button>
            </form>
        </article>

        <article class="ai-box">
            <h3>AI Career Guidance</h3>
            <p>Explore career paths, skills and learning plans.</p>
            <form method="POST" action="/ai">
                <input type="hidden" name="feature" value="career">

                <label for="career_degree">Your degree</label>
                <select id="career_degree" name="degree" required>
                    <option value="">Select degree</option>
                    <option>B.Tech</option>
                    <option>B.Com</option>
                    <option>BA</option>
                    <option>B.Sc</option>
                    <option>Other</option>
                </select>

                <label for="career_skills">Your skills</label>
                <textarea id="career_skills" name="skills"
                    maxlength="1000" required
                    placeholder="What skills do you have?"></textarea>

                <label for="career_interests">Your interests</label>
                <textarea id="career_interests" name="interests"
                    maxlength="1000" required
                    placeholder="What subjects or careers interest you?"></textarea>

                <button type="submit">Get Career Guidance</button>
            </form>
        </article>

        <article class="ai-box">
            <h3>AI Resume Analysis</h3>
            <p>Get suggestions to improve your resume.</p>
            <form method="POST" action="/ai">
                <input type="hidden" name="feature" value="resume">

                <label for="resume">Paste your resume text</label>
                <textarea id="resume" name="resume"
                    maxlength="10000" required
                    placeholder="Paste resume text here..."></textarea>

                <p class="skills">
                    Remove your phone number, address and other
                    personal details before pasting.
                </p>

                <button type="submit">Analyze Resume</button>
            </form>
        </article>
    </section>

    {% if ai_result %}
    <section class="ai-box">
        <h2>GradPath AI Results</h2>
        <div class="result">{{ ai_result }}</div>
    </section>
    {% endif %}
</main>

<footer>GradPath AI | Student Opportunities Navigator</footer>
</body>
</html>
"""


def generate_ai_advice(feature, degree, skills, interests, resume=""):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "AI is not configured. Please add OPENAI_API_KEY "
            "to your Render environment variables."
        )

    if feature == "recommendations":
        prompt = f"""
Recommend suitable student opportunities based on the information below.

Degree: {degree}
Skills: {skills}
Interests: {interests}

Available sample opportunities:
{opportunities}

Explain which listed opportunities may fit and why. Identify skills
to develop and suggest practical next steps. Clearly distinguish
these sample opportunities from verified live vacancies. Do not
invent employers, open positions, deadlines, or application links.
"""

    elif feature == "career":
        prompt = f"""
Give practical career guidance to a student.

Degree: {degree}
Skills: {skills}
Interests: {interests}

Suggest suitable career paths, skills to develop, beginner projects,
and a realistic learning roadmap. Explain that these are suggestions,
not guarantees, and avoid making unsupported claims about job openings.
"""

    elif feature == "resume":
        prompt = f"""
Review the resume text provided by the student.

Resume:
{resume}

Provide:
1. Strengths in the resume.
2. Suggestions for clearer wording.
3. Relevant skills or projects to highlight.
4. Formatting and organization improvements.
5. Examples of stronger bullet points where appropriate.

Do not invent qualifications, achievements, or experience.
Avoid repeating personal contact details.
"""

    else:
        return "Please select a valid AI feature."

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        instructions=(
            "You are GradPath AI, a supportive student career assistant. "
            "Be practical, respectful, clear and honest. Never invent facts."
        ),
        input=prompt,
        max_output_tokens=700,
    )

    return response.output_text


@app.route("/")
def home():
    selected = request.args.get("degree", "All")

    if selected not in ("All", "B.Tech", "B.Com", "BA", "B.Sc"):
        selected = "All"

    if selected == "All":
        results = opportunities
    else:
        results = [
            item for item in opportunities
            if item["degree"] in (selected, "Any Degree")
        ]

    return render_template_string(
        HTML_PAGE,
        results=results,
        selected=selected,
        ai_result=None,
    )


@app.route("/ai", methods=["POST"])
def ai_features():
    feature = request.form.get("feature", "").strip()
    degree = request.form.get("degree", "").strip()[:100]
    skills = request.form.get("skills", "").strip()[:1000]
    interests = request.form.get("interests", "").strip()[:1000]
    resume = request.form.get("resume", "").strip()[:10000]

    if feature not in ("recommendations", "career", "resume"):
        return "Invalid AI feature.", 400

    if feature == "resume":
        if not resume:
            return "Please enter your resume text.", 400
    elif not degree or not skills or not interests:
        return "Please complete all required fields.", 400

    try:
        ai_result = generate_ai_advice(
            feature=feature,
            degree=degree,
            skills=skills,
            interests=interests,
            resume=resume,
        )
    except Exception:
        app.logger.exception("GradPath AI request failed")
        ai_result = (
            "Sorry, the AI request could not be completed. "
            "Please check your OpenAI API key, API billing or credits, "
            "model access, and server logs before trying again."
        )

    selected = "All"
    results = opportunities

    return render_template_string(
        HTML_PAGE,
        results=results,
        selected=selected,
        ai_result=ai_result,
    )


if __name__ == "__main__":
    app.run(debug=True)
