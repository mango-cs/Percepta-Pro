"""
📊 EXECUTIVE REPORTING ENGINE - Phase 3B
Automated Intelligence Briefings for Percepta Pro v2.0

Generates executive-level reports, strategic insights, and automated briefings
with comprehensive reputation intelligence and predictive analytics.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple, Optional
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/executive_reporting.log'),
        logging.StreamHandler()
    ]
)

class ExecutiveReportingEngine:
    """
    Advanced Executive Reporting Engine for Reputation Intelligence
    
    Features:
    - Automated intelligence briefings
    - Executive summary reports
    - Predictive analytics and forecasting
    - Strategic recommendations
    - Trend analysis and insights
    - Performance metrics and KPIs
    """
    
    def __init__(self):
        """Initialize executive reporting engine"""
        self.logger = logging.getLogger(__name__)
        
        # Report templates and configurations
        self.report_templates = {
            'daily_briefing': {
                'title': '📊 Daily Intelligence Briefing',
                'sections': ['executive_summary', 'threat_assessment', 'sentiment_analysis', 'recommendations'],
                'priority': 'HIGH',
                'frequency': 'daily'
            },
            'weekly_intelligence': {
                'title': '📈 Weekly Intelligence Report',
                'sections': ['executive_summary', 'trend_analysis', 'threat_assessment', 'performance_metrics', 'strategic_insights'],
                'priority': 'CRITICAL',
                'frequency': 'weekly'
            },
            'crisis_briefing': {
                'title': '🚨 Crisis Management Briefing',
                'sections': ['crisis_overview', 'immediate_actions', 'threat_assessment', 'strategic_response'],
                'priority': 'IMMEDIATE',
                'frequency': 'as_needed'
            },
            'executive_dashboard': {
                'title': '🎯 Executive Dashboard Summary',
                'sections': ['key_metrics', 'performance_indicators', 'trend_summary', 'action_items'],
                'priority': 'HIGH',
                'frequency': 'real_time'
            }
        }
        
        # Performance benchmarks
        self.benchmarks = {
            'reputation_score': {'excellent': 80, 'good': 60, 'fair': 40, 'poor': 20},
            'sentiment_score': {'positive': 0.1, 'neutral': -0.1, 'negative': -0.3},
            'engagement_rate': {'high': 10.0, 'medium': 5.0, 'low': 2.0},
            'threat_level': {'critical': 5, 'high': 15, 'medium': 30, 'low': 50}
        }
        
        # Strategic insights categories
        self.insight_categories = [
            'reputation_trends', 'audience_engagement', 'content_performance',
            'threat_landscape', 'competitive_analysis', 'brand_perception'
        ]
        
        self.logger.info("Executive Reporting Engine initialized with automated briefing capabilities")
    
    def generate_daily_briefing(self, videos_df: pd.DataFrame, comments_df: pd.DataFrame, 
                               crisis_data: Dict = None) -> Dict:
        """Generate comprehensive daily intelligence briefing"""
        self.logger.info("Generating daily intelligence briefing")
        
        try:
            briefing = {
                'report_type': 'daily_briefing',
                'generated_at': datetime.now().isoformat(),
                'report_period': {
                    'start_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'end_date': datetime.now().strftime('%Y-%m-%d')
                },
                'executive_summary': {},
                'key_metrics': {},
                'threat_assessment': {},
                'sentiment_analysis': {},
                'recommendations': [],
                'action_items': []
            }
            
            # Executive Summary
            briefing['executive_summary'] = self._generate_executive_summary(videos_df, comments_df, crisis_data)
            
            # Key Performance Metrics
            briefing['key_metrics'] = self._calculate_key_metrics(videos_df, comments_df)
            
            # Threat Assessment
            if crisis_data:
                briefing['threat_assessment'] = self._analyze_threat_landscape(crisis_data)
            
            # Sentiment Analysis
            briefing['sentiment_analysis'] = self._analyze_sentiment_intelligence(comments_df)
            
            # Strategic Recommendations
            briefing['recommendations'] = self._generate_strategic_recommendations(briefing)
            
            # Action Items
            briefing['action_items'] = self._generate_action_items(briefing)
            
            self.logger.info("Daily briefing generated successfully")
            return briefing
            
        except Exception as e:
            self.logger.error(f"Daily briefing generation failed: {e}")
            return {'error': str(e), 'generated_at': datetime.now().isoformat()}
    
    def generate_weekly_intelligence(self, videos_df: pd.DataFrame, comments_df: pd.DataFrame,
                                   crisis_data: Dict = None) -> Dict:
        """Generate comprehensive weekly intelligence report"""
        self.logger.info("Generating weekly intelligence report")
        
        try:
            # Filter data for last 7 days
            week_start = datetime.now() - timedelta(days=7)
            videos_week = videos_df[videos_df['Upload Date'] >= week_start] if 'Upload Date' in videos_df.columns else videos_df
            comments_week = comments_df[comments_df['Date'] >= week_start] if 'Date' in comments_df.columns else comments_df
            
            report = {
                'report_type': 'weekly_intelligence',
                'generated_at': datetime.now().isoformat(),
                'report_period': {
                    'start_date': week_start.strftime('%Y-%m-%d'),
                    'end_date': datetime.now().strftime('%Y-%m-%d')
                },
                'executive_summary': {},
                'performance_metrics': {},
                'trend_analysis': {},
                'threat_landscape': {},
                'strategic_insights': {},
                'competitive_analysis': {},
                'recommendations': [],
                'forecast': {}
            }
            
            # Executive Summary
            report['executive_summary'] = self._generate_weekly_executive_summary(videos_week, comments_week, crisis_data)
            
            # Performance Metrics
            report['performance_metrics'] = self._calculate_weekly_performance(videos_week, comments_week)
            
            # Trend Analysis
            report['trend_analysis'] = self._analyze_weekly_trends(videos_week, comments_week)
            
            # Threat Landscape
            if crisis_data:
                report['threat_landscape'] = self._analyze_weekly_threats(crisis_data)
            
            # Strategic Insights
            report['strategic_insights'] = self._generate_strategic_insights(videos_week, comments_week)
            
            # Competitive Analysis
            report['competitive_analysis'] = self._analyze_competitive_landscape(videos_week)
            
            # Strategic Recommendations
            report['recommendations'] = self._generate_weekly_recommendations(report)
            
            # Forecast
            report['forecast'] = self._generate_forecast(videos_week, comments_week)
            
            self.logger.info("Weekly intelligence report generated successfully")
            return report
            
        except Exception as e:
            self.logger.error(f"Weekly intelligence generation failed: {e}")
            return {'error': str(e), 'generated_at': datetime.now().isoformat()}
    
    def _generate_executive_summary(self, videos_df: pd.DataFrame, comments_df: pd.DataFrame, 
                                  crisis_data: Dict = None) -> Dict:
        """Generate executive summary with key insights"""
        summary = {
            'overall_status': 'STABLE',
            'key_highlights': [],
            'critical_issues': [],
            'performance_indicators': {},
            'reputation_health': 'GOOD'
        }
        
        try:
            # Calculate key metrics
            total_videos = len(videos_df)
            total_comments = len(comments_df)
            avg_sentiment = comments_df['Sentiment'].mean() if 'Sentiment' in comments_df.columns else 0
            
            # Determine overall status
            if crisis_data and crisis_data.get('status') == 'CRITICAL':
                summary['overall_status'] = 'CRITICAL'
                summary['reputation_health'] = 'AT_RISK'
            elif avg_sentiment < -0.2:
                summary['overall_status'] = 'CONCERNING'
                summary['reputation_health'] = 'DECLINING'
            elif avg_sentiment > 0.2:
                summary['overall_status'] = 'POSITIVE'
                summary['reputation_health'] = 'STRONG'
            
            # Key highlights
            summary['key_highlights'] = [
                f"Monitoring {total_videos} videos and {total_comments:,} comments",
                f"Average sentiment score: {avg_sentiment:.3f}",
                f"Reputation health: {summary['reputation_health']}"
            ]
            
            # Critical issues
            if crisis_data and crisis_data.get('threat_counts', {}).get('critical', 0) > 0:
                critical_count = crisis_data['threat_counts']['critical']
                summary['critical_issues'].append(f"{critical_count} critical threats requiring immediate attention")
            
            if avg_sentiment < -0.3:
                summary['critical_issues'].append("Negative sentiment trend detected")
            
            # Performance indicators
            summary['performance_indicators'] = {
                'content_volume': total_videos,
                'engagement_level': total_comments,
                'sentiment_score': round(avg_sentiment, 3),
                'threat_level': crisis_data.get('threat_counts', {}).get('total', 0) if crisis_data else 0
            }
            
        except Exception as e:
            self.logger.error(f"Executive summary generation failed: {e}")
            summary['error'] = str(e)
        
        return summary
    
    def _calculate_key_metrics(self, videos_df: pd.DataFrame, comments_df: pd.DataFrame) -> Dict:
        """Calculate key performance metrics"""
        metrics = {
            'content_metrics': {},
            'engagement_metrics': {},
            'sentiment_metrics': {},
            'growth_metrics': {}
        }
        
        try:
            # Content Metrics
            metrics['content_metrics'] = {
                'total_videos': len(videos_df),
                'unique_channels': videos_df['Channel'].nunique() if 'Channel' in videos_df.columns else 0,
                'avg_video_views': videos_df['Views'].mean() if 'Views' in videos_df.columns else 0,
                'total_video_views': videos_df['Views'].sum() if 'Views' in videos_df.columns else 0
            }
            
            # Engagement Metrics
            metrics['engagement_metrics'] = {
                'total_comments': len(comments_df),
                'unique_commenters': comments_df['Author'].nunique() if 'Author' in comments_df.columns else 0,
                'avg_likes_per_comment': comments_df['LikeCount'].mean() if 'LikeCount' in comments_df.columns else 0,
                'engagement_rate': len(comments_df) / len(videos_df) if len(videos_df) > 0 else 0
            }
            
            # Sentiment Metrics
            if 'Sentiment' in comments_df.columns:
                sentiment_dist = comments_df['SentLabel'].value_counts() if 'SentLabel' in comments_df.columns else {}
                metrics['sentiment_metrics'] = {
                    'avg_sentiment': comments_df['Sentiment'].mean(),
                    'positive_percentage': (sentiment_dist.get('Positive', 0) / len(comments_df)) * 100,
                    'negative_percentage': (sentiment_dist.get('Negative', 0) / len(comments_df)) * 100,
                    'sentiment_volatility': comments_df['Sentiment'].std()
                }
            
            # Growth Metrics (simplified)
            if 'Upload Date' in videos_df.columns:
                recent_videos = videos_df[videos_df['Upload Date'] >= datetime.now() - timedelta(days=7)]
                metrics['growth_metrics'] = {
                    'videos_this_week': len(recent_videos),
                    'content_growth_rate': (len(recent_videos) / len(videos_df)) * 100 if len(videos_df) > 0 else 0
                }
            
        except Exception as e:
            self.logger.error(f"Key metrics calculation failed: {e}")
            metrics['error'] = str(e)
        
        return metrics
    
    def _analyze_sentiment_intelligence(self, comments_df: pd.DataFrame) -> Dict:
        """Analyze sentiment intelligence with deep insights"""
        analysis = {
            'overall_sentiment': 'NEUTRAL',
            'sentiment_distribution': {},
            'sentiment_trends': {},
            'key_insights': [],
            'sentiment_drivers': []
        }
        
        try:
            if 'Sentiment' in comments_df.columns:
                avg_sentiment = comments_df['Sentiment'].mean()
                
                # Overall sentiment classification
                if avg_sentiment > 0.1:
                    analysis['overall_sentiment'] = 'POSITIVE'
                elif avg_sentiment < -0.1:
                    analysis['overall_sentiment'] = 'NEGATIVE'
                
                # Sentiment distribution
                if 'SentLabel' in comments_df.columns:
                    sent_counts = comments_df['SentLabel'].value_counts()
                    total = len(comments_df)
                    analysis['sentiment_distribution'] = {
                        'positive': round((sent_counts.get('Positive', 0) / total) * 100, 1),
                        'negative': round((sent_counts.get('Negative', 0) / total) * 100, 1),
                        'neutral': round((sent_counts.get('Neutral', 0) / total) * 100, 1)
                    }
                
                # Key insights
                analysis['key_insights'] = [
                    f"Average sentiment: {avg_sentiment:.3f}",
                    f"Dominant sentiment: {analysis['overall_sentiment']}",
                    f"Sentiment volatility: {comments_df['Sentiment'].std():.3f}"
                ]
                
                # Sentiment drivers (top keywords from positive/negative comments)
                if 'Comment' in comments_df.columns:
                    positive_comments = comments_df[comments_df['Sentiment'] > 0.1]['Comment'].fillna('')
                    negative_comments = comments_df[comments_df['Sentiment'] < -0.1]['Comment'].fillna('')
                    
                    # Simple keyword extraction
                    positive_words = ' '.join(positive_comments.astype(str)).lower().split()
                    negative_words = ' '.join(negative_comments.astype(str)).lower().split()
                    
                    analysis['sentiment_drivers'] = {
                        'positive_keywords': [word for word, count in Counter(positive_words).most_common(5)],
                        'negative_keywords': [word for word, count in Counter(negative_words).most_common(5)]
                    }
            
        except Exception as e:
            self.logger.error(f"Sentiment intelligence analysis failed: {e}")
            analysis['error'] = str(e)
        
        return analysis
    
    def _generate_strategic_recommendations(self, briefing_data: Dict) -> List[Dict]:
        """Generate strategic recommendations based on analysis"""
        recommendations = []
        
        try:
            executive_summary = briefing_data.get('executive_summary', {})
            key_metrics = briefing_data.get('key_metrics', {})
            threat_assessment = briefing_data.get('threat_assessment', {})
            sentiment_analysis = briefing_data.get('sentiment_analysis', {})
            
            # Crisis-based recommendations
            if executive_summary.get('overall_status') == 'CRITICAL':
                recommendations.append({
                    'priority': 'IMMEDIATE',
                    'category': 'Crisis Management',
                    'title': 'Activate Crisis Response Protocol',
                    'description': 'Critical reputation threats detected requiring immediate executive action',
                    'actions': [
                        'Convene crisis management team immediately',
                        'Prepare official response statement',
                        'Monitor threat escalation hourly',
                        'Consider legal consultation if needed'
                    ]
                })
            
            # Sentiment-based recommendations
            if sentiment_analysis.get('overall_sentiment') == 'NEGATIVE':
                recommendations.append({
                    'priority': 'HIGH',
                    'category': 'Reputation Recovery',
                    'title': 'Implement Positive Engagement Strategy',
                    'description': 'Negative sentiment trend detected requiring proactive response',
                    'actions': [
                        'Increase positive content creation',
                        'Engage with community directly',
                        'Address concerns transparently',
                        'Amplify positive testimonials'
                    ]
                })
            
            # Engagement-based recommendations
            engagement_rate = key_metrics.get('engagement_metrics', {}).get('engagement_rate', 0)
            if engagement_rate < 2.0:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'Audience Engagement',
                    'title': 'Boost Audience Engagement',
                    'description': 'Low engagement rate indicates need for improved audience connection',
                    'actions': [
                        'Create more interactive content',
                        'Respond to comments actively',
                        'Host live sessions or Q&A',
                        'Collaborate with popular channels'
                    ]
                })
            
            # Growth-based recommendations
            growth_rate = key_metrics.get('growth_metrics', {}).get('content_growth_rate', 0)
            if growth_rate < 5.0:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'Content Strategy',
                    'title': 'Accelerate Content Production',
                    'description': 'Content growth rate below optimal levels',
                    'actions': [
                        'Increase content publishing frequency',
                        'Diversify content formats',
                        'Focus on trending topics',
                        'Optimize content for search visibility'
                    ]
                })
            
        except Exception as e:
            self.logger.error(f"Strategic recommendations generation failed: {e}")
            recommendations.append({'error': str(e)})
        
        return recommendations
    
    def _generate_action_items(self, briefing_data: Dict) -> List[Dict]:
        """Generate specific action items for executive team"""
        action_items = []
        
        try:
            executive_summary = briefing_data.get('executive_summary', {})
            recommendations = briefing_data.get('recommendations', [])
            
            # High-priority actions based on status
            if executive_summary.get('overall_status') in ['CRITICAL', 'CONCERNING']:
                action_items.append({
                    'priority': 'IMMEDIATE',
                    'owner': 'CEO/Executive Team',
                    'action': 'Review crisis status and activate response protocol',
                    'deadline': 'Within 2 hours',
                    'status': 'PENDING'
                })
            
            # Extract actions from recommendations
            for rec in recommendations:
                if rec.get('priority') == 'IMMEDIATE':
                    for action in rec.get('actions', []):
                        action_items.append({
                            'priority': 'IMMEDIATE',
                            'owner': 'Crisis Team',
                            'action': action,
                            'deadline': 'Today',
                            'status': 'PENDING'
                        })
                elif rec.get('priority') == 'HIGH':
                    for action in rec.get('actions', []):
                        action_items.append({
                            'priority': 'HIGH',
                            'owner': 'Marketing/PR Team',
                            'action': action,
                            'deadline': 'This week',
                            'status': 'PENDING'
                        })
            
            # Always include monitoring action
            action_items.append({
                'priority': 'ONGOING',
                'owner': 'Monitoring Team',
                'action': 'Continue real-time reputation monitoring',
                'deadline': 'Continuous',
                'status': 'ACTIVE'
            })
            
        except Exception as e:
            self.logger.error(f"Action items generation failed: {e}")
            action_items.append({'error': str(e)})
        
        return action_items
    
    def generate_executive_summary_report(self, videos_df: pd.DataFrame, comments_df: pd.DataFrame,
                                        crisis_data: Dict = None) -> str:
        """Generate formatted executive summary report"""
        try:
            daily_briefing = self.generate_daily_briefing(videos_df, comments_df, crisis_data)
            
            # Format as executive summary
            report = f"""
