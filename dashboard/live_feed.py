"""
Live video feed component for Vehicle Speed Violation Detection System dashboard.
"""

# """
# This file defines the live video feed display for the dashboard. It will periodically update the frame from the video feed.
# """

# import dash
# from dash import dcc, html
# import dash_core_components as dcc
# import base64
# from io import BytesIO
# import cv2

# # Initialize the Dash app object here if needed
# app = dash.get_app()

# # Live Feed layout component
# def layout():
#     return html.Div([
#         html.H3("Live Detection Feed"),
#         dcc.Interval(
#             id="live-update-interval",
#             interval=1000,  # in milliseconds
#             n_intervals=0
#         ),
#         html.Div([
#             html.Img(id="live-video-feed", style={"width": "100%", "height": "auto"})
#         ])
#     ])

# # Update live video feed
# @app.callback(
#     dash.dependencies.Output("live-video-feed", "src"),
#     [dash.dependencies.Input("live-update-interval", "n_intervals")]
# )
# def update_video_feed(n):
#     # Capture video from webcam or video stream
#     # For demonstration purposes, assume you have a capture source from OpenCV
#     cap = cv2.VideoCapture(0)  # For webcam feed, use video file path for a video stream
#     ret, frame = cap.read()
#     cap.release()
    
#     if ret:
#         _, img_encoded = cv2.imencode('.jpg', frame)
#         img_bytes = img_encoded.tobytes()
#         img_b64 = base64.b64encode(img_bytes).decode('utf-8')
#         return "data:image/jpeg;base64," + img_b64
#     return dash.no_update

"""
Live feed layout and callbacks for displaying real-time video feed and detection results.
"""

from dash import dcc, html, Input, Output
from backend.config import CAMERA_SOURCES

def layout(app):
    return html.Div([
        html.H3("Live Feed"),
        dcc.Dropdown(
            id="camera-dropdown",
            options=[{"label": f"Camera {i+1}", "value": i} for i in range(len(CAMERA_SOURCES))],
            value=0,
            clearable=False,
            style={"width": "300px", "marginBottom": "1rem"}
        ),
        html.Img(
            id="live-video-feed",
            src=f"/backend/live-feed/0",
            style={"width": "100%", "height": "auto", "border": "2px solid #007bff", "borderRadius": "8px"}
        )
    ])

def register_callbacks(app):
    @app.callback(
        Output("live-video-feed", "src"),
        [Input("camera-dropdown", "value")]
    )
    def update_feed_src(camera_id):
        return f"/backend/live-feed/{camera_id}"
