# Resume_Screening_Tool
An NLP-based Resume Screening Tool built with Python and Streamlit to evaluate resumes against job descriptions. It scores candidates based on skills, education, experience, and job relevance, identifies matched and missing skills, checks eligibility, and ranks candidates to support recruitment decisions.

Resume Screening Tool
An intelligent, explainable resume screening application that evaluates and ranks candidates against a given Job Description (JD). Built using Python, NLP-based text processing, weighted matching techniques, and Streamlit.
The application analyzes resumes based on experience, education, required skills, job-specific relevance, and eligibility. It generates screening scores, identifies matched and missing skills, ranks eligible candidates, and provides explanations and visualizations to support recruiters during initial screening.
Table of Contents
1.	Project Overview
2.	Objectives
3.	Dataset
4.	Technologies Used
5.	System Workflow
6.	Resume Processing
7.	Education Matching
8.	Experience Matching
9.	Skill Matching
10.	Weighted Skill Scoring
11.	Job Relevance
12.	Screening Score
13.	Candidate Eligibility
14.	Recommendation System
15.	Candidate Ranking
16.	Example Candidate Explanation
17.	Streamlit Application
18.	Visualizations
19.	Machine Learning Experiments
20.	Project Structure
21.	Installation and Setup
22.	Advantages
23.	Limitations
24.	Future Improvements
25.	Ethical Considerations
26.	Conclusion
1. Project Overview
Recruiters often need to review a large number of resumes for a single job opening. Manually comparing each resume against job requirements can be time-consuming and inconsistent.
The Resume Screening Tool simplifies this process by comparing candidate resumes with a provided Job Description. It extracts relevant information, evaluates candidates using weighted criteria, checks mandatory eligibility requirements, and ranks eligible candidates based on their screening scores.
The application also explains candidate results by displaying matched skills, missing skills, component scores, and relevant job terms.
2. Objectives
•	Automate the initial resume screening process.
•	Compare candidate resumes against a Job Description.
•	Identify matched and missing skills.
•	Evaluate education and experience requirements.
•	Measure job-specific relevance.
•	Calculate an overall screening score.
•	Check candidate eligibility against mandatory requirements.
•	Rank eligible candidates by screening score.
•	Provide explainable candidate-level results.
•	Display screening results through an interactive web application.
3. Dataset
The project uses a Kaggle Resume Dataset containing resumes from multiple professional categories.
Attribute	Details
Resumes after preprocessing	2,481
Resume categories	24
TF-IDF features explored	5,000
Examples of categories include:
•	INFORMATION-TECHNOLOGY
•	BUSINESS-DEVELOPMENT
•	ENGINEERING
•	ACCOUNTANT
•	CONSULTANT
•	BANKING
•	AGRICULTURE
•	FINANCE
•	FITNESS
•	ADVOCATE
•	CHEF
Processed Dataset Columns
•	ID
•	Resume_str
•	Resume_html
•	Category
•	Cleaned_Resume
•	Education_Match_New
•	Job Relevance_New
The last two columns are derived features generated during processing. Additional candidate-level columns are created by the screening and ranking pipeline.
4. Technologies Used
Technology	Purpose
Python	Core programming language
Pandas	Data manipulation and analysis
NumPy	Numerical operations
Regular Expressions (re)	Pattern-based information extraction
Streamlit	Interactive web application
Scikit-learn	TF-IDF vectorization and classification experiments
NLP techniques	Resume text processing and matching
Jupyter Notebook	Data exploration and model experimentation
The final screening pipeline focuses on explainable rule-based and NLP matching. TF-IDF, Logistic Regression, and LSTM were explored during model development for resume category classification.
5. System Workflow
       Job Description + Resumes
                  |
                  v
          Text Extraction
                  |
                  v
       Resume Text Preprocessing
                  |
                  v
      Extract Education & Experience
                  |
                  v
          Required Skill Matching
                  |
                  v
          Job Relevance Analysis
                  |
                  v
        Calculate Screening Score
                  |
                  v
         Check Candidate Eligibility
                  |
                  v
       Rank Eligible Candidates
                  |
                  v
      Explanations & Visualizations
                  |
                  v
          Streamlit Dashboard
