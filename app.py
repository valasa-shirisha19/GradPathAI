
from flask import Flask, render_template_string, request

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GradPath AI</title>

    <style>
        * {
            box-sizing: border-box;
        }

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

        header h1 {
            margin: 0 0 10px;
            font-size: 32px;
        }

        header p {
            margin: 0;
        }

        main {
            max-width: 1050px;
            margin: 35px auto;
            padding: 0 20px;
        }

        .search-box {
            background: white;
            padding: 25px;
            border-radius: 14px;
            box-shadow: 0 4px 16px #00000010;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }

        select, button {
            padding: 12px;
            border-radius: 7px;
            font-size: 15px;
            margin: 5px 5px 5px 0;
        }

        select {
            border: 1px solid #cbd5e1;
            min-width: 190px;
        }

        button {
            border: none;
            background: #245bc4;
            color: white;
            cursor: pointer;
        }

        button:hover {
            background: #173b70;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
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

        .card h3 {
            margin-bottom: 10px;
        }

        .skills {
            color: #52627b;
            font-size: 14px;
        }

        .count {
            color: #52627b;
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

            <form method="GET">
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
                    <p class="skills">
                        <strong>Degree:</strong> {{ item.degree }}
                    </p>
                    <p class="skills">
                        <strong>Skills:</strong> {{ item.skills }}
                    </p>
                </article>
            {% else %}
                <p>No opportunities match your selection.</p>
            {% endfor %}
        </section>
    </main>

    <footer>
        GradPath AI | Student Opportunities Navigator
    </footer>
</body>
</html>
"""


@app.route("/")
def home():
    selected = request.args.get("degree", "All")

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
        selected=selected
    )


if __name__ == "__main__":
    app.run(debug=True)
