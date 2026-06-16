import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_tfidf_similarity(resume_text: str, job_description: str) -> float:
    try:
        if not resume_text.strip() or not job_description.strip():
            return 0.0
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = similarity_matrix[0][0] * 100
        return round(score, 2)
    except Exception as e:
        print(f"Error calculating TF-IDF: {e}")
        return 0.0

def generate_competition_plot(match_score: float):
    """
    Generates a clean Plotly interactive bell curve for the Corporate theme.
    """
    np.random.seed(42)
    simulated_scores = np.random.normal(loc=60, scale=15, size=1000)
    simulated_scores = np.clip(simulated_scores, 0, 100)
    
    df = pd.DataFrame(simulated_scores, columns=['Score'])
    
    fig = px.histogram(df, x="Score", nbins=30, histnorm='probability density', 
                       opacity=0.3, color_discrete_sequence=['#2563eb']) # Trust blue
    
    x = np.linspace(0, 100, 100)
    p = (1 / (15 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 60) / 15) ** 2)
    fig.add_trace(go.Scatter(x=x, y=p, mode='lines', line=dict(color='#1e40af', width=2), name='Normal Dist'))
    
    fig.add_vline(x=match_score, line_width=2, line_dash="dash", line_color="#dc2626", 
                  annotation_text=f"Your Score: {match_score}", annotation_position="top right",
                  annotation_font_color="#b91c1c")
    
    fig.update_layout(
        title="Applicant Score Distribution",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#111827", family="Inter"),
        xaxis_title="Match Score",
        yaxis_title="Density",
        showlegend=False
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb', zerolinecolor='#d1d5db')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb', zerolinecolor='#d1d5db')
    
    return fig
