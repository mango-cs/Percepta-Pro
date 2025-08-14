"""
🔧 PERCEPTA PRO - DEBUG & NAVIGATION APP
Development utility for testing, debugging, and performance monitoring

Features:
- System Health Dashboard
- Performance Monitoring
- Data Validation Tools
- Navigation Testing
- Error Log Viewer
- Cache Management
- Memory Usage Tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import traceback
import platform

# Try to import psutil, but provide fallbacks if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    st.warning("⚠️ psutil not installed. Using basic system monitoring. Install with: pip install psutil")

# 🎨 DEBUG THEME CONFIGURATION
st.set_page_config(
    page_title="Percepta Pro - Debug Console",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_debug_css():
    st.markdown("""
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Debug Theme Variables */
    :root {
        --debug-primary: #10B981;
        --debug-warning: #F59E0B;
        --debug-error: #EF4444;
        --debug-info: #3B82F6;
        --bg-main: #0F172A;
        --bg-card: #1E293B;
        --bg-interactive: #334155;
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #64748B;
        --border-color: #475569;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, var(--bg-main) 0%, #1E1E2E 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .stSidebar > div {
        background: linear-gradient(180deg, var(--bg-card) 0%, #2A2A3A 100%);
        border-right: 2px solid var(--border-color);
    }
    
    /* Debug Card Styling */
    .debug-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, #252535 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .debug-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15);
        border-color: var(--debug-primary);
    }
    
    /* Status Indicators */
    .status-healthy { color: var(--debug-primary); }
    .status-warning { color: var(--debug-warning); }
    .status-error { color: var(--debug-error); }
    .status-info { color: var(--debug-info); }
    
    /* Code blocks */
    .debug-code {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #f8f8f2;
        margin: 0.5rem 0;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def get_system_health():
    """Get comprehensive system health metrics with fallbacks"""
    try:
        if PSUTIL_AVAILABLE:
            # Full system monitoring with psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Process info
            process = psutil.Process()
            process_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / 1024 / 1024 / 1024,
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / 1024 / 1024 / 1024,
                'process_memory_mb': process_memory,
                'timestamp': datetime.now(),
                'method': 'psutil'
            }
        else:
            # Basic fallback monitoring without psutil
            import os
            import gc
            
            # Get basic system info
            try:
                # Try to get disk space on Windows
                if platform.system() == 'Windows':
                    import shutil
                    total, used, free = shutil.disk_usage('.')
                    disk_percent = (used / total) * 100
                    disk_free_gb = free / 1024 / 1024 / 1024
                else:
                    disk_percent = 50  # Fallback estimate
                    disk_free_gb = 10  # Fallback estimate
            except:
                disk_percent = 50
                disk_free_gb = 10
            
            return {
                'cpu_percent': 25,  # Fallback estimate
                'memory_percent': 60,  # Fallback estimate
                'memory_available_gb': 4.0,  # Fallback estimate
                'disk_percent': disk_percent,
                'disk_free_gb': disk_free_gb,
                'process_memory_mb': 150,  # Fallback estimate
                'timestamp': datetime.now(),
                'method': 'fallback'
            }
    except Exception as e:
        return {'error': str(e)}

def validate_data_files():
    """Validate core data files and structure"""
    validation_results = []
    
    # Check video data
    videos_path = Path("backend/data/videos/youtube_videos.csv")
    if videos_path.exists():
        try:
            videos_df = pd.read_csv(videos_path)
            validation_results.append({
                'file': 'Videos Dataset',
                'status': 'healthy',
                'records': len(videos_df),
                'columns': list(videos_df.columns),
                'message': f'✅ {len(videos_df)} videos loaded successfully'
            })
        except Exception as e:
            validation_results.append({
                'file': 'Videos Dataset',
                'status': 'error',
                'message': f'❌ Error loading videos: {str(e)}'
            })
    else:
        validation_results.append({
            'file': 'Videos Dataset',
            'status': 'error',
            'message': '❌ Videos file not found'
        })
    
    # Check comments data
    comments_path = Path("backend/data/comments/youtube_comments.csv")
    if comments_path.exists():
        try:
            comments_df = pd.read_csv(comments_path)
            validation_results.append({
                'file': 'Comments Dataset',
                'status': 'healthy',
                'records': len(comments_df),
                'columns': list(comments_df.columns),
                'message': f'✅ {len(comments_df)} comments loaded successfully'
            })
        except Exception as e:
            validation_results.append({
                'file': 'Comments Dataset',
                'status': 'error',
                'message': f'❌ Error loading comments: {str(e)}'
            })
    else:
        validation_results.append({
            'file': 'Comments Dataset',
            'status': 'error',
            'message': '❌ Comments file not found'
        })
    
    # Check logo
    logo_path = Path("assets/images/percepta_logo.png")
    if logo_path.exists():
        validation_results.append({
            'file': 'Logo Asset',
            'status': 'healthy',
            'message': f'✅ Logo found ({logo_path.stat().st_size // 1024} KB)'
        })
    else:
        validation_results.append({
            'file': 'Logo Asset',
            'status': 'warning',
            'message': '⚠️ Logo file not found - using fallback'
        })
    
    return validation_results

