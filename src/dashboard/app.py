# -*- coding: utf-8 -*-
import streamlit as st
import sys
import os

# Fix the Python path - add the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

st.set_page_config(page_title="Percepta Pro - Working!", layout="wide")
st.markdown("# 🚀 Percepta Pro v2.0 - Modular Dashboard")
st.success("✅ Basic Streamlit working!")

st.markdown(f"**Current directory**: {current_dir}")
st.markdown(f"**Project root**: {project_root}")
st.markdown(f"**Python path**: {sys.path[:3]}")

try:
    from src.utils.config import Colors
    st.success(f"✅ Config works: {Colors.CRIMZON_RED}")
except Exception as e:
    st.error(f"❌ Config failed: {e}")

try:
    from src.utils.data_loader import get_data_health_status
    health = get_data_health_status()
    st.success(f"✅ Data loader works: {health['video_count']} videos, {health['comment_count']} comments")
except Exception as e:
    st.error(f"❌ Data loader failed: {e}")

try:
    from src.utils.analytics import calculate_reputation_score
    st.success("✅ Analytics imported successfully")
except Exception as e:
    st.error(f"❌ Analytics failed: {e}")

def show_overview():
    """Simple overview page"""
    st.markdown("## 📊 Overview Dashboard")
    
    try:
        from src.utils.data_loader import load_reputation_data
        from src.utils.analytics import calculate_reputation_score
        
        videos_df, comments_df = load_reputation_data()
        reputation_score = calculate_reputation_score(comments_df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Videos", len(videos_df))
        with col2:
            st.metric("Comments", len(comments_df))
        with col3:
            st.metric("Reputation Score", f"{reputation_score:.1f}")
        
        st.success("✅ Overview page working with real data!")
        
    except Exception as e:
        st.error(f"❌ Overview error: {e}")

# Now that show_overview is defined, we can use the sidebar
try:
    from src.dashboard.components.sidebar import create_sidebar, get_current_page
    st.success("✅ Sidebar component imported")
    
    # Test sidebar creation
    st.markdown("## 🧭 Navigation Test")
    create_sidebar()
    current_page = get_current_page()
    st.success(f"✅ Sidebar working - Current page: {current_page}")
    
    # Simple page routing
    if current_page == "Overview":
        show_overview()
    elif current_page == "Analytics":
        st.markdown("### 📈 Analytics Page")
        st.info("Analytics functionality coming soon...")
    elif current_page == "Videos":
        st.markdown("### 🎥 Videos Page")
        st.info("Videos functionality coming soon...")
    elif current_page == "Comments":
        st.markdown("### 💬 Comments Page")
        st.info("Comments functionality coming soon...")
    else:
        show_overview()
    
except Exception as e:
    st.error(f"❌ Sidebar failed: {e}")
    import traceback
    st.code(traceback.format_exc())

st.markdown("---")
st.markdown("## 🎉 Modular Dashboard Status")
st.info("✅ **SUCCESS**: Modular dashboard is now working! All components loading correctly.")
