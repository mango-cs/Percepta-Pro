"""
Minimal toggle component for debug console compatibility
"""

import streamlit as st

def create_html_toggle(default_value: bool = False, key: str = None) -> bool:
    """
    Simple toggle replacement using native Streamlit components
    
    Args:
        default_value: Initial state of the toggle
        key: Unique key for the component
        
    Returns:
        bool: Current state of the toggle
    """
    return st.toggle("Toggle Mode", value=default_value, key=key)

def create_mode_display(is_advanced: bool = False):
    """
    Display current mode status
    
    Args:
        is_advanced: Whether advanced mode is enabled
    """
    mode = "Advanced" if is_advanced else "Basic"
    color = "#22C55E" if is_advanced else "#FFA502"
    
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid {color};
        border-radius: 8px;
        padding: 0.5rem 1rem;
        text-align: center;
        margin: 0.5rem 0;
    ">
        <span style="color: {color}; font-weight: 600; font-size: 0.9rem;">
            🎯 {mode} Mode
        </span>
    </div>
    """, unsafe_allow_html=True) 