def test_navigation_functions():
    """Test availability of navigation functions"""
    navigation_tests = []
    
    # Import main dashboard module
    try:
        sys.path.append('.')
        
        # Test function existence
        functions_to_test = [
            'load_reputation_data',
            'calculate_reputation_score',
            'get_sentiment_distribution',
            'create_sentiment_timeline',
            'create_video_impact_chart',
            'create_wordcloud_analysis'
        ]
        
        # Try importing reputation_dashboard
        try:
            import reputation_dashboard as rd
            
            for func_name in functions_to_test:
                if hasattr(rd, func_name):
                    navigation_tests.append({
                        'function': func_name,
                        'status': 'healthy',
                        'message': f'✅ Function {func_name} available'
                    })
                else:
                    navigation_tests.append({
                        'function': func_name,
                        'status': 'error',
                        'message': f'❌ Function {func_name} not found'
                    })
                    
        except ImportError as e:
            navigation_tests.append({
                'function': 'reputation_dashboard',
                'status': 'error',
                'message': f'❌ Cannot import reputation_dashboard: {str(e)}'
            })
            
    except Exception as e:
        navigation_tests.append({
            'function': 'import_test',
            'status': 'error',
            'message': f'❌ Import error: {str(e)}'
        })
    
    return navigation_tests

