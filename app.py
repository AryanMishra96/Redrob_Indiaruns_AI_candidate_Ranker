import streamlit as st
import pandas as pd
import json
from groq import Groq

# -------------------------------------------------------------
# WEB PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(page_title="Groq AI Recruiter Ranker", page_icon="⚡", layout="wide")
st.title("⚡ Ultra-Fast AI Candidate Ranking Engine")
st.caption("Powered by Groq Cloud - Track 01: Data & AI Challenge")

# -------------------------------------------------------------
# API INITIALIZATION (SIDEBAR)
# -------------------------------------------------------------
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Groq API Key (gsk_...):", type="password")
    st.markdown("[Get a free key from ](https://groq.com)")
    
    # Selecting an incredibly fast and free model hosted on Groq
    model_choice = st.selectbox(
        "Select LLM Model:",
        ["llama-3.3-70b-versatile", "llama3-8b-8192"]
    )

# -------------------------------------------------------------
# WEB APP INTERFACE
# -------------------------------------------------------------
job_description = st.text_area(
    "1. Define the Job Description (JD):", 
    placeholder="Paste the target job role details, core required skills, and expectations here...",
    height=150
)

uploaded_file = st.file_uploader("2. Upload Candidate Dataset (CSV format):", type=["csv"])

# -------------------------------------------------------------
# PROCESSING CORE LOGIC
# -------------------------------------------------------------
if uploaded_file and job_description:
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar to begin processing.")
    else:
        # Load the file into Pandas
        df = pd.read_csv(uploaded_file)
        
        st.subheader("Dataset Preview")
        st.dataframe(df.head(3))
        
        # Verify required columns exist
        if "Resume_Text" not in df.columns or "Candidate_Name" not in df.columns:
            st.error("Your CSV must contain 'Candidate_Name' and 'Resume_Text' columns.")
        else:
            # Initialize session state so data persists when clicking "Download"
            if "ranked_df" not in st.session_state:
                st.session_state.ranked_df = None

            if st.button("Run Groq AI Ranking Engine", type="primary"):
                
                # Initialize the official Groq client
                client = Groq(api_key=api_key)
                
                system_instruction = (
                    "You are an elite corporate technical recruiter. Evaluate candidates objectively. "
                    "Analyze candidate skills contextually (e.g., if a candidate knows Django, they inherently know Python). "
                    "You must output valid raw JSON matching this exact structure: {\"score\": 85, \"reason\": \"Explanation\"}. "
                    "Do not include markdown tags like ```json or any conversational filler. Only return the JSON object."
                )
                
                scores = []
                reasons = []
                
                # Visual UI elements for tracking progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                total_candidates = len(df)
                
                # Loop through every candidate in the dataset
                for index, row in df.iterrows():
                    status_text.text(f"Evaluating candidate {index + 1} of {total_candidates}: {row['Candidate_Name']}")
                    
                    user_prompt = f"""
                    Job Description:
                    {job_description}
                    
                    Candidate Profile:
                    Name: {row['Candidate_Name']}
                    Background Details: {row['Resume_Text']}
                    
                    Rate this candidate match score from 0 to 100 based on true capabilities. 
                    Do not penalize them for missing specific keywords if they have equivalent experience.
                    """
                    
                    try:
                        # Call Groq API for sub-second text completions
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": system_instruction},
                                {"role": "user", "content": user_prompt}
                            ],
                            model=model_choice,
                            temperature=0.1,  # Focused and strict analytical output
                            response_format={"type": "json_object"}  # Forces Groq to guarantee a JSON output
                        )
                        
                        # Extract and parse the response string
                        raw_response = chat_completion.choices[0].message.content
                        result_data = json.loads(raw_response)
                        
                        scores.append(int(result_data.get("score", 0)))
                        reasons.append(result_data.get("reason", "Processed successfully."))
                        
                    except Exception as e:
                        scores.append(0)
                        reasons.append(f"Processing error: {str(e)}")
                    
                    # Update progress bar
                    progress_bar.progress((index + 1) / total_candidates)
                
                # Append results to DataFrame
                df['Match_Score'] = scores
                df['Recruiter_Reasoning'] = reasons
                
                # Store the sorted results safely in session memory
                st.session_state.ranked_df = df.sort_values(by="Match_Score", ascending=False).reset_index(drop=True)
                
                # Clean up UI elements
                status_text.empty()
                progress_bar.empty()
            
            # Display and download logic outside the button block so it persists during page rerenders
            if st.session_state.ranked_df is not None:
                st.success("Here is your human-like sorted shortlist:")
                st.dataframe(st.session_state.ranked_df[['Candidate_Name', 'Match_Score', 'Recruiter_Reasoning']])
                
                # Enable final submission dataset download
                csv_download = st.session_state.ranked_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Ranked CSV for Hackathon Submission",
                    data=csv_download,
                    file_name="groq_ranked_candidates.csv",
                    mime="text/csv",
                )

elif not uploaded_file or not job_description:
    st.info("to run, put a Job Description and paste your Candidate Dataset CSV file.")
