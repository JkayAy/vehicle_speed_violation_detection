"""
Violations table component for Vehicle Speed Violation Detection System dashboard.

This file defines a table that displays the detected vehicle violations, including license plate, speed, timestamp, and vehicle type.

"""

import dash
from dash import dcc, html
import dash_table
from backend.database import get_violation_records

# Initialize the Dash app object here if needed
app = dash.get_app()

# Violations Table Layout Component
def layout():
    return html.Div([
        html.H3("Detected Violations"),
        dash_table.DataTable(
            id='violations-table',
            columns=[
                {"name": "License Plate", "id": "license_plate"},
                {"name": "Speed (km/h)", "id": "speed"},
                {"name": "Vehicle Type", "id": "vehicle_type"},
                {"name": "Timestamp", "id": "timestamp"},
            ],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={'fontWeight': 'bold'},
        )
    ])

# Update Violations Table
@app.callback(
    dash.dependencies.Output("violations-table", "data"),
    [dash.dependencies.Input("live-update-interval", "n_intervals")]
)
def update_violations_table(n):
    # Fetch violation records from the database
    violations = get_violation_records()
    
    if not violations:
        return []
    
    # Return violation records in the format expected by the DataTable component
    return [{
        "license_plate": record['license_plate'],
        "speed": record['speed'],
        "vehicle_type": record['vehicle_type'],
        "timestamp": record['timestamp']
    } for record in violations]
