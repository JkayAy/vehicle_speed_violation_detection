import streamlit as st

# Set page config - must be the first Streamlit command
st.set_page_config(
    page_title="Vehicle Speed Violation Detection Dashboard",
    page_icon="🚗",
    layout="wide"
)

import logging
import sys
import os
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
Main Streamlit application for Vehicle Speed Violation Detection Dashboard.
"""

from backend.routes import get_violation_records
from backend.database import setup_database
from backend.config import SQLITE_DB_PATH

# Initialize database
setup_database(SQLITE_DB_PATH)

# Header
st.title("Vehicle Speed Violation Detection Dashboard")

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Feed")
    # Placeholder for live feed
    st.image("https://via.placeholder.com/800x400?text=Live+Feed", use_column_width=True)

with col2:
    st.subheader("Analytics")
    
    # Get violation records
    try:
        records = get_violation_records()
        if records:
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(records)
            
            # Violations by Camera
            st.write("### Violations by Camera")
            camera_counts = df['camera_id'].value_counts()
            fig_camera = px.bar(
                x=camera_counts.index,
                y=camera_counts.values,
                title="Violations by Camera"
            )
            st.plotly_chart(fig_camera, use_container_width=True)
            
            # Violations by Time
            st.write("### Violations by Time")
            df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
            time_counts = df['hour'].value_counts().sort_index()
            fig_time = px.line(
                x=time_counts.index,
                y=time_counts.values,
                title="Violations by Hour"
            )
            st.plotly_chart(fig_time, use_container_width=True)
            
            # Top Violators
            st.write("### Top Violators")
            top_violators = df['license_plate'].value_counts().head(10)
            fig_violators = px.bar(
                x=top_violators.index,
                y=top_violators.values,
                title="Top 10 Violators"
            )
            st.plotly_chart(fig_violators, use_container_width=True)
        else:
            st.info("No violation records available.")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

# Add a sidebar for controls
with st.sidebar:
    st.header("Controls")
    st.write("### Camera Selection")
    camera_id = st.selectbox(
        "Select Camera",
        options=["All Cameras"] + [str(i) for i in range(1, 6)],
        index=0
    )
    
    st.write("### Date Range")
    start_date = st.date_input("Start Date", datetime.now())
    end_date = st.date_input("End Date", datetime.now())
    
    if st.button("Refresh Data"):
        st.experimental_rerun()
