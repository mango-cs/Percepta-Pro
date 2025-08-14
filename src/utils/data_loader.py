"""
Percepta Pro v2.0 - Data Loading Utilities
Centralized data loading and caching for reputation intelligence
"""

import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
import sys
from typing import Tuple, Optional, Dict, Any

# Add scripts directory to path for imports
sys.path.append('scripts')

class DataLoader:
    """Centralized data loading with caching and error handling"""
    
    def __init__(self):
        self.videos_df = None
        self.comments_df = None
        self.processed_videos_df = None
        self.processed_comments_df = None
        self.ml_ready_videos_df = None
        
    @st.cache_data
    def load_reputation_data(_self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load core reputation data with caching"""
        try:
            # Load main datasets
            videos_df = pd.read_csv('backend/data/videos/youtube_videos_final.csv')
            comments_df = pd.read_csv('backend/data/comments/youtube_comments_final.csv')
            
            # Data validation
            if videos_df.empty or comments_df.empty:
                st.warning("⚠️ Core datasets are empty. Please check data sources.")
                return pd.DataFrame(), pd.DataFrame()
            
            # Convert date columns
            if 'Upload_Date' in videos_df.columns:
                videos_df['Upload_Date'] = pd.to_datetime(videos_df['Upload_Date'], errors='coerce')
            if 'Publish_Date' in comments_df.columns:
                comments_df['Publish_Date'] = pd.to_datetime(comments_df['Publish_Date'], errors='coerce')
            
            return videos_df, comments_df
            
        except FileNotFoundError as e:
            st.error(f"❌ Data files not found: {e}")
            return pd.DataFrame(), pd.DataFrame()
        except Exception as e:
            st.error(f"❌ Error loading reputation data: {e}")
            return pd.DataFrame(), pd.DataFrame()
    
    @st.cache_data
    def load_processed_data(_self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load processed Phase 2B data"""
        try:
            videos_df = pd.read_csv('backend/data/videos/youtube_videos_phase2b_ready.csv')
            comments_df = pd.read_csv('backend/data/comments/youtube_comments_ai_enhanced_cleaned.csv')
            
            # Convert date columns
            if 'Upload_Date' in videos_df.columns:
                videos_df['Upload_Date'] = pd.to_datetime(videos_df['Upload_Date'], errors='coerce')
            if 'Publish_Date' in comments_df.columns:
                comments_df['Publish_Date'] = pd.to_datetime(comments_df['Publish_Date'], errors='coerce')
            
            return videos_df, comments_df
            
        except FileNotFoundError:
            st.warning("⚠️ Processed data not found. Using basic datasets.")
            return _self.load_reputation_data()
        except Exception as e:
            st.error(f"❌ Error loading processed data: {e}")
            return pd.DataFrame(), pd.DataFrame()
    
    @st.cache_data
    def load_ml_ready_data(_self) -> pd.DataFrame:
        """Load ML-ready video dataset"""
        try:
            ml_videos_df = pd.read_csv('backend/data/videos/youtube_videos_ml_ready.csv')
            
            # Convert date columns
            if 'Upload_Date' in ml_videos_df.columns:
                ml_videos_df['Upload_Date'] = pd.to_datetime(ml_videos_df['Upload_Date'], errors='coerce')
            
            return ml_videos_df
            
        except FileNotFoundError:
            st.warning("⚠️ ML-ready data not found.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"❌ Error loading ML-ready data: {e}")
            return pd.DataFrame()
    
    @st.cache_data
    def load_phase3c_predictions(_self) -> Optional[Dict[str, Any]]:
        """Load Phase 3C predictive analytics results"""
        try:
            with open('scripts/logs/phase3c_robust_report.json', 'r') as f:
                predictions = json.load(f)
            return predictions
        except FileNotFoundError:
            st.warning("⚠️ Phase 3C predictions not found.")
            return None
        except Exception as e:
            st.error(f"❌ Error loading predictions: {e}")
            return None
    
    @st.cache_data
    def load_reputation_intelligence_report(_self) -> Optional[Dict[str, Any]]:
        """Load reputation intelligence report"""
        try:
            with open('scripts/logs/reputation_intelligence_report.json', 'r') as f:
                report = json.load(f)
            return report
        except FileNotFoundError:
            return None
        except Exception as e:
            st.error(f"❌ Error loading intelligence report: {e}")
            return None
    
    @st.cache_data
    def load_crisis_detection_data(_self) -> Optional[Dict[str, Any]]:
        """Load crisis detection results"""
        try:
            # Import crisis detection engine
            from crisis_detection_engine import CrisisDetectionEngine
            
            # Initialize engine
            engine = CrisisDetectionEngine()
            
            # Load data if available
            videos_df, comments_df = _self.load_processed_data()
            if not videos_df.empty and not comments_df.empty:
                engine.load_data(videos_df, comments_df)
                return engine.get_crisis_status()
            
            return None
            
        except ImportError:
            st.warning("⚠️ Crisis detection engine not available.")
            return None
        except Exception as e:
            st.error(f"❌ Error loading crisis detection: {e}")
            return None
    
    @st.cache_data
    def load_executive_reports(_self) -> Optional[Dict[str, Any]]:
        """Load executive reporting data"""
        try:
            from executive_reporting_engine import ExecutiveReportingEngine
            
            engine = ExecutiveReportingEngine()
            videos_df, comments_df = _self.load_processed_data()
            
            if not videos_df.empty and not comments_df.empty:
                engine.load_data(videos_df, comments_df)
                return engine.generate_executive_summary()
            
            return None
            
        except ImportError:
            st.warning("⚠️ Executive reporting engine not available.")
            return None
        except Exception as e:
            st.error(f"❌ Error loading executive reports: {e}")
            return None

# Global data loader instance
data_loader = DataLoader()

# Convenience functions for backward compatibility
@st.cache_data
def load_reputation_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load core reputation data"""
    return data_loader.load_reputation_data()

@st.cache_data
def load_processed_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load processed data"""
    return data_loader.load_processed_data()

@st.cache_data
def load_ml_ready_data() -> pd.DataFrame:
    """Load ML-ready data"""
    return data_loader.load_ml_ready_data()

@st.cache_data
def load_phase3c_predictions() -> Optional[Dict[str, Any]]:
    """Load Phase 3C predictions"""
    return data_loader.load_phase3c_predictions()

@st.cache_data
def load_reputation_intelligence_report() -> Optional[Dict[str, Any]]:
    """Load reputation intelligence report"""
    return data_loader.load_reputation_intelligence_report()

def get_data_health_status() -> Dict[str, Any]:
    """Get overall data health status"""
    videos_df, comments_df = load_reputation_data()
    processed_videos_df, processed_comments_df = load_processed_data()
    ml_ready_df = load_ml_ready_data()
    
    return {
        'core_data_available': not videos_df.empty and not comments_df.empty,
        'processed_data_available': not processed_videos_df.empty and not processed_comments_df.empty,
        'ml_ready_available': not ml_ready_df.empty,
        'video_count': len(videos_df) if not videos_df.empty else 0,
        'comment_count': len(comments_df) if not comments_df.empty else 0,
        'processed_video_count': len(processed_videos_df) if not processed_videos_df.empty else 0,
        'processed_comment_count': len(processed_comments_df) if not processed_comments_df.empty else 0,
        'ml_ready_count': len(ml_ready_df) if not ml_ready_df.empty else 0
    } 