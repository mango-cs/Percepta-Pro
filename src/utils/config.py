"""
Percepta Pro v2.0 - Configuration and Styling Utilities
Central configuration for the reputation intelligence platform
"""

import streamlit as st
import base64
import os
from pathlib import Path

# 🎨 CRIMZON DESIGN SYSTEM CONSTANTS
class Colors:
    CRIMZON_RED = "#FF4757"
    CRIMZON_ORANGE = "#FF6348"
    CRIMZON_SUCCESS = "#22C55E"
    CRIMZON_WARNING = "#FFA502"
    BG_MAIN = "#1A1A1A"
    BG_CARD = "#2D2D2D"
    BG_INTERACTIVE = "#3A3A3A"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#CCCCCC"
    TEXT_MUTED = "#999999"
    BORDER_COLOR = "#404040"

class Config:
    """Application configuration constants"""
    APP_TITLE = "Percepta Pro - Reputation Intelligence"
    APP_ICON = "assets/images/percepta_logo.png"
    LAYOUT = "wide"
    SIDEBAR_STATE = "expanded"
    
    # Data paths
    VIDEOS_DATA_PATH = "backend/data/videos/youtube_videos_final.csv"
    COMMENTS_DATA_PATH = "backend/data/comments/youtube_comments_final.csv"
    PROCESSED_VIDEOS_PATH = "backend/data/videos/youtube_videos_phase2b_ready.csv"
    PROCESSED_COMMENTS_PATH = "backend/data/comments/youtube_comments_ai_enhanced_cleaned.csv"
    ML_READY_VIDEOS_PATH = "backend/data/videos/youtube_videos_ml_ready.csv"
    
    # Scripts paths
    SCRIPTS_DIR = "scripts"
    MODELS_DIR = "scripts/models"
    LOGS_DIR = "scripts/logs"

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout=Config.LAYOUT,
        initial_sidebar_state=Config.SIDEBAR_STATE
    )

def load_logo_image():
    """Load and encode the Percepta Pro logo image"""
    try:
        logo_path = Config.APP_ICON
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode()
                return f"data:image/png;base64,{encoded_image}"
        return None
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        return None

def get_logo_base64():
    """Get base64 encoded logo for display"""
    return load_logo_image()

