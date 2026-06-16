import streamlit as st
import json
import time
from resume_parser import parse_resume
from llm_analyzer import analyze_resume_against_job
from ml_features import calculate_tfidf_similarity, generate_competition_plot

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and paste a job description to analyze your match and get feedback.")

# Classic side-by-side columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste the job description here", height=200)

if st.button("🔍 Analyze Resume", type="primary"):
    if not uploaded_file:
        st.error("Please upload a resume to proceed.")
    elif not job_description.strip():
        st.error("Please paste a job description to proceed.")
    else:
        # TRANSPARENT BACKEND LOGS
        st.markdown("### ⚙️ Backend Process Logs (Developer Mode)")
        
        try:
            resume_text = parse_resume(uploaded_file, uploaded_file.name)
            st.success("📄 Step 1: Document Text Successfully Extracted!")
            st.markdown("**Raw Extracted Text (Preview):**")
            # Show a snippet of the extracted text
            preview_text = resume_text[:800] + "\n\n... [TEXT TRUNCATED FOR DISPLAY]" if len(resume_text) > 800 else resume_text
            st.code(preview_text, language="text")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()
            
        if not resume_text.strip():
            st.error("The uploaded resume appears to be empty or unreadable.")
            st.stop()

        tfidf_score = calculate_tfidf_similarity(resume_text, job_description)
        st.success("🧮 Step 2: TF-IDF Machine Learning Keyword Similarity Calculated!")
        st.markdown("**Raw Math Output:**")
        st.code(f"Cosine Similarity Matrix Score: {tfidf_score}", language="python")

        st.info("🤖 Step 3: Querying Gemini AI... (Waiting for server response)")
        try:
            backend_data = analyze_resume_against_job(resume_text, job_description)
            
            # The backend_data contains parsed_json, raw_prompt, and raw_response
            results = backend_data["parsed_json"]
            raw_prompt = backend_data["raw_prompt"]
            raw_response = backend_data["raw_response"]
            
            st.success("🤖 API Connection Successful! Data Retrieved.")
            
            with st.expander("🔍 View Raw Prompt Sent to Google Gemini API"):
                st.code(raw_prompt, language="markdown")
                
            with st.expander("📦 View Raw JSON Response from Google Gemini API"):
                st.code(raw_response, language="json")
                
        except Exception as e:
            st.error(f"An error occurred during AI analysis: {e}")
            st.stop()
            
        st.success("📊 Step 4: Formatting JSON into UI Dashboard!")
            
        st.markdown("---")
        # -------------------------------------------------------------
        # Dashboard Rendering
        # -------------------------------------------------------------
        st.header("📊 Analysis Dashboard")
        
        score = results.get("match_score", 0)
        comp_fig = generate_competition_plot(score)
        
        # Metrics Row
        mcol1, mcol2, mcol3 = st.columns([1, 1, 2])
        with mcol1:
            st.metric(label="Gemini Semantic Score", value=f"{score}%")
        with mcol2:
            st.metric(label="TF-IDF Keyword Score", value=f"{tfidf_score}%")
        with mcol3:
            st.progress(score / 100.0, text="Overall Match Percentage")
            
        st.markdown("---")
        
        st.subheader("📈 Competition Analysis")
        st.pyplot(comp_fig)
        
        st.markdown("---")
        
        # Summary
        st.subheader("📝 Executive Summary")
        st.info(results.get("resume_summary", "No summary provided."))
        
        # Skills Analysis
        scol1, scol2 = st.columns(2)
        with scol1:
            with st.expander("✅ Extracted Skills", expanded=True):
                skills = results.get("extracted_skills", [])
                if skills:
                    for skill in skills:
                        st.markdown(f"- {skill}")
                else:
                    st.write("None found.")
        
        with scol2:
            with st.expander("❌ Missing Skills", expanded=True):
                missing = results.get("missing_skills", [])
                if missing:
                    for ms in missing:
                        st.markdown(f"- {ms}")
                else:
                    st.write("No major gaps found!")

        # Strengths & Weaknesses
        stcol1, stcol2 = st.columns(2)
        with stcol1:
            with st.expander("💪 Strengths"):
                for s in results.get("strengths", []):
                    st.markdown(f"- {s}")
        with stcol2:
            with st.expander("⚠️ Weaknesses"):
                for w in results.get("weaknesses", []):
                    st.markdown(f"- {w}")
        
        # ATS & Resume Improvements
        st.markdown("---")
        st.subheader("✨ Improvement Suggestions")
        
        with st.expander("ATS Optimization Suggestions", expanded=True):
            for a in results.get("ats_suggestions", []):
                st.markdown(f"- {a}")
                
        with st.expander("Improved Resume Bullet Points", expanded=True):
            for b in results.get("improved_bullet_points", []):
                st.markdown(f"- {b}")
        
        # Final Feedback
        st.markdown("---")
        st.subheader("🎯 Hiring Readiness")
        st.warning(results.get("readiness_feedback", "No feedback provided."))
        
        # Download JSON
        st.download_button(
            label="Download Raw JSON Analysis",
            data=json.dumps(results, indent=2),
            file_name="resume_analysis.json",
            mime="application/json"
        )
