import plotly.graph_objects as go
import plotly.express as px

def create_gauge_chart(score):
    """Creates a beautiful interactive speedometer gauge for the Match Score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Match Score", 'font': {'size': 24, 'color': 'white'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "rgba(0,0,0,0)"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.2)",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.6)'},  # Red
                {'range': [40, 75], 'color': 'rgba(245, 158, 11, 0.6)'}, # Yellow
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.6)'} # Green
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Outfit"},
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def create_radar_chart(extracted_skills, missing_skills):
    """Creates a Radar Chart comparing present vs missing skills."""
    # We combine them to form the axis. 
    # To make it look good, we cap it at 10 skills total (top 5 from each).
    present = extracted_skills[:5]
    missing = missing_skills[:5]
    
    categories = present + missing
    if not categories:
        return None
        
    # Present skills get a score of 5, missing get a score of 1.
    values = [5] * len(present) + [1] * len(missing)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(139, 92, 246, 0.5)',
        line=dict(color='#8b5cf6'),
        name='Skill Proficiency'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(color='rgba(255,255,255,0.5)')
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=12)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit", color="white"),
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    return fig
