"""
Percepta Pro v2.0 - Sidebar Navigation Component
Professional sidebar with logo, navigation, and metrics
"""

import streamlit as st
from src.utils.config import load_logo_image, create_metric_card
from src.utils.data_loader import get_data_health_status
from src.utils.analytics import calculate_reputation_score
import sys
sys.path.append('scripts')

def create_sidebar():
    """Create the professional sidebar with navigation and metrics"""
    
    # Load logo
    logo_base64 = load_logo_image()
    
    # Sidebar header with logo
    with st.sidebar:
        if logo_base64:
            st.markdown(f"""
            <div class="sidebar-logo">
                <img src="{logo_base64}" alt="Percepta Pro Logo">
                <h1>PERCEPTA PRO</h1>
                <p>REPUTATION INTELLIGENCE</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sidebar-logo">
                <h1>PERCEPTA PRO</h1>
                <p>REPUTATION INTELLIGENCE</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation section
        st.markdown('<div class="nav-section"><h3>CORE ANALYTICS</h3></div>', unsafe_allow_html=True)
        
        # Navigation buttons with session state
        if st.button("📊 Overview", key="nav_overview", use_container_width=True):
            st.session_state.current_page = "Overview"
        
        if st.button("📈 Analytics", key="nav_analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
        
        if st.button("🎥 Videos", key="nav_videos", use_container_width=True):
            st.session_state.current_page = "Videos"
        
        if st.button("💬 Comments", key="nav_comments", use_container_width=True):
            st.session_state.current_page = "Comments"
        
        # Advanced Analytics section
        st.markdown('<div class="nav-section"><h3>ADVANCED INTELLIGENCE</h3></div>', unsafe_allow_html=True)
        
        if st.button("📊 Data Intelligence", key="nav_data_intelligence", use_container_width=True):
            st.session_state.current_page = "Data Intelligence"
        
        if st.button("🔔 Reputation Alerts", key="nav_reputation_alerts", use_container_width=True):
            st.session_state.current_page = "Reputation Alerts"
        
        if st.button("📋 Executive Reports", key="nav_executive_reports", use_container_width=True):
            st.session_state.current_page = "Executive Reports"
        
        if st.button("🔮 Predictive Analytics", key="nav_predictive_analytics", use_container_width=True):
            st.session_state.current_page = "Predictive Analytics"
        
        # System section
        st.markdown('<div class="nav-section"><h3>SYSTEM</h3></div>', unsafe_allow_html=True)
        
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.session_state.current_page = "Settings"
        
        # System status metrics
        st.markdown('<div class="nav-section"><h3>SYSTEM STATUS</h3></div>', unsafe_allow_html=True)
        
        try:
            # Get data health status
            health_status = get_data_health_status()
            
            # System health indicator
            if health_status['core_data_available']:
                st.markdown(
                    '<div class="metric-container">'
                    '<div style="display: flex; align-items: center; margin-bottom: 0.5rem;">'
                    '<span class="status-indicator status-good"></span>'
                    '<span style="color: #22C55E; font-size: 0.8rem;">SYSTEM OPERATIONAL</span>'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="metric-container">'
                    '<div style="display: flex; align-items: center; margin-bottom: 0.5rem;">'
                    '<span class="status-indicator status-critical"></span>'
                    '<span style="color: #FF4757; font-size: 0.8rem;">SYSTEM OFFLINE</span>'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            
            # Quick metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Videos",
                    health_status['video_count'],
                    help="Total videos monitored"
                )
            with col2:
                st.metric(
                    "Comments", 
                    health_status['comment_count'],
                    help="Total comments analyzed"
                )
            
            # Data quality indicator
            if health_status['processed_data_available']:
                st.metric(
                    "AI Enhanced",
                    f"{health_status['processed_comment_count']:,}",
                    help="Comments with AI sentiment analysis"
                )
        
        except Exception as e:
            st.error(f"Status error: {e}")
        
        # Footer
        st.markdown("""
        <div style="position: fixed; bottom: 1rem; left: 1rem; right: 1rem; text-align: center; color: #666; font-size: 0.7rem;">
            Percepta Pro v2.0<br>
            Reputation Intelligence Platform
        </div>
        """, unsafe_allow_html=True)

def get_current_page():
    """Get the current page from session state"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Overview"
    return st.session_state.current_page

def set_current_page(page_name: str):
    """Set the current page in session state"""
    st.session_state.current_page = page_name 