# 🎯 EXECUTIVE INTELLIGENCE BRIEFING
## {datetime.now().strftime('%B %d, %Y')}

### 📊 EXECUTIVE SUMMARY
- **Overall Status**: {daily_briefing['executive_summary'].get('overall_status', 'Unknown')}
- **Reputation Health**: {daily_briefing['executive_summary'].get('reputation_health', 'Unknown')}
- **Threat Level**: {crisis_data.get('status', 'NORMAL') if crisis_data else 'NORMAL'}

### 🔥 KEY HIGHLIGHTS
"""
            
            for highlight in daily_briefing['executive_summary'].get('key_highlights', []):
                report += f"- {highlight}\n"
            
            if daily_briefing['executive_summary'].get('critical_issues'):
                report += "\n### 🚨 CRITICAL ISSUES\n"
                for issue in daily_briefing['executive_summary']['critical_issues']:
                    report += f"- {issue}\n"
            
            report += "\n### 📈 KEY METRICS\n"
            metrics = daily_briefing.get('key_metrics', {})
            if 'content_metrics' in metrics:
                report += f"- Total Videos: {metrics['content_metrics'].get('total_videos', 0):,}\n"
                report += f"- Total Comments: {metrics['engagement_metrics'].get('total_comments', 0):,}\n"
                report += f"- Engagement Rate: {metrics['engagement_metrics'].get('engagement_rate', 0):.1f}\n"
            
            if daily_briefing.get('recommendations'):
                report += "\n### 💡 STRATEGIC RECOMMENDATIONS\n"
                for rec in daily_briefing['recommendations'][:3]:  # Top 3 recommendations
                    report += f"- **{rec.get('title', 'Recommendation')}** ({rec.get('priority', 'MEDIUM')})\n"
            
            if daily_briefing.get('action_items'):
                report += "\n### ✅ IMMEDIATE ACTION ITEMS\n"
                for action in daily_briefing['action_items'][:5]:  # Top 5 actions
                    if action.get('priority') in ['IMMEDIATE', 'HIGH']:
                        report += f"- {action.get('action', 'Action required')} (Owner: {action.get('owner', 'TBD')})\n"
            
            report += f"\n---\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
            
            return report
            
        except Exception as e:
            self.logger.error(f"Executive summary report generation failed: {e}")
            return f"Error generating executive summary: {e}"
    
    def export_report(self, report_data: Dict, report_type: str = 'daily_briefing', 
                     format: str = 'json') -> str:
        """Export report to file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reports/{report_type}_{timestamp}.{format}"
            
            os.makedirs('reports', exist_ok=True)
            
            if format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            elif format == 'txt':
                with open(filename, 'w', encoding='utf-8') as f:
                    if isinstance(report_data, dict):
                        f.write(json.dumps(report_data, indent=2, ensure_ascii=False, default=str))
                    else:
                        f.write(str(report_data))
            
            self.logger.info(f"Report exported to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Report export failed: {e}")
            return f"Export failed: {e}"