6. Resume Processing
Resume text is normalized before being compared with the Job Description.
Processing includes:
•	Converting text to lowercase.
•	Extracting recognized education information.
•	Detecting experience-related patterns.
•	Identifying required skills.
•	Detecting relevant job-related terms.
•	Comparing extracted information with job requirements.
The application uses pattern matching and predefined vocabularies to identify relevant information from candidate resumes.
7. Education Matching
The system extracts education-related information and compares it with the education requirements specified in the Job Description.
Examples of recognized education fields include:
•	Data Science
•	Computer Science
•	Information Technology
•	Information Systems
•	Statistics
•	Mathematics
•	Machine Learning
•	Artificial Intelligence
•	Software Engineering
•	Computer Engineering
•	Mechanical Engineering
•	Electrical Engineering
•	Civil Engineering
•	Business Administration
•	Finance
•	Marketing
Recognized degree patterns include B.E., B.Tech, B.Sc, M.E., M.Tech, M.Sc, MBA, and Ph.D.
Education matching considers direct and related education fields according to predefined matching rules.
A candidate receives a full education match when the configured mandatory education condition is satisfied.
8. Experience Matching
The system uses regular expressions and predefined patterns to detect experience information in resumes.
Examples of supported patterns include:
•	5 years experience
•	3+ years of experience
•	2 years of professional experience
•	2020 - Present
•	January 2021 - Present
The extracted experience is compared with the experience requirement specified in the Job Description.
Experience extraction may not recognize every possible date format or wording, so results should be verified when used for recruitment decisions.
9. Skill Matching
The application compares candidate skills against the required skills identified for the target role.
For the Data Scientist example used during testing, the required skills included:
•	Python
•	SQL
•	Pandas
•	NumPy
•	Data Analysis
•	Statistics
•	Data Visualization
•	Machine Learning
•	Predictive Modeling
•	Scikit-learn
The system identifies:
•	Matched skills
•	Missing skills
•	Skill match percentage
This helps recruiters understand how closely a candidate's listed skills align with the job requirements.
10. Weighted Skill Scoring
Different skills can be assigned different importance weights according to the role's requirements.
Skill	Weight
Python	15
SQL	8
Pandas	8
NumPy	5
Data Analysis	8
Statistics	12
Data Visualization	5
Machine Learning	15
Predictive Modeling	14
Scikit-learn	10
Total	100
The skill match percentage is calculated as:
[
\text{Skill Match} =
\frac{\text{Matched Skill Weight}}
{\text{Total Required Skill Weight}}\times100
]
This approach gives more importance to skills with higher assigned weights.
The weights are configurable examples for the tested role and can be adjusted for different Job Descriptions.
11. Job Relevance
Job relevance measures how closely a resume's content aligns with important concepts from the Job Description.
Example relevant terms include:
•	Data Science
•	Data Analysis
•	Machine Learning
•	Data Analyst
•	Statistical Modeling
The application can also use predefined related-term mappings to recognize selected related concepts.
The relevance score is calculated as:
[
\text{Job Relevance} =
\frac{\text{Matched Relevant Terms}}
{\text{Total Relevant JD Terms}}\times100
]
The score is based on the application's configured vocabulary and matching rules rather than a full semantic understanding of every resume.
12. Screening Score
The overall screening score combines four major components.
Component	Weight
Experience Match	20%
Education Match	20%
Skills Match	40%
Job Relevance	20%
Total	100%
The formula is:
[
\begin{aligned}
\text{Screening Score}={}&
(0.20\times E)\
&+(0.20\times D)\
&+(0.40\times S)\
&+(0.20\times R)
\end{aligned}
]
Where:
•	(E) = Experience Match percentage
•	(D) = Education Match percentage
•	(S) = Skills Match percentage
•	(R) = Job Relevance percentage
The resulting score ranges from 0 to 100.
13. Candidate Eligibility
Candidates are classified according to the configured mandatory education and experience requirements.
Eligibility status	Condition
Eligible	Both mandatory requirements are satisfied
Experience Gap	Required experience is not satisfied
Education Gap	Required education is not satisfied
Experience + Education Gap	Neither mandatory requirement is satisfied
Only eligible candidates are included in the final eligible-candidate ranking.
Eligibility is determined separately from the screening score. A high score does not automatically make a candidate eligible if a mandatory requirement is unmet.
14. Recommendation System
Candidates receive a recommendation based on their overall screening score.
Screening score	Recommendation
70 or above	Good Match
50 to below 70	Moderate Match
Below 50	Weak Match
These categories support initial screening and should not replace human evaluation.
15. Candidate Ranking
Eligible candidates are sorted in descending order of their screening scores.
Example results from testing:
Rank	Candidate ID	Category	Score	Recommendation
1	21156767	CONSULTANT	80.4%	Good Match
2	29839396	BANKING	69.0%	Moderate Match
3	32042584	BUSINESS-DEVELOPMENT	68.0%	Moderate Match
4	11813872	AGRICULTURE	67.4%	Moderate Match
5	18067556	INFORMATION-TECHNOLOGY	67.4%	Moderate Match
These are example results from the tested configuration, not guaranteed results for every Job Description.
16. Example Candidate Explanation
The following example illustrates how the application explains an individual candidate's results.
Candidate ID: 21156767
Metric	Result
Experience Match	100.0%
Education Match	100.0%
Skills Match	51.0%
Job Relevance	100.0%
Screening Score	80.4%
Eligibility	Eligible
Recommendation	Good Match
Matched skills
•	Python
•	SQL
•	Data Analysis
•	Data Visualization
•	Machine Learning
Missing skills
•	Pandas
•	NumPy
•	Statistics
•	Predictive Modeling
•	Scikit-learn
Matched relevant job terms
•	Data Science
•	Data Analysis
•	Machine Learning
This explanation provides more transparency than a ranking based on a single score.
17. Streamlit Application
The project includes an interactive Streamlit application that enables users to:
1.	Enter or upload a Job Description.
2.	Upload multiple candidate resumes.
3.	Process resume text.
4.	Compare resumes with the Job Description.
5.	Calculate screening scores.
6.	Check eligibility.
7.	Rank eligible candidates.
8.	View matched and missing skills.
9.	Inspect individual candidate details.
10.	Review explanations and visualizations.
The interface is designed to make resume screening accessible without requiring users to interact directly with the underlying Python code.
18. Visualizations
The dashboard provides visual summaries of screening results.
Screening Score Distribution
Displays how candidate screening scores are distributed.
Recommendation Distribution
Shows the number of candidates classified as Good Match, Moderate Match, or Weak Match.
Top Candidate Comparison
Compares selected candidates across experience, education, skills, job relevance, and overall screening score.
The visualizations update according to the screening results generated by the application.
19. Machine Learning Experiments
During development, several approaches were evaluated for resume category classification.
Model / Approach	Observed accuracy
Baseline TF-IDF + Logistic Regression	65.79%
Tuned TF-IDF + Logistic Regression	68.41%
Bigram TF-IDF experiment	66.40%
LSTM experiment	20.12%
TF-IDF
Term Frequency–Inverse Document Frequency converts resume text into numerical features based on the importance of terms in documents. The experiment used 5,000 TF-IDF features.
Logistic Regression
Logistic Regression was used to classify resumes into predefined professional categories. Further tuning improved the observed accuracy from 65.79% to 68.41%.
Bigram TF-IDF
The bigram experiment included two-word combinations to capture phrases that individual words might not represent as effectively.
The observed accuracy was 66.40%.
LSTM
A Long Short-Term Memory network was tested as a neural-network approach for text classification. It achieved an observed accuracy of 20.12%, underperforming the simpler TF-IDF and Logistic Regression approach in these experiments.
Final Approach
The final application emphasizes explainable candidate-to-job matching through weighted scoring and NLP-based text processing rather than relying solely on resume category classification.
Important: These classification accuracies measure the experimental models' ability to predict resume categories. They do not measure the accuracy of candidate eligibility decisions or the reliability of the final screening scores.
20. Project Structure
Example repository structure:
Resume-Screening-Tool/
├── app.py
├── Resume_Screening_Tool.ipynb
├── requirements.txt
├── README.md
└── screenshots/
    └── dashboard.png
