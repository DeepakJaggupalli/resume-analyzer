import streamlit as st
import json
from resume_parser import parse_resume
from llm_analyzer import analyze_resume_against_job

st.set_page_config(
    page_title="AI Resume Analyzer & Job Match Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer & Job Match Assistant")
st.markdown("Upload your resume and paste a job description to see how well you match, and get actionable tips to improve your ATS score.")

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
        with st.spinner("Parsing resume..."):
            try:
                resume_text = parse_resume(uploaded_file, uploaded_file.name)
            except Exception as e:
                st.error(f"Error reading file: {e}")
                st.stop()
        
        if not resume_text.strip():
            st.error("The uploaded resume appears to be empty or unreadable.")
            st.stop()

        with st.spinner("Analyzing with AI... This might take a few seconds."):
            try:
                results = analyze_resume_against_job(resume_text, job_description)
                
                st.success("Analysis Complete!")
                
                # Layout for results
                st.header("📊 Analysis Dashboard")
                
                score = results.get("match_score", 0)
                
                # Metrics Row
                mcol1, mcol2 = st.columns([1, 3])
                with mcol1:
                    st.metric(label="Match Score", value=f"{score}%")
                with mcol2:
                    st.progress(score / 100.0, text="Match Percentage")
                    
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
                    with st.expander("❌ Missing Skills (Gap Analysis)", expanded=True):
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
                        strengths = results.get("strengths", [])
                        for s in strengths:
                            st.markdown(f"- {s}")
                with stcol2:
                    with st.expander("⚠️ Weaknesses"):
                        weaknesses = results.get("weaknesses", [])
                        for w in weaknesses:
                            st.markdown(f"- {w}")
                
                # ATS & Resume Improvements
                st.markdown("---")
                st.subheader("✨ Improvement Suggestions")
                
                with st.expander("ATS Optimization Suggestions", expanded=True):
                    ats = results.get("ats_suggestions", [])
                    for a in ats:
                        st.markdown(f"- {a}")
                        
                with st.expander("Improved Resume Bullet Points", expanded=True):
                    bullets = results.get("improved_bullet_points", [])
                    for b in bullets:
                        st.markdown(f"- {b}")
                
                # Final Feedback
                st.markdown("---")
                st.subheader("🎯 Hiring Readiness")
                st.warning(results.get("readiness_feedback", "No feedback provided."))
                
                # Download JSON Option
                st.download_button(
                    label="Download Raw JSON Analysis",
                    data=json.dumps(results, indent=2),
                    file_name="resume_analysis.json",
                    mime="application/json"
                )

            except Exception as e:
                st.error(f"An error occurred during AI analysis: {e}")