# Example usage and testing
if __name__ == "__main__":
    # Initialize executive reporting engine
    reporting_engine = ExecutiveReportingEngine()
    
    try:
        # Load AI-processed datasets
        videos_df = pd.read_csv("backend/data/videos/youtube_videos_ai_processed.csv")
        comments_df = pd.read_csv("backend/data/comments/youtube_comments_ai_enhanced.csv")
        
        print("📊 EXECUTIVE REPORTING ENGINE - TESTING")
        print("=" * 50)
        
        # Generate daily briefing
        daily_briefing = reporting_engine.generate_daily_briefing(videos_df, comments_df)
        
        # Display results
        print(f"📋 Daily briefing generated at: {daily_briefing['generated_at']}")
        print(f"🎯 Overall status: {daily_briefing['executive_summary'].get('overall_status', 'Unknown')}")
        print(f"💪 Reputation health: {daily_briefing['executive_summary'].get('reputation_health', 'Unknown')}")
        
        # Show key metrics
        if 'key_metrics' in daily_briefing:
            content_metrics = daily_briefing['key_metrics'].get('content_metrics', {})
            engagement_metrics = daily_briefing['key_metrics'].get('engagement_metrics', {})
            
            print(f"\n📊 KEY METRICS:")
            print(f"  Videos: {content_metrics.get('total_videos', 0):,}")
            print(f"  Comments: {engagement_metrics.get('total_comments', 0):,}")
            print(f"  Engagement Rate: {engagement_metrics.get('engagement_rate', 0):.1f}")
        
        # Show recommendations
        if daily_briefing.get('recommendations'):
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(daily_briefing['recommendations'][:3], 1):
                print(f"  {i}. {rec.get('title', 'Recommendation')} ({rec.get('priority', 'MEDIUM')})")
        
        # Generate executive summary report
        executive_summary = reporting_engine.generate_executive_summary_report(videos_df, comments_df)
        print(f"\n📄 Executive Summary Report Generated:")
        print(executive_summary[:500] + "..." if len(executive_summary) > 500 else executive_summary)
        
        # Export report
        export_filename = reporting_engine.export_report(daily_briefing, 'daily_briefing', 'json')
        print(f"\n💾 Report exported to: {export_filename}")
        
        print("\n✅ Executive Reporting Engine test completed successfully!")
        
    except Exception as e:
        print(f"❌ Executive Reporting Engine test failed: {e}") 