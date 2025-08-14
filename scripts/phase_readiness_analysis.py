#!/usr/bin/env python3
"""
Percepta Pro v2.0 - Phase Readiness Analysis
Comprehensive assessment of system status and next phase readiness
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

def analyze_platform_readiness():
    """
    Comprehensive analysis of platform readiness for next phase
    """
    print('🔍 PERCEPTA PRO v2.0 - COMPREHENSIVE READINESS ANALYSIS')
    print('=' * 65)
    
    try:
        # Load enhanced datasets
        videos_df = pd.read_csv('backend/data/videos/youtube_videos_ai_processed.csv')
        comments_df = pd.read_csv('backend/data/comments/youtube_comments_ai_enhanced.csv')
        print(f'✅ Datasets loaded: {len(videos_df)} videos, {len(comments_df)} comments')
        
        # 1. DATA QUALITY ASSESSMENT
        print('\n📊 DATA QUALITY ASSESSMENT:')
        
        # Video data completeness
        video_completeness = videos_df.notna().mean().mean() * 100
        comment_completeness = comments_df.notna().mean().mean() * 100
        
        print(f'✅ Video Data Completeness: {video_completeness:.1f}%')
        print(f'✅ Comment Data Completeness: {comment_completeness:.1f}%')
        
        # AI enhancement verification
        video_ai_cols = [col for col in videos_df.columns if any(x in col for x in ['Sentiment', 'Keywords', 'Transcript', 'Summary'])]
        comment_ai_cols = [col for col in comments_df.columns if any(x in col for x in ['Sentiment', 'Keywords', 'Threat'])]
        
        print(f'✅ Video AI Features: {len(video_ai_cols)} columns')
        print(f'✅ Comment AI Features: {len(comment_ai_cols)} columns')
        
        # 2. TEMPORAL DATA ANALYSIS
        print('\n📅 TEMPORAL DATA ANALYSIS:')
        
        if 'PublishedAt_Formatted' in videos_df.columns:
            videos_df['Date'] = pd.to_datetime(videos_df['PublishedAt_Formatted'], format='%d-%m-%Y', errors='coerce')
            valid_dates = videos_df['Date'].dropna()
            if len(valid_dates) > 0:
                date_range = valid_dates.max() - valid_dates.min()
                print(f'✅ Data Span: {date_range.days} days ({valid_dates.min().strftime("%d-%m-%Y")} to {valid_dates.max().strftime("%d-%m-%Y")})')
                
                # Monthly distribution
                monthly_counts = valid_dates.dt.to_period('M').value_counts().sort_index()
                print(f'✅ Monthly Distribution: {len(monthly_counts)} months with data')
            else:
                print('⚠️ No valid dates found in dataset')
        
        # 3. ENGAGEMENT METRICS ANALYSIS
        print('\n📈 ENGAGEMENT METRICS ANALYSIS:')
        
        engagement_metrics = ['Views', 'LikeCount', 'CommentCount_API', 'FavoriteCount']
        available_metrics = [col for col in engagement_metrics if col in videos_df.columns]
        
        for metric in available_metrics:
            if metric in videos_df.columns:
                mean_val = videos_df[metric].mean()
                print(f'✅ {metric}: Available (avg: {mean_val:.0f})')
        
        print(f'✅ Total Engagement Metrics: {len(available_metrics)}/{len(engagement_metrics)}')
        
        # 4. BILINGUAL PROCESSING VERIFICATION
        print('\n🌐 BILINGUAL PROCESSING VERIFICATION:')
        
        # Check Telugu and English features
        te_features = [col for col in videos_df.columns if col.endswith('_TE')]
        en_features = [col for col in videos_df.columns if col.endswith('_EN')]
        
        print(f'✅ Telugu Features: {len(te_features)} columns')
        print(f'✅ English Features: {len(en_features)} columns')
        
        # Comment bilingual features
        comment_te_features = [col for col in comments_df.columns if col.endswith('_TE')]
        comment_en_features = [col for col in comments_df.columns if col.endswith('_EN')]
        
        print(f'✅ Comment Telugu Features: {len(comment_te_features)} columns')
        print(f'✅ Comment English Features: {len(comment_en_features)} columns')
        
        # 5. THREAT DETECTION CAPABILITY
        print('\n🚨 THREAT DETECTION CAPABILITY:')
        
        threat_features = [col for col in comments_df.columns if 'threat' in col.lower()]
        print(f'✅ Threat Detection Features: {len(threat_features)} columns')
        
        if 'ThreatDetected' in comments_df.columns:
            total_threats = comments_df['ThreatDetected'].sum()
            threat_rate = (total_threats / len(comments_df)) * 100
            print(f'✅ Threats Detected: {total_threats} ({threat_rate:.1f}% of comments)')
        
        # 6. PREDICTIVE ANALYTICS READINESS ASSESSMENT
        print('\n🎯 PREDICTIVE ANALYTICS READINESS ASSESSMENT:')
        
        readiness_score = 0
        max_score = 10
        
        # Data volume check
        if len(videos_df) >= 150:
            print('✅ Sufficient video volume for ML (150+ videos)')
            readiness_score += 1
        else:
            print(f'⚠️ Limited video volume ({len(videos_df)} videos, 150+ recommended)')
            
        if len(comments_df) >= 1000:
            print('✅ Sufficient comment volume for ML (1000+ comments)')
            readiness_score += 1
        else:
            print(f'⚠️ Limited comment volume ({len(comments_df)} comments, 1000+ recommended)')
        
        # Feature richness
        if len(video_ai_cols) >= 8:
            print('✅ Rich video feature set for ML')
            readiness_score += 1
        else:
            print(f'⚠️ Limited video features ({len(video_ai_cols)} AI columns)')
            
        if len(comment_ai_cols) >= 10:
            print('✅ Rich comment feature set for ML')
            readiness_score += 1
        else:
            print(f'⚠️ Limited comment features ({len(comment_ai_cols)} AI columns)')
        
        # Temporal depth
        if 'Date' in locals() and len(valid_dates) > 0 and date_range.days >= 60:
            print('✅ Sufficient temporal depth for trend analysis (60+ days)')
            readiness_score += 1
        else:
            print('⚠️ Limited temporal depth for robust trend analysis')
            
        # Bilingual completeness
        if len(te_features) >= 3 and len(en_features) >= 3:
            print('✅ Complete bilingual processing capability')
            readiness_score += 1
        else:
            print('⚠️ Incomplete bilingual feature set')
            
        # Engagement metrics
        if len(available_metrics) >= 3:
            print('✅ Comprehensive engagement metrics available')
            readiness_score += 1
        else:
            print('⚠️ Limited engagement metrics for prediction')
            
        # Threat detection
        if len(threat_features) >= 3:
            print('✅ Advanced threat detection features available')
            readiness_score += 1
        else:
            print('⚠️ Basic threat detection features only')
            
        # Data quality
        if video_completeness >= 90 and comment_completeness >= 70:
            print('✅ High data quality for reliable predictions')
            readiness_score += 1
        else:
            print('⚠️ Data quality may affect prediction reliability')
            
        # Integration status
        unique_video_ids = len(set(videos_df['VideoID'].unique()).intersection(set(comments_df['VideoID'].unique())))
        if unique_video_ids >= 30:
            print('✅ Good video-comment integration for cross-analysis')
            readiness_score += 1
        else:
            print(f'⚠️ Limited video-comment integration ({unique_video_ids} linked videos)')
        
        # 7. FINAL ASSESSMENT
        print('\n🎉 FINAL READINESS ASSESSMENT:')
        readiness_percentage = (readiness_score / max_score) * 100
        print(f'📊 Readiness Score: {readiness_score}/{max_score} ({readiness_percentage:.1f}%)')
        
        if readiness_score >= 8:
            print('🚀 EXCELLENT: Ready for advanced Phase 3C implementation')
            recommendation = 'PROCEED'
        elif readiness_score >= 6:
            print('✅ GOOD: Ready for Phase 3C with minor optimizations')
            recommendation = 'PROCEED_WITH_OPTIMIZATION'
        elif readiness_score >= 4:
            print('⚠️ FAIR: Significant improvements needed before Phase 3C')
            recommendation = 'IMPROVE_FIRST'
        else:
            print('❌ POOR: Major foundational work required')
            recommendation = 'MAJOR_IMPROVEMENTS_NEEDED'
        
        # 8. NEXT PHASE RECOMMENDATIONS
        print('\n📋 NEXT PHASE RECOMMENDATIONS:')
        
        if recommendation == 'PROCEED':
            print('🎯 Phase 3C: Predictive Analytics - Full Implementation')
            print('   • Reputation trend forecasting')
            print('   • Threat escalation prediction')
            print('   • Engagement pattern analysis')
            print('   • Crisis probability assessment')
            
        elif recommendation == 'PROCEED_WITH_OPTIMIZATION':
            print('🔧 Phase 3C: Predictive Analytics - With Optimizations')
            print('   • Address data quality gaps')
            print('   • Enhance feature engineering')
            print('   • Improve video-comment integration')
            print('   • Then implement predictive models')
            
        else:
            print('🛠️ Pre-Phase 3C: Foundation Improvements Required')
            print('   • Enhance data collection and quality')
            print('   • Improve AI feature completeness')
            print('   • Strengthen bilingual processing')
            print('   • Optimize system integration')
        
        return {
            'readiness_score': readiness_score,
            'max_score': max_score,
            'percentage': readiness_percentage,
            'recommendation': recommendation,
            'videos_count': len(videos_df),
            'comments_count': len(comments_df),
            'video_ai_features': len(video_ai_cols),
            'comment_ai_features': len(comment_ai_cols)
        }
        
    except Exception as e:
        print(f'❌ Analysis Error: {str(e)}')
        return None

if __name__ == "__main__":
    analysis_result = analyze_platform_readiness()
    if analysis_result:
        print('\n✅ Phase readiness analysis completed successfully')
    else:
        print('\n❌ Phase readiness analysis failed') 