import streamlit as st
import pandas as pd
import re
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(
    page_title="Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Screening Tool")
st.write(
    "Upload a Job Description and one or more Resumes "
    "to automatically calculate candidate matching scores."
)

st.divider()

EDUCATION_DIRECT = {
    "data science",
    "computer science",
    "information technology",
    "information systems",
    "statistics",
    "mathematics",
    "machine learning",
    "artificial intelligence",
    "computer engineering"
}

EDUCATION_RELATED = {
    "software engineering",
    "engineering",
    "electrical engineering",
    "mechanical engineering",
    "industrial and systems engineering"
}

related_terms = {
    "data science": {
        "data scientist",
        "data analytics",
        "data analysis",
        "machine learning"
    },
    "data analysis": {
        "data analyst",
        "analytics",
        "data analytics"
    },
    "machine learning": {
        "ml",
        "predictive modeling",
        "artificial intelligence",
        "ai"
    },
    "data visualization": {
        "visualization",
        "tableau",
        "power bi",
        "matplotlib",
        "seaborn"
    },
    "statistics": {
        "statistical modeling",
        "statistical analysis"
    },
    "python": {
        "python programming"
    },
    "sql": {
        "mysql",
        "postgresql",
        "database querying"
    }
}

skill_weights = {
    "python": 15,
    "sql": 8,
    "pandas": 8,
    "numpy": 5,
    "data analysis": 8,
    "statistics": 12,
    "data visualization": 5,
    "machine learning": 15,
    "predictive modeling": 14,
    "scikit-learn": 10
}

if "results_df" not in st.session_state:
    st.session_state.results_df = None

if "job_profile" not in st.session_state:
    st.session_state.job_profile = None

if "selected_resume" not in st.session_state:
    st.session_state.selected_resume = None


def extract_education(resume_text):
    text = str(resume_text).lower()
    education_section = text

    education_patterns = [
        r'\beducation\b(.*?)(?=\b(?:skills|experience|work experience|professional experience|employment|projects|certifications|achievements|summary|objective)\b)',
        r'\bqualification[s]?\b(.*?)(?=\b(?:skills|experience|work experience|employment|projects|certifications)\b)'
    ]

    for pattern in education_patterns:
        match = re.search(
            pattern,
            text,
            re.DOTALL
        )

        if match:
            education_section = match.group(1)
            break

    degree_patterns = {
        "b.e": r'\b(?:b\.e\.?|bachelors?\s+of\s+engineering)\b',
        "b.tech": r'\b(?:b\.tech\.?|btech|bachelors?\s+of\s+technology)\b',
        "b.sc": r'\b(?:b\.sc\.?|bsc|b\.s\.?|bachelors?\s+of\s+science)\b',
        "m.e": r'\b(?:m\.e\.?|masters?\s+of\s+engineering)\b',
        "m.tech": r'\b(?:m\.tech\.?|mtech|masters?\s+of\s+technology)\b',
        "m.sc": r'\b(?:m\.sc\.?|msc|m\.s\.?|masters?\s+of\s+science)\b',
        "mba": r'\bmba\b',
        "ph.d": r'\b(?:ph\.d\.?|phd|doctor\s+of\s+philosophy)\b'
    }

    degrees = []

    for degree, pattern in degree_patterns.items():
        if re.search(pattern, education_section):
            degrees.append(degree)

    field_patterns = [
        "data science",
        "computer science",
        "information technology",
        "information systems",
        "statistics",
        "mathematics",
        "machine learning",
        "artificial intelligence",
        "software engineering",
        "computer engineering",
        "mechanical engineering",
        "electrical engineering",
        "civil engineering",
        "business administration",
        "finance",
        "marketing",
        "industrial and systems engineering"
    ]

    fields = []

    for field in field_patterns:
        if field in education_section:
            fields.append(field)

    return {
        "degrees": degrees,
        "fields": fields
    }


def calculate_education_match(
    candidate_education,
    required_education
):
    if not isinstance(candidate_education, dict):
        return 0.0

    fields = {
        field.lower().strip()
        for field in candidate_education.get(
            "fields",
            []
        )
    }

    if not fields:
        return 0.0

    if fields.intersection(EDUCATION_DIRECT):
        return 100.0

    if fields.intersection(EDUCATION_RELATED):
        return 60.0

    return 0.0


def extract_experience(resume_text):
    text = str(resume_text).lower()

    patterns = [
        r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:professional\s+)?(?:work\s+)?experience',
        r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:relevant\s+)?experience',
        r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+(?:in|of)\s+(?:professional\s+)?(?:work|employment)',
        r'(?:experience|worked|working)\s+(?:for|of|with)?\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)'
    ]

    values = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text
        )

        for match in matches:
            try:
                values.append(
                    float(match)
                )
            except:
                pass

    if values:
        return round(
            max(values),
            2
        )

    return 0.0