def load_custom_css():
    """Load the complete Crimzon dark theme CSS"""
    st.markdown(f"""
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Variables - Crimzon Design System */
    :root {{
        --crimzon-red: {Colors.CRIMZON_RED};
        --crimzon-orange: {Colors.CRIMZON_ORANGE};
        --crimzon-success: {Colors.CRIMZON_SUCCESS};
        --crimzon-warning: {Colors.CRIMZON_WARNING};
        --bg-main: {Colors.BG_MAIN};
        --bg-card: {Colors.BG_CARD};
        --bg-interactive: {Colors.BG_INTERACTIVE};
        --text-primary: {Colors.TEXT_PRIMARY};
        --text-secondary: {Colors.TEXT_SECONDARY};
        --text-muted: {Colors.TEXT_MUTED};
        --border-color: {Colors.BORDER_COLOR};
    }}
    
    /* Main App Background */
    .stApp {{
        background: linear-gradient(135deg, var(--bg-main) 0%, #1F1F1F 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    /* Sidebar Styling */
    .css-1d391kg, .stSidebar > div {{
        background: linear-gradient(180deg, var(--bg-card) 0%, #2A2A2A 100%);
        border-right: 2px solid var(--border-color);
        padding: 0 !important;
    }}
    
    .stSidebar .stSelectbox > div > div {{
        background: var(--bg-interactive);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }}
    
    /* Sidebar Logo Area */
    .sidebar-logo {{
        text-align: center;
        padding: 1.5rem 1rem 1.5rem 1rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    
    .sidebar-logo img {{
        width: 80px;
        height: 80px;
        object-fit: contain;
        margin-bottom: 0.75rem;
        filter: brightness(0.9) contrast(1.1);
        transition: all 0.3s ease;
    }}
    
    .sidebar-logo img:hover {{
        filter: brightness(1.1) contrast(1.2);
        transform: scale(1.05);
    }}
    
    .sidebar-logo h1 {{
        color: var(--crimzon-red);
        font-size: 1.4rem;
        margin: 0;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, var(--crimzon-red), var(--crimzon-orange));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .sidebar-logo p {{
        color: var(--text-muted);
        font-size: 0.7rem;
        margin: 0.25rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: center;
    }}
    
    /* Navigation Menu Styling */
    .nav-section {{
        margin-bottom: 1.5rem;
        padding: 0 1rem;
    }}
    
    .nav-section h3 {{
        color: var(--text-muted);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        text-align: left;
        font-weight: 600;
    }}
    
    /* Navigation Button Styling */
    .stSidebar .stButton > button {{
        background: rgba(58, 58, 58, 0.5) !important;
        color: white !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
        width: 100% !important;
        text-align: left !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        height: auto !important;
        min-height: 3rem !important;
        justify-content: flex-start !important;
    }}
    
    .stSidebar .stButton > button:hover {{
        background: rgba(255, 71, 87, 0.2) !important;
        border-color: #FF4757 !important;
        transform: translateX(2px) !important;
        box-shadow: 0 2px 8px rgba(255, 71, 87, 0.2) !important;
    }}
    
    /* Custom Card Styling */
    .metric-card {{
        background: linear-gradient(135deg, var(--bg-card) 0%, #323232 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 71, 87, 0.15);
        border-color: var(--crimzon-red);
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0.5rem 0;
        line-height: 1;
    }}
    
    .metric-label {{
        font-size: 0.875rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }}
    
    .metric-change {{
        font-size: 0.75rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }}
    
    .metric-change.positive {{
        color: var(--crimzon-success);
    }}
    
    .metric-change.negative {{
        color: var(--crimzon-red);
    }}
    
    /* Page Title Styling */
    .page-title {{
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, var(--crimzon-red), var(--crimzon-orange));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .page-subtitle {{
        font-size: 1.125rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }}
    
    /* Alert Styling */
    .reputation-alert {{
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 99, 72, 0.05) 100%);
        border: 1px solid rgba(255, 71, 87, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }}
    
    .alert-critical {{
        border-color: var(--crimzon-red);
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.15) 0%, rgba(255, 71, 87, 0.05) 100%);
    }}
    
    /* Status Indicators */
    .status-indicator {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    
    .status-critical {{ background-color: var(--crimzon-red); }}
    .status-warning {{ background-color: var(--crimzon-warning); }}
    .status-good {{ background-color: var(--crimzon-success); }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    footer {{visibility: hidden;}}
    
    /* Custom Button Styling */
    .stButton > button {{
        background: linear-gradient(45deg, var(--crimzon-red), var(--crimzon-orange));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
    }}
    
    /* Status Badge */
    .status-badge {{
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }}
    
    .status-positive {{
        background: rgba(46, 213, 115, 0.2);
        color: var(--crimzon-success);
        border: 1px solid var(--crimzon-success);
    }}
    
    .status-negative {{
        background: rgba(255, 71, 87, 0.2);
        color: var(--crimzon-red);
        border: 1px solid var(--crimzon-red);
    }}
    
    .status-neutral {{
        background: rgba(255, 165, 2, 0.2);
        color: var(--crimzon-warning);
        border: 1px solid var(--crimzon-warning);
    }}
    
    /* Predictive Analytics Styles */
    .prediction-card {{
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 2px solid #2ED573;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }}
    
    .crisis-card {{
        background: linear-gradient(135deg, #2a1a1a 0%, #3d2d2d 100%);
        border: 2px solid #FFA502;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }}
    
    .forecast-timeline {{
        background: rgba(46, 213, 115, 0.1);
        border-left: 4px solid #2ED573;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, change=None, change_type="neutral", icon="📊"):
    """Create a professional metric card with Crimzon styling"""
    change_class = f"metric-change {change_type}" if change else ""
    change_html = f'<div class="{change_class}">{change}</div>' if change else ""
    
    return f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <span class="metric-label">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
        {change_html}
    </div>
    """ 