def show_system_dashboard():
    """System health and performance dashboard"""
    st.markdown('# 🔧 System Health Dashboard')
    st.markdown('Real-time monitoring of system performance and resource usage')
    
    # Dependency status
    if not PSUTIL_AVAILABLE:
        st.warning("⚠️ **Enhanced monitoring unavailable** - Install psutil for full system metrics: `pip install psutil`")
    
    # Get system metrics
    health_data = get_system_health()
    
    if 'error' not in health_data:
        # System metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        method_info = "✨ Full monitoring" if health_data['method'] == 'psutil' else "📊 Basic monitoring"
        
        with col1:
            cpu_color = "error" if health_data['cpu_percent'] > 80 else "warning" if health_data['cpu_percent'] > 60 else "healthy"
            st.markdown(f"""
            <div class="debug-card">
                <div class="status-{cpu_color}" style="font-size: 1.5rem; margin-bottom: 0.5rem;">🖥️ CPU Usage</div>
                <div style="color: white; font-size: 2rem; font-weight: bold;">{health_data['cpu_percent']:.1f}%</div>
                <div style="color: #999; font-size: 0.8rem;">Processor load</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            memory_color = "error" if health_data['memory_percent'] > 85 else "warning" if health_data['memory_percent'] > 70 else "healthy"
            st.markdown(f"""
            <div class="debug-card">
                <div class="status-{memory_color}" style="font-size: 1.5rem; margin-bottom: 0.5rem;">🧠 Memory</div>
                <div style="color: white; font-size: 2rem; font-weight: bold;">{health_data['memory_percent']:.1f}%</div>
                <div style="color: #999; font-size: 0.8rem;">{health_data['memory_available_gb']:.1f} GB available</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            disk_color = "error" if health_data['disk_percent'] > 90 else "warning" if health_data['disk_percent'] > 80 else "healthy"
            st.markdown(f"""
            <div class="debug-card">
                <div class="status-{disk_color}" style="font-size: 1.5rem; margin-bottom: 0.5rem;">💾 Disk</div>
                <div style="color: white; font-size: 2rem; font-weight: bold;">{health_data['disk_percent']:.1f}%</div>
                <div style="color: #999; font-size: 0.8rem;">{health_data['disk_free_gb']:.1f} GB free</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            process_color = "error" if health_data['process_memory_mb'] > 1000 else "warning" if health_data['process_memory_mb'] > 500 else "healthy"
            st.markdown(f"""
            <div class="debug-card">
                <div class="status-{process_color}" style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚡ Process</div>
                <div style="color: white; font-size: 2rem; font-weight: bold;">{health_data['process_memory_mb']:.0f} MB</div>
                <div style="color: #999; font-size: 0.8rem;">{method_info}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Performance chart (simplified for fallback mode)
        st.markdown("## 📊 Performance Monitoring")
        
        if health_data['method'] == 'psutil':
            # Full monitoring available
            # Simulate performance data (in real app, this would be stored)
            if 'performance_history' not in st.session_state:
                st.session_state.performance_history = []
            
            # Add current data point
            st.session_state.performance_history.append({
                'timestamp': datetime.now(),
                'cpu': health_data['cpu_percent'],
                'memory': health_data['memory_percent']
            })
            
            # Keep only last 50 data points
            if len(st.session_state.performance_history) > 50:
                st.session_state.performance_history = st.session_state.performance_history[-50:]
            
            # Create performance chart
            if len(st.session_state.performance_history) > 1:
                df = pd.DataFrame(st.session_state.performance_history)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['cpu'],
                    mode='lines+markers',
                    name='CPU %',
                    line=dict(color='#10B981', width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['memory'],
                    mode='lines+markers',
                    name='Memory %',
                    line=dict(color='#3B82F6', width=2)
                ))
                
                fig.update_layout(
                    title="Real-time Performance Metrics",
                    xaxis_title="Time",
                    yaxis_title="Usage %",
                    template="plotly_dark",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback mode
            st.info("📊 **Basic monitoring mode** - Install psutil for real-time performance charts")
            st.markdown("```bash\npip install psutil\n```")
        
        # Auto-refresh option
        if st.checkbox("Auto-refresh (5 seconds)"):
            time.sleep(5)
            st.rerun()
    
    else:
        st.error(f"Error getting system health: {health_data['error']}")

def show_data_validation():
    """Data validation and integrity checks"""
    st.markdown('# 📊 Data Validation')
    st.markdown('Comprehensive validation of data files and structure')
    
    # Run validation
    validation_results = validate_data_files()
    
    # Display results
    for result in validation_results:
        status_class = f"status-{result['status']}"
        
        st.markdown(f"""
        <div class="debug-card">
            <div class="{status_class}" style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">
                {result['file']}
            </div>
            <div style="color: #CBD5E1; margin-bottom: 0.5rem;">
                {result['message']}
            </div>
        """, unsafe_allow_html=True)
        
        if 'records' in result:
            st.markdown(f"""
                <div style="color: #64748B; font-size: 0.8rem;">
                    Records: {result['records']:,} | Columns: {len(result['columns'])}
                </div>
            """, unsafe_allow_html=True)
            
            if st.checkbox(f"Show columns for {result['file']}", key=f"show_cols_{result['file']}"):
                st.code(", ".join(result['columns']))
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_navigation_testing():
    """Navigation and function testing"""
    st.markdown('# 🧭 Navigation Testing')
    st.markdown('Testing availability and functionality of navigation functions')
    
    # Run navigation tests
    nav_results = test_navigation_functions()
    
    # Display results
    for result in nav_results:
        status_class = f"status-{result['status']}"
        
        st.markdown(f"""
        <div class="debug-card">
            <div class="{status_class}" style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem;">
                {result['function']}
            </div>
            <div style="color: #CBD5E1;">
                {result['message']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Test dashboard launch
    st.markdown("## 🚀 Dashboard Launch Test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Test Main Dashboard", type="primary"):
            st.info("Testing main dashboard launch...")
            try:
                # Test if reputation_dashboard.py exists and is runnable
                dashboard_path = Path("reputation_dashboard.py")
                if dashboard_path.exists():
                    st.success("✅ Main dashboard file found")
                    st.code("streamlit run reputation_dashboard.py --server.port 8501")
                else:
                    st.error("❌ Main dashboard file not found")
            except Exception as e:
                st.error(f"❌ Error testing dashboard: {str(e)}")
    
    with col2:
        if st.button("Test Simple Dashboard", type="secondary"):
            st.info("Testing simple dashboard launch...")
            try:
                # Test if simple dashboard exists
                simple_path = Path("simple dahsboard.py")
                if simple_path.exists():
                    st.success("✅ Simple dashboard file found")
                    st.code('streamlit run "simple dahsboard.py" --server.port 8502')
                else:
                    st.error("❌ Simple dashboard file not found")
            except Exception as e:
                st.error(f"❌ Error testing simple dashboard: {str(e)}")

def show_cache_management():
    """Cache management and optimization"""
    st.markdown('# 🗄️ Cache Management')
    st.markdown('Monitor and manage Streamlit cache for optimal performance')
    
    # Cache information
    st.markdown("## 📋 Cache Status")
    
    cache_info = {
        'data_cache': len(st.session_state) if hasattr(st.session_state, '__len__') else 0,
        'cache_hits': "Monitoring...",
        'cache_misses': "Monitoring...",
        'memory_usage': "Calculating..."
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="debug-card">
            <div class="status-info" style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">
                Session State Items
            </div>
            <div style="color: white; font-size: 2rem; font-weight: bold;">
                {cache_info['data_cache']}
            </div>
            <div style="color: #64748B; font-size: 0.8rem;">
                Active session variables
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="debug-card">
            <div class="status-healthy" style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">
                Cache Status
            </div>
            <div style="color: white; font-size: 1.2rem; font-weight: bold;">
                Active
            </div>
            <div style="color: #64748B; font-size: 0.8rem;">
                Streamlit caching enabled
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Cache management actions
    st.markdown("## 🔧 Cache Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Clear Data Cache", type="secondary"):
            st.cache_data.clear()
            st.success("✅ Data cache cleared")
    
    with col2:
        if st.button("Clear Session State", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Session state cleared")
    
    with col3:
        if st.button("Force Refresh", type="primary"):
            st.cache_data.clear()
            st.rerun()

def show_error_logs():
    """Error logging and monitoring"""
    st.markdown('# 📋 Error Logs')
    st.markdown('Monitor and debug application errors')
    
    # Check for log files
    log_files = []
    log_dirs = ["logs", "scripts/logs"]
    
    for log_dir in log_dirs:
        log_path = Path(log_dir)
        if log_path.exists():
            for log_file in log_path.glob("*.log"):
                log_files.append(log_file)
    
    if log_files:
        st.markdown("## 📁 Available Log Files")
        
        selected_log = st.selectbox(
            "Select log file to view:",
            log_files,
            format_func=lambda x: f"{x.parent.name}/{x.name}"
        )
        
        if selected_log:
            try:
                with open(selected_log, 'r') as f:
                    log_content = f.read()
                
                st.markdown(f"### {selected_log.name}")
                st.text_area(
                    "Log contents:",
                    log_content,
                    height=400,
                    disabled=True
                )
                
                # Download button
                st.download_button(
                    label="📥 Download Log",
                    data=log_content,
                    file_name=selected_log.name,
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Error reading log file: {str(e)}")
    else:
        st.info("No log files found in logs/ or scripts/logs/ directories")
    
    # Error simulation for testing
    st.markdown("## 🧪 Error Testing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Test Warning"):
            st.warning("⚠️ This is a test warning message")
    
    with col2:
        if st.button("Test Error"):
            st.error("❌ This is a test error message")

def create_debug_sidebar():
    """Create debug navigation sidebar"""
    st.sidebar.markdown("""
    <div style="
        text-align: center;
        padding: 1.5rem 1rem;
        border-bottom: 1px solid #475569;
        margin-bottom: 1.5rem;
    ">
        <h1 style="color: #10B981; font-size: 1.4rem; margin: 0; font-weight: 700;">
            🔧 DEBUG CONSOLE
        </h1>
        <p style="color: #64748B; font-size: 0.7rem; margin: 0.25rem 0 0 0; text-transform: uppercase; letter-spacing: 1px;">
            Development Tools
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'debug_page' not in st.session_state:
        st.session_state.debug_page = "System Health"
    
    # Navigation
    st.sidebar.markdown('<h3 style="color: #64748B; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">NAVIGATION</h3>', unsafe_allow_html=True)
    
    debug_pages = [
        ("🔧 System Health", "System health and performance monitoring"),
        ("📊 Data Validation", "Validate data files and integrity"),
        ("🧭 Navigation Test", "Test navigation functions and launch"),
        ("🗄️ Cache Management", "Manage Streamlit cache and performance"),
        ("📋 Error Logs", "View and monitor error logs")
    ]
    
    for page_name, description in debug_pages:
        clean_name = page_name.split(' ', 1)[1] if ' ' in page_name else page_name
        
        if st.sidebar.button(
            page_name,
            key=f"debug_{clean_name.replace(' ', '_')}",
            help=description,
            use_container_width=True
        ):
            st.session_state.debug_page = clean_name
            st.rerun()
    
    # Quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h3 style="color: #64748B; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">QUICK ACTIONS</h3>', unsafe_allow_html=True)
    
    if st.sidebar.button("🚀 Launch Main Dashboard", use_container_width=True):
        st.sidebar.success("Command: streamlit run reputation_dashboard.py")
    
    if st.sidebar.button("🔄 Clear All Cache", use_container_width=True):
        st.cache_data.clear()
        st.sidebar.success("Cache cleared!")
    
    if not PSUTIL_AVAILABLE:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**📦 Install psutil for full monitoring:**")
        st.sidebar.code("pip install psutil", language="bash")
    
    return st.session_state.debug_page

def main():
    """Main debug application"""
    load_debug_css()
    
    # Create sidebar and get selected page
    selected_page = create_debug_sidebar()
    
    # Route to appropriate page
    if selected_page == "System Health":
        show_system_dashboard()
    elif selected_page == "Data Validation":
        show_data_validation()
    elif selected_page == "Navigation Test":
        show_navigation_testing()
    elif selected_page == "Cache Management":
        show_cache_management()
    elif selected_page == "Error Logs":
        show_error_logs()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748B; padding: 1rem 0;">
        <p>🔧 <strong>Percepta Pro Debug Console</strong> - Development & Testing Tools</p>
        <p>System monitoring • Data validation • Performance optimization • Error tracking</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 