def calculate_job_relevance(
    resume_text,
    jd_terms
):
    resume_text = str(
        resume_text
    ).lower()

    matched_terms = []

    for jd_term in jd_terms:
        jd_term_lower = jd_term.lower()

        if jd_term_lower in resume_text:
            matched_terms.append(
                jd_term
            )
            continue

        related = related_terms.get(
            jd_term_lower,
            set()
        )

        if any(
            term in resume_text
            for term in related
        ):
            matched_terms.append(
                jd_term
            )

    if len(jd_terms) == 0:
        return 0.0

    score = (
        len(set(matched_terms))
        /
        len(jd_terms)
    ) * 100

    return round(
        score,
        2
    )


def calculate_skill_match(
    resume_text,
    required_skills
):
    resume_text = str(
        resume_text
    ).lower()

    matched = []
    missing = []

    for skill in required_skills:
        skill_lower = skill.lower().strip()

        if skill_lower in resume_text:
            matched.append(
                skill_lower
            )
        else:
            missing.append(
                skill_lower
            )

    total_weight = sum(
        skill_weights.get(
            skill,
            1
        )
        for skill in required_skills
    )

    matched_weight = sum(
        skill_weights.get(
            skill,
            1
        )
        for skill in matched
    )

    if total_weight == 0:
        score = 0.0
    else:
        score = (
            matched_weight
            /
            total_weight
        ) * 100

    return (
        round(score, 2),
        matched,
        missing
    )


def calculate_experience_match(
    candidate_experience,
    required_experience
):
    if required_experience <= 0:
        return 100.0

    if candidate_experience >= required_experience:
        return 100.0

    return round(
        (
            candidate_experience
            /
            required_experience
        ) * 100,
        2
    )


def get_eligibility(row):
    experience_gap = (
        row["Experience Match"] < 100
    )

    education_gap = (
        row["Education Match"] < 100
    )

    if not experience_gap and not education_gap:
        return "Eligible"

    elif experience_gap and education_gap:
        return "Experience + Education Gap"

    elif experience_gap:
        return "Experience Gap"

    else:
        return "Education Gap"


def get_recommendation(score):
    if score >= 70:
        return "Good Match"

    elif score >= 50:
        return "Moderate Match"

    else:
        return "Weak Match"


