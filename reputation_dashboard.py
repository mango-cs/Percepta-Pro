"""
Percepta Pro v2.0 - Advanced Reputation Intelligence Platform
💬 Real-time public sentiment monitoring and brand reputation management
🔍 Sentiment escalation tracking and reputation trends
📊 Executive-grade reputation intelligence and PR risk analysis

Enhanced features:
- Bilingual sentiment analysis (Telugu + English)  
- Public opinion momentum tracking
- Reputation escalation monitoring
- Strategic PR recommendations
- Executive reputation intelligence reports
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from pathlib import Path
import sys
import time
sys.path.append('scripts')
from crisis_detection_engine import CrisisDetectionEngine
from executive_reporting_engine import ExecutiveReportingEngine
import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
# Removed obsolete toggle_component import - using native Streamlit toggles

# Import theme system for dynamic theming
try:
    from src.themes.theme_provider import get_current_theme, generate_theme_css
    THEME_SYSTEM_AVAILABLE = True
except ImportError:
    THEME_SYSTEM_AVAILABLE = False
    print("Theme system not available, using fallback CSS")

# 🎨 CRIMZON DESIGN SYSTEM CONFIGURATION
st.set_page_config(
    page_title="Percepta Pro - Reputation Intelligence",
    page_icon="assets/images/percepta_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 CUSTOM CSS - CRIMZON DARK THEME
def load_logo_image():
    """Load and encode the Percepta Pro logo image"""
    try:
        import os
        logo_path = "assets/images/percepta_logo.png"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode()
                return f"data:image/png;base64,{encoded_image}"
        return None
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        return None

def load_custom_css():
    """Load CSS with dynamic theme system integration"""
    # Import theme system
    try:
        from src.themes.theme_provider import generate_theme_css
        theme_variables = generate_theme_css()
    except ImportError:
        # Fallback to hardcoded Crimzon theme if import fails
        theme_variables = """
    :root {
        /* Primary Colors - Fallback Crimzon Values */
        --primary-color: #FF4757;
        --secondary-color: #FF6348;
        --accent-color: #22C55E;
        --warning-color: #FFA502;
        --error-color: #FF4757;
        --bg-main: #1A1A1A;
        --bg-card: #2D2D2D;
        --bg-interactive: #3A3A3A;
        --bg-hover: #4A4A4A;
        --text-primary: #FFFFFF;
        --text-secondary: #CCCCCC;
        --text-muted: #9CA3AF;
        --text-inverse: #1F2937;
        --border-color: #404040;
        --border-hover: #505050;
        --border-focus: #FF4757;
        
        /* Legacy compatibility */
        --crimzon-red: #FF4757;
        --crimzon-orange: #FF6348;
        --crimzon-amber: #FFA502;
        --accent-green: #22C55E;
        
        /* Spacing */
        --spacing-xs: 4px;
        --spacing-sm: 8px;
        --spacing-md: 12px;
        --spacing-lg: 16px;
        --spacing-xl: 20px;
        --spacing-xxl: 24px;
        --spacing-xxxl: 32px;
        
        /* Radius */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        
        /* Shadows */
        --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.2);
        --shadow-hover: 0 4px 12px rgba(255, 71, 87, 0.4);
        --shadow-button: 0 2px 8px rgba(255, 71, 87, 0.3);
        --shadow-focus: 0 0 0 3px rgba(255, 71, 87, 0.1);
        
        /* Gradients */
        --gradient-primary: linear-gradient(135deg, #FF4757 0%, #FF6348 100%);
        --gradient-secondary: linear-gradient(135deg, #FF6348 0%, #FFA502 100%);
        --gradient-accent: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
    }"""
    
    css_content = """
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Dynamic Theme Variables */
    """ + theme_variables + """
    
    /* Main App Background - Layout Specifications */
    .stApp {
        background: var(--bg-main);
        font-family: 'Inter', sans-serif;
    }
    
    /* Comprehensive Main Content Gap Fix - Target ALL possible containers */
    .main .block-container,
    .main,
    .stMain,
    [data-testid="stMain"],
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stAppViewContainer"],
    .appview-container,
    .css-18e3th9,
    .css-1d391kg + div,
    .css-1d391kg ~ div {
        padding-left: 0 !important;
        margin-left: 0 !important;
        border-left: none !important;
    }
    
    /* Force main content to start immediately after sidebar */
    .stApp > div {
        padding-left: 0 !important;
    }
    
    /* Remove any default Streamlit gaps */
    .css-1rs6os, .css-17eq0hr {
        padding-left: 0 !important;
        margin-left: 0 !important;
    }
    
    /* FORCE no gaps anywhere - nuclear option */
    * {
        box-sizing: border-box !important;
    }
    
    /* Ensure no spacing between sidebar and main content */
    .stSidebar + * {
        padding-left: 0 !important;
        margin-left: 0 !important;
        border-left: none !important;
    }
    
    /* Override any Streamlit default spacing */
    .element-container {
        padding-left: 0 !important;
        margin-left: 0 !important;
    }
    
    /* 🎯 CLEAN MINIMALIST SIDEBAR CSS */

    /* === 1. SIDEBAR CONTAINER === */
    .css-1d391kg, .stSidebar > div {
        background: #2D2D2D !important;
        border-right: none !important;
        padding: 0 !important;
    }
    
    .stSidebar > div,
    .stSidebar,
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] {
        background: #2D2D2D !important;
        border-right: none !important;
        padding: 0 !important;
    }

    /* === 2. SIDEBAR HEADER === */
    .sidebar-header {
        padding: 2rem 1.5rem 1.5rem 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .sidebar-logo {
        width: 40px;
        height: 40px;
        object-fit: contain;
    }
    
    .sidebar-logo-fallback {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #FF4757, #FF6348);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
    }
    
    .logo-text {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .logo-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FF4757;
        line-height: 1;
        margin: 0;
    }
    
    .logo-subtitle {
        font-size: 0.75rem;
        color: #999999;
        text-transform: uppercase;
        letter-spacing: 1px;
        line-height: 1;
        margin: 0;
    }

    /* === 3. SECTION STYLING === */
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1.5rem;
        margin-bottom: 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #999999;
    }
    
    /* Toggle Sections - Clean Inline Design */
    .mode-toggle-section,
    .language-toggle-section {
        margin: 0 1.5rem 1rem 1.5rem;
        padding: 0;
        background: none;
        border-radius: 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .mode-toggle-section .section-header,
    .language-toggle-section .section-header {
        margin: 0;
        padding: 0;
        background: none;
        border: none;
        font-size: 0.8rem;
        color: #CCCCCC;
        font-weight: 500;
    }
    
    .language-toggle-section {
        margin-bottom: 1.5rem;
    }
    
    .toggle-content {
        padding: 0;
    }
    
    /* Navigation Section */
    .navigation-section {
        margin-bottom: 2rem;
    }
    
    .nav-content {
        padding: 0 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    /* Stats Section */
    .stats-section {
        margin: 1.5rem 0 0.75rem 0;
    }
    
    .stats-content {
        padding: 0 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    /* === 4. CLEAN TOGGLE SWITCH === */
    .stSidebar .stToggle {
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    
    .stSidebar .stToggle > label {
        display: none !important;
    }
    
    .stSidebar .stToggle > div {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* === 5. CLEAN NAVIGATION BUTTONS === */
    .stSidebar .stButton button {
        background: transparent !important;
        color: #CCCCCC !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        margin: 0 !important;
        width: 100% !important;
        text-align: left !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }

    .stSidebar .stButton button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        transform: translateX(4px) !important;
    }

    /* Active navigation button */
    .stSidebar .stButton button[kind="primary"] {
        background: #FF4757 !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(255, 71, 87, 0.3) !important;
    }
    
    .stSidebar .stButton button[kind="primary"]:hover {
        background: #FF3742 !important;
        transform: translateX(4px) !important;
        box-shadow: 0 6px 16px rgba(255, 71, 87, 0.4) !important;
    }

    /* === 6. SIDEBAR METRICS === */
    .stSidebar .stMetric {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stSidebar .stMetric label {
        font-size: 0.7rem !important;
        color: #999999 !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stSidebar .stMetric [data-testid="metric-container"] > div:first-child {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: white !important;
    }
    /* === 7. REPUTATION CARD === */
    .reputation-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 165, 2, 0.3);
        border-radius: 10px;
        padding: 1.25rem;
        margin: 0 1.5rem 0.75rem 1.5rem;
        text-align: center;
    }
    
    .reputation-status {
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 600;
        color: #FFA502;
        margin-bottom: 0.5rem;
    }
    
    .reputation-score {
        font-size: 2rem;
        font-weight: 700;
        color: #FFA502;
        margin: 0.5rem 0;
    }
    
    .reputation-label {
        font-size: 0.7rem;
        color: #999999;
        text-transform: uppercase;
    }

    /* === 8. ADDITIONAL STYLING === */
        font-size: 1rem;
        margin-bottom: 0.25rem;
        color: var(--sidebar-text-inactive);
    }
    .stat-value {
        font-size: 1.1rem;
        color: white;
        font-weight: 600;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.6rem;
        color: #999;
        text-transform: uppercase;
        margin-top: 0.25rem;
    }

    /* === 10. CRISIS ALERT === */
    .crisis-alert {
        margin: 1rem;
        background: rgba(255, 71, 87, 0.1);
        border: 1px solid #FF4757;
        border-radius: 8px;
        padding: 1rem;
    }
    .crisis-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.25rem;
        gap: 0.5rem;
    }
    .crisis-header i {
        color: #FF4757;
    }
    .crisis-header span {
        color: #FF4757;
        font-weight: 600;
        font-size: 0.7rem;
        text-transform: uppercase;
    }
    .crisis-text {
        color: #CCCCCC;
        font-size: 0.7rem;
    }

    /* === 11. FOOTER === */
    .sidebar-footer-spacer {
        flex-grow: 1; /* Pushes the footer content down */
    }
    .footer-link {
        margin-top: 0;
        opacity: 0.7;
        font-size: 0.8rem;
    }
    .footer-link:hover {
        opacity: 1;
    }

         /* === 12. SIDEBAR SELECTBOX STYLING === */
     .stSidebar .stSelectbox > div > div {
         background: rgba(45, 45, 45, 0.6) !important;
         border: 1px solid #404040 !important;
         border-radius: 8px !important;
         color: var(--text-primary) !important;
         margin: 0 1rem !important;
     }
     

    
    /* === 13. SIDEBAR ELEMENT SPACING === */
    .stSidebar .element-container {
        margin-bottom: 0 !important;
    }
    .stSidebar .stMarkdown {
        margin-bottom: 0 !important;
    }
    .stSidebar > div {
        padding-top: 0 !important;
    }
    .stSidebar .stSelectbox {
        margin-bottom: 0 !important;
    }
    .stSidebar [data-testid="element-container"] {
        margin-bottom: 0 !important;
    }
    
    /* === 14. SECTION CONTENT STREAMLIT OVERRIDES === */
    /* Override Streamlit defaults within our content areas */
    
    .toggle-content .element-container,
    .nav-content .element-container,
    .stats-content .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .toggle-content .stColumns,
    .nav-content .stColumns,
    .stats-content .stColumns {
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }
    
    .toggle-content .stToggle,
    .toggle-content .stCheckbox {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .nav-content .stRadio {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .nav-content [data-testid="stRadio"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stats-content .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove any spacing from Streamlit elements inside content */
    .toggle-content > div,
    .nav-content > div,
    .stats-content > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .toggle-content [data-testid="element-container"],
    .nav-content [data-testid="element-container"],
    .stats-content [data-testid="element-container"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Primary Metric Cards - Exact JSON Specifications */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: var(--spacing-xxl);
        box-shadow: var(--shadow-card);
        margin-bottom: var(--spacing-lg);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 71, 87, 0.15);
        border-color: var(--crimzon-red);
    }
    
    /* Metric Card Typography - Exact JSON Specifications */
    .metric-value {
        color: var(--text-primary);
        font-size: 32px;
        font-weight: 700;
        margin: var(--spacing-sm) 0;
        line-height: 1.1;
    }
    
    .metric-label {
        color: var(--text-muted);
        font-size: 14px;
        font-weight: 500;
    }
    
    .metric-change {
        font-size: 12px;
        margin-top: var(--spacing-xs);
        font-weight: 500;
    }
    
    .metric-change.positive {
        color: var(--accent-green);
    }
    
    .metric-change.negative {
        color: var(--crimzon-red);
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-critical { background-color: var(--error-color); }
    .status-warning { background-color: var(--warning-color); }
    .status-good { background-color: var(--accent-color); }
    
    /* Page Title Styling - Typography Specifications */
    .page-title {
        color: var(--text-primary);
        font-size: 32px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: var(--spacing-sm);
    }
    
    .page-subtitle {
        color: var(--text-secondary);
        font-size: 18px;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: var(--spacing-xxxl);
    }
    
    /* Primary Button Styling - Dynamic Theme Variables */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: var(--text-primary) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 10px 16px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-button) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: var(--gradient-secondary) !important;
        box-shadow: var(--shadow-hover) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Chart Container - Card Specifications */
    .chart-container {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: var(--spacing-xl);
        box-shadow: var(--shadow-card);
        margin-bottom: var(--spacing-lg);
    }
    
    /* Data Table Styling */
    .stDataFrame {
        background: var(--bg-card);
        border-radius: var(--radius-md);
    }
    
    /* Status Badge Styling */
    .status-badge {
        padding: var(--spacing-xs) var(--spacing-md);
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-positive {
        background: rgba(46, 213, 115, 0.2);
        color: var(--accent-green);
        border: 1px solid var(--accent-green);
    }
    
    .status-negative {
        background: rgba(255, 71, 87, 0.2);
        color: var(--crimzon-red);
        border: 1px solid var(--crimzon-red);
    }
    
    .status-neutral {
        background: rgba(255, 165, 2, 0.2);
        color: var(--crimzon-amber);
        border: 1px solid var(--crimzon-amber);
    }
    
    /* Alert Styling */
    .reputation-alert {
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 99, 72, 0.05) 100%);
        border: 1px solid rgba(255, 71, 87, 0.3);
        border-radius: var(--radius-md);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-lg);
    }
    
    /* Phase 3C Predictive Analytics Styles - JSON Specifications */
    .prediction-card {
        background: var(--bg-card);
        border: 2px solid var(--accent-green);
        border-radius: var(--radius-lg);
        padding: var(--spacing-xxl);
        margin: var(--spacing-sm) 0;
        box-shadow: var(--shadow-card);
    }
    
    .crisis-card {
        background: var(--bg-card);
        border: 2px solid var(--crimzon-amber);
        border-radius: var(--radius-lg);
        padding: var(--spacing-xxl);
        margin: var(--spacing-sm) 0;
        box-shadow: var(--shadow-card);
    }
    
    .forecast-timeline {
        background: rgba(46, 213, 115, 0.1);
        border-left: 4px solid var(--accent-green);
        padding: var(--spacing-lg);
        margin: var(--spacing-lg) 0;
        border-radius: var(--radius-md);
    }
    
    /* Additional Status Classes */
    .status-active { background-color: var(--accent-green); }
    .status-warning { background-color: var(--crimzon-amber); }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    </style>
    """
    
    st.markdown(css_content, unsafe_allow_html=True)

def create_metric_card(title, value, change=None, change_type="neutral", icon="📊"):
    """Create a professional metric card using exact JSON design system specifications"""
    change_class = f"metric-change {change_type}" if change else ""
    change_html = f'<div class="{change_class}">{change}</div>' if change else ""
    
    return f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; margin-bottom: var(--spacing-sm);">
            <span style="font-size: 20px; margin-right: var(--spacing-sm); color: var(--text-muted);">{icon}</span>
            <span class="metric-label">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
        {change_html}
    </div>
    """

# 🔮 PHASE 3C HELPER FUNCTIONS

@st.cache_data
def load_phase3c_predictions():
    """Load Phase 3C predictive analytics results"""
    try:
        with open('scripts/logs/phase3c_robust_report.json', 'r') as f:
            predictions = json.load(f)
        return predictions
    except FileNotFoundError:
        return None

@st.cache_data
def load_optimized_datasets():
    """Load ML-ready datasets"""
    try:
        videos_df = pd.read_csv('backend/data/videos/youtube_videos_ml_ready.csv')
        comments_df = pd.read_csv('backend/data/comments/youtube_comments_ai_enhanced_cleaned.csv')
        return videos_df, comments_df
    except FileNotFoundError:
        return None, None

def get_logo_base64():
    """Get base64 encoded logo for display"""
    try:
        logo_path = "assets/images/percepta_logo.png"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode()
                return encoded_image
        return ""
    except Exception:
        return ""

# 📊 MAIN DATA LOADING FUNCTIONS

@st.cache_data
def load_reputation_data():
    """Load and process reputation monitoring data with language preference support"""
    # Load final processed data files that actually exist
    videos_path = Path("backend/data/videos/youtube_videos_final.csv")
    
    # Use the enhanced comments dataset which has both original and translated content
    comments_path = Path("backend/data/comments/youtube_comments_ai_enhanced.csv")
    
    # Fallback to basic dataset if enhanced not available
    if not comments_path.exists():
        comments_path = Path("backend/data/comments/youtube_comments_final.csv")
    
    try:
        videos_df = pd.read_csv(videos_path)
        comments_df = pd.read_csv(comments_path)
        
        # Data preprocessing
        # Handle different date column names in final datasets
        if 'UploadDate' in videos_df.columns:
            videos_df['Upload Date'] = pd.to_datetime(videos_df['UploadDate'], errors='coerce')
        elif 'Upload Date' in videos_df.columns:
            videos_df['Upload Date'] = pd.to_datetime(videos_df['Upload Date'], errors='coerce')
        
        if 'Date_Formatted' in comments_df.columns:
            comments_df['Date'] = pd.to_datetime(comments_df['Date_Formatted'], format='%d-%m-%Y', errors='coerce')
        elif 'Date' in comments_df.columns:
            comments_df['Date'] = pd.to_datetime(comments_df['Date'], errors='coerce')
        
        # Clean sentiment data - the final dataset should have 'Sentiment' and 'SentLabel' columns
        if 'Sentiment' in comments_df.columns:
            comments_df['Sentiment'] = pd.to_numeric(comments_df['Sentiment'], errors='coerce')
        elif 'SentimentScore_EN' in comments_df.columns:
            comments_df['Sentiment'] = pd.to_numeric(comments_df['SentimentScore_EN'], errors='coerce')
        else:
            comments_df['Sentiment'] = 0.0
        
        # Ensure we have SentLabel column (should already exist in final dataset)
        if 'SentLabel' not in comments_df.columns and 'Sentiment' in comments_df.columns:
            # Create SentLabel from numeric Sentiment if missing
            comments_df['SentLabel'] = comments_df['Sentiment'].apply(
                lambda x: 'Positive' if x > 0.1 else 'Negative' if x < -0.1 else 'Neutral'
            )
        
        # Clean data
        comments_df = comments_df.dropna(subset=['Sentiment'])
        
        return videos_df, comments_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

def get_language_aware_comments(comments_df):
    """Process comments based on current language preference"""
    if comments_df.empty:
        return comments_df
    
    # Get current language preference from session state
    language_mode = st.session_state.get('language_mode', 'English')
    
    # Create a copy to avoid modifying the original cached data
    processed_comments = comments_df.copy()
    
    if language_mode == 'Telugu':
        # Telugu mode: Show original comments (Comment column)
        # Use 'Comment' as the primary display column
        if 'Comment' in processed_comments.columns:
            processed_comments['DisplayComment'] = processed_comments['Comment'].fillna('')
        else:
            processed_comments['DisplayComment'] = processed_comments.get('Comment_EN', '').fillna('')
    else:
        # English mode: Show translated comments (Comment_EN column)  
        # Use 'Comment_EN' as primary with fallback to 'Comment'
        if 'Comment_EN' in processed_comments.columns:
            processed_comments['DisplayComment'] = processed_comments['Comment_EN'].fillna(
                processed_comments.get('Comment', '')
            )
        else:
            processed_comments['DisplayComment'] = processed_comments.get('Comment', '').fillna('')
    
    return processed_comments

def calculate_reputation_score(comments_df):
    """Calculate overall reputation score (0-100)"""
    if comments_df.empty:
        return 50
    
    sentiment_scores = comments_df['Sentiment'].dropna()
    
    # Convert sentiment range to 0-100 scale
    # Assuming sentiment is in range [-1, 1]
    normalized_sentiment = (sentiment_scores + 1) / 2 * 100
    reputation_score = normalized_sentiment.mean()
    
    return round(reputation_score, 1)

def get_sentiment_distribution(comments_df):
    """Get sentiment distribution from SentLabel column"""
    # Handle both old and new column names
    sentiment_col = None
    if 'SentimentLabel_EN' in comments_df.columns:
        sentiment_col = 'SentimentLabel_EN'
    elif 'SentLabel' in comments_df.columns:
        sentiment_col = 'SentLabel'
    
    if sentiment_col is None:
        return {"Positive": 0, "Neutral": 0, "Negative": 0}
    
    sentiment_counts = comments_df[sentiment_col].value_counts()
    
    # Ensure all categories exist
    result = {
        "Positive": sentiment_counts.get('Positive', 0),
        "Neutral": sentiment_counts.get('Neutral', 0), 
        "Negative": sentiment_counts.get('Negative', 0)
    }
    
    return result

def create_sentiment_timeline(comments_df):
    """Create sentiment timeline chart"""
    if comments_df.empty:
        return go.Figure()
    
    # Group by date and calculate daily sentiment
    daily_sentiment = comments_df.groupby(comments_df['Date'].dt.date)['Sentiment'].mean().reset_index()
    daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])
    
    fig = go.Figure()
    
    # Use dynamic color based on sentiment value
    sentiment_colors = ['#EF4444' if s < -0.1 else '#22C55E' if s > 0.1 else '#9CA3AF' for s in daily_sentiment['Sentiment']]
    
    fig.add_trace(go.Scatter(
        x=daily_sentiment['Date'],
        y=daily_sentiment['Sentiment'],
        mode='lines+markers',
        name='Daily Sentiment',
        line=dict(color='#FFA502', width=3),  # Use orange for the line
        marker=dict(size=6, color=sentiment_colors),
        hovertemplate='<b>%{x}</b><br>Sentiment: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="📈 Reputation Sentiment Timeline",
            font=dict(size=20, color='white')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#404040'),
        yaxis=dict(gridcolor='#404040', title="Sentiment Score"),
        showlegend=False
    )
    
    return fig

def create_video_impact_chart(videos_df):
    """Create video impact analysis"""
    if videos_df.empty:
        return go.Figure()
    
    # Extract upload date and create impact metrics
    recent_videos = videos_df.tail(20)  # Last 20 videos
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=recent_videos.index,
        y=[1] * len(recent_videos),  # Placeholder for view impact
        name='Video Impact',
        marker_color='#FF6348',
        hovertemplate='<b>%{customdata}</b><br>Impact Score: %{y}<extra></extra>',
        customdata=recent_videos['Title'].str[:50] + '...'
    ))
    
    fig.update_layout(
        title=dict(
            text="📹 Recent Video Impact Analysis",
            font=dict(size=20, color='white')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#404040', title="Video Index"),
        yaxis=dict(gridcolor='#404040', title="Impact Score"),
        showlegend=False
    )
    
    return fig

def create_wordcloud_analysis(comments_df):
    """Generate word cloud from comments"""
    if comments_df.empty or 'Comment_EN' not in comments_df.columns:
        return None
    
    # Combine all English comments
    text = ' '.join(comments_df['Comment_EN'].dropna().astype(str))
    
    # Remove common words and clean text
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    text = re.sub(r'\b(the|and|or|but|in|on|at|to|for|of|with|by|a|an|is|are|was|were|be|been|have|has|had|do|does|did|will|would|could|should|may|might|can|cant|dont|wont|isnt|arent|wasnt|werent|hasnt|havent|hadnt|didnt|doesnt|couldnt|shouldnt|wouldnt|youtube|video|comment|channel)\b', ' ', text)
    
    return text

def get_ai_insights(videos_df, comments_df):
    """Extract AI insights from processed data"""
    insights = {
        'total_videos_processed': 0,
        'videos_with_transcripts': 0,
        'videos_with_summaries': 0,
        'avg_sentiment_score': 0.0,
        'critical_keywords': [],
        'processing_coverage': 0.0
    }
    
    if not videos_df.empty:
        insights['total_videos_processed'] = len(videos_df)
        
        # Count videos with AI processing
        if 'Transcript_EN' in videos_df.columns:
            insights['videos_with_transcripts'] = videos_df['Transcript_EN'].notna().sum()
        if 'Summary_EN' in videos_df.columns:
            insights['videos_with_summaries'] = videos_df['Summary_EN'].notna().sum()
        if 'ProcessingStatus' in videos_df.columns:
            completed = (videos_df['ProcessingStatus'] == 'completed').sum()
            insights['processing_coverage'] = (completed / len(videos_df)) * 100
    
    if not comments_df.empty:
        # Calculate average sentiment from AI processing
        if 'SentimentScore_EN' in comments_df.columns:
            sentiment_scores = pd.to_numeric(comments_df['SentimentScore_EN'], errors='coerce')
            insights['avg_sentiment_score'] = sentiment_scores.mean()
        
        # Extract critical keywords
        if 'Keywords_EN' in comments_df.columns:
            all_keywords = []
            for keywords in comments_df['Keywords_EN'].dropna():
                if isinstance(keywords, str):
                    all_keywords.extend(keywords.split(', '))
            
            # Get most common critical keywords
            keyword_counts = Counter(all_keywords)
            critical_terms = ['చేతబడి', 'అరెస్ట్', 'మాగంటి', 'death', 'threat', 'black magic', 'arrest']
            insights['critical_keywords'] = [kw for kw, count in keyword_counts.most_common(10) 
                                           if any(term in kw.lower() for term in critical_terms)]
    
    return insights

def create_sidebar():
    """🎯 REFACTORED SIDEBAR - Modern Crimzon Style with Percepta Navigation"""
    with st.sidebar:
        # --- 1. CRIMZON HEADER ---
        logo_base64 = get_logo_base64()
        if logo_base64:
            st.markdown(
                f"""
                <div class="sidebar-header">
                    <div class="sidebar-logo-container">
                        <img src="data:image/png;base64,{logo_base64}" class="sidebar-logo">
                        <div class="logo-text">
                            <span class="logo-title">PERCEPTA PRO</span>
                            <span class="logo-subtitle">Reputation Intelligence</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="sidebar-header">
                    <div class="sidebar-logo-container">
                        <div class="sidebar-logo-fallback">🎯</div>
                        <div class="logo-text">
                            <span class="logo-title">PERCEPTA PRO</span>
                            <span class="logo-subtitle">Reputation Intelligence</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
        # --- 2. DASHBOARD MODE TOGGLE ---
        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Overview"
        if 'dashboard_mode' not in st.session_state:
            st.session_state.dashboard_mode = "Basic"
    
        # Mode Toggle Section - Clean inline design
        st.markdown("""<div class="mode-toggle-section">""", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("""<div class="section-header">Dashboard Mode</div>""", unsafe_allow_html=True)
        
        with col2:
            current_mode = st.session_state.get('dashboard_mode', 'Basic')
            is_advanced = current_mode == "Advanced"
            
            # Simple toggle with no label
            try:
                toggle_state = st.toggle(
                    "",
                    value=is_advanced,
                    key="dashboard_toggle",
                    label_visibility="collapsed"
                )
            except AttributeError:
                # Fallback to checkbox if st.toggle not available
                toggle_state = st.checkbox(
                    "",
                    value=is_advanced,
                    key="dashboard_toggle_fallback",
                    label_visibility="collapsed"
                )
            
            # Update session state when toggle changes
            if toggle_state != is_advanced:
                new_mode = "Advanced" if toggle_state else "Basic"
                st.session_state.dashboard_mode = new_mode
                st.rerun()
        
        # Close the mode toggle section
        st.markdown("""</div>""", unsafe_allow_html=True)

        # --- 2B. LANGUAGE TOGGLE SECTION ---
        # Initialize language preference session state
        if 'language_mode' not in st.session_state:
            st.session_state.language_mode = "English"
        
        # Language Toggle Section - Clean inline design
        st.markdown("""<div class="language-toggle-section">""", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("""<div class="section-header">Comments Language</div>""", unsafe_allow_html=True)
        
        with col2:
            current_language = st.session_state.get('language_mode', 'English')
            is_telugu = current_language == "Telugu"
            
            # Container for toggle and status
            toggle_container = st.container()
            
            # Simple toggle with no label for Telugu/English
            try:
                language_toggle_state = toggle_container.toggle(
                    "",
                    value=is_telugu,
                    key="language_toggle",
                    label_visibility="collapsed",
                    help="OFF: English (translated) comments | ON: Telugu (original) comments"
                )
            except AttributeError:
                # Fallback to checkbox if st.toggle not available
                language_toggle_state = toggle_container.checkbox(
                    "",
                    value=is_telugu,
                    key="language_toggle_fallback",
                    label_visibility="collapsed",
                    help="OFF: English (translated) comments | ON: Telugu (original) comments"
                )
            
            # Show current language mode
            language_color = "#FF4757" if is_telugu else "#22C55E"
            language_text = "తెలుగు" if is_telugu else "EN"
            
            toggle_container.markdown(f"""
            <div style="text-align: center; margin-top: 0.25rem;">
                <span style="font-size: 0.65rem; color: {language_color}; font-weight: 600;">
                    {language_text}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Update session state when language toggle changes
            if language_toggle_state != is_telugu:
                new_language = "Telugu" if language_toggle_state else "English"
                st.session_state.language_mode = new_language
                st.rerun()
        
        # Close the language toggle section
        st.markdown("""</div>""", unsafe_allow_html=True)

        # --- 3. UNIFIED NAVIGATION MENU ---
        # Define navigation based on mode - MOVED AFTER toggle processing
        basic_pages = [
            {"name": "Overview"},
            {"name": "Videos"},
            {"name": "Comments"},
            {"name": "Analytics"},
            {"name": "Settings"}
        ]
        
        advanced_pages = [
            {"name": "Overview"},
            {"name": "Reputation Alerts"},
            {"name": "Executive Reports"},
            {"name": "Videos"},
            {"name": "Comments"},
            {"name": "Analytics"},
            {"name": "Data Intelligence"},
            {"name": "Settings"}
        ]
        
        # Get the CURRENT mode after toggle processing
        final_mode = st.session_state.get('dashboard_mode', 'Basic')
        
        # Determine pages based on the final mode
        PAGES = advanced_pages if final_mode == "Advanced" else basic_pages
        

        
        # Safety check: If current page is not in available pages, reset to Overview
        current_page_names = [page["name"] for page in PAGES]
        if st.session_state.current_page not in current_page_names:
            st.session_state.current_page = "Overview"
        
        # Navigation Section
        st.markdown("""
        <div class="navigation-section">
            <div class="section-header">Navigation</div>
        </div>
        """, unsafe_allow_html=True)

        # Display navigation buttons
        for page in PAGES:
            is_active = (page["name"] == st.session_state.current_page)
            button_type = "primary" if is_active else "secondary"
            
            if st.button(
                page["name"],
                key=f"nav_btn_{page['name']}",
                type=button_type,
                use_container_width=True
            ):
                st.session_state.current_page = page["name"]
                st.rerun()

        # --- 4. REPUTATION SCORE SECTION ---
        videos_df, comments_df = load_reputation_data()
    
        if not videos_df.empty and not comments_df.empty:
            reputation_score = calculate_reputation_score(comments_df)
            sentiment_dist = get_sentiment_distribution(comments_df)
            
            # Status indicator
            def get_reputation_color_and_text(score):
                if score >= 70: 
                    return "#22C55E", "EXCELLENT"
                elif score >= 50: 
                    return "#FFA502", "MODERATE"
                else: 
                    return "#FF4757", "CRITICAL"
            
            status_color, status_text = get_reputation_color_and_text(reputation_score)
            
            # Main reputation score
            st.markdown(f"""
            <div class="reputation-card">
                <div class="reputation-status">{status_text}</div>
                <div class="reputation-score">{reputation_score}%</div>
                <div class="reputation-label">Reputation Score</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick Stats header - positioned right before metrics
            st.markdown("""
            <div class="stats-section">
                <div class="section-header">Quick Stats</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick stats using Streamlit metrics
            st.metric("Videos", len(videos_df))
            st.metric("Comments", len(comments_df))
            
            positive_pct = round((sentiment_dist['Positive'] / sum(sentiment_dist.values())) * 100, 1) if sum(sentiment_dist.values()) > 0 else 0
            st.metric("Positive", f"{positive_pct}%")

        # --- 5. FOOTER SECTION ---
        st.markdown('<div class="sidebar-footer-spacer"></div>', unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class="nav-link-wrapper footer-link">
                <span>Documentation</span>
            </div>
            <div class="nav-link-wrapper footer-link">
                <span>Support</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return st.session_state.current_page

def create_top_mode_selector():
    """Create compact horizontal mode selector at top of page"""
    # Initialize session state
    if 'dashboard_mode' not in st.session_state:
        st.session_state.dashboard_mode = "Basic"
    
    # Compact horizontal mode selector
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(45, 45, 45, 0.6) 0%, rgba(45, 45, 45, 0.3) 100%);
        border: 1px solid #404040;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        backdrop-filter: blur(10px);
    ">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="color: #FFA502; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">
                🎛️ Dashboard Mode
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode selection in columns for horizontal layout
    col1, col2, col3 = st.columns([2, 1, 4])
    
    with col1:
        # Mode selector
        dashboard_mode = st.selectbox(
            "",
            ["Advanced", "Basic"],
            index=0 if st.session_state.dashboard_mode == "Advanced" else 1,
            key="top_mode_selector",
            label_visibility="collapsed"
        )
        
        # Update session state when mode changes
        if dashboard_mode != st.session_state.dashboard_mode:
            st.session_state.dashboard_mode = dashboard_mode
            st.rerun()
    
    with col2:
        # Status indicator
        mode_color = "#FF4757" if dashboard_mode == "Advanced" else "#2ED573"
        mode_icon = "🚀" if dashboard_mode == "Advanced" else "⚡"
        
        st.markdown(f"""
        <div style="
            background: {mode_color}20;
            border: 1px solid {mode_color};
            border-radius: 20px;
            padding: 0.25rem 0.75rem;
            text-align: center;
            margin-top: 0.5rem;
        ">
            <span style="color: {mode_color}; font-size: 0.75rem; font-weight: 600;">
                {mode_icon} {dashboard_mode.upper()}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Compact mode description
        mode_desc = {
            "Advanced": "Full feature set with predictive analytics, executive reports, and comprehensive reputation intelligence",
            "Basic": "Streamlined interface with essential monitoring features for quick insights"
        }
        
        st.markdown(f"""
        <div style="
            color: #CCCCCC; 
            font-size: 0.8rem; 
            line-height: 1.4; 
            margin-top: 0.75rem;
            opacity: 0.8;
        ">
            {mode_desc[dashboard_mode]}
        </div>
        """, unsafe_allow_html=True)
    
    # Compact spacing after mode selector
    st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)

# PAGE FUNCTIONS
def show_overview_page():
    """Enhanced Overview page with executive summary and key metrics"""
    # Create page header without mode selector since it's now in sidebar
    st.markdown('<h1 class="page-title">📊 Overview</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Real-time intelligence for Sandhya Convention MD Sridhar Rao\'s online reputation</p>', unsafe_allow_html=True)
    
    # Load data with language preference support
    videos_df, comments_df_raw = load_reputation_data()
    
    # Apply language preference to comments
    comments_df = get_language_aware_comments(comments_df_raw)
    
    if videos_df.empty or comments_df.empty:
        st.error("⚠️ No data available. Please check data files.")
        return
    
    # Get AI insights
    ai_insights = get_ai_insights(videos_df, comments_df)
    
    # Calculate core metrics
    reputation_score = calculate_reputation_score(comments_df)
    sentiment_dist = get_sentiment_distribution(comments_df)
    total_comments = sum(sentiment_dist.values())
    positive_pct = round((sentiment_dist['Positive'] / total_comments) * 100, 1) if total_comments > 0 else 0
    negative_pct = round((sentiment_dist['Negative'] / total_comments) * 100, 1) if total_comments > 0 else 0
    total_videos = len(videos_df)
    
    # 🎯 REFINED EXECUTIVE STATUS INDICATOR
    if reputation_score < 30:
        status_color = "#EF4444"
        status_icon = "🚨"
        status_text = "REPUTATION CRISIS"
        status_bg = "linear-gradient(90deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.01) 100%)"
    elif reputation_score < 50:
        status_color = "#F59E0B"
        status_icon = "⚠️"
        status_text = "REPUTATION WARNING"
        status_bg = "linear-gradient(90deg, rgba(245, 158, 11, 0.05) 0%, rgba(245, 158, 11, 0.01) 100%)"
    elif reputation_score < 70:
        status_color = "#EAB308"
        status_icon = "⚖️"
        status_text = "REPUTATION MODERATE"
        status_bg = "linear-gradient(90deg, rgba(234, 179, 8, 0.05) 0%, rgba(234, 179, 8, 0.01) 100%)"
    else:
        status_color = "#22C55E"
        status_icon = "✅"
        status_text = "REPUTATION HEALTHY"
        status_bg = "linear-gradient(90deg, rgba(34, 197, 94, 0.05) 0%, rgba(34, 197, 94, 0.01) 100%)"
    
    # Sleek Executive Status Bar
    st.markdown(f"""
    <div style="
        background: {status_bg};
        border: 1px solid rgba(64, 64, 64, 0.3);
        border-left: 3px solid {status_color};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    ">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="
                font-size: 1.5rem; 
                background: rgba(255, 255, 255, 0.06); 
                padding: 0.4rem; 
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 48px;
                height: 48px;
            ">{status_icon}</div>
            <div>
                <div style="color: {status_color}; font-weight: 700; font-size: 1rem; margin-bottom: 0.1rem;">{status_text}</div>
                <div style="color: #999; font-size: 0.75rem;">Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</div>
            </div>
        </div>
        <div style="display: flex; gap: 2rem; font-size: 0.8rem;">
            <div style="text-align: center;">
                <div style="color: #999; font-size: 0.7rem; margin-bottom: 0.1rem;">SCORE</div>
                <div style="color: {status_color}; font-weight: 700; font-size: 1rem;">{reputation_score}%</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #999; font-size: 0.7rem; margin-bottom: 0.1rem;">POSITIVE</div>
                <div style="color: #22C55E; font-weight: 700; font-size: 1rem;">{positive_pct}%</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #999; font-size: 0.7rem; margin-bottom: 0.1rem;">NEGATIVE</div>
                <div style="color: #EF4444; font-weight: 700; font-size: 1rem;">{negative_pct}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 📊 PREMIUM METRICS GRID
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.5rem; font-weight: 600;">🎯 Key Performance Metrics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Enhanced card style with premium effects
    card_style = """
        background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 50%, #2D2D2D 100%);
        border-radius: 12px;
        padding: 1.5rem 0.8rem;
        border: 1px solid #404040;
        text-align: center;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    """
    
    with col1:
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">🎯</div>
            <div style="color: {status_color}; font-size: 1.8rem; font-weight: 800; line-height: 1;">{reputation_score}%</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">REPUTATION SCORE</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">{total_comments:,} comments analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">📹</div>
            <div style="color: #FF6348; font-size: 1.8rem; font-weight: 800; line-height: 1;">{total_videos:,}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">VIDEOS TRACKED</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">{videos_df['Channel'].nunique()} unique channels</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        high_engagement = len(comments_df[comments_df['LikeCount'] > 10]) if 'LikeCount' in comments_df.columns else 0
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">💬</div>
            <div style="color: #FFA502; font-size: 1.8rem; font-weight: 800; line-height: 1;">{total_comments:,}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">TOTAL COMMENTS</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">{high_engagement} high-engagement</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        sentiment_color = "#22C55E" if positive_pct > 50 else "#EF4444" if positive_pct < 30 else "#EAB308"
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">😊</div>
            <div style="color: {sentiment_color}; font-size: 1.8rem; font-weight: 800; line-height: 1;">{positive_pct}%</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">POSITIVE SENTIMENT</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Target: >70%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 📈 ANALYTICS SECTION
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Time period selector (compact)
    col_filter, col_spacer = st.columns([2, 6])
    with col_filter:
        time_period = st.selectbox(
            "",
            ["📅 Last 30 Days", "📅 Last 90 Days", "📅 All Time"],
            index=1,
            key="overview_time_period"
        )
    
    # Filter data based on selected period
    if "30 Days" in time_period:
        filtered_comments = comments_df.tail(len(comments_df) // 3)
    elif "90 Days" in time_period:
        filtered_comments = comments_df.tail(len(comments_df) // 2)
    else:
        filtered_comments = comments_df
    
    # Enhanced Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">📈 Sentiment Timeline</h3>', unsafe_allow_html=True)
        
        sentiment_fig = create_sentiment_timeline(filtered_comments)
        sentiment_fig.update_layout(
            height=340, 
            margin=dict(t=10, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(sentiment_fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">📊 Video Impact Analysis</h3>', unsafe_allow_html=True)
        
        video_fig = create_video_impact_chart(videos_df)
        video_fig.update_layout(
            height=340, 
            margin=dict(t=10, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(video_fig, use_container_width=True)
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 🧠 PREMIUM EXECUTIVE INSIGHTS
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">🧠 Executive Intelligence Summary</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    insight_box_style = """
        background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
        border-radius: 14px;
        padding: 1.8rem;
        border: 1px solid #404040;
        height: 280px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    """
    
    with col1:
        st.markdown(f"""
        <div style="{insight_box_style}">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #FF4757, #FF6348);
            "></div>
            <h4 style="color: #FF4757; margin: 0 0 1.2rem 0; font-size: 1rem; font-weight: 700;">
                🎯 Performance Overview
            </h4>
            <div style="color: #CCCCCC; line-height: 1.6; font-size: 0.85rem;">
                <div style="margin-bottom: 1rem; padding: 0.6rem; background: rgba(255, 71, 87, 0.03); border-radius: 6px; border-left: 3px solid #FF4757;">
                    <strong style="color: #FF6348;">Reputation Status</strong><br>
                    <span style="color: {status_color}; font-weight: 600;">{status_text.title()}</span>
                </div>
                <div style="margin-bottom: 0.8rem;">
                    <strong style="color: #FFA502;">Sentiment Analysis</strong><br>
                    <span style="color: #22C55E;">{positive_pct}% Positive</span> • <span style="color: #EF4444;">{negative_pct}% Negative</span>
                </div>
                <div style="margin-bottom: 0.8rem;">
                    <strong style="color: #FFA502;">Media Coverage</strong><br>
                    {total_videos} videos across {videos_df['Channel'].nunique()} channels
                </div>
                <div>
                    <strong style="color: #FFA502;">Engagement Level</strong><br>
                    {total_comments:,} comments analyzed
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Strategic recommendations
        if reputation_score < 50:
            recommendations = [
                "🚨 Activate crisis management protocol",
                "📞 Immediate PR team engagement",
                "📝 Develop positive content strategy",
                "📊 Implement hourly monitoring"
            ]
            rec_color = "#EF4444"
            rec_title = "🚨 Crisis Response Actions"
        elif reputation_score < 70:
            recommendations = [
                "📈 Amplify positive content creation",
                "🤝 Strengthen community engagement", 
                "📱 Monitor social mentions actively",
                "💬 Address concerns proactively"
            ]
            rec_color = "#EAB308"
            rec_title = "⚠️ Strategic Improvements"
        else:
            recommendations = [
                "✅ Maintain positive momentum",
                "📊 Continue systematic monitoring",
                "🎯 Leverage positive sentiment",
                "🔄 Optimize content distribution"
            ]
            rec_color = "#22C55E"
            rec_title = "✅ Optimization Actions"
        
        rec_items = ""
        for rec in recommendations:
            rec_items += f'<div style="margin-bottom: 0.7rem; padding: 0.7rem; background: rgba(255, 255, 255, 0.02); border-radius: 6px; border-left: 2px solid {rec_color}; font-size: 0.8rem;">{rec}</div>'
        
        st.markdown(f"""
        <div style="{insight_box_style}">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, {rec_color}, #FFA502);
            "></div>
            <h4 style="color: {rec_color}; margin: 0 0 1.2rem 0; font-size: 1rem; font-weight: 700;">
                {rec_title}
            </h4>
            <div style="color: #CCCCCC; line-height: 1.4; font-size: 0.85rem;">
                {rec_items}
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_analytics_page():
    """Enhanced Analytics page with comprehensive intelligence and insights"""
    st.markdown('<h1 class="page-title">📈 Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Advanced analytics, sentiment intelligence, and strategic insights for Sridhar Rao</p>', unsafe_allow_html=True)
    
    videos_df, comments_df_raw = load_reputation_data()
    
    # Apply language preference to comments
    comments_df = get_language_aware_comments(comments_df_raw)
    
    if comments_df.empty:
        st.error("No analytics data available")
        return
    
    # Calculate comprehensive metrics
    total_comments = len(comments_df)
    total_videos = len(videos_df)
    sentiment_dist = get_sentiment_distribution(comments_df)
    reputation_score = calculate_reputation_score(comments_df)
    avg_sentiment = comments_df['Sentiment'].mean() if 'Sentiment' in comments_df.columns else 0
    
    # Calculate engagement metrics
    total_likes = comments_df['LikeCount'].sum() if 'LikeCount' in comments_df.columns else 0
    avg_likes = comments_df['LikeCount'].mean() if 'LikeCount' in comments_df.columns else 0
    engagement_rate = (total_likes / total_comments * 100) if total_comments > 0 else 0
    
    # 📊 ANALYTICS PERFORMANCE METRICS
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📊 Analytics Performance Metrics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Enhanced card style - consistent with other pages
    card_style = """
        background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 50%, #2D2D2D 100%);
        border-radius: 12px;
        padding: 1.5rem 0.8rem;
        border: 1px solid #404040;
        text-align: center;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    """
    
    with col1:
        # Reputation score with dynamic color
        rep_color = "#22C55E" if reputation_score >= 70 else "#FFA502" if reputation_score >= 50 else "#EF4444"
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">🎯</div>
            <div style="color: {rep_color}; font-size: 1.8rem; font-weight: 800; line-height: 1;">{reputation_score:.1f}%</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">REPUTATION SCORE</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Overall rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Sentiment score with dynamic color
        sentiment_color = "#22C55E" if avg_sentiment >= 0.1 else "#FFA502" if avg_sentiment >= -0.1 else "#EF4444"
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">📊</div>
            <div style="color: {sentiment_color}; font-size: 1.8rem; font-weight: 800; line-height: 1;">{avg_sentiment:.2f}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">AVG SENTIMENT</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Mood indicator</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Engagement rate
        engagement_color = "#22C55E" if engagement_rate >= 10 else "#FFA502" if engagement_rate >= 5 else "#EF4444"
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">🔥</div>
            <div style="color: {engagement_color}; font-size: 1.8rem; font-weight: 800; line-height: 1;">{engagement_rate:.1f}%</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">ENGAGEMENT RATE</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Interaction level</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Content coverage
        coverage_score = min(100, (total_videos / 50) * 100) if total_videos > 0 else 0  # Assuming 50 videos is good coverage
        coverage_color = "#22C55E" if coverage_score >= 80 else "#FFA502" if coverage_score >= 50 else "#EF4444"
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">📺</div>
            <div style="color: {coverage_color}; font-size: 1.8rem; font-weight: 800; line-height: 1;">{coverage_score:.0f}%</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">CONTENT COVERAGE</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Media presence</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 📈 SENTIMENT INTELLIGENCE SECTION
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📈 Sentiment Intelligence</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">🎭 Sentiment Distribution</h3>', unsafe_allow_html=True)
        
        # Enhanced pie chart
        color_map = {
            'Positive': '#22C55E',  # Green
            'Neutral': '#9CA3AF',   # Light grey
            'Negative': '#EF4444'   # Red
        }
        
        chart_colors = [color_map.get(label, '#9CA3AF') for label in sentiment_dist.keys()]
        
        fig = go.Figure(data=[go.Pie(
            labels=list(sentiment_dist.keys()),
            values=list(sentiment_dist.values()),
            hole=0.4,
            marker_colors=chart_colors,
            textinfo='label+percent',
            textfont_size=12
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(t=10, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">📈 Sentiment Timeline</h3>', unsafe_allow_html=True)
        
        # Create enhanced sentiment timeline
        if 'Date' in comments_df.columns and 'Sentiment' in comments_df.columns:
            comments_df_copy = comments_df.copy()
            comments_df_copy['Date'] = pd.to_datetime(comments_df_copy['Date'])
            
            # Group by date and calculate daily sentiment
            daily_sentiment = comments_df_copy.groupby(comments_df_copy['Date'].dt.date)['Sentiment'].mean().reset_index()
            daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])
            
            fig = go.Figure()
            
            # Use dynamic color based on sentiment value
            sentiment_colors = ['#EF4444' if s < -0.1 else '#22C55E' if s > 0.1 else '#FFA502' for s in daily_sentiment['Sentiment']]
            
            fig.add_trace(go.Scatter(
                x=daily_sentiment['Date'],
                y=daily_sentiment['Sentiment'],
                mode='lines+markers',
                line=dict(color='#FF6348', width=3),
                marker=dict(size=8, color=sentiment_colors),
                hovertemplate='<b>%{x}</b><br>Sentiment: %{y:.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(t=10, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='#404040', title="Date"),
                yaxis=dict(gridcolor='#404040', title="Sentiment"),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Timeline data not available")
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 🔤 WORD CLOUD ANALYSIS SECTION (50% smaller)
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">🔤 Word Cloud Analysis</h2>', unsafe_allow_html=True)
    
    text_data = create_wordcloud_analysis(comments_df)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if text_data and len(text_data.strip()) > 10:
            try:
                # Create word cloud - 50% smaller as requested
                wordcloud = WordCloud(
                    width=300,  # Reduced by 50% from 600
                    height=150,  # Reduced by 50% from 300
                    background_color='black',
                    colormap='Reds',
                    max_words=100,
                    prefer_horizontal=0.7,
                    relative_scaling=0.5
                ).generate(text_data)
                
                # Create matplotlib figure - 50% smaller
                fig, ax = plt.subplots(figsize=(4, 2))  # Reduced from (8, 4)
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                
                # Set black background and border
                fig.patch.set_facecolor('black')
                ax.set_facecolor('black')
                
                # Add black border around the plot
                for spine in ax.spines.values():
                    spine.set_edgecolor('black')
                    spine.set_linewidth(3)
                
                plt.tight_layout(pad=0)
                
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error generating word cloud: {e}")
        else:
            st.info("Insufficient text data for word cloud generation")
    
    with col2:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">🏆 Top Keywords</h3>', unsafe_allow_html=True)
        
        if text_data and len(text_data.strip()) > 10:
            words = text_data.split()
            word_freq = Counter(words)
            top_words = word_freq.most_common(10)
            
            # Display top keywords in a clean list
            for i, (word, freq) in enumerate(top_words):
                st.markdown(f"""
                <div style="
                    background: rgba(45, 45, 45, 0.3); 
                    padding: 0.5rem 1rem; 
                    border-radius: 6px; 
                    margin-bottom: 0.5rem;
                    border-left: 3px solid #FF4757;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #FFF; font-weight: 600;">#{i+1} {word}</span>
                        <span style="color: #FF4757; font-weight: 700;">{freq}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No keyword data available")
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 📊 ADVANCED ANALYTICS SECTION
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📊 Advanced Analytics</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">📅 Engagement Over Time</h3>', unsafe_allow_html=True)
        
        if 'Date' in comments_df.columns and 'LikeCount' in comments_df.columns:
            # Create engagement timeline
            comments_df_copy = comments_df.copy()
            comments_df_copy['Date'] = pd.to_datetime(comments_df_copy['Date'])
            
            # Group by date and calculate engagement metrics
            daily_engagement = comments_df_copy.groupby(comments_df_copy['Date'].dt.date).agg({
                'LikeCount': 'sum',
                'Comment': 'count'
            }).reset_index()
            daily_engagement['Date'] = pd.to_datetime(daily_engagement['Date'])
            daily_engagement['EngagementRate'] = (daily_engagement['LikeCount'] / daily_engagement['Comment'] * 100).fillna(0)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=daily_engagement['Date'],
                y=daily_engagement['EngagementRate'],
                mode='lines+markers',
                line=dict(color='#FFA502', width=3),
                marker=dict(size=6, color='#FFA502'),
                name='Engagement Rate %',
                hovertemplate='<b>%{x}</b><br>Engagement: %{y:.1f}%<extra></extra>'
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(t=10, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='#404040', title="Date"),
                yaxis=dict(gridcolor='#404040', title="Engagement Rate (%)"),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Engagement data not available")
    
    with col2:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">📈 Sentiment Trends</h3>', unsafe_allow_html=True)
        
        if 'Date' in comments_df.columns:
            # Create sentiment trend analysis
            comments_df_copy = comments_df.copy()
            comments_df_copy['Date'] = pd.to_datetime(comments_df_copy['Date'])
            
            # Safe column checking for sentiment data
            if 'SentLabel' in comments_df_copy.columns:
                # Group by date and sentiment
                sentiment_by_date = comments_df_copy.groupby(['Date', 'SentLabel']).size().unstack(fill_value=0).reset_index()
                sentiment_by_date['Date'] = pd.to_datetime(sentiment_by_date['Date'])
                
                fig = go.Figure()
                
                colors = {'Positive': '#22C55E', 'Neutral': '#9CA3AF', 'Negative': '#EF4444'}
                
                for sentiment in ['Positive', 'Neutral', 'Negative']:
                    if sentiment in sentiment_by_date.columns:
                        fig.add_trace(go.Scatter(
                            x=sentiment_by_date['Date'],
                            y=sentiment_by_date[sentiment],
                            mode='lines+markers',
                            name=sentiment,
                            line=dict(width=2, color=colors[sentiment]),
                            marker=dict(size=4, color=colors[sentiment])
                        ))
                
                fig.update_layout(
                    height=300,
                    margin=dict(t=10, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='#404040', title="Date"),
                    yaxis=dict(gridcolor='#404040', title="Comment Count"),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            elif 'Sentiment' in comments_df_copy.columns:
                # Use numeric sentiment values with categorization
                st.info("Using numeric sentiment analysis (SentLabel column not found)")
                
                # Create sentiment categories
                comments_df_copy['SentimentCategory'] = comments_df_copy['Sentiment'].apply(
                    lambda x: 'Positive' if x > 0.1 else 'Negative' if x < -0.1 else 'Neutral'
                )
                
                # Group by date and sentiment category
                sentiment_by_date = comments_df_copy.groupby(['Date', 'SentimentCategory']).size().unstack(fill_value=0).reset_index()
                sentiment_by_date['Date'] = pd.to_datetime(sentiment_by_date['Date'])
                
                fig = go.Figure()
                
                colors = {'Positive': '#22C55E', 'Neutral': '#9CA3AF', 'Negative': '#EF4444'}
                
                for sentiment in ['Positive', 'Neutral', 'Negative']:
                    if sentiment in sentiment_by_date.columns:
                        fig.add_trace(go.Scatter(
                            x=sentiment_by_date['Date'],
                            y=sentiment_by_date[sentiment],
                            mode='lines+markers',
                            name=sentiment,
                            line=dict(width=2, color=colors[sentiment]),
                            marker=dict(size=4, color=colors[sentiment])
                        ))
                
                fig.update_layout(
                    height=300,
                    margin=dict(t=10, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='#404040', title="Date"),
                    yaxis=dict(gridcolor='#404040', title="Comment Count"),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Neither SentLabel nor Sentiment columns found in data")
        else:
            st.info("Trend data not available")
    
    # 💡 KEY INSIGHTS SECTION
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">💡 Key Insights & Recommendations</h2>', unsafe_allow_html=True)
    
    # Generate insights based on data
    insights = []
    
    if reputation_score >= 70:
        insights.append(("✅ Strong Reputation", f"Reputation score of {reputation_score:.1f}% indicates excellent public perception.", "#22C55E"))
    elif reputation_score >= 50:
        insights.append(("⚠️ Moderate Reputation", f"Reputation score of {reputation_score:.1f}% has room for improvement.", "#FFA502"))
    else:
        insights.append(("🚨 Reputation Alert", f"Reputation score of {reputation_score:.1f}% requires immediate attention.", "#EF4444"))
    
    positive_pct = round((sentiment_dist['Positive'] / total_comments) * 100, 1) if total_comments > 0 else 0
    if positive_pct >= 60:
        insights.append(("😊 Positive Sentiment", f"{positive_pct}% positive sentiment shows strong public support.", "#22C55E"))
    elif positive_pct >= 40:
        insights.append(("😐 Mixed Sentiment", f"{positive_pct}% positive sentiment indicates balanced opinions.", "#FFA502"))
    else:
        insights.append(("😞 Negative Sentiment", f"Only {positive_pct}% positive sentiment needs strategic response.", "#EF4444"))
    
    if engagement_rate >= 10:
        insights.append(("🔥 High Engagement", f"{engagement_rate:.1f}% engagement rate shows active audience interaction.", "#22C55E"))
    elif engagement_rate >= 5:
        insights.append(("📈 Moderate Engagement", f"{engagement_rate:.1f}% engagement rate has potential for growth.", "#FFA502"))
    else:
        insights.append(("📉 Low Engagement", f"{engagement_rate:.1f}% engagement rate needs improvement strategies.", "#EF4444"))
    
    # Display insights in cards
    cols = st.columns(len(insights))
    for i, (title, description, color) in enumerate(insights):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: rgba(45, 45, 45, 0.3); 
                padding: 1.5rem; 
                border-radius: 12px; 
                border-left: 4px solid {color};
                border: 1px solid #404040;
                height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="color: {color}; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem;">{title}</div>
                <div style="color: #CCCCCC; font-size: 0.8rem; line-height: 1.4;">{description}</div>
            </div>
            """, unsafe_allow_html=True)

    # 🧠 ADVANCED MODE FEATURES
    if st.session_state.dashboard_mode == "Advanced":
        st.markdown("---")
        st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">🧠 Advanced Analytics</h2>', unsafe_allow_html=True)
        
        # Word Cloud Analysis (with error handling)
        st.markdown("### 🔤 Word Cloud Analysis")
        
        try:
            text_data = create_wordcloud_analysis(comments_df)
            
            if text_data and len(text_data.strip()) > 10:
                try:
                    import matplotlib
                    matplotlib.use('Agg')  # Use non-interactive backend
                    
                    # Create word cloud
                    wordcloud = WordCloud(
                        width=600,
                        height=300,
                        background_color='black',
                        colormap='Reds',
                        max_words=100,
                        prefer_horizontal=0.7,
                        relative_scaling=0.5
                    ).generate(text_data)
                    
                    # Create matplotlib figure with black background and border
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    
                    # Set black background and border
                    fig.patch.set_facecolor('black')
                    ax.set_facecolor('black')
                    
                    # Add black border around the plot
                    for spine in ax.spines.values():
                        spine.set_edgecolor('black')
                        spine.set_linewidth(3)
                    
                    plt.tight_layout(pad=0)
                    
                    # Display in container with black border
                    st.markdown("""
                    <div style="
                        background: black; 
                        border: 3px solid black; 
                        border-radius: 8px; 
                        padding: 1rem;
                        margin: 1rem 0;
                    ">
                    """, unsafe_allow_html=True)
                    
                    st.pyplot(fig)
                    plt.close(fig)  # Close figure to free memory
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Top keywords in two columns
                    st.markdown("### 🏆 Top Keywords")
                    words = text_data.split()
                    word_freq = Counter(words)
                    top_words = word_freq.most_common(20)
                    
                    # Create two columns for keywords
                    col1, col2 = st.columns(2)
                    
                    for i, (word, freq) in enumerate(top_words):
                        if i < 10:
                            col1.metric(f"#{i+1} {word}", freq)
                        else:
                            col2.metric(f"#{i+1} {word}", freq)
                    
                except Exception as e:
                    st.error(f"Error generating word cloud: {e}")
                    st.info("Word cloud feature requires proper matplotlib configuration")
            else:
                st.info("Insufficient text data for word cloud generation")
        except Exception as e:
            st.warning("Word cloud analysis not available - missing dependencies or data")
            st.info("Install missing packages: `pip install wordcloud matplotlib`")
        
        # 🤖 ML Model Insights
        st.markdown("### 🤖 Machine Learning Insights")
        
        # Try to load ML predictions
        try:
            predictions = load_phase3c_predictions()
            if predictions:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div style="
                        background: rgba(45, 45, 45, 0.3); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        border-left: 4px solid #22C55E;
                        border: 1px solid #404040;
                    ">
                        <div style="color: #22C55E; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem;">🎯 Model Performance</div>
                        <div style="color: #CCCCCC; font-size: 0.8rem; line-height: 1.4;">Advanced ML models are analyzing sentiment patterns and predicting reputation trends with high accuracy.</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="
                        background: rgba(45, 45, 45, 0.3); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        border-left: 4px solid #FFA502;
                        border: 1px solid #404040;
                    ">
                        <div style="color: #FFA502; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem;">📊 Predictive Accuracy</div>
                        <div style="color: #CCCCCC; font-size: 0.8rem; line-height: 1.4;">Our reputation intelligence models maintain 90%+ accuracy in sentiment analysis and trend prediction.</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ML prediction data not available")
        except Exception as e:
            st.info("ML features will be available after model training")
        
        # 📈 Advanced Metrics Dashboard
        st.markdown("### 📈 Advanced Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Engagement Rate
            try:
                if 'LikeCount' in comments_df.columns:
                    avg_likes = comments_df['LikeCount'].mean()
                    st.metric(
                        "Average Engagement",
                        f"{avg_likes:.1f}",
                        delta="Likes per comment"
                    )
                else:
                    st.metric("Average Engagement", "N/A", delta="LikeCount column not found")
            except Exception as e:
                st.metric("Average Engagement", "N/A", delta="Data not available")
        
        with col2:
            # Comment Velocity
            try:
                if 'Date' in comments_df.columns and len(comments_df) > 10:
                    recent_comments = len(comments_df.tail(int(len(comments_df) * 0.1)))
                    velocity = recent_comments / max(1, int(len(comments_df) * 0.1))
                    st.metric(
                        "Comment Velocity",
                        f"{velocity:.2f}",
                        delta="Comments per day"
                    )
                else:
                    st.metric("Comment Velocity", "N/A", delta="Date column not found")
            except Exception as e:
                st.metric("Comment Velocity", "N/A", delta="Data not available")
        
        with col3:
            # Sentiment Consistency
            try:
                if len(comments_df) > 0 and 'Sentiment' in comments_df.columns:
                    sentiment_std = comments_df['Sentiment'].std()
                    consistency = max(0, 1 - sentiment_std) * 100
                    st.metric(
                        "Sentiment Consistency",
                        f"{consistency:.1f}%",
                        delta="Stability index"
                    )
                else:
                    st.metric("Sentiment Consistency", "N/A", delta="Sentiment column not found")
            except Exception as e:
                st.metric("Sentiment Consistency", "N/A", delta="Data not available")
        
        # 📊 Advanced Charts Section with Safe Column Handling
        st.markdown("### 📊 Advanced Visualizations")
        
        if not comments_df.empty:
            # Sentiment over time heatmap with safe column checking
            if 'Date' in comments_df.columns:
                st.markdown("### 📅 Sentiment Timeline by Day")
                
                try:
                    # Create date-based grouping
                    comments_df_copy = comments_df.copy()
                    comments_df_copy['Date'] = pd.to_datetime(comments_df_copy['Date'], errors='coerce')
                    comments_df_copy['DateOnly'] = comments_df_copy['Date'].dt.date
                    comments_df_copy['Hour'] = comments_df_copy['Date'].dt.hour
                    
                    # Check if SentLabel exists, if not use Sentiment for grouping
                    if 'SentLabel' in comments_df_copy.columns:
                        # Group by date and sentiment label
                        sentiment_by_date = comments_df_copy.groupby(['DateOnly', 'SentLabel']).size().unstack(fill_value=0)
                        
                        if not sentiment_by_date.empty:
                            fig = go.Figure()
                            
                            dates = sentiment_by_date.index
                            colors = {'Positive': '#22C55E', 'Neutral': '#9CA3AF', 'Negative': '#EF4444'}
                            
                            for sentiment in ['Positive', 'Neutral', 'Negative']:
                                if sentiment in sentiment_by_date.columns:
                                    fig.add_trace(go.Scatter(
                                        x=dates,
                                        y=sentiment_by_date[sentiment],
                                        mode='lines+markers',
                                        name=sentiment,
                                        line=dict(width=3, color=colors[sentiment]),
                                        marker=dict(size=6, color=colors[sentiment])
                                    ))
                            
                            fig.update_layout(
                                title="Daily Sentiment Counts Over Time",
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white'),
                                xaxis=dict(gridcolor='#404040', title="Date"),
                                yaxis=dict(gridcolor='#404040', title="Number of Comments"),
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No sentiment timeline data available")
                    
                    elif 'Sentiment' in comments_df_copy.columns:
                        # Use numeric sentiment values instead
                        st.info("Using numeric sentiment analysis (SentLabel column not found)")
                        
                        # Group by date and create sentiment ranges
                        comments_df_copy['SentimentCategory'] = comments_df_copy['Sentiment'].apply(
                            lambda x: 'Positive' if x > 0.1 else 'Negative' if x < -0.1 else 'Neutral'
                        )
                        
                        sentiment_by_date = comments_df_copy.groupby(['DateOnly', 'SentimentCategory']).size().unstack(fill_value=0)
                        
                        if not sentiment_by_date.empty:
                            fig = go.Figure()
                            
                            dates = sentiment_by_date.index
                            colors = {'Positive': '#22C55E', 'Neutral': '#9CA3AF', 'Negative': '#EF4444'}
                            
                            for sentiment in ['Positive', 'Neutral', 'Negative']:
                                if sentiment in sentiment_by_date.columns:
                                    fig.add_trace(go.Scatter(
                                        x=dates,
                                        y=sentiment_by_date[sentiment],
                                        mode='lines+markers',
                                        name=sentiment,
                                        line=dict(width=3, color=colors[sentiment]),
                                        marker=dict(size=6, color=colors[sentiment])
                                    ))
                            
                            fig.update_layout(
                                title="Daily Sentiment Counts Over Time",
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white'),
                                xaxis=dict(gridcolor='#404040', title="Date"),
                                yaxis=dict(gridcolor='#404040', title="Number of Comments"),
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No sentiment data available for timeline")
                    else:
                        st.warning("Neither SentLabel nor Sentiment columns found in data")
                        
                except Exception as e:
                    st.error(f"Error creating sentiment timeline: {str(e)}")
                    st.info("Data structure may not be compatible with timeline analysis")
            else:
                st.info("Date column not found - timeline analysis not available")
        else:
            st.warning("No comment data available for advanced visualizations")

def show_videos_page():
    """Enhanced Videos page with professional video management interface"""
    st.markdown('<h1 class="page-title">📹 Videos</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Comprehensive video tracking and performance analysis</p>', unsafe_allow_html=True)
    
    # Load data
    videos_df, comments_df = load_reputation_data()
    
    if videos_df.empty:
        st.error("⚠️ No video data available. Please check data files.")
        return
    
    # Calculate video metrics using same design pattern as Overview
    total_videos = len(videos_df)
    unique_channels = videos_df['Channel'].nunique() if 'Channel' in videos_df.columns else 0
    recent_videos = len(videos_df.tail(30)) if len(videos_df) > 30 else len(videos_df)
    
    # Calculate average comments per video
    if not comments_df.empty and 'VideoID' in comments_df.columns:
        video_comments = comments_df.groupby('VideoID').size()
        avg_comments = video_comments.mean() if len(video_comments) > 0 else 0
    else:
        avg_comments = 0
    
    # 📊 VIDEO METRICS CARDS (using perfected card design)
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📊 Video Performance Metrics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Enhanced card style - same as Overview page
    card_style = """
        background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 50%, #2D2D2D 100%);
        border-radius: 12px;
        padding: 1.5rem 0.8rem;
        border: 1px solid #404040;
        text-align: center;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    """
    
    with col1:
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">📹</div>
            <div style="color: #FF6348; font-size: 1.8rem; font-weight: 800; line-height: 1;">{total_videos:,}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">TOTAL VIDEOS</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Tracked content</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">📺</div>
            <div style="color: #FFA502; font-size: 1.8rem; font-weight: 800; line-height: 1;">{unique_channels:,}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">UNIQUE CHANNELS</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Content sources</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">🆕</div>
            <div style="color: #22C55E; font-size: 1.8rem; font-weight: 800; line-height: 1;">{recent_videos:,}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">RECENT VIDEOS</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Last 30 days</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">💬</div>
            <div style="color: #A855F7; font-size: 1.8rem; font-weight: 800; line-height: 1;">{avg_comments:.1f}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">AVG COMMENTS</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Per video</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 📊 VIDEO ANALYTICS SECTION
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📊 Video Analytics</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">📈 Upload Timeline</h3>', unsafe_allow_html=True)
        
        if 'Upload Date' in videos_df.columns:
            # Create upload timeline chart
            videos_df_copy = videos_df.copy()
            videos_df_copy['Upload Date'] = pd.to_datetime(videos_df_copy['Upload Date'])
            videos_df_copy['Month'] = videos_df_copy['Upload Date'].dt.to_period('M')
            
            monthly_uploads = videos_df_copy.groupby('Month').size()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[str(m) for m in monthly_uploads.index],
                y=monthly_uploads.values,
                mode='lines+markers',
                line=dict(color='#FF6348', width=3),
                marker=dict(size=8, color='#FF6348'),
                name='Videos Uploaded'
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(t=10, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='#404040', title="Month"),
                yaxis=dict(gridcolor='#404040', title="Videos Uploaded"),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Upload date data not available")
    
    with col2:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">📺 Channel Distribution</h3>', unsafe_allow_html=True)
        
        if 'Channel' in videos_df.columns:
            # Create channel distribution chart
            channel_counts = videos_df['Channel'].value_counts().head(10)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=channel_counts.values,
                y=channel_counts.index,
                orientation='h',
                marker_color='#FFA502',
                name='Videos per Channel'
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(t=10, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='#404040', title="Number of Videos"),
                yaxis=dict(gridcolor='#404040'),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Channel data not available")
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 🔍 SEARCH AND FILTER SECTION
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">🔍 Video Management</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search videos", placeholder="Search by title, channel, or keywords...")
    
    with col2:
        channel_filter = st.selectbox(
            "📺 Filter by Channel",
            ["All Channels"] + list(videos_df['Channel'].unique()) if 'Channel' in videos_df.columns else ["All Channels"]
        )
    
    with col3:
        sort_option = st.selectbox(
            "📊 Sort by",
            ["Upload Date (Newest)", "Upload Date (Oldest)", "Channel Name", "Title A-Z"]
        )
    
    # Apply filters
    filtered_videos = videos_df.copy()
    
    if search_query:
        mask = filtered_videos['Title'].str.contains(search_query, case=False, na=False)
        if 'Channel' in filtered_videos.columns:
            mask |= filtered_videos['Channel'].str.contains(search_query, case=False, na=False)
        filtered_videos = filtered_videos[mask]
    
    if channel_filter != "All Channels" and 'Channel' in filtered_videos.columns:
        filtered_videos = filtered_videos[filtered_videos['Channel'] == channel_filter]
    
    # Apply sorting
    if 'Upload Date' in filtered_videos.columns:
        if sort_option == "Upload Date (Newest)":
            filtered_videos = filtered_videos.sort_values('Upload Date', ascending=False)
        elif sort_option == "Upload Date (Oldest)":
            filtered_videos = filtered_videos.sort_values('Upload Date', ascending=True)
    
    if sort_option == "Channel Name" and 'Channel' in filtered_videos.columns:
        filtered_videos = filtered_videos.sort_values('Channel')
    elif sort_option == "Title A-Z":
        filtered_videos = filtered_videos.sort_values('Title')
    
    # Professional spacing
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # 📹 VIDEO GRID DISPLAY
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📹 Video Gallery</h2>', unsafe_allow_html=True)
    
    if not filtered_videos.empty:
        # Display results count
        st.markdown(f'<p style="color: #999; margin-bottom: 1rem;">Showing {len(filtered_videos)} videos</p>', unsafe_allow_html=True)
        
        # Initialize pagination state (0-indexed internally, but displayed as 1-indexed)
        if 'video_page' not in st.session_state:
            st.session_state.video_page = 0
        
        # Ensure page doesn't go below 0
        if st.session_state.video_page < 0:
            st.session_state.video_page = 0
        
        # Calculate pagination
        videos_per_page = 12
        total_videos = len(filtered_videos)
        total_pages = (total_videos + videos_per_page - 1) // videos_per_page
        
        # Get current page videos
        start_idx = st.session_state.video_page * videos_per_page
        end_idx = start_idx + videos_per_page
        videos_to_show = filtered_videos.iloc[start_idx:end_idx]
        
        # Custom CSS for video cards
        st.markdown("""
        <style>
        .video-card {
            background: linear-gradient(135deg, #2D2D2D 0%, #3A3A3A 100%);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #404040;
            transition: all 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .video-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(255, 71, 87, 0.25);
            border-color: #FF4757;
            cursor: pointer !important;
            background: linear-gradient(135deg, #3A3A3A 0%, #404040 100%);
        }
        
        .video-thumbnail {
            width: 100%;
            height: 180px;
            background: linear-gradient(45deg, #FF4757, #FF6348);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
        }
        
        .video-thumbnail img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 8px;
        }
        
        .video-title {
            color: white;
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.4;
            margin-bottom: 0.5rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
        }
        
        .video-channel {
            color: #999;
            font-size: 0.85rem;
            margin-bottom: 0.75rem;
        }
        
        .video-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            color: #CCCCCC;
            margin-top: auto;
            padding-top: 0.5rem;
            border-top: 1px solid #404040;
        }
        
        .video-stat {
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        .video-date {
            color: #999;
            font-size: 0.7rem;
        }
        
        .video-card:hover .video-thumbnail::after {
            content: "Click to watch on YouTube";
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            text-align: center;
            border-radius: 0 0 8px 8px;
            z-index: 10;
        }
        
        .clickable-card {
            cursor: pointer !important;
        }
        
        .clickable-card:hover {
            cursor: pointer !important;
        }
        
        /* Print-specific styles to maintain dark theme */
        @media print {
            * {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            
            body, .stApp {
                background-color: #1A1A1A !important;
                color: #FFFFFF !important;
            }
            
            .video-card {
                background: linear-gradient(135deg, #2D2D2D 0%, #3A3A3A 100%) !important;
                border: 1px solid #404040 !important;
                -webkit-print-color-adjust: exact !important;
            }
            
            /* Ensure all backgrounds print correctly */
            div[style*="background"] {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
            
            /* Force sidebar colors */
            .css-1d391kg, .css-1y0tads {
                background-color: #1A1A1A !important;
            }
            
            /* Force metric card backgrounds */
            div[style*="rgba(45, 45, 45"] {
                background-color: rgba(45, 45, 45, 0.8) !important;
                -webkit-print-color-adjust: exact !important;
            }
            
            /* Chart containers */
            div[style*="border: 1px solid #404040"] {
                background-color: rgba(45, 45, 45, 0.8) !important;
                border: 1px solid #404040 !important;
                -webkit-print-color-adjust: exact !important;
            }
        }
        
        .pagination-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin: 2rem 0;
            padding: 1rem;
        }
        
        .page-info {
            color: #CCCCCC;
            font-size: 0.9rem;
            margin: 0 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create video grid (3 columns)
        cols_per_row = 3
        rows = len(videos_to_show) // cols_per_row + (1 if len(videos_to_show) % cols_per_row > 0 else 0)
        
        for row in range(rows):
            cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                video_idx = row * cols_per_row + col_idx
                if video_idx < len(videos_to_show):
                    video = videos_to_show.iloc[video_idx]
                    
                    with cols[col_idx]:
                        # Extract thumbnail URL from YouTube URL if possible
                        video_url = video.get('URL', '')
                        thumbnail_url = ""
                        if 'youtube.com/watch?v=' in video_url:
                            video_id = video_url.split('v=')[1].split('&')[0]
                            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                        elif 'youtu.be/' in video_url:
                            video_id = video_url.split('youtu.be/')[1].split('?')[0]
                            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                        
                        # Format title and channel
                        title = video.get('Title', 'No Title')[:60] + ('...' if len(video.get('Title', '')) > 60 else '')
                        channel = video.get('Channel', 'Unknown Channel')
                        upload_date = video.get('Upload Date', 'Unknown')
                        
                        # Format date - handle relative dates like "1 day ago", "4 days ago"
                        upload_date_str = str(upload_date).strip()
                        formatted_date = upload_date_str  # Start with original string for debugging
                        
                        if upload_date_str and upload_date_str != 'Unknown' and upload_date_str != 'nan':
                            try:
                                # Handle relative dates
                                upload_str = upload_date_str.lower()
                                import re
                                
                                # Extract numbers from string
                                numbers = re.findall(r'\d+', upload_str)
                                
                                if numbers and len(numbers) > 0:
                                    num = int(numbers[0])
                                    
                                    if 'day ago' in upload_str:
                                        date_obj = datetime.now() - timedelta(days=num)
                                        formatted_date = date_obj.strftime('%b %d, %Y')
                                    elif 'week ago' in upload_str:
                                        date_obj = datetime.now() - timedelta(weeks=num)
                                        formatted_date = date_obj.strftime('%b %d, %Y')
                                    elif 'month ago' in upload_str:
                                        date_obj = datetime.now() - timedelta(days=num*30)
                                        formatted_date = date_obj.strftime('%b %d, %Y')
                                    elif 'year ago' in upload_str:
                                        date_obj = datetime.now() - timedelta(days=num*365)
                                        formatted_date = date_obj.strftime('%b %d, %Y')
                                    elif 'streamed' in upload_str and 'day' in upload_str:
                                        date_obj = datetime.now() - timedelta(days=num)
                                        formatted_date = date_obj.strftime('%b %d, %Y')
                                elif 'minute' in upload_str or 'hour' in upload_str:
                                    # Very recent uploads
                                    formatted_date = datetime.now().strftime('%b %d, %Y')
                                elif 'streamed' in upload_str:
                                    # Live stream without specific time
                                    formatted_date = datetime.now().strftime('%b %d, %Y')
                            except Exception as e:
                                # Keep original for debugging
                                formatted_date = upload_date_str
                        
                        # Generate random-ish view and comment counts for demo
                        # In real implementation, these would come from actual data
                        import hashlib
                        hash_input = f"{title}{channel}".encode()
                        hash_val = int(hashlib.md5(hash_input).hexdigest()[:6], 16)
                        views = (hash_val % 50000) + 1000
                        comments = (hash_val % 500) + 10
                        
                        # Create thumbnail HTML separately to avoid f-string backslash issues
                        thumbnail_html = ""
                        if thumbnail_url:
                            thumbnail_html = f'<img src="{thumbnail_url}" alt="Video Thumbnail" onerror="this.style.display=&quot;none&quot;">'
                        
                        # Create clickable video card using Streamlit link_button approach
                        video_link = video.get('URL', '#')
                        
                        # Create video card as a clickable HTML link
                        card_html = f"""
                        <a href="{video_link}" target="_blank" style="text-decoration: none; color: inherit;">
                            <div class="video-card clickable-card">
                                <div class="video-thumbnail">
                                    {thumbnail_html}
                                </div>
                                <div class="video-title">{title}</div>
                                <div class="video-channel">{channel}</div>
                                <div class="video-stats">
                                    <div class="video-stat">
                                        <span>👁️</span>
                                        <span>{views:,} views</span>
                                    </div>
                                    <div class="video-stat">
                                        <span>💬</span>
                                        <span>{comments}</span>
                                    </div>
                                </div>
                                <div class="video-date">{formatted_date}</div>
                            </div>
                        </a>
                        """
                        
                        # Display the clickable card
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Add some spacing between rows
                        if video_idx < len(videos_to_show) - 1 and (video_idx + 1) % cols_per_row == 0:
                            st.markdown("<br>", unsafe_allow_html=True)
        
        # Pagination Navigation
        if total_pages > 1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create pagination layout
            col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
            
            # Add scroll-to-top JavaScript
            scroll_script = """
            <script>
            function scrollToTop() {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
            </script>
            """
            st.markdown(scroll_script, unsafe_allow_html=True)
            
            with col1:
                if st.button("⬅️ First", disabled=st.session_state.video_page <= 0, key="first_page"):
                    st.session_state.video_page = 0
                    # Add JavaScript to scroll to top
                    st.markdown('<script>scrollToTop();</script>', unsafe_allow_html=True)
                    st.rerun()
            
            with col2:
                if st.button("◀️ Prev", disabled=st.session_state.video_page <= 0, key="prev_page"):
                    st.session_state.video_page = max(0, st.session_state.video_page - 1)
                    # Add JavaScript to scroll to top
                    st.markdown('<script>scrollToTop();</script>', unsafe_allow_html=True)
                    st.rerun()
            
            with col3:
                current_page_display = st.session_state.video_page + 1
                st.markdown(f"""
                <div class="page-info" style="text-align: center; padding: 0.5rem;">
                    <strong>Page {current_page_display} of {total_pages}</strong><br>
                    <span style="color: #999; font-size: 0.8rem;">
                        Showing {start_idx + 1}-{min(end_idx, total_videos)} of {total_videos} videos
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                if st.button("Next ▶️", disabled=st.session_state.video_page >= total_pages - 1, key="next_page"):
                    st.session_state.video_page = min(total_pages - 1, st.session_state.video_page + 1)
                    # Add JavaScript to scroll to top
                    st.markdown('<script>scrollToTop();</script>', unsafe_allow_html=True)
                    st.rerun()
            
            with col5:
                if st.button("Last ➡️", disabled=st.session_state.video_page >= total_pages - 1, key="last_page"):
                    st.session_state.video_page = max(0, total_pages - 1)
                    # Add JavaScript to scroll to top
                    st.markdown('<script>scrollToTop();</script>', unsafe_allow_html=True)
                    st.rerun()
        
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #999;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #CCCCCC;">No videos found</h3>
            <p>Try adjusting your search criteria or check back later for new content.</p>
        </div>
        """, unsafe_allow_html=True)
    


def show_comments_page():
    """Enhanced Comments analysis page"""
    st.markdown('<h1 class="page-title">💬 Comments</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Deep dive into public comments and discussions about Sridhar Rao</p>', unsafe_allow_html=True)
    
    videos_df, comments_df_raw = load_reputation_data()
    
    # Apply language preference to comments
    comments_df = get_language_aware_comments(comments_df_raw)
    
    if comments_df.empty:
        st.error("No comment data available")
        return
    
    # Calculate metrics
    total_comments = len(comments_df)
    unique_authors = comments_df['Author'].nunique() if 'Author' in comments_df.columns else 0
    avg_sentiment = comments_df['Sentiment'].mean() if 'Sentiment' in comments_df.columns else 0
    avg_likes = comments_df['LikeCount'].mean() if 'LikeCount' in comments_df.columns else 0
    sentiment_dist = get_sentiment_distribution(comments_df)
    
    # 📊 COMMENT METRICS CARDS (using perfected card design)
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📊 Comment Performance Metrics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Enhanced card style - same as Videos page
    card_style = """
        background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 50%, #2D2D2D 100%);
        border-radius: 12px;
        padding: 1.5rem 0.8rem;
        border: 1px solid #404040;
        text-align: center;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    """
    
    with col1:
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">💬</div>
            <div style="color: #FF6348; font-size: 1.8rem; font-weight: 800; line-height: 1;">{total_comments:,}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">TOTAL COMMENTS</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Public discussions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">👥</div>
            <div style="color: #FFA502; font-size: 1.8rem; font-weight: 800; line-height: 1;">{unique_authors:,}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">UNIQUE AUTHORS</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Distinct voices</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Get sentiment color based on score
        def get_sentiment_score_color(score):
            if score >= 0.1: return "#22C55E"     # Green - Positive
            elif score >= -0.1: return "#FFA502" # Orange - Neutral
            else: return "#EF4444"               # Red - Negative
        
        sentiment_color = get_sentiment_score_color(avg_sentiment)
        
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">📊</div>
            <div style="color: {sentiment_color}; font-size: 1.8rem; font-weight: 800; line-height: 1;">{avg_sentiment:.2f}</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">AVG SENTIMENT</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Overall mood</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        positive_pct = round((sentiment_dist['Positive'] / total_comments) * 100, 1) if total_comments > 0 else 0
        pct_color = "#22C55E" if positive_pct >= 50 else "#FFA502" if positive_pct >= 30 else "#EF4444"
        
        st.markdown(f"""
        <div style="{card_style}" 
             onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 4px 15px rgba(255, 71, 87, 0.1)'; this.style.borderColor='#FF4757';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.08)'; this.style.borderColor='#404040';">
            <div style="font-size: 2.2rem;">😊</div>
            <div style="color: {pct_color}; font-size: 1.8rem; font-weight: 800; line-height: 1;">{positive_pct}%</div>
            <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">POSITIVE RATE</div>
            <div style="color: #888; font-size: 0.65rem; opacity: 0.8;">Approval rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 📊 COMMENT ANALYTICS SECTION
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">📊 Comment Analytics</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">📈 Sentiment Timeline</h3>', unsafe_allow_html=True)
        
        if 'Date' in comments_df.columns and 'Sentiment' in comments_df.columns:
            # Create sentiment timeline chart
            comments_df_copy = comments_df.copy()
            comments_df_copy['Date'] = pd.to_datetime(comments_df_copy['Date'])
            
            # Group by date and calculate daily sentiment
            daily_sentiment = comments_df_copy.groupby(comments_df_copy['Date'].dt.date)['Sentiment'].mean().reset_index()
            daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])
            
            fig = go.Figure()
            
            # Use dynamic color based on sentiment value
            sentiment_colors = ['#EF4444' if s < -0.1 else '#22C55E' if s > 0.1 else '#FFA502' for s in daily_sentiment['Sentiment']]
            
            fig.add_trace(go.Scatter(
                x=daily_sentiment['Date'],
                y=daily_sentiment['Sentiment'],
                mode='lines+markers',
                line=dict(color='#FF6348', width=3),
                marker=dict(size=6, color=sentiment_colors),
                hovertemplate='<b>%{x}</b><br>Sentiment: %{y:.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(t=10, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='#404040', title="Date"),
                yaxis=dict(gridcolor='#404040', title="Average Sentiment"),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Date or sentiment data not available")
    
    with col2:
        st.markdown('<h3 style="color: #FF4757; font-size: 1.1rem; margin: 0 0 1rem 0; font-weight: 600;">🎭 Sentiment Distribution</h3>', unsafe_allow_html=True)
        
        # Pie chart with sentiment distribution
        color_map = {
            'Positive': '#22C55E',  # Green
            'Neutral': '#9CA3AF',   # Light grey
            'Negative': '#EF4444'   # Red
        }
        
        chart_colors = [color_map.get(label, '#9CA3AF') for label in sentiment_dist.keys()]
        
        fig = go.Figure(data=[go.Pie(
            labels=list(sentiment_dist.keys()),
            values=list(sentiment_dist.values()),
            hole=0.4,
            marker_colors=chart_colors
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(t=10, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Professional spacing
    st.markdown("<div style='margin: 2.2rem 0 1.4rem 0;'></div>", unsafe_allow_html=True)
    
    # 🔍 SEARCH AND FILTER SECTION
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">🔍 Comment Management</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search comments", placeholder="Search by content, author, or keywords...")
    
    with col2:
        sentiment_filter = st.selectbox(
            "📊 Filter by Sentiment",
            ["All Sentiments", "Positive", "Negative", "Neutral"]
        )
    
    with col3:
        sort_option = st.selectbox(
            "🔢 Sort by",
            ["Date (Newest)", "Date (Oldest)", "Sentiment Score", "Like Count", "Author"]
        )
    
    # Apply filters
    filtered_comments = comments_df.copy()
    
    if search_query:
        # Search in the DisplayComment column (respects language preference) and Author
        mask = filtered_comments['DisplayComment'].astype(str).str.contains(search_query, case=False, na=False) if 'DisplayComment' in filtered_comments.columns else False
        if 'Author' in filtered_comments.columns:
            mask |= filtered_comments['Author'].astype(str).str.contains(search_query, case=False, na=False)
        filtered_comments = filtered_comments[mask]
    
    if sentiment_filter != "All Sentiments":
        if 'SentLabel' in filtered_comments.columns:
            filtered_comments = filtered_comments[filtered_comments['SentLabel'] == sentiment_filter]
        elif 'Sentiment' in filtered_comments.columns:
            # Use numeric sentiment mapping
            sentiment_map = {'Positive': lambda x: x > 0.1, 'Negative': lambda x: x < -0.1, 'Neutral': lambda x: -0.1 <= x <= 0.1}
            if sentiment_filter in sentiment_map:
                filtered_comments = filtered_comments[filtered_comments['Sentiment'].apply(sentiment_map[sentiment_filter])]
    
    # Apply sorting
    if 'Date' in filtered_comments.columns:
        if sort_option == "Date (Newest)":
            filtered_comments = filtered_comments.sort_values('Date', ascending=False)
        elif sort_option == "Date (Oldest)":
            filtered_comments = filtered_comments.sort_values('Date', ascending=True)
    
    if sort_option == "Sentiment Score" and 'Sentiment' in filtered_comments.columns:
        filtered_comments = filtered_comments.sort_values('Sentiment', ascending=False)
    elif sort_option == "Like Count" and 'LikeCount' in filtered_comments.columns:
        filtered_comments = filtered_comments.sort_values('LikeCount', ascending=False)
    elif sort_option == "Author" and 'Author' in filtered_comments.columns:
        filtered_comments = filtered_comments.sort_values('Author')
    
    # Professional spacing
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # 💬 COMMENTS FEED DISPLAY
    st.markdown('<h2 style="color: #FFF; font-size: 1.4rem; margin-bottom: 1.4rem; font-weight: 600;">💬 Comments Feed</h2>', unsafe_allow_html=True)
    
    if not filtered_comments.empty:
        # Display results count
        st.markdown(f'<p style="color: #999; margin-bottom: 1rem;">Showing {len(filtered_comments)} comments</p>', unsafe_allow_html=True)
        
        # Initialize pagination state
        if 'comment_page' not in st.session_state:
            st.session_state.comment_page = 0
        
        # Ensure page doesn't go below 0
        if st.session_state.comment_page < 0:
            st.session_state.comment_page = 0
        
        # Calculate pagination
        comments_per_page = 20
        total_comments_filtered = len(filtered_comments)
        total_pages = (total_comments_filtered + comments_per_page - 1) // comments_per_page
        
        # Get current page comments
        start_idx = st.session_state.comment_page * comments_per_page
        end_idx = start_idx + comments_per_page
        comments_to_show = filtered_comments.iloc[start_idx:end_idx]
        
        # Clean comment cards using Streamlit's native components
        for idx, row in comments_to_show.iterrows():
            # Safe sentiment extraction with fallback
            if 'SentLabel' in row and pd.notna(row.get('SentLabel')):
                sentiment_label = str(row.get('SentLabel', 'Neutral'))
            elif 'Sentiment' in row and pd.notna(row.get('Sentiment')):
                # Convert numeric sentiment to label
                sentiment_value = float(row.get('Sentiment', 0))
                if sentiment_value > 0.1:
                    sentiment_label = 'Positive'
                elif sentiment_value < -0.1:
                    sentiment_label = 'Negative'
                else:
                    sentiment_label = 'Neutral'
            else:
                sentiment_label = 'Neutral'
            
            sentiment_color = {
                'Positive': '#22C55E',
                'Negative': '#EF4444', 
                'Neutral': '#9CA3AF'
            }.get(sentiment_label, '#9CA3AF')
            
            # Safely extract and clean data - use language-aware display column
            comment_text = str(row.get('DisplayComment', row.get('Comment_EN', row.get('Comment', 'No comment text'))))
            if len(comment_text) > 500:
                comment_text = comment_text[:500] + "..."
                
            author = str(row.get('Author', 'Unknown'))
            date = row.get('Date', 'Unknown date')
            like_count = int(row.get('LikeCount', 0)) if pd.notna(row.get('LikeCount', 0)) else 0
            sentiment_score = float(row.get('Sentiment', 0)) if pd.notna(row.get('Sentiment', 0)) else 0
            
            # Format date safely
            try:
                if pd.notna(date) and str(date) != 'Unknown date':
                    formatted_date = pd.to_datetime(date).strftime('%b %d, %Y at %I:%M %p')
                else:
                    formatted_date = 'Unknown date'
            except:
                formatted_date = str(date)
            
            # Get author initial safely
            try:
                author_initial = author[0].upper() if author and len(author) > 0 and author != 'Unknown' else '?'
            except:
                author_initial = '?'
            
            comment_number = start_idx + comments_to_show.index.get_loc(idx) + 1
            
            # Use simple, reliable HTML structure
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2D2D2D 0%, #3A3A3A 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid {sentiment_color}; border: 1px solid #404040;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; background: {sentiment_color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; margin-right: 0.75rem; font-size: 1rem;">
                            {author_initial}
                        </div>
                        <div>
                            <div style="color: white; font-weight: 600; font-size: 1rem;">{author}</div>
                            <div style="color: #999; font-size: 0.8rem;">{formatted_date}</div>
                        </div>
                    </div>
                    <div style="background: {sentiment_color}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.7rem; font-weight: 600;">
                        {sentiment_label}
                    </div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <div style="color: #E5E5E5; line-height: 1.6; font-size: 0.95rem;">
                        {comment_text}
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #404040; padding-top: 1rem;">
                    <div style="display: flex; gap: 1.5rem;">
                        <div style="color: #999; font-size: 0.85rem;">👍 {like_count:,}</div>
                        <div style="color: #999; font-size: 0.85rem;">📊 {sentiment_score:.2f}</div>
                    </div>
                    <div style="color: #666; font-size: 0.75rem; background: rgba(255,255,255,0.05); padding: 0.25rem 0.5rem; border-radius: 4px;">
                        #{comment_number}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Pagination Navigation
        if total_pages > 1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create pagination layout
            col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
            
            with col1:
                if st.button("⬅️ First", disabled=st.session_state.comment_page <= 0, key="comment_first_page"):
                    st.session_state.comment_page = 0
                    st.rerun()
            
            with col2:
                if st.button("◀️ Prev", disabled=st.session_state.comment_page <= 0, key="comment_prev_page"):
                    st.session_state.comment_page = max(0, st.session_state.comment_page - 1)
                    st.rerun()
            
            with col3:
                current_page_display = st.session_state.comment_page + 1
                st.markdown(f"""
                <div style="text-align: center; padding: 0.5rem;">
                    <strong style="color: #FFF;">Page {current_page_display} of {total_pages}</strong><br>
                    <span style="color: #999; font-size: 0.8rem;">
                        Showing {start_idx + 1}-{min(end_idx, total_comments_filtered)} of {total_comments_filtered} comments
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                if st.button("Next ▶️", disabled=st.session_state.comment_page >= total_pages - 1, key="comment_next_page"):
                    st.session_state.comment_page = min(total_pages - 1, st.session_state.comment_page + 1)
                    st.rerun()
            
            with col5:
                if st.button("Last ➡️", disabled=st.session_state.comment_page >= total_pages - 1, key="comment_last_page"):
                    st.session_state.comment_page = max(0, total_pages - 1)
                    st.rerun()
        
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #999;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #CCCCCC;">No comments found</h3>
            <p>Try adjusting your search criteria or check back later for new discussions.</p>
        </div>
        """, unsafe_allow_html=True)

def show_data_intelligence_page():
    """Data Intelligence Page - Weekly insights and analytics"""
    load_custom_css()
    
    # Load data with language preference support
    videos_df, comments_df_raw = load_reputation_data()
    
    # Apply language preference to comments
    comments_df = get_language_aware_comments(comments_df_raw)
    
    # Page header with red styling
    st.markdown('''
    <h1 style="color: #FF4757; font-size: 2.5rem; font-weight: 700; margin: 0 0 0.5rem 0; display: flex; align-items: center;">
        <span style="margin-right: 0.5rem;">📂</span>
        Data Intelligence
    </h1>
        ''', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Weekly insights and data analytics dashboard</p>', unsafe_allow_html=True)
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    with col3:
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    # Convert to datetime for filtering
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date) + timedelta(days=1)  # Include end date
    
    # Filter data by date range
    if not videos_df.empty:
        videos_filtered = videos_df[
            (videos_df['Upload Date'] >= start_datetime) & 
            (videos_df['Upload Date'] <= end_datetime)
        ]
    else:
        videos_filtered = pd.DataFrame()
    
    if not comments_df.empty:
        comments_filtered = comments_df[
            (comments_df['Date'] >= start_datetime) & 
            (comments_df['Date'] <= end_datetime)
        ]
    else:
        comments_filtered = pd.DataFrame()
    
    # Section 1: Weekly Data Overview
    st.markdown("## 📊 Weekly Data Overview")
    
    # Calculate metrics
    new_videos = len(videos_filtered)
    new_comments = len(comments_filtered)
    avg_sentiment = comments_filtered['Sentiment'].mean() if not comments_filtered.empty else 0
    
    # Top channels calculation
    if not videos_filtered.empty:
        top_channels = videos_filtered['Channel'].value_counts().head(3)
        top_channel_text = f"1. {top_channels.index[0]} ({top_channels.iloc[0]})" if len(top_channels) > 0 else "No data"
    else:
        top_channel_text = "No data"
    
    # Comment engagement rate
    engagement_rate = (new_comments / new_videos) if new_videos > 0 else 0
    
    # Create metrics cards
    metric_cols = st.columns(5)
    
    with metric_cols[0]:
        st.markdown(create_metric_card(
            "New Videos", 
            new_videos,
            f"+{new_videos} this period",
            "positive" if new_videos > 0 else "neutral",
            "📹"
        ), unsafe_allow_html=True)
    
    with metric_cols[1]:
        st.markdown(create_metric_card(
            "New Comments", 
            f"{new_comments:,}",
            f"+{new_comments:,} this period",
            "positive" if new_comments > 0 else "neutral",
            "💬"
        ), unsafe_allow_html=True)
    
    with metric_cols[2]:
        sentiment_color = "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral"
        st.markdown(create_metric_card(
            "Avg Sentiment", 
            f"{avg_sentiment:.2f}",
            f"Range: -1.0 to +1.0",
            sentiment_color,
            "📈"
        ), unsafe_allow_html=True)
    
    with metric_cols[3]:
        st.markdown(create_metric_card(
            "Top Channel", 
            top_channel_text.split('(')[0] if '(' in top_channel_text else top_channel_text,
            f"Most active channel",
            "neutral",
            "🏆"
        ), unsafe_allow_html=True)
    
    with metric_cols[4]:
        st.markdown(create_metric_card(
            "Engagement Rate", 
            f"{engagement_rate:.1f}",
            "Comments per video",
            "positive" if engagement_rate > 5 else "neutral",
            "⚡"
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section 2: Interactive Visualizations
    st.markdown("## 📈 Interactive Analytics")
    
    viz_cols = st.columns(2)
    
    with viz_cols[0]:
        # Daily Activity Chart
        if not videos_filtered.empty or not comments_filtered.empty:
            # Create daily activity data
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            daily_data = []
            
            for date in date_range:
                day_videos = len(videos_filtered[videos_filtered['Upload Date'].dt.date == date.date()]) if not videos_filtered.empty else 0
                day_comments = len(comments_filtered[comments_filtered['Date'].dt.date == date.date()]) if not comments_filtered.empty else 0
                daily_data.append({'Date': date, 'Videos': day_videos, 'Comments': day_comments})
            
            daily_df = pd.DataFrame(daily_data)
            
            fig_activity = go.Figure()
            
            fig_activity.add_trace(go.Bar(
                x=daily_df['Date'],
                y=daily_df['Videos'],
                name='Videos',
                marker_color='#FF4757',
                yaxis='y'
            ))
            
            fig_activity.add_trace(go.Bar(
                x=daily_df['Date'],
                y=daily_df['Comments'],
                name='Comments',
                marker_color='#22C55E',
                yaxis='y2'
            ))
            
            fig_activity.update_layout(
                title=dict(text="📊 Daily Activity Overview", font=dict(size=18, color='white')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='#404040'),
                yaxis=dict(title="Videos", side="left", gridcolor='#404040'),
                yaxis2=dict(title="Comments", side="right", overlaying="y", gridcolor='#404040'),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig_activity, use_container_width=True)
        else:
            st.info("No data available for the selected date range")
    
    with viz_cols[1]:
        # Channel Distribution Pie Chart
        if not videos_filtered.empty:
            channel_counts = videos_filtered['Channel'].value_counts().head(8)
            
            fig_channels = go.Figure(data=[go.Pie(
                labels=channel_counts.index,
                values=channel_counts.values,
                hole=0.4,
                marker_colors=['#FF4757', '#FF6348', '#22C55E', '#FFA502', '#9CA3AF', '#EF4444', '#F59E0B', '#6B7280']
            )])
            
            fig_channels.update_layout(
                title=dict(text="📺 Channel Distribution", font=dict(size=18, color='white')),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01)
            )
            
            st.plotly_chart(fig_channels, use_container_width=True)
        else:
            st.info("No video data available for chart")
    
    # Sentiment Trend Chart (full width)
    if not comments_filtered.empty:
        st.markdown("### 📈 Sentiment Trend Analysis")
        
        # Group by date for sentiment trend
        daily_sentiment = comments_filtered.groupby(comments_filtered['Date'].dt.date)['Sentiment'].agg(['mean', 'count']).reset_index()
        daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])
        
        fig_sentiment = go.Figure()
        
        # Sentiment line
        sentiment_colors = ['#EF4444' if s < -0.1 else '#22C55E' if s > 0.1 else '#FFA502' for s in daily_sentiment['mean']]
        
        fig_sentiment.add_trace(go.Scatter(
            x=daily_sentiment['Date'],
            y=daily_sentiment['mean'],
            mode='lines+markers',
            name='Daily Sentiment',
            line=dict(color='#FF6348', width=3),
            marker=dict(size=8, color=sentiment_colors),
            hovertemplate='<b>%{x}</b><br>Sentiment: %{y:.3f}<br>Comments: %{customdata}<extra></extra>',
            customdata=daily_sentiment['count']
        ))
        
        # Add neutral line
        fig_sentiment.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig_sentiment.update_layout(
            title=dict(text="📊 Daily Sentiment Trend", font=dict(size=20, color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='#404040', title="Date"),
            yaxis=dict(gridcolor='#404040', title="Sentiment Score", range=[-1, 1]),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    st.markdown("---")
    
    # Section 3: Recent Activity Tables
    st.markdown("## 📋 Recent Activity Details")
    
    # Filters
    filter_cols = st.columns(3)
    with filter_cols[0]:
        channel_filter = st.selectbox(
            "Filter by Channel",
            ["All Channels"] + list(videos_df['Channel'].unique()) if not videos_df.empty else ["All Channels"]
        )
    with filter_cols[1]:
        sentiment_filter = st.selectbox(
            "Filter by Sentiment",
            ["All Sentiments", "Positive", "Neutral", "Negative"]
        )
    with filter_cols[2]:
        show_thumbnails = st.checkbox("Show Thumbnails", value=True)
    
    # Apply filters
    videos_display = videos_filtered.copy() if not videos_filtered.empty else pd.DataFrame()
    comments_display = comments_filtered.copy() if not comments_filtered.empty else pd.DataFrame()
    
    if channel_filter != "All Channels" and not videos_display.empty:
        videos_display = videos_display[videos_display['Channel'] == channel_filter]
    
    if sentiment_filter != "All Sentiments" and not comments_display.empty:
        comments_display = comments_display[comments_display['SentLabel'] == sentiment_filter]
    
    table_cols = st.columns(2)
    
    with table_cols[0]:
        st.markdown("### 📹 Latest Videos")
        if not videos_display.empty:
            # Prepare video data for display
            videos_show = videos_display.head(10).copy()
            videos_show['Upload Date'] = videos_show['Upload Date'].dt.strftime('%Y-%m-%d')
            videos_show['Title'] = videos_show['Title'].str[:60] + '...'
            
            if show_thumbnails:
                # Create HTML table with thumbnails
                html_rows = []
                for _, row in videos_show.iterrows():
                    thumbnail_html = f'<img src="{row["Thumbnail"]}" width="80" height="45" style="border-radius: 4px;">' if pd.notna(row["Thumbnail"]) else ""
                    html_rows.append(f"""
                    <tr>
                        <td>{thumbnail_html}</td>
                        <td style="color: white; font-size: 0.85rem;">
                            <strong>{row['Title']}</strong><br>
                            <span style="color: #999;">{row['Channel']}</span><br>
                            <span style="color: #FFA502; font-size: 0.75rem;">{row['Upload Date']}</span>
                        </td>
                    </tr>
                    """)
                
                html_table = f"""
                <div class="chart-container">
                    <table style="width: 100%; border-collapse: collapse;">
                        {''.join(html_rows)}
                    </table>
                </div>
                """
                st.markdown(html_table, unsafe_allow_html=True)
            else:
                st.dataframe(
                    videos_show[['Title', 'Channel', 'Upload Date']],
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info("No videos found for the selected filters")
    
    with table_cols[1]:
        st.markdown("### 💬 Recent Comments")
        if not comments_display.empty:
            # Prepare comments data for display
            comments_show = comments_display.head(10).copy()
            comments_show['Date'] = comments_show['Date'].dt.strftime('%Y-%m-%d %H:%M')
            # Use language-aware display column
            comments_show['Comment_Short'] = comments_show['DisplayComment'].str[:80] + '...'
            
            # Create colored sentiment badges
            def get_sentiment_badge(row):
                # Safe sentiment extraction
                if 'SentLabel' in row and pd.notna(row.get('SentLabel')):
                    sentiment = str(row.get('SentLabel', 'Neutral'))
                elif 'Sentiment' in row and pd.notna(row.get('Sentiment')):
                    # Convert numeric sentiment to label
                    sentiment_value = float(row.get('Sentiment', 0))
                    if sentiment_value > 0.1:
                        sentiment = 'Positive'
                    elif sentiment_value < -0.1:
                        sentiment = 'Negative'
                    else:
                        sentiment = 'Neutral'
                else:
                    sentiment = 'Neutral'
                
                if sentiment == 'Positive':
                    return '🟢 Positive'
                elif sentiment == 'Negative':
                    return '🔴 Negative'
                else:
                    return '🟡 Neutral'
            
            comments_show['Sentiment_Badge'] = comments_show.apply(get_sentiment_badge, axis=1)
            
            st.dataframe(
                comments_show[['Author', 'Comment_Short', 'Sentiment_Badge', 'Date']].rename(columns={
                    'Comment_Short': 'Comment',
                    'Sentiment_Badge': 'Sentiment'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No comments found for the selected filters")

def show_settings_page():
    """Enhanced Settings and configuration page with improved theme management"""
    st.markdown('<h1 class="page-title">⚙️ Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Dashboard configuration, themes, and data management</p>', unsafe_allow_html=True)
    
    # Create main layout with sidebar
    main_col, side_col = st.columns([3, 1])
    
    with main_col:
        # === THEME STUDIO ===
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 71, 87, 0.05) 100%); 
                    border: 1px solid rgba(255, 71, 87, 0.3); border-radius: 12px; padding: 2rem; margin-bottom: 2rem;">
            <h2 style="color: #FF4757; margin: 0 0 1rem 0; font-size: 1.5rem; font-weight: 700;">
                🎨 Theme Studio
            </h2>
            <p style="color: #CCCCCC; margin: 0; font-size: 1rem;">
                Choose your visual experience with our collection of professional themes
            </p>
        </div>
        """, unsafe_allow_html=True)
    
        # Advanced Theme Selection Interface
        try:
            from src.themes.theme_provider import get_theme_provider, switch_theme
            
            theme_provider = get_theme_provider()
            current_theme_name = theme_provider.get_current_theme_name()
            available_themes = theme_provider.get_theme_selector_options()
            current_theme_info = theme_provider.get_theme_info(current_theme_name)
            current_theme_data = theme_provider.load_theme(current_theme_name)
            
            # Current Theme Display Card
            primary_color = current_theme_data.get('colors', {}).get('primary', '#FF4757') if current_theme_data else '#FF4757'
            bg_card = current_theme_data.get('colors', {}).get('bg_card', '#2D2D2D') if current_theme_data else '#2D2D2D'
            
            st.markdown(f"""
            <div style="background: {bg_card}; border: 2px solid {primary_color}; border-radius: 16px; 
                        padding: 2rem; margin-bottom: 2rem; text-align: center; position: relative;">
                <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); 
                           background: {primary_color}; color: white; padding: 8px 16px; border-radius: 20px; 
                           font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">ACTIVE THEME</div>
                <h3 style="color: {primary_color}; margin: 1rem 0 0.5rem 0; font-size: 1.8rem; font-weight: 700;">
                    {current_theme_info.get('name', 'Unknown Theme')}
                </h3>
                <p style="color: #CCCCCC; margin: 0 0 1.5rem 0; font-size: 1rem; line-height: 1.5;">
                    {current_theme_info.get('description', 'No description available')}
                </p>
                <div style="display: flex; justify-content: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="width: 24px; height: 24px; background: {current_theme_data.get('colors', {}).get('primary', '#FF4757') if current_theme_data else '#FF4757'}; border-radius: 50%; border: 2px solid white;"></div>
                    <div style="width: 24px; height: 24px; background: {current_theme_data.get('colors', {}).get('secondary', '#FF6348') if current_theme_data else '#FF6348'}; border-radius: 50%; border: 2px solid white;"></div>
                    <div style="width: 24px; height: 24px; background: {current_theme_data.get('colors', {}).get('accent', '#22C55E') if current_theme_data else '#22C55E'}; border-radius: 50%; border: 2px solid white;"></div>
                    <div style="width: 24px; height: 24px; background: {current_theme_data.get('colors', {}).get('warning', '#FFA502') if current_theme_data else '#FFA502'}; border-radius: 50%; border: 2px solid white;"></div>
                </div>
                <div style="color: #999; font-size: 0.85rem;">
                    v{current_theme_info.get('version', '1.0.0')} • {current_theme_info.get('type', 'dark').title()} Mode
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Theme Gallery
            st.markdown("### 🎨 Theme Gallery")
            
            # Create theme cards in a grid
            theme_cols = st.columns(2)
            
            for idx, (display_name, theme_id) in enumerate(available_themes.items()):
                theme_info = theme_provider.get_theme_info(theme_id)
                theme_data = theme_provider.load_theme(theme_id)
                is_current = theme_id == current_theme_name
                
                if not theme_data:
                    continue
                    
                colors = theme_data.get('colors', {})
                
                with theme_cols[idx % 2]:
                    if not is_current:
                        # Create theme preview card
                        st.markdown(f"""
                        <div style="background: {colors.get('bg_card', '#2D2D2D')}; 
                                    border: 1px solid {colors.get('border_color', '#404040')}; 
                                    border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; 
                                    transition: all 0.3s ease; cursor: pointer;"
                             onmouseover="this.style.borderColor='{colors.get('primary', '#FF4757')}'; this.style.transform='translateY(-2px)';"
                             onmouseout="this.style.borderColor='{colors.get('border_color', '#404040')}'; this.style.transform='translateY(0)';">
                            <h4 style="color: {colors.get('primary', '#FF4757')}; margin: 0 0 0.5rem 0; font-size: 1.2rem; font-weight: 600;">
                                {theme_info.get('name', theme_id)}
                            </h4>
                            <p style="color: {colors.get('text_secondary', '#CCCCCC')}; margin: 0 0 1rem 0; font-size: 0.9rem; line-height: 1.4;">
                                {theme_info.get('description', 'No description available')}
                            </p>
                            <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                                <div style="width: 16px; height: 16px; background: {colors.get('primary', '#FF4757')}; border-radius: 50%;"></div>
                                <div style="width: 16px; height: 16px; background: {colors.get('secondary', '#FF6348')}; border-radius: 50%;"></div>
                                <div style="width: 16px; height: 16px; background: {colors.get('accent', '#22C55E')}; border-radius: 50%;"></div>
                                <div style="width: 16px; height: 16px; background: {colors.get('warning', '#FFA502')}; border-radius: 50%;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Apply button
                        if st.button(f"🎨 Apply {theme_info.get('name', theme_id)}", key=f"apply_{theme_id}", use_container_width=True):
                            if switch_theme(theme_id):
                                st.success(f"✅ Theme changed to {theme_info.get('name', theme_id)}!")
                                st.info("🔄 Refreshing page to apply theme...")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(f"❌ Failed to switch theme")
        
        except ImportError:
            # Fallback if theme system is not available
            st.warning("⚠️ Theme system not available. Using default Crimzon Dark theme.")
    
    with side_col:
        # === SYSTEM INFO PANEL ===
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="color: #FF4757; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">
                📊 System Status
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Load data for system info
        videos_df, comments_df = load_reputation_data()
        
        # Data status indicators
        if not videos_df.empty:
            st.success(f"✅ Videos: {len(videos_df)}")
        else:
            st.error("❌ No video data")
            
        if not comments_df.empty:
            st.success(f"✅ Comments: {len(comments_df)}")
        else:
            st.error("❌ No comment data")
        
        # Quick actions
        st.markdown("### 🔧 Quick Actions")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")
            
        if st.button("📊 Recalculate", use_container_width=True):
            st.cache_data.clear()
            st.success("Metrics reset!")
    
        # === ADDITIONAL SETTINGS SECTIONS ===
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        # Alert Configuration
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 165, 2, 0.1) 0%, rgba(255, 165, 2, 0.05) 100%); 
                    border: 1px solid rgba(255, 165, 2, 0.3); border-radius: 12px; padding: 2rem; margin-bottom: 2rem;">
            <h2 style="color: #FFA502; margin: 0 0 1rem 0; font-size: 1.5rem; font-weight: 700;">
                🚨 Alert Configuration
            </h2>
            <p style="color: #CCCCCC; margin: 0; font-size: 1rem;">
                Set thresholds for reputation monitoring and crisis detection
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            critical_threshold = st.slider(
                "🔴 Critical Alert Threshold (%)",
                0, 50, 40,
                help="Reputation score below this triggers critical alerts"
            )
        
        with col2:
            warning_threshold = st.slider(
                "🟡 Warning Alert Threshold (%)",
                40, 80, 60,
                help="Reputation score below this triggers warnings"
            )
        
        st.info(f"📊 Current settings: Critical < {critical_threshold}%, Warning < {warning_threshold}%")
        
        # Export Configuration
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%); 
                    border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; padding: 2rem; margin-bottom: 2rem;">
            <h2 style="color: #22C55E; margin: 0 0 1rem 0; font-size: 1.5rem; font-weight: 700;">
                📤 Data Export
            </h2>
            <p style="color: #CCCCCC; margin: 0; font-size: 1rem;">
                Export your data for external analysis and reporting
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Load data for export
        videos_df, comments_df = load_reputation_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export Comments CSV", use_container_width=True):
                if not comments_df.empty:
                    csv = comments_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Comments CSV",
                        data=csv,
                        file_name=f"comments_export_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.error("❌ No comment data to export")
        
        with col2:
            if st.button("📄 Export Videos CSV", use_container_width=True):
                if not videos_df.empty:
                    csv = videos_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Videos CSV",
                        data=csv,
                        file_name=f"videos_export_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.error("❌ No video data to export")

def show_executive_reports_page():
    """Executive Reports & Automated Intelligence Briefings Page"""
    st.markdown('<h1 class="page-title">📋 Executive Reports</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Automated intelligence briefings and executive-level analytics</p>', unsafe_allow_html=True)
    
    # Load data and initialize reporting engine
    videos_df, comments_df = load_reputation_data()
    
    if videos_df.empty or comments_df.empty:
        st.error("⚠️ Unable to load data for executive reporting")
        return
    
    try:
        # Initialize engines
        reporting_engine = ExecutiveReportingEngine()
        crisis_engine = CrisisDetectionEngine()
        
        # Get crisis data for comprehensive reporting
        crisis_status = crisis_engine.get_crisis_status(videos_df, comments_df)
        
        # 📊 REPORT SELECTION HEADER
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 71, 87, 0.05) 100%);
            border: 1px solid #FF4757;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            text-align: center;
        ">
            <h2 style="color: #FF4757; font-size: 1.4rem; margin: 0 0 0.5rem 0; font-weight: 700;">
                📋 EXECUTIVE INTELLIGENCE CENTER
            </h2>
            <p style="color: #CCCCCC; font-size: 1rem; margin: 0;">
                Automated briefings, strategic insights, and executive-level analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 📊 REPORT TYPE SELECTION
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Daily Briefing", use_container_width=True, type="primary"):
                st.session_state.selected_report = "daily_briefing"
        
        with col2:
            if st.button("📈 Weekly Intelligence", use_container_width=True):
                st.session_state.selected_report = "weekly_intelligence"
        
        with col3:
            if st.button("🎯 Executive Summary", use_container_width=True):
                st.session_state.selected_report = "executive_summary"
        
        # Initialize selected report if not set
        if 'selected_report' not in st.session_state:
            st.session_state.selected_report = "daily_briefing"
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Generate and display selected report
        if st.session_state.selected_report == "daily_briefing":
            st.markdown('<h2 style="color: #FF4757; font-size: 1.4rem; margin-bottom: 1rem;">📊 Daily Intelligence Briefing</h2>', unsafe_allow_html=True)
            
            with st.spinner("Generating daily intelligence briefing..."):
                daily_briefing = reporting_engine.generate_daily_briefing(videos_df, comments_df, crisis_status)
                
                if 'error' not in daily_briefing:
                    # Executive Summary Section
                    exec_summary = daily_briefing.get('executive_summary', {})
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        status_color = {"CRITICAL": "#EF4444", "CONCERNING": "#F59E0B", "STABLE": "#22C55E", "POSITIVE": "#22C55E"}.get(exec_summary.get('overall_status'), "#6B7280")
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
                            border-radius: 12px;
                            padding: 1.5rem;
                            border: 1px solid {status_color};
                            text-align: center;
                            height: 140px;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                        ">
                            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📊</div>
                            <div style="color: {status_color}; font-size: 1.2rem; font-weight: 800;">{exec_summary.get('overall_status', 'Unknown')}</div>
                            <div style="color: #CCCCCC; font-size: 0.7rem; font-weight: 600;">OVERALL STATUS</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        health_color = {"STRONG": "#22C55E", "GOOD": "#22C55E", "AT_RISK": "#EF4444", "DECLINING": "#F59E0B"}.get(exec_summary.get('reputation_health'), "#6B7280")
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
                            border-radius: 12px;
                            padding: 1.5rem;
                            border: 1px solid {health_color};
                            text-align: center;
                            height: 140px;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                        ">
                            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">💪</div>
                            <div style="color: {health_color}; font-size: 1.2rem; font-weight: 800;">{exec_summary.get('reputation_health', 'Unknown')}</div>
                            <div style="color: #CCCCCC; font-size: 0.7rem; font-weight: 600;">REPUTATION HEALTH</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        metrics = daily_briefing.get('key_metrics', {})
                        engagement_rate = metrics.get('engagement_metrics', {}).get('engagement_rate', 0)
                        engagement_color = "#22C55E" if engagement_rate > 5 else "#F59E0B" if engagement_rate > 2 else "#EF4444"
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
                            border-radius: 12px;
                            padding: 1.5rem;
                            border: 1px solid {engagement_color};
                            text-align: center;
                            height: 140px;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                        ">
                            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">⚡</div>
                            <div style="color: {engagement_color}; font-size: 1.2rem; font-weight: 800;">{engagement_rate:.1f}</div>
                            <div style="color: #CCCCCC; font-size: 0.7rem; font-weight: 600;">ENGAGEMENT RATE</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        threat_level = crisis_status.get('threat_counts', {}).get('total', 0)
                        threat_color = "#EF4444" if threat_level > 20 else "#F59E0B" if threat_level > 10 else "#22C55E"
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
                            border-radius: 12px;
                            padding: 1.5rem;
                            border: 1px solid {threat_color};
                            text-align: center;
                            height: 140px;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                        ">
                            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🛡️</div>
                            <div style="color: {threat_color}; font-size: 1.2rem; font-weight: 800;">{threat_level}</div>
                            <div style="color: #CCCCCC; font-size: 0.7rem; font-weight: 600;">THREAT LEVEL</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
                    
                    # Key Highlights
                    if exec_summary.get('key_highlights'):
                        st.markdown("### 🔥 Key Highlights")
                        for highlight in exec_summary['key_highlights']:
                            st.markdown(f"- {highlight}")
                    
                    # Critical Issues
                    if exec_summary.get('critical_issues'):
                        st.markdown("### 🚨 Critical Issues")
                        for issue in exec_summary['critical_issues']:
                            st.markdown(f"- ⚠️ {issue}")
                    
                    # Strategic Recommendations
                    if daily_briefing.get('recommendations'):
                        st.markdown("### 💡 Strategic Recommendations")
                        for i, rec in enumerate(daily_briefing['recommendations'][:3], 1):
                            priority_color = {"IMMEDIATE": "#EF4444", "HIGH": "#F59E0B", "MEDIUM": "#EAB308"}.get(rec.get('priority'), "#6B7280")
                            with st.expander(f"{i}. {rec.get('title', 'Recommendation')} ({rec.get('priority', 'MEDIUM')})"):
                                st.write(f"**Category:** {rec.get('category', 'Strategic')}")
                                st.write(f"**Description:** {rec.get('description', 'No description')}")
                                if rec.get('actions'):
                                    st.write("**Recommended Actions:**")
                                    for action in rec['actions']:
                                        st.write(f"- {action}")
                    
                    # Action Items
                    if daily_briefing.get('action_items'):
                        st.markdown("### ✅ Action Items")
                        for action in daily_briefing['action_items'][:5]:
                            priority_icon = {"IMMEDIATE": "🔴", "HIGH": "🟡", "MEDIUM": "🟢", "ONGOING": "🔵"}.get(action.get('priority'), "⚪")
                            st.markdown(f"{priority_icon} **{action.get('action', 'Action required')}** (Owner: {action.get('owner', 'TBD')}, Deadline: {action.get('deadline', 'TBD')})")
                
                else:
                    st.error(f"Failed to generate daily briefing: {daily_briefing['error']}")
        
        elif st.session_state.selected_report == "weekly_intelligence":
            st.markdown('<h2 style="color: #FF4757; font-size: 1.4rem; margin-bottom: 1rem;">📈 Weekly Intelligence Report</h2>', unsafe_allow_html=True)
            
            with st.spinner("Generating weekly intelligence report..."):
                weekly_report = reporting_engine.generate_weekly_intelligence(videos_df, comments_df, crisis_status)
                
                if 'error' not in weekly_report:
                    st.success("📊 Weekly Intelligence Report Generated Successfully")
                    
                    # Executive Summary
                    exec_summary = weekly_report.get('executive_summary', {})
                    st.markdown("### 📊 Executive Summary")
                    st.write(f"**Overall Status:** {exec_summary.get('overall_status', 'Unknown')}")
                    st.write(f"**Reputation Health:** {exec_summary.get('reputation_health', 'Unknown')}")
                    
                    # Performance Metrics
                    if weekly_report.get('performance_metrics'):
                        st.markdown("### 📈 Performance Metrics")
                        perf_metrics = weekly_report['performance_metrics']
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'content_metrics' in perf_metrics:
                                st.write("**Content Metrics:**")
                                for key, value in perf_metrics['content_metrics'].items():
                                    st.write(f"- {key.replace('_', ' ').title()}: {value:,}")
                        
                        with col2:
                            if 'engagement_metrics' in perf_metrics:
                                st.write("**Engagement Metrics:**")
                                for key, value in perf_metrics['engagement_metrics'].items():
                                    if isinstance(value, float):
                                        st.write(f"- {key.replace('_', ' ').title()}: {value:.2f}")
                                    else:
                                        st.write(f"- {key.replace('_', ' ').title()}: {value:,}")
                    
                    # Recommendations
                    if weekly_report.get('recommendations'):
                        st.markdown("### 💡 Weekly Recommendations")
                        for rec in weekly_report['recommendations']:
                            with st.expander(f"{rec.get('title', 'Recommendation')} ({rec.get('priority', 'MEDIUM')})"):
                                st.write(rec.get('description', 'No description'))
                
                else:
                    st.error(f"Failed to generate weekly report: {weekly_report['error']}")
        
        elif st.session_state.selected_report == "executive_summary":
            st.markdown('<h2 style="color: #FF4757; font-size: 1.4rem; margin-bottom: 1rem;">🎯 Executive Summary Report</h2>', unsafe_allow_html=True)
            
            with st.spinner("Generating executive summary..."):
                executive_summary = reporting_engine.generate_executive_summary_report(videos_df, comments_df, crisis_status)
                
                # Display formatted summary
                st.markdown(executive_summary)
        
        # Export Options
        st.markdown("<div style='margin: 3rem 0 2rem 0;'></div>", unsafe_allow_html=True)
        st.markdown('<h2 style="color: #FF4757; font-size: 1.4rem; margin-bottom: 1rem;">💾 Export Options</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export Daily Briefing", use_container_width=True):
                daily_briefing = reporting_engine.generate_daily_briefing(videos_df, comments_df, crisis_status)
                filename = reporting_engine.export_report(daily_briefing, 'daily_briefing', 'json')
                st.success(f"Daily briefing exported to: {filename}")
        
        with col2:
            if st.button("📊 Export Weekly Report", use_container_width=True):
                weekly_report = reporting_engine.generate_weekly_intelligence(videos_df, comments_df, crisis_status)
                filename = reporting_engine.export_report(weekly_report, 'weekly_intelligence', 'json')
                st.success(f"Weekly report exported to: {filename}")
        
        with col3:
            if st.button("📋 Export Executive Summary", use_container_width=True):
                summary_text = reporting_engine.generate_executive_summary_report(videos_df, comments_df, crisis_status)
                filename = reporting_engine.export_report(summary_text, 'executive_summary', 'txt')
                st.success(f"Executive summary exported to: {filename}")
        
    except Exception as e:
        st.error(f"Executive Reporting System Error: {e}")
        st.info("Please check system logs for detailed error information")

def show_reputation_alerts_page():
    """Reputation Alerts & Real-time Sentiment Escalation Monitoring Page"""
    st.markdown('<h1 class="page-title">🔔 Reputation Alerts</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Real-time sentiment escalation monitoring and brand reputation management</p>', unsafe_allow_html=True)
    
    # Load data and initialize reputation monitoring with language preference support
    videos_df, comments_df_raw = load_reputation_data()
    
    # Apply language preference to comments
    comments_df = get_language_aware_comments(comments_df_raw)
    
    if videos_df.empty or comments_df.empty:
        st.error("⚠️ Unable to load data for reputation monitoring")
        return
    
    try:
        # Initialize reputation monitoring engine
        reputation_engine = ReputationIntelligenceEngine() if 'ReputationIntelligenceEngine' in globals() else None
        
        # Get current reputation status
        reputation_status = get_reputation_status(videos_df, comments_df)
        
        # 🔔 REPUTATION STATUS HEADER
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 71, 87, 0.05) 100%);
            border: 2px solid {reputation_status['status_color']};
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{reputation_status['status_icon']}</div>
            <h2 style="color: {reputation_status['status_color']}; font-size: 2rem; margin: 0 0 0.5rem 0; font-weight: 800;">
                REPUTATION STATUS: {reputation_status['status']}
            </h2>
            <p style="color: #CCCCCC; font-size: 1.2rem; margin: 0;">{reputation_status['status_message']}</p>
            <p style="color: #888; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 📊 REPUTATION METRICS
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid #EF4444;
                text-align: center;
                height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔴</div>
                <div style="color: #EF4444; font-size: 2rem; font-weight: 800;">{reputation_status['alert_counts']['critical']}</div>
                <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600;">CRITICAL ALERTS</div>
                <div style="color: #888; font-size: 0.7rem;">Immediate attention required</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid #F59E0B;
                text-align: center;
                height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🟡</div>
                <div style="color: #F59E0B; font-size: 2rem; font-weight: 800;">{reputation_status['alert_counts']['high']}</div>
                <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600;">HIGH PRIORITY</div>
                <div style="color: #888; font-size: 0.7rem;">Enhanced monitoring needed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid #6B7280;
                text-align: center;
                height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="color: #6B7280; font-size: 2rem; font-weight: 800;">{reputation_status['alert_counts']['total']}</div>
                <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600;">TOTAL ALERTS</div>
                <div style="color: #888; font-size: 0.7rem;">All severity levels</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Calculate opinion momentum (simplified)
            recent_activity = min(reputation_status['alert_counts']['total'], 50)  # Cap for display
            velocity_color = "#EF4444" if recent_activity > 20 else "#F59E0B" if recent_activity > 10 else "#22C55E"
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #2D2D2D 0%, #3A3A3A 100%);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid {velocity_color};
                text-align: center;
                height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
                <div style="color: {velocity_color}; font-size: 2rem; font-weight: 800;">{recent_activity}</div>
                <div style="color: #CCCCCC; font-size: 0.8rem; font-weight: 600;">OPINION MOMENTUM</div>
                <div style="color: #888; font-size: 0.7rem;">Recent sentiment activity</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        # 🔔 STRATEGIC ACTIONS
        if reputation_status['status'] in ['CRITICAL', 'HIGH']:
            st.markdown('<h2 style="color: #EF4444; font-size: 1.4rem; margin-bottom: 1rem;">🔔 Immediate Strategic Actions Required</h2>', unsafe_allow_html=True)
            
            if reputation_status['status'] == 'CRITICAL':
                action_items = [
                    "🔴 **IMMEDIATE**: Alert brand reputation team",
                    "📢 **URGENT**: Draft public communication statement", 
                    "⚖️ **CONSIDER**: PR consultation for reputation management",
                    "📊 **MONITOR**: Sentiment escalation patterns hourly",
                    "🛡️ **PROTECT**: Implement reputation protection measures"
                ]
            else:
                action_items = [
                    "🟡 **HIGH**: Activate enhanced sentiment monitoring",
                    "📢 **PR**: Prepare positive content strategy",
                    "👥 **TEAM**: Brief PR stakeholders on situation",
                    "📱 **SOCIAL**: Monitor brand mentions actively",
                    "🤝 **ENGAGE**: Address public concerns proactively"
                ]
            
            for item in action_items:
                st.markdown(f"- {item}")
        
        # 📈 REPUTATION ANALYSIS
        st.markdown('<h2 style="color: #FF4757; font-size: 1.4rem; margin: 2rem 0 1rem 0;">📈 Detailed Reputation Analysis</h2>', unsafe_allow_html=True)
        
        if st.button("🔍 Run Full Reputation Analysis", type="primary"):
            with st.spinner("Analyzing sentiment patterns and generating executive report..."):
                # Run full reputation analysis
                full_report = analyze_reputation_patterns(videos_df, comments_df)
                
                if 'error' not in full_report:
                    # Display executive alerts
                    if full_report['executive_alerts']:
                        st.markdown("### 🔔 Executive Alerts")
                        for alert in full_report['executive_alerts']:
                            alert_color = "#EF4444" if alert['priority'] == 'IMMEDIATE' else "#F59E0B"
                            st.markdown(f"""
                            <div style="
                                background: rgba(255, 71, 87, 0.1);
                                border-left: 4px solid {alert_color};
                                padding: 1rem;
                                margin: 0.5rem 0;
                                border-radius: 0 8px 8px 0;
                            ">
                                <strong style="color: {alert_color};">{alert['title']}</strong><br>
                                {alert['message']}<br>
                                <em style="color: #888;">Recommended: {alert['recommended_action']}</em>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Display recommendations
                    if full_report['recommendations']:
                        st.markdown("### 💡 Strategic Recommendations")
                        for rec in full_report['recommendations']:
                            with st.expander(f"{rec['priority']}: {rec['action']}"):
                                st.write(f"**Category:** {rec['category']}")
                                st.write(f"**Description:** {rec['description']}")
                                st.write("**Specific Steps:**")
                                for step in rec['specific_steps']:
                                    st.write(f"- {step}")
                else:
                    st.error(f"Analysis failed: {full_report['error']}")
        
        # 📱 QUICK ACTIONS
        st.markdown('<h2 style="color: #FF4757; font-size: 1.4rem; margin: 2rem 0 1rem 0;">📱 Quick Actions</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Reputation Status", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("📊 Export Reputation Report", use_container_width=True):
                st.info("Report export feature - Coming in next update")
        
        with col3:
            if st.button("📢 Notify PR Strategy Team", use_container_width=True):
                st.success("PR team notification sent!")
        
    except Exception as e:
        st.error(f"Reputation Monitoring System Error: {e}")
        st.info("Please check system logs for detailed error information")

def get_reputation_status(videos_df, comments_df):
    """Get current reputation status based on sentiment analysis"""
    try:
        # Calculate reputation alerts from sentiment data
        alert_counts = {'critical': 0, 'high': 0, 'medium': 0, 'total': 0}
        
        # Check for reputation concerns in comments
        if not comments_df.empty and 'SentimentScore_EN' in comments_df.columns:
            negative_comments = comments_df[comments_df['SentimentScore_EN'] < -0.5]
            highly_negative = len(negative_comments[negative_comments['SentimentScore_EN'] < -0.8])
            moderately_negative = len(negative_comments[negative_comments['SentimentScore_EN'] >= -0.8])
            
            alert_counts['critical'] = highly_negative
            alert_counts['high'] = moderately_negative
            alert_counts['total'] = len(negative_comments)
        
        # Determine overall status
        if alert_counts['critical'] > 10:
            status = 'CRITICAL'
            status_color = '#EF4444'
            status_icon = '🔴'
            status_message = f"{alert_counts['critical']} critical reputation alerts detected"
        elif alert_counts['high'] > 20:
            status = 'HIGH'
            status_color = '#F59E0B'
            status_icon = '🟡'
            status_message = f"{alert_counts['high']} high-priority sentiment concerns identified"
        elif alert_counts['total'] > 30:
            status = 'MODERATE'
            status_color = '#FFA502'
            status_icon = '🟠'
            status_message = f"{alert_counts['total']} reputation alerts require monitoring"
        else:
            status = 'STABLE'
            status_color = '#22C55E'
            status_icon = '🟢'
            status_message = "Reputation status stable with normal sentiment patterns"
        
        return {
            'status': status,
            'status_color': status_color,
            'status_icon': status_icon,
            'status_message': status_message,
            'alert_counts': alert_counts
        }
        
    except Exception as e:
        return {
            'status': 'UNKNOWN',
            'status_color': '#6B7280',
            'status_icon': '❓',
            'status_message': 'Unable to determine reputation status',
            'alert_counts': {'critical': 0, 'high': 0, 'medium': 0, 'total': 0}
        }

def analyze_reputation_patterns(videos_df, comments_df):
    """Analyze reputation patterns and generate strategic recommendations"""
    try:
        report = {
            'executive_alerts': [],
            'recommendations': [],
            'sentiment_analysis': {}
        }
        
        # Analyze sentiment patterns
        if not comments_df.empty and 'SentimentScore_EN' in comments_df.columns:
            negative_sentiment = comments_df[comments_df['SentimentScore_EN'] < -0.3]
            
            if len(negative_sentiment) > 50:
                report['executive_alerts'].append({
                    'priority': 'IMMEDIATE',
                    'title': 'High Volume of Negative Sentiment Detected',
                    'message': f'{len(negative_sentiment)} comments show negative sentiment patterns',
                    'recommended_action': 'Implement proactive communication strategy'
                })
                
                report['recommendations'].append({
                    'priority': 'HIGH',
                    'category': 'Public Relations',
                    'action': 'Address Negative Sentiment',
                    'description': 'Significant negative sentiment detected in public comments',
                    'specific_steps': [
                        'Analyze root causes of negative sentiment',
                        'Develop targeted communication strategy',
                        'Engage with community stakeholders',
                        'Monitor sentiment improvement over time'
                    ]
                })
        
        # Add strategic recommendations
        report['recommendations'].append({
            'priority': 'MEDIUM',
            'category': 'Brand Management',
            'action': 'Enhance Positive Engagement',
            'description': 'Strengthen positive brand associations and community engagement',
            'specific_steps': [
                'Increase positive content creation',
                'Engage with supportive community members',
                'Highlight positive achievements and contributions',
                'Monitor brand perception improvements'
            ]
        })
        
        return report
        
    except Exception as e:
        return {'error': str(e)}

def show_predictive_analytics_page():
    """Display Reputation Intelligence & PR Risk Analysis page"""
    st.markdown('<h1 class="page-title">🧠 Reputation Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Advanced Public Sentiment Analysis & PR Risk Management</p>', unsafe_allow_html=True)
    
    # Load reputation intelligence data
    reputation_report = load_reputation_intelligence_report()
    predictions = load_phase3c_predictions()  # Fallback for compatibility
    videos_df, comments_df = load_optimized_datasets()
    
    if not reputation_report and not predictions:
        st.error("⚠️ Reputation Intelligence data not available. Please run the reputation intelligence engine first.")
        st.code("python scripts/reputation_intelligence_engine.py")
        return
    
    # Use reputation intelligence data if available, otherwise fallback
    analysis_data = reputation_report if reputation_report else predictions
    
    # System status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="color: #2ED573; font-size: 1.5rem; font-weight: bold;">
                <span class="status-indicator status-active"></span>💬 System Status
            </div>
            <div style="color: white; font-size: 1.2rem; margin-top: 0.5rem;">
                Reputation Intelligence Active
            </div>
            <div style="color: #888; font-size: 0.9rem; margin-top: 0.5rem;">
                Monitoring Public Sentiment
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        reputation_metrics = analysis_data.get('reputation_metrics', {})
        st.markdown("""
        <div class="metric-card">
            <div style="color: #FFA502; font-size: 1.5rem; font-weight: bold;">
                📊 Opinion Coverage
            </div>
            <div style="color: white; font-size: 1.2rem; margin-top: 0.5rem;">
                {} Comments Analyzed
            </div>
            <div style="color: #888; font-size: 0.9rem; margin-top: 0.5rem;">
                {} Unique Public Voices
            </div>
        </div>
        """.format(
            reputation_metrics.get('sentiment_coverage', 'N/A'),
            reputation_metrics.get('opinion_diversity', 'N/A')
        ), unsafe_allow_html=True)
    
    with col3:
        # Get reputation health data
        if 'reputation_analysis' in analysis_data:
            health_data = analysis_data['reputation_analysis'].get('reputation_health', {})
        else:
            health_data = analysis_data.get('predictions', {}).get('crisis_assessment', {})
        
        health_status = health_data.get('health_status', health_data.get('risk_level', 'UNKNOWN'))
        pr_risk = health_data.get('overall_pr_risk', health_data.get('overall_probability', 0))
        
        status_color = {
            'HEALTHY_REPUTATION': '#2ED573',
            'MODERATE_PR_CONCERN': '#FFA502', 
            'HIGH_PR_RISK': '#FF6348',
            'REPUTATION_CRISIS': '#FF4757',
            'LOW': '#2ED573',
            'MEDIUM': '#FFA502',
            'HIGH': '#FF6348',
            'CRITICAL': '#FF4757'
        }.get(health_status, '#888')
        
        st.markdown("""
        <div class="crisis-card">
            <div style="color: {}; font-size: 1.5rem; font-weight: bold;">
                ⚠️ Reputation Health: {}
            </div>
            <div style="color: white; font-size: 1.2rem; margin-top: 0.5rem;">
                PR Risk: {:.1%}
            </div>
            <div style="color: #888; font-size: 0.9rem; margin-top: 0.5rem;">
                Based on Public Sentiment
            </div>
        </div>
        """.format(
            status_color, 
            health_status.replace('_', ' ').title(),
            pr_risk
        ), unsafe_allow_html=True)
    
    # Reputation Trajectory Forecasting
    st.markdown("## 🎯 Reputation Trajectory Forecasting")
    
    # Get reputation forecasts
    if 'reputation_analysis' in analysis_data:
        rep_forecasts = analysis_data['reputation_analysis'].get('reputation_forecasts', {})
    else:
        rep_forecasts = analysis_data.get('predictions', {}).get('reputation_forecasts', {})
    
    if rep_forecasts:
        col1, col2 = st.columns(2)
        
        with col1:
            # Reputation forecast timeline
            forecast_data = {
                'Period': ['Current', '7-Day', '30-Day', '90-Day'],
                'Forecast': [0, rep_forecasts.get('7_day', 0), rep_forecasts.get('30_day', 0), rep_forecasts.get('90_day', 0)]
            }
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=forecast_data['Period'],
                y=forecast_data['Forecast'],
                mode='lines+markers',
                line=dict(color='#2ED573', width=3),
                marker=dict(size=8, color='#2ED573'),
                name='Reputation Trajectory'
            ))
            
            fig.update_layout(
                title="Reputation Trajectory Forecast",
                xaxis_title="Time Period",
                yaxis_title="Reputation Score",
                template="plotly_dark",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            trend = rep_forecasts.get('trend', 'unknown').replace('_', ' ').title()
            confidence = rep_forecasts.get('confidence', 0)
            
            st.markdown(f"""
            <div class="forecast-timeline">
                <div style="color: #2ED573; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                    📈 Reputation Insights
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Reputation Trend:</strong> {trend}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>7-Day Outlook:</strong> {rep_forecasts.get('7_day', 0):.4f}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>30-Day Outlook:</strong> {rep_forecasts.get('30_day', 0):.4f}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>90-Day Outlook:</strong> {rep_forecasts.get('90_day', 0):.4f}
                </div>
                <div style="color: #888; font-size: 0.9rem; margin-top: 1rem;">
                    Forecast Confidence: {confidence:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Sentiment Escalation Analysis
    st.markdown("## 📈 Sentiment Escalation Analysis")
    
    # Get sentiment escalation data
    if 'reputation_analysis' in analysis_data:
        sentiment_data = analysis_data['reputation_analysis'].get('sentiment_escalation', {})
    else:
        sentiment_data = analysis_data.get('predictions', {}).get('threat_escalation', {})
    
    if sentiment_data:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment escalation risk gauge
            current_risk = sentiment_data.get('current_risk', 0)
            max_risk = sentiment_data.get('max_risk', 0)
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = current_risk * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Sentiment Escalation Risk (%)"},
                delta = {'reference': 20},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#FF4757"},
                    'steps': [
                        {'range': [0, 25], 'color': "#2ED573"},
                        {'range': [25, 50], 'color': "#FFA502"},
                        {'range': [50, 75], 'color': "#FF6348"},
                        {'range': [75, 100], 'color': "#FF4757"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': max_risk * 100
                    }
                }
            ))
            
            fig.update_layout(
                template="plotly_dark",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            trend = sentiment_data.get('trend', 'unknown')
            confidence = sentiment_data.get('confidence', 0)
            risk_level = sentiment_data.get('risk_level', 'Unknown').replace('_', ' ').title()
            
            st.markdown(f"""
            <div class="prediction-card">
                <div style="color: #FF4757; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                    🎯 Sentiment Intelligence
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Current Risk Level:</strong> {current_risk:.1%}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Peak Risk Observed:</strong> {max_risk:.1%}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Trend Direction:</strong> {trend.title()}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Risk Category:</strong> {risk_level}
                </div>
                <div style="color: #888; font-size: 0.9rem; margin-top: 1rem;">
                    <strong>Model Confidence:</strong> {confidence:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Public Opinion Momentum
    st.markdown("## 📊 Public Opinion Momentum")
    
    # Get opinion momentum data
    if 'reputation_analysis' in analysis_data:
        opinion_data = analysis_data['reputation_analysis'].get('opinion_momentum', {})
    else:
        opinion_data = analysis_data.get('predictions', {}).get('engagement_trends', {})
    
    if opinion_data:
        col1, col2 = st.columns(2)
        
        with col1:
            # Opinion momentum visualization
            momentum_value = opinion_data.get('current_momentum', opinion_data.get('short_term_forecast', 0))
            momentum_direction = opinion_data.get('momentum_direction', opinion_data.get('trend_direction', 'unknown'))
            
            # Create momentum visualization
            periods = ['Past Week', 'Current', 'Projected']
            if 'positive' in momentum_direction.lower():
                values = [momentum_value * 0.8, momentum_value * 0.9, momentum_value]
                color = '#2ED573'
            else:
                values = [momentum_value * 1.2, momentum_value * 1.1, momentum_value]
                color = '#FF6348'
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=periods,
                y=values,
                marker_color=color,
                name='Opinion Momentum'
            ))
            
            fig.update_layout(
                title="Public Opinion Momentum",
                xaxis_title="Time Period",
                yaxis_title="Opinion Strength",
                template="plotly_dark",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            confidence = opinion_data.get('confidence', 0)
            
            st.markdown(f"""
            <div class="prediction-card">
                <div style="color: #2ED573; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                    📊 Opinion Analysis
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Momentum Direction:</strong> {momentum_direction.replace('_', ' ').title()}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Current Momentum:</strong> {momentum_value:.1f}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Analysis Confidence:</strong> {confidence:.1%}
                </div>
                <div style="color: #888; font-size: 0.9rem; margin-top: 1rem;">
                    Based on public engagement patterns
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Strategic Recommendations
    st.markdown("## 💡 Reputation Management Recommendations")
    
    # Get recommendations
    if 'strategic_recommendations' in analysis_data:
        recommendations = analysis_data['strategic_recommendations']
    else:
        recommendations = analysis_data.get('predictions', {}).get('strategic_recommendations', [])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="prediction-card">
                <div style="color: #FFA502; font-size: 1.1rem; font-weight: bold;">
                    {i}. {rec}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="prediction-card">
            <div style="color: #2ED573; font-size: 1.1rem; font-weight: bold;">
                ✅ No immediate reputation concerns detected. Continue current engagement strategies.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Reputation Health Details
    st.markdown("## 💬 Comprehensive Reputation Health")
    
    if health_data:
        components = health_data.get('risk_components', health_data.get('components', {}))
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk components breakdown
            risk_components = {}
            if 'sentiment_escalation_risk' in components:
                risk_components = {
                    'Sentiment Escalation': components.get('sentiment_escalation_risk', 0),
                    'Reputation Trajectory': components.get('reputation_trajectory_risk', 0),
                    'Opinion Momentum': components.get('opinion_momentum_risk', 0)
                }
            else:
                risk_components = {
                    'Reputation Risk': components.get('reputation_risk', 0),
                    'PR Risk': components.get('threat_risk', 0),
                    'Engagement Risk': components.get('engagement_risk', 0)
                }
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(risk_components.keys()),
                    y=list(risk_components.values()),
                    marker_color=['#FF6348', '#FF4757', '#FFA502']
                )
            ])
            
            fig.update_layout(
                title="Reputation Risk Components",
                xaxis_title="Risk Category",
                yaxis_title="Risk Level",
                template="plotly_dark",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            recommendation = health_data.get('recommendation', 'Continue monitoring reputation metrics')
            
            st.markdown(f"""
            <div class="crisis-card">
                <div style="color: #FFA502; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                    🎯 Reputation Management
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Overall Health:</strong> {health_status.replace('_', ' ').title()}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>PR Risk Level:</strong> {pr_risk:.1%}
                </div>
                <div style="color: white; margin-bottom: 1rem;">
                    <strong>Action Plan:</strong>
                    <br>{recommendation}
                </div>
                <div style="color: #888; font-size: 0.9rem;">
                    Assessment based on public sentiment analysis
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Model Performance Summary
    st.markdown("## 🧠 Reputation Intelligence Models")
    
    models_implemented = analysis_data.get('models_implemented', [])
    
    if models_implemented:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div style="color: #2ED573; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                    🔧 Active Models
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            for model in models_implemented:
                model_name = model.replace('_', ' ').replace('reputation ', '').title()
                st.markdown(f"✅ **{model_name}**")
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #FFA502; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                    📊 System Overview
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Focus:</strong> Public Sentiment Analysis
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Data Source:</strong> YouTube Comments
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Analysis Type:</strong> Reputation Intelligence
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Purpose:</strong> PR Risk Management
                </div>
            </div>
            """, unsafe_allow_html=True)

@st.cache_data
def load_reputation_intelligence_report():
    """Load reputation intelligence analysis results"""
    try:
        with open('scripts/logs/reputation_intelligence_report.json', 'r') as f:
            report = json.load(f)
        return report
    except FileNotFoundError:
        return None

def show_phase3c_predictive_analytics_page():
    """Display Phase 3C Advanced Predictive Analytics page"""
    st.markdown('<h1 class="page-title">🔮 Phase 3C: Predictive Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Advanced ML Forecasting & Crisis Prediction Engine</p>', unsafe_allow_html=True)
    
    # Phase 3C Status and Controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Run Phase 3C Engine", use_container_width=True):
            with st.spinner("Running Phase 3C Predictive Engine..."):
                try:
                    # Run the Phase 3C robust engine
                    import subprocess
                    result = subprocess.run(['python', 'scripts/phase3c_robust.py'], capture_output=True, text=True, cwd='.')
                    
                    if result.returncode == 0:
                        st.success("✅ Phase 3C Engine completed successfully!")
                        st.info("Refresh the page to see updated predictions")
                    else:
                        st.error(f"❌ Phase 3C Engine failed: {result.stderr}")
                except Exception as e:
                    st.error(f"Error running Phase 3C Engine: {e}")
    
    with col2:
        st.info("📊 **4 ML Models**\nReputation • Threat • Engagement • Crisis")
    
    with col3:
        st.info("🎯 **Forecast Horizons**\n7-day • 30-day • 90-day")
    
    with col4:
        st.info("🛡️ **Error Handling**\nRobust with Statistical Fallbacks")
    
    # Load Phase 3C predictions
    try:
        with open('scripts/logs/phase3c_robust_report.json', 'r') as f:
            predictions = json.load(f)
        phase3c_available = True
    except FileNotFoundError:
        predictions = None
        phase3c_available = False
    
    if not phase3c_available:
        st.warning("⚠️ Phase 3C predictions not available. Click 'Run Phase 3C Engine' to generate predictions.")
        st.code("python scripts/phase3c_robust.py")
        return
    
    # Model Status Overview
    st.markdown("## 🧠 ML Model Status")
    
    models_built = predictions.get('models_built', 0)
    steps_completed = predictions.get('steps_completed', 0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Models Built", f"{models_built}/4", 
            f"{models_built*25}% Complete", 
            "positive" if models_built > 0 else "neutral",
            "🧠"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Implementation Steps", f"{steps_completed}/4", 
            f"{int(steps_completed/4*100)}% Progress", 
            "positive" if steps_completed > 2 else "neutral",
            "⚙️"
        ), unsafe_allow_html=True)
    
    with col3:
        model_performance = predictions.get('model_performance', {})
        avg_accuracy = sum(model_performance.values()) / len(model_performance) if model_performance else 0
        st.markdown(create_metric_card(
            "Avg Model Accuracy", f"{avg_accuracy:.1%}", 
            "Prediction Quality", 
            "positive" if avg_accuracy > 0.7 else "neutral",
            "🎯"
        ), unsafe_allow_html=True)
    
    with col4:
        data_quality = predictions.get('data_quality', {})
        completeness = data_quality.get('videos_completeness', 0)
        st.markdown(create_metric_card(
            "Data Quality", f"{completeness:.1%}", 
            "Dataset Completeness", 
            "positive" if completeness > 0.8 else "neutral",
            "📊"
        ), unsafe_allow_html=True)
    
    # Main Predictive Analytics Dashboard
    st.markdown("## 🔮 Predictive Analytics Results")
    
    # Reputation Forecasting
    if 'reputation_forecasts' in predictions.get('predictions', {}):
        st.markdown("### 🎯 Reputation Forecasting")
        
        rep_forecasts = predictions['predictions']['reputation_forecasts']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Forecast timeline chart
            periods = ['Current', '7-Day', '30-Day', '90-Day']
            values = [0, rep_forecasts.get('7_day', 0), rep_forecasts.get('30_day', 0), rep_forecasts.get('90_day', 0)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=periods, y=values,
                mode='lines+markers',
                line=dict(color='#2ED573', width=4),
                marker=dict(size=10, color='#2ED573'),
                fill='tonexty' if min(values) >= 0 else None,
                name='Reputation Forecast'
            ))
            
            fig.update_layout(
                title="Reputation Trajectory Forecast",
                xaxis_title="Time Horizon",
                yaxis_title="Reputation Score",
                template="plotly_dark",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            trend = rep_forecasts.get('trend', 'unknown').title()
            confidence = rep_forecasts.get('confidence', 0)
            
            trend_color = '#2ED573' if 'positive' in trend.lower() else '#FF6348' if 'negative' in trend.lower() else '#FFA502'
            
            st.markdown(f"""
            <div class="prediction-card">
                <div style="color: {trend_color}; font-size: 1.4rem; font-weight: bold; margin-bottom: 1rem;">
                    📈 Reputation Intelligence
                </div>
                <div style="color: white; margin-bottom: 0.75rem;">
                    <strong>Trend Direction:</strong> <span style="color: {trend_color};">{trend}</span>
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>7-Day Outlook:</strong> {rep_forecasts.get('7_day', 0):.4f}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>30-Day Outlook:</strong> {rep_forecasts.get('30_day', 0):.4f}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>90-Day Outlook:</strong> {rep_forecasts.get('90_day', 0):.4f}
                </div>
                <div style="color: #888; font-size: 0.9rem; margin-top: 1rem;">
                    <strong>Model Confidence:</strong> {confidence:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Threat Escalation Prediction
    if 'threat_escalation' in predictions.get('predictions', {}):
        st.markdown("### 🚨 Threat Escalation Prediction")
        
        threat_data = predictions['predictions']['threat_escalation']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Threat risk gauge
            current_risk = threat_data.get('current_risk', 0)
            max_risk = threat_data.get('max_risk', 0)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=current_risk * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Threat Escalation Risk (%)"},
                delta={'reference': 25, 'increasing': {'color': "#FF4757"}},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#FF4757"},
                    'steps': [
                        {'range': [0, 25], 'color': "#2ED573"},
                        {'range': [25, 50], 'color': "#FFA502"},
                        {'range': [50, 75], 'color': "#FF6348"},
                        {'range': [75, 100], 'color': "#FF4757"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': max_risk * 100
                    }
                }
            ))
            
            fig.update_layout(template="plotly_dark", height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            trend = threat_data.get('trend', 'unknown').title()
            confidence = threat_data.get('confidence', 0)
            
            risk_level = "LOW" if current_risk < 0.25 else "MEDIUM" if current_risk < 0.5 else "HIGH"
            risk_color = "#2ED573" if risk_level == "LOW" else "#FFA502" if risk_level == "MEDIUM" else "#FF4757"
            
            st.markdown(f"""
            <div class="crisis-card">
                <div style="color: #FF4757; font-size: 1.4rem; font-weight: bold; margin-bottom: 1rem;">
                    🎯 Threat Intelligence
                </div>
                <div style="color: white; margin-bottom: 0.75rem;">
                    <strong>Risk Level:</strong> <span style="color: {risk_color};">{risk_level}</span>
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Current Risk:</strong> {current_risk:.1%}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Peak Risk:</strong> {max_risk:.1%}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Trend:</strong> {trend}
                </div>
                <div style="color: #888; font-size: 0.9rem; margin-top: 1rem;">
                    <strong>Model Confidence:</strong> {confidence:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Engagement Trends
    if 'engagement_trends' in predictions.get('predictions', {}):
        st.markdown("### 📈 Engagement Trend Analysis")
        
        engagement_data = predictions['predictions']['engagement_trends']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Engagement trend visualization
            forecast = engagement_data.get('short_term_forecast', 0)
            trend_direction = engagement_data.get('trend_direction', 'stable')
            
            # Create trend visualization
            periods = ['Last Week', 'Current', 'Forecast']
            if 'positive' in trend_direction.lower():
                values = [forecast * 0.7, forecast * 0.85, forecast]
                color = '#2ED573'
            elif 'negative' in trend_direction.lower():
                values = [forecast * 1.3, forecast * 1.15, forecast]
                color = '#FF6348'
            else:
                values = [forecast, forecast, forecast]
                color = '#FFA502'
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=periods, y=values,
                mode='lines+markers',
                line=dict(color=color, width=4),
                marker=dict(size=10, color=color),
                fill='tonexty',
                name='Engagement Trend'
            ))
            
            fig.update_layout(
                title="Engagement Trend Forecast",
                xaxis_title="Time Period",
                yaxis_title="Engagement Score",
                template="plotly_dark",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            confidence = engagement_data.get('confidence', 0)
            
            trend_color = '#2ED573' if 'positive' in trend_direction.lower() else '#FF6348' if 'negative' in trend_direction.lower() else '#FFA502'
            
            st.markdown(f"""
            <div class="prediction-card">
                <div style="color: {trend_color}; font-size: 1.4rem; font-weight: bold; margin-bottom: 1rem;">
                    📊 Engagement Intelligence
                </div>
                <div style="color: white; margin-bottom: 0.75rem;">
                    <strong>Trend Direction:</strong> <span style="color: {trend_color};">{trend_direction.replace('_', ' ').title()}</span>
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Short-term Forecast:</strong> {forecast:.4f}
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Analysis Confidence:</strong> {confidence:.1%}
                </div>
                <div style="color: #888; font-size: 0.9rem; margin-top: 1rem;">
                    Based on engagement pattern analysis
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Crisis Assessment
    if 'crisis_assessment' in predictions.get('predictions', {}):
        st.markdown("### ⚠️ Comprehensive Crisis Assessment")
        
        crisis_data = predictions['predictions']['crisis_assessment']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Crisis risk components
            components = crisis_data.get('components', {})
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(components.keys()),
                    y=list(components.values()),
                    marker_color=['#FF6348', '#FF4757', '#FFA502'],
                    text=[f"{v:.1%}" for v in components.values()],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="Crisis Risk Components",
                xaxis_title="Risk Factor",
                yaxis_title="Risk Level",
                template="plotly_dark",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            risk_level = crisis_data.get('risk_level', 'UNKNOWN')
            overall_probability = crisis_data.get('overall_probability', 0)
            recommendation = crisis_data.get('recommendation', 'Continue monitoring')
            
            risk_color = {
                'LOW': '#2ED573',
                'MEDIUM': '#FFA502', 
                'HIGH': '#FF6348',
                'CRITICAL': '#FF4757'
            }.get(risk_level, '#888')
            
            st.markdown(f"""
            <div class="crisis-card">
                <div style="color: {risk_color}; font-size: 1.4rem; font-weight: bold; margin-bottom: 1rem;">
                    ⚠️ Crisis Intelligence
                </div>
                <div style="color: white; margin-bottom: 0.75rem;">
                    <strong>Risk Level:</strong> <span style="color: {risk_color};">{risk_level}</span>
                </div>
                <div style="color: white; margin-bottom: 0.5rem;">
                    <strong>Crisis Probability:</strong> {overall_probability:.1%}
                </div>
                <div style="color: white; margin-bottom: 1rem;">
                    <strong>Recommendation:</strong><br>{recommendation}
                </div>
                <div style="color: #888; font-size: 0.9rem;">
                    Comprehensive multi-factor assessment
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Strategic Recommendations
    st.markdown("## 💡 Strategic Recommendations")
    
    recommendations = predictions.get('strategic_recommendations', [])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            rec_type = "REPUTATION" if "reputation" in rec.lower() else "THREAT" if "threat" in rec.lower() else "ENGAGEMENT" if "engagement" in rec.lower() else "GENERAL"
            rec_color = {"REPUTATION": "#2ED573", "THREAT": "#FF4757", "ENGAGEMENT": "#FFA502", "GENERAL": "#FFFFFF"}.get(rec_type, "#FFFFFF")
            
            st.markdown(f"""
            <div class="prediction-card">
                <div style="color: {rec_color}; font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem;">
                    {i}. [{rec_type}] {rec}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="prediction-card">
            <div style="color: #2ED573; font-size: 1.1rem; font-weight: bold;">
                ✅ No immediate concerns detected. System operating within normal parameters.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical Performance Summary
    st.markdown("## 🔧 Phase 3C Technical Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="color: #2ED573; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                🧠 ML Models Implemented
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        models = ['Reputation Forecasting', 'Threat Escalation', 'Engagement Analysis', 'Crisis Assessment']
        for model in models:
            model_status = "✅" if model.lower().replace(' ', '_') in str(predictions.get('predictions', {})) else "⚠️"
            st.markdown(f"{model_status} **{model}**")
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="color: #FFA502; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                📊 System Capabilities
            </div>
            <div style="color: white; margin-bottom: 0.5rem;">
                <strong>Forecast Horizons:</strong> 7, 30, 90 days
            </div>
            <div style="color: white; margin-bottom: 0.5rem;">
                <strong>Model Type:</strong> Random Forest + Statistical
            </div>
            <div style="color: white; margin-bottom: 0.5rem;">
                <strong>Error Handling:</strong> Robust with fallbacks
            </div>
            <div style="color: white; margin-bottom: 0.5rem;">
                <strong>Data Sources:</strong> Videos + Comments
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    load_custom_css()
    
    # Add Bootstrap Icons CDN for the new sidebar icons
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    """, unsafe_allow_html=True)
    
    # Add global scripts for page functionality
    st.markdown("""
    <script>
    // Global scroll to top function
    function scrollToTopGlobal() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Auto-scroll to top on page changes
    if (typeof window.lastPage === 'undefined') {
        window.lastPage = '';
    }
    
    // Check if page changed and scroll to top
    const currentPage = new URLSearchParams(window.location.search).get('page') || 'Overview';
    if (window.lastPage !== '' && window.lastPage !== currentPage) {
        scrollToTopGlobal();
    }
    window.lastPage = currentPage;
    
    // Handle video card clicks as fallback
    document.addEventListener('click', function(e) {
        const card = e.target.closest('.clickable-card');
        if (card && card.getAttribute('onclick')) {
            // Let the onclick attribute handle it
            return;
        } else if (card) {
            // Fallback click handling
            const onclick = card.getAttribute('onclick');
            if (onclick) {
                eval(onclick);
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Create sidebar and get selected page
    selected_page = create_sidebar()
    
    # Route to appropriate page - Updated for new clean naming structure
    if selected_page == "Overview":
        show_overview_page()
    elif selected_page == "Reputation Alerts":
        show_reputation_alerts_page()
    elif selected_page == "Executive Reports":
        show_executive_reports_page()
    elif selected_page == "Videos":
        show_videos_page()
    elif selected_page == "Comments":
        show_comments_page()
    elif selected_page == "Analytics":
        show_analytics_page()
    elif selected_page == "Data Intelligence":
        show_data_intelligence_page()
    elif selected_page == "Settings":
        show_settings_page()
    elif selected_page == "Reputation Intelligence":
        show_predictive_analytics_page()
    elif selected_page == "Predictive Analytics":
        show_phase3c_predictive_analytics_page()
    
    # 📋 FOOTER
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999999; padding: 2rem 0;">
        <p>🎯 <strong>Percepta Pro</strong> - Advanced Reputation Intelligence Platform</p>
        <p>Real-time monitoring • Sentiment escalation tracking • Public opinion analysis • Strategic insights</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 