Adjust this structure to match the actual files in your repository. Include the notebook and screenshots only if they are part of your project.
21. Installation and Setup
Follow these steps to install and run the Resume Screening Tool locally.
Prerequisites
•	Python 3.x
•	pip package manager
•	Git (optional, for cloning the repository)
Step 1: Clone the Repository
git clone https://github.com/YOUR_USERNAME/Resume-Screening-Tool.git
cd Resume-Screening-Tool
Replace YOUR_USERNAME with your GitHub username.
Alternatively, download the repository as a ZIP file from GitHub and extract it.
Step 2: Create a Virtual Environment (Recommended)
Windows — Command Prompt or PowerShell:
python -m venv venv
venv\Scripts\activate
macOS / Linux:
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
If the repository contains a requirements.txt file, run:
pip install -r requirements.txt
Otherwise, install the packages required by the application:
pip install pandas numpy streamlit scikit-learn pypdf python-docx
The exact dependencies depend on the packages imported by the final application. Make sure requirements.txt includes all required packages.
Step 4: Navigate to the Project Directory
Open Command Prompt, PowerShell, or a terminal in the directory containing app.py.
Example:
cd "C:\Users\Data Science\Resume screening Tool"
Replace the example path with your actual project directory.
Step 5: Run the Application
Execute:
streamlit run app.py
If the streamlit command is not recognized, try:
python -m streamlit run app.py
Streamlit will display a local URL, usually:
http://localhost:8501
Open the URL in your browser to access the Resume Screening Tool.
Step 6: Use the Application
1.	Enter or upload a Job Description.
2.	Upload one or more candidate resumes.
3.	Run the screening process.
4.	Review candidate scores, eligibility, and rankings.
5.	Examine matched skills, missing skills, and candidate explanations.
6.	Explore the screening visualizations.
Troubleshooting
•	Streamlit is not recognized: Activate your virtual environment and run python -m streamlit run app.py.
•	Module not found: Install the missing package using pip install package_name.
•	Application file not found: Confirm that your terminal is in the directory containing app.py.
•	Upload errors: Verify that the uploaded file format is supported by the application.
Important: Run Streamlit commands in Command Prompt, PowerShell, or a terminal, not directly in a regular Python or Jupyter Notebook cell.
22. Advantages
1.	Automated screening: Reduces repetitive manual comparison of resumes.
2.	Explainability: Displays component scores and reasons behind candidate results.
3.	Skill gap identification: Highlights matched and missing required skills.
4.	Candidate ranking: Organizes eligible candidates by screening score.
5.	Interactive interface: Provides a user-friendly Streamlit dashboard.
6.	Configurable scoring: Allows different weights and requirements for different roles.
7.	Visual analysis: Summarizes screening results through charts and comparisons.
23. Limitations
•	Resume formatting can vary significantly across candidates.
•	Regular-expression-based experience extraction may miss some date formats or wording.
•	Skill matching depends on predefined vocabularies and related-term mappings.
•	Education matching depends on recognized education fields and configured rules.
•	Relevant skills may be expressed using unfamiliar terminology.
•	Keyword-based relevance may miss contextual or semantic similarities.
•	The dataset may not represent every industry or resume format.
•	Classification accuracy does not directly measure screening quality.
•	Scores may be affected by missing information or inaccurate text extraction.
The screening score should be treated as decision support, not as a definitive measure of a candidate's ability.
24. Future Improvements
Potential enhancements include:
•	Transformer-based NLP models.
•	Semantic similarity using sentence embeddings.
•	Improved skill extraction using Named Entity Recognition.
•	More robust experience extraction using date-range analysis.
•	Automatic extraction of Job Description requirements.
•	Support for multiple Job Descriptions.
•	Candidate comparison and filtering.
•	Screening history and report downloads.
•	Recruiter authentication.
•	Multilingual resume support.
•	More comprehensive evaluation of screening quality.
25. Ethical Considerations
The Resume Screening Tool is designed to support the initial stages of recruitment.
It should not be used as the sole basis for hiring decisions. Recruiters should review original resumes, consider qualifications that automated matching may miss, and evaluate candidates fairly.
The system should be tested regularly for inaccurate results and unintended bias. Sensitive personal attributes should not be used as proxies for candidate suitability.
26. Conclusion
The Resume Screening Tool demonstrates how Python, NLP-based text processing, feature extraction, weighted scoring, and interactive visualization can be combined to support the initial recruitment process.
The application can analyze resumes against a Job Description, evaluate mandatory education and experience requirements, identify matching and missing skills, calculate screening scores, rank eligible candidates, and generate explainable results.
The project also demonstrates practical experience in data preprocessing, text analysis, machine learning experimentation, rule-based scoring, and Streamlit application development.
Author
Shruti
B.Tech in Information Technology
Project: Resume Screening Tool
Technologies: Python, Pandas, NumPy, NLP, Scikit-learn, Streamlit, Data Visualization