def extract_file_text(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        return uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

    elif filename.endswith(".pdf"):
        reader = PdfReader(
            uploaded_file
        )

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif filename.endswith(".docx"):
        document = Document(
            uploaded_file
        )

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text

    return ""


def extract_jd_requirements(jd_text):
    text = jd_text.lower()

    experience_patterns = [
        r'(\d+(?:\.\d+)?)\+?\s*years?',
        r'(\d+(?:\.\d+)?)\+?\s*yrs?'
    ]

    required_experience = 0.0

    for pattern in experience_patterns:
        matches = re.findall(
            pattern,
            text
        )

        if matches:
            required_experience = max(
                float(x)
                for x in matches
            )
            break

    all_skills = list(
        skill_weights.keys()
    )

    required_skills = []

    for skill in all_skills:
        if skill.lower() in text:
            required_skills.append(
                skill
            )

    relevant_terms = []

    possible_terms = [
        "data science",
        "data analysis",
        "data analyst",
        "machine learning",
        "statistical modeling",
        "predictive modeling",
        "data visualization",
        "artificial intelligence"
    ]

    for term in possible_terms:
        if term in text:
            relevant_terms.append(
                term
            )

    required_education = []

    education_terms = [
        "data science",
        "computer science",
        "information technology",
        "information systems",
        "statistics",
        "mathematics",
        "machine learning",
        "artificial intelligence",
        "computer engineering"
    ]

    for term in education_terms:
        if term in text:
            required_education.append(
                term
            )

    return {
        "experience": required_experience,
        "skills": required_skills,
        "terms": relevant_terms,
        "education": required_education
    }


def generate_explanation(row):
    matched = str(
        row["Matched Skills"]
    )

    missing = str(
        row["Missing Skills"]
    )

    relevant = str(
        row["Relevant Terms"]
    )

    if matched.strip():
        matched_list = [
            x.strip()
            for x in matched.split(",")
            if x.strip()
        ]

        matched_text = ", ".join(
            matched_list
        )

        matched_count = len(
            matched_list
        )

    else:
        matched_text = "none"
        matched_count = 0

    if missing.strip():
        missing_text = missing
    else:
        missing_text = "none"

    if relevant.strip():
        relevance_text = (
            f"Relevant job terms: {relevant}."
        )
    else:
        relevance_text = (
            "No strong job-specific terms detected."
        )

    return (
        f"Candidate has an experience match of "
        f"{row['Experience Match']:.1f}% and an education "
        f"match of {row['Education Match']:.1f}%. "

        f"The candidate matches {matched_count} required "
        f"skills ({matched_text}). "

        f"Skills match is {row['Skills Match']:.1f}%. "

        f"Job relevance is "
        f"{row['Job Relevance']:.1f}%. "

        f"Missing skills include: "
        f"{missing_text}. "

        f"{relevance_text} "

        f"Overall screening score is "
        f"{row['Screening Score']:.1f}%, "

        f"with recommendation: "
        f"{row['Recommendation']}."
    )


st.header("1️⃣ Upload Job Description")

jd_file = st.file_uploader(
    "Upload Job Description (.txt, .pdf, .docx)",
    type=["txt", "pdf", "docx"],
    key="jd"
)

jd_text = st.text_area(
    "Or paste Job Description here",
    height=220,
    placeholder=(
        "Example: We are looking for a Data Scientist "
        "with 2+ years of experience..."
    )
)

st.header("2️⃣ Upload Resumes")

resume_files = st.file_uploader(
    "Upload one or more resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if st.button(
    "🚀 Match Resumes",
    type="primary",
    use_container_width=True
):

    current_jd_text = jd_text

    if jd_file is not None:
        current_jd_text = extract_file_text(
            jd_file
        )

    if not current_jd_text.strip():
        st.error(
            "Please upload or paste a Job Description."
        )
        st.stop()

    if not resume_files:
        st.error(
            "Please upload at least one resume."
        )
        st.stop()

    job_profile = extract_jd_requirements(
        current_jd_text
    )

    required_experience = (
        job_profile["experience"]
    )

    required_skills = (
        job_profile["skills"]
    )

    relevant_terms = (
        job_profile["terms"]
    )

    required_education = (
        job_profile["education"]
    )

    st.session_state.job_profile = job_profile

    with st.expander(
        "🔍 Debug Information"
    ):
        st.write(
            "Required Experience:",
            required_experience
        )

        st.write(
            "Required Skills:",
            required_skills
        )

        st.write(
            "Relevant Terms:",
            relevant_terms
        )

        st.write(
            "Required Education:",
            required_education
        )

    results = []

    progress = st.progress(0)

    for i, uploaded_file in enumerate(
        resume_files
    ):

        resume_text = extract_file_text(
            uploaded_file
        )

        if not resume_text.strip():
            continue

        candidate_experience = (
            extract_experience(
                resume_text
            )
        )

        experience_match = (
            calculate_experience_match(
                candidate_experience,
                required_experience
            )
        )

        candidate_education = (
            extract_education(
                resume_text
            )
        )

        education_match = (
            calculate_education_match(
                candidate_education,
                required_education
            )
        )

        (
            skills_match,
            matched_skills,
            missing_skills
        ) = calculate_skill_match(
            resume_text,
            required_skills
        )

        job_relevance = (
            calculate_job_relevance(
                resume_text,
                relevant_terms
            )
        )

        screening_score = (
            experience_match * 0.20
            +
            education_match * 0.20
            +
            skills_match * 0.40
            +
            job_relevance * 0.20
        )

        screening_score = round(
            screening_score,
            2
        )

        recommendation = (
            get_recommendation(
                screening_score
            )
        )

        result = {
            "Resume": uploaded_file.name,
            "Experience Match": experience_match,
            "Education Match": education_match,
            "Skills Match": skills_match,
            "Job Relevance": job_relevance,
            "Screening Score": screening_score,
            "Recommendation": recommendation,
            "Matched Skills": ", ".join(
                matched_skills
            ),
            "Missing Skills": ", ".join(
                missing_skills
            ),
            "Relevant Terms": ", ".join(
                relevant_terms
            )
        }

        results.append(
            result
        )

        progress.progress(
            (i + 1) / len(resume_files)
        )

    if not results:
        st.error(
            "Could not extract text from the uploaded resumes."
        )
        st.stop()

    results_df = pd.DataFrame(
        results
    )

    results_df["Eligibility"] = (
        results_df.apply(
            get_eligibility,
            axis=1
        )
    )

    results_df["Explanation"] = (
        results_df.apply(
            generate_explanation,
            axis=1
        )
    )

    results_df = results_df.sort_values(
        "Screening Score",
        ascending=False
    ).reset_index(
        drop=True
    )

    results_df["Rank"] = (
        results_df.index + 1
    )

    st.session_state.results_df = results_df

    st.session_state.selected_resume = (
        results_df.iloc[0]["Resume"]
    )

    st.rerun()


if st.session_state.results_df is not None:

    results_df = st.session_state.results_df

    st.divider()

    st.header(
        "📊 Screening Results"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Resumes",
        len(results_df)
    )

    col2.metric(
        "Eligible",
        int(
            (
                results_df["Eligibility"]
                == "Eligible"
            ).sum()
        )
    )

    col3.metric(
        "Best Score",
        f"{results_df['Screening Score'].max():.1f}%"
    )

    col4.metric(
        "Good Matches",
        int(
            (
                results_df["Recommendation"]
                == "Good Match"
            ).sum()
        )
    )

    best = results_df.iloc[0]

    st.subheader(
        "🏆 Best Matching Candidate"
    )

    st.success(
        f"{best['Resume']} — "
        f"{best['Screening Score']:.1f}% — "
        f"{best['Recommendation']}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Experience Match:** "
            f"{best['Experience Match']:.1f}%"
        )

        st.write(
            f"**Education Match:** "
            f"{best['Education Match']:.1f}%"
        )

        st.write(
            f"**Skills Match:** "
            f"{best['Skills Match']:.1f}%"
        )

        st.write(
            f"**Job Relevance:** "
            f"{best['Job Relevance']:.1f}%"
        )

    with col2:

        st.write(
            f"**Eligibility:** "
            f"{best['Eligibility']}"
        )

        st.write(
            f"**Matched Skills:** "
            f"{best['Matched Skills'] or 'None'}"
        )

        st.write(
            f"**Missing Skills:** "
            f"{best['Missing Skills'] or 'None'}"
        )

    st.info(
        best["Explanation"]
    )

    st.subheader(
        "🏅 Ranked Candidates"
    )

    display_columns = [
        "Rank",
        "Resume",
        "Experience Match",
        "Education Match",
        "Skills Match",
        "Job Relevance",
        "Screening Score",
        "Recommendation",
        "Eligibility"
    ]

    st.dataframe(
        results_df[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "🔎 Candidate Details"
    )

    resume_list = results_df[
        "Resume"
    ].tolist()

    current_selected = (
        st.session_state.selected_resume
    )

    if current_selected not in resume_list:
        current_selected = resume_list[0]

    selected_resume = st.selectbox(
        "Select a candidate",
        resume_list,
        index=resume_list.index(
            current_selected
        ),
        key="candidate_selector"
    )

    st.session_state.selected_resume = (
        selected_resume
    )

    selected = results_df[
        results_df["Resume"]
        == selected_resume
    ].iloc[0]

    st.write(
        f"### {selected['Resume']}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Screening Score",
            f"{selected['Screening Score']:.1f}%"
        )

    with col2:
        st.metric(
            "Skills Match",
            f"{selected['Skills Match']:.1f}%"
        )

    with col3:
        st.metric(
            "Job Relevance",
            f"{selected['Job Relevance']:.1f}%"
        )

    st.write(
        f"**Recommendation:** "
        f"{selected['Recommendation']}"
    )

    st.write(
        f"**Eligibility:** "
        f"{selected['Eligibility']}"
    )

    st.write(
        f"**Experience Match:** "
        f"{selected['Experience Match']:.1f}%"
    )

    st.write(
        f"**Education Match:** "
        f"{selected['Education Match']:.1f}%"
    )

    st.write(
        f"**Matched Skills:** "
        f"{selected['Matched Skills'] or 'None'}"
    )

    st.write(
        f"**Missing Skills:** "
        f"{selected['Missing Skills'] or 'None'}"
    )

    st.write(
        f"**Relevant Terms:** "
        f"{selected['Relevant Terms'] or 'None'}"
    )

    st.info(
        selected["Explanation"]
    )

    st.divider()

    st.header(
        "📈 Visualizations"
    )

    st.subheader(
        "1. Screening Score by Candidate"
    )

    score_chart = results_df[
        [
            "Resume",
            "Screening Score"
        ]
    ].set_index(
        "Resume"
    )

    st.bar_chart(
        score_chart
    )

    st.subheader(
        "2. Recommendation Distribution"
    )

    recommendation_counts = (
        results_df[
            "Recommendation"
        ]
        .value_counts()
    )

    st.bar_chart(
        recommendation_counts
    )

    st.subheader(
        "3. Candidate Match Components"
    )

    component_df = results_df[
        [
            "Resume",
            "Experience Match",
            "Education Match",
            "Skills Match",
            "Job Relevance"
        ]
    ].set_index(
        "Resume"
    )

    st.bar_chart(
        component_df
    )

    st.divider()

    st.subheader(
        "⬇️ Export Results"
    )

    csv = results_df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )

    st.download_button(
        label="Download Screening Results CSV",
        data=csv,
        file_name="resume_screening_results.csv",
        mime="text/csv",
        use_container_width=True
    )