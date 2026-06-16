import streamlit as st
import json
from resume_parser import parse_resume
from llm_analyzer import analyze_resume_against_job
from ml_features import calculate_tfidf_similarity, generate_competition_plot
from visualizations import create_gauge_chart, create_radar_chart

st.set_page_config(
    page_title="Enterprise Resume Analytics",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS for Professional Corporate Theme
with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.title("Resume Analytics")
    st.markdown("Upload documents to perform semantic and TF-IDF analysis.")
    st.markdown("---")
    
    st.markdown("### 1. Applicant Document")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"], label_visibility="collapsed")
    
    st.markdown("### 2. Job Description")
    job_description = st.text_area("Paste the job description", height=300, label_visibility="collapsed")
    
    analyze_button = st.button("Run Full Analysis", type="primary", use_container_width=True)

# ----------------- MAIN SCREEN -----------------
if not analyze_button:
    # Professional Landing State
    st.markdown("<h1 style='text-align: center; margin-top: 10vh;'>Enterprise Resume Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280;'>Please upload an applicant document in the sidebar to begin processing.</p>", unsafe_allow_html=True)

else:
    if not uploaded_file:
        st.error("Please upload an applicant document in the sidebar.")
    elif not job_description.strip():
        st.error("Please paste a job description in the sidebar.")
    else:
        with st.spinner("Processing document..."):
            try:
                resume_text = parse_resume(uploaded_file, uploaded_file.name)
            except Exception as e:
                st.error(f"Error reading file: {e}")
                st.stop()
        
        if not resume_text.strip():
            st.error("The uploaded document contains no readable text.")
            st.stop()

        with st.spinner("Running Semantic NLP Analysis..."):
            try:
                results = analyze_resume_against_job(resume_text, job_description)
                tfidf_score = calculate_tfidf_similarity(resume_text, job_description)
                
                score = results.get("match_score", 0)
                
                # ------ DASHBOARD TOP ROW ------
                st.header("Analytics Dashboard")
                
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    st.metric(label="Semantic Match (AI)", value=f"{score}%", delta="High Match" if score > 75 else "Review Needed")
                with col2:
                    st.metric(label="Keyword Similarity (TF-IDF)", value=f"{tfidf_score}%", help="Cosine similarity of extracted keywords.")
                with col3:
                    st.plotly_chart(create_gauge_chart(score), use_container_width=True, config={'displayModeBar': False})
                    
                st.markdown("---")
                
                # ------ SECOND ROW: CHARTS & SKILLS ------
                row2_col1, row2_col2 = st.columns([1, 1])
                
                extracted = results.get("extracted_skills", [])
                missing = results.get("missing_skills", [])
                
                with row2_col1:
                    st.subheader("Skill Coverage Matrix")
                    radar_fig = create_radar_chart(extracted, missing)
                    if radar_fig:
                        st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.write("Insufficient data for matrix.")
                        
                with row2_col2:
                    st.subheader("Applicant Percentile")
                    comp_fig = generate_competition_plot(score)
                    st.plotly_chart(comp_fig, use_container_width=True, config={'displayModeBar': False})
                
                st.markdown("---")
                
                # ------ THIRD ROW: INSIGHTS ------
                st.subheader("Executive Summary")
                st.info(results.get("resume_summary", "No summary provided."))
                
                in_col1, in_col2 = st.columns(2)
                with in_col1:
                    with st.expander("Extracted Capabilities", expanded=True):
                        for s in extracted: st.markdown(f"- {s}")
                    with st.expander("Key Strengths"):
                        for s in results.get("strengths", []): st.markdown(f"- {s}")
                        
                with in_col2:
                    with st.expander("Identified Gaps", expanded=True):
                        for m in missing: st.markdown(f"- {m}")
                    with st.expander("Areas for Improvement"):
                        for w in results.get("weaknesses", []): st.markdown(f"- {w}")

                st.markdown("---")
                st.subheader("Optimization Directives")
                
                opt_col1, opt_col2 = st.columns(2)
                with opt_col1:
                    with st.expander("ATS Compliance Suggestions", expanded=True):
                        for a in results.get("ats_suggestions", []): st.markdown(f"- {a}")
                with opt_col2:
                    with st.expander("Actionable Revisions", expanded=True):
                        for b in results.get("improved_bullet_points", []): st.markdown(f"- {b}")
                
                st.markdown("---")
                st.subheader("Final Readiness Assessment")
                st.warning(results.get("readiness_feedback", "No feedback provided."))
                
                # Download JSON Option
                st.download_button(
                    label="Download Raw JSON Report",
                    data=json.dumps(results, indent=2),
                    file_name="analytics_report.json",
                    mime="application/json",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Analysis Failed: {e}")
