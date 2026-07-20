# ScholarScore Expanded

ScholarScore is a blue-and-white college-planning web app prototype for the
Congressional App Challenge.

This expanded version allows a student to enter:

- Academic information
- Multiple extracurricular activities
- Roles and leadership positions
- Years, hours per week, and weeks per year
- Detailed activity impact descriptions
- Multiple awards and honors
- Award level and recognition type
- Intended major
- Possible second major
- Possible minor
- Career interests
- A written explanation of academic interests
- A longer student profile statement
- A list of colleges to compare

## Why majors and minors belong in the app

A major section is useful because students are not only applying to a college;
they are often applying with an academic direction. A student's intended field
can affect:

- Which colleges are a strong academic fit
- Which activities are most relevant
- Which classes and projects strengthen the application
- Which career opportunities the student may want
- How the student explains their story

A minor should be optional. Many high-school students do not know their minor
yet, and most colleges do not require students to select one during admission.

## How the updated score works

The overall ScholarScore uses these weights:

- Academics: 45%
- Extracurricular activities: 23%
- Awards and honors: 10%
- Student story: 12%
- Major and career focus: 10%

The extracurricular score considers:

- Years involved
- Hours per week
- Weeks per year
- Leadership
- Description quality
- Action words
- Numbers and measurable impact
- Depth of the strongest activities
- Breadth across multiple activities

The awards score considers:

- School, local, regional, state, national, or international level
- Winner, finalist, placement, selection, recognition, or participation
- Description quality
- Number of meaningful awards

The major-focus score considers:

- Intended major
- Possible second major
- Possible minor
- Career interests
- How clearly the student connects interests to experiences

## Responsible AI note

This app does not calculate a guaranteed chance of admission. Admissions
decisions are holistic and can include institutional priorities that are not
available in public datasets.

ScholarScore instead provides:

- A transparent student profile score
- A sample college benchmark
- A Reach, Target, or Likely planning category
- A sample major-interest alignment score
- Improvement recommendations

## Run the website in VS Code

### 1. Open the project

Unzip the folder and open `ScholarScore_Expanded` in VS Code.

### 2. Open the terminal

Click:

```text
Terminal → New Terminal
```

### 3. Create a virtual environment

Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install the libraries

```bash
pip install -r requirements.txt
```

### 5. Run Flask

Mac:

```bash
python3 app.py
```

Windows:

```bash
python app.py
```

### 6. Open the website

```text
http://127.0.0.1:5000
```

## Project structure

```text
ScholarScore_Expanded/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   ├── colleges.json
│   └── sources.txt
├── scrapers/
│   └── sample_scraper.py
├── static/
│   ├── script.js
│   └── style.css
└── templates/
    └── index.html
```

## Good future additions

- Save student profiles with accounts
- Add a database such as SQLite
- Connect to the College Scorecard API
- Add school-specific program data
- Let students upload a resume
- Create charts for activity and academic categories
- Add essay-topic feedback without writing the essay for the student
- Add a timeline for application deadlines
- Add financial-aid and scholarship matching
- Let users export a profile report as a PDF
