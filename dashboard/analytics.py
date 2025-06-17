"""
Analytics components for Vehicle Speed Violation Detection System dashboard.
"""

# """
# This file displays the analytics for violations, including speed distributions, violation counts, and trends over time.
# """

# import dash
# from dash import dcc, html
# import plotly.express as px
# import pandas as pd
# from backend.database import get_violation_records

# # Initialize the Dash app
# app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"])

# # Analytics layout component
# app.layout = html.Div([
#     html.H3("Violation Analytics"),
#     dcc.Interval(id="live-update-interval", interval=5000, n_intervals=0),  # Updates every 5 seconds
#     dcc.Graph(id="speed-distribution"),
#     dcc.Graph(id="violation-trends")
# ])

# # Update Analytics Graphs
# @app.callback(
#     [dash.dependencies.Output("speed-distribution", "figure"),
#      dash.dependencies.Output("violation-trends", "figure")],
#     [dash.dependencies.Input("live-update-interval", "n_intervals")]
# )
# def update_analytics(n):
#     # Fetch violation records from the database
#     violations = get_violation_records()
    
#     if not violations:
#         return {}, {}
    
#     # Convert violations data into a Pandas DataFrame
#     df = pd.DataFrame(violations)
    
#     # Speed Distribution Plot
#     speed_fig = px.histogram(df, x="speed", title="Speed Distribution")
    
#     # Violation Trends Plot
#     df['timestamp'] = pd.to_datetime(df['timestamp'])
#     trends_data = df.groupby(df['timestamp'].dt.date).size().reset_index(name='violations')
#     trends_data.rename(columns={"timestamp": "date"}, inplace=True)
#     violation_trends_fig = px.line(trends_data, x="date", y="violations", title="Violation Trends")
    
#     return speed_fig, violation_trends_fig

# if __name__ == "__main__":
#     app.run_server(debug=True)


import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import requests

def layout(app):
    return html.Div([
        html.H3("Advanced Analytics"),
        dcc.Graph(id="violations-by-camera"),
        dcc.Graph(id="violations-by-time"),
        dcc.Graph(id="top-violators"),
        dcc.Interval(id="analytics-interval", interval=60000, n_intervals=0)
    ])

def register_callbacks(app):
    @app.callback(
        Output("violations-by-camera", "figure"),
        [Input("analytics-interval", "n_intervals")]
    )
    def update_violations_by_camera(n):
        data = requests.get("/backend/analytics/violations-by-camera/").json()
        fig = px.bar(x=list(data.keys()), y=list(data.values()), labels={"x": "Camera", "y": "Violations"}, title="Violations by Camera")
        return fig

    @app.callback(
        Output("violations-by-time", "figure"),
        [Input("analytics-interval", "n_intervals")]
    )
    def update_violations_by_time(n):
        data = requests.get("/backend/analytics/violations-by-time/").json()
        fig = px.bar(x=list(data.keys()), y=list(data.values()), labels={"x": "Hour", "y": "Violations"}, title="Violations by Hour")
        return fig

    @app.callback(
        Output("top-violators", "figure"),
        [Input("analytics-interval", "n_intervals")]
    )
    def update_top_violators(n):
        data = requests.get("/backend/analytics/top-violators/").json()
        fig = px.bar(x=[x[0] for x in data], y=[x[1] for x in data], labels={"x": "License Plate", "y": "Violations"}, title="Top Violators")
        return fig
