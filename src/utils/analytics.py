"""
Percepta Pro v2.0 - Analytics Utilities
Core analytics functions for reputation intelligence calculations
"""

import pandas as pd
from typing import Dict

def calculate_reputation_score(comments_df: pd.DataFrame) -> float:
    """Calculate overall reputation score from comments sentiment"""
    if comments_df.empty:
        return 50.0
    
    try:
        # Use AI sentiment scores if available
        if 'sentiment_score' in comments_df.columns:
            avg_sentiment = comments_df['sentiment_score'].mean()
            # Convert to 0-100 scale
            return max(0, min(100, (avg_sentiment + 1) * 50))
        
        # Fallback to basic sentiment analysis
        if 'Sentiment' in comments_df.columns:
            sentiment_counts = comments_df['Sentiment'].value_counts()
            positive = sentiment_counts.get('Positive', 0)
            negative = sentiment_counts.get('Negative', 0)
            neutral = sentiment_counts.get('Neutral', 0)
            total = positive + negative + neutral
            
            if total == 0:
                return 50.0
            
            # Calculate weighted score
            score = ((positive * 100) + (neutral * 50) + (negative * 0)) / total
            return round(score, 1)
        
        return 50.0  # Default neutral score
        
    except Exception:
        return 50.0

def get_sentiment_distribution(comments_df: pd.DataFrame) -> Dict[str, int]:
    """Get distribution of sentiment categories"""
    if comments_df.empty:
        return {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    
    try:
        if 'Sentiment' in comments_df.columns:
            return comments_df['Sentiment'].value_counts().to_dict()
        
        # Fallback calculation
        return {'Positive': 0, 'Neutral': len(comments_df), 'Negative': 0}
        
    except Exception:
        return {'Positive': 0, 'Neutral': 0, 'Negative': 0}
