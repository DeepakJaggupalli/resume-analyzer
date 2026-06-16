import plotly.graph_objects as go
import plotly.express as px

def create_gauge_chart(score):
    """Creates a clean, professional speedometer gauge for the Match Score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Match Score", 'font': {'size': 20, 'color': '#111827'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#d1d5db"},
            'bar': {'color': "rgba(0,0,0,0)"},
            'bgcolor': "#f3f4f6",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': '#fca5a5'},  # Light Red
                {'range': [40, 75], 'color': '#fcd34d'}, # Light Yellow
                {'range': [75, 100], 'color': '#6ee7b7'} # Light Green
            ],
            'threshold': {
                'line': {'color': "#1f2937", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#111827", 'family': "Inter"},
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def create_radar_chart(extracted_skills, missing_skills):
    """Creates a clean Radar Chart comparing present vs missing skills."""
    present = extracted_skills[:5]
    missing = missing_skills[:5]
    
    categories = present + missing
    if not categories:
        return None
        
    values = [5] * len(present) + [1] * len(missing)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(37, 99, 235, 0.2)', # Trust Blue transparent
        line=dict(color='#2563eb'),
        name='Skill Proficiency'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(color='#9ca3af')
            ),
            angularaxis=dict(
                tickfont=dict(color='#374151', size=11)
            ),
            bgcolor='#ffffff'
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#111827"),
        margin=dict(l=40, r=40, t=30, b=30),
        showlegend=False
    )
    return fig
