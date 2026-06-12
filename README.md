# Redrob_Indiaruns_AI_candidate_Ranker
An Smart System That Ranks candidates based on requirements and demand skills , Utilizing Python backend wrapper built using Streamlit and Groq Cloud SDK , using fast llama-3.3-70b-versatile model to filter the candidture using AI models to rank candidates.
Mock Job Description for testing : 
To test ranking engine paste the below job decription into the bar--
text
Job Title: Backend Python Engineer
Core Requirements:
- 2+ years of experience with Python and backend frameworks like Django or Flask.
- Strong knowledge of building and managing RESTful APIs.
- Experience with relational databases and writing clean SQL queries.
- Basic understanding of frontend concepts is a plus, but the primary focus is data pipelines and backend architecture.
```

### Expected Benchmark Output
When using the provided `candidates.csv` with this JD, the Groq Engine will generate a ranked leaderboard matching these true capabilities:
1. **Rahul Sharma** (Highest match - exact stack fit with Django/Flask).
2. **Amit Verma** (Medium match - strong Python/Pandas data background, missing web frameworks).
3. **Priya Patel** (Lowest match - pure frontend UI focus, explicitly lacks backend experience).
