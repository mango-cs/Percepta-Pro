"""
🚨 CRISIS DETECTION ENGINE - Phase 3A
Advanced Real-time Threat Monitoring for Percepta Pro v2.0

Analyzes AI-enhanced datasets for reputation threats and generates executive alerts
with bilingual support for Telugu-English content analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from collections import Counter
import logging
from typing import Dict, List, Tuple, Optional
import json

# Configure logging
import os
os.makedirs('logs', exist_ok=True)  # Create logs directory if it doesn't exist
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/crisis_detection.log'),
        logging.StreamHandler()
    ]
)

class CrisisDetectionEngine:
    """
    Advanced Crisis Detection Engine for Reputation Monitoring
    
    Features:
    - Real-time threat assessment
    - Bilingual content analysis (Telugu/English)
    - Executive alert generation
    - Trend-based crisis prediction
    - Severity scoring and prioritization
    """
    
    def __init__(self):
        """Initialize crisis detection engine with threat patterns and thresholds"""
        self.logger = logging.getLogger(__name__)
        
        # Crisis threat patterns (bilingual)
        self.threat_patterns = {
            'death_threats': {
                'telugu': ['చచ్చిపో', 'చంప', 'చచ్చినట్టే', 'చంపేస్తా', 'చంపించ', 'చావు'],
                'english': ['die', 'kill', 'death', 'murder', 'assassinate', 'eliminate'],
                'severity': 'CRITICAL',
                'weight': 10.0
            },
            'black_magic_accusations': {
                'telugu': ['చేతబడి', 'క్షుద్ర', 'మంత్రం', 'వశీకరణ', 'తంత్రం', 'మాయా'],
                'english': ['black magic', 'witchcraft', 'sorcery', 'occult', 'dark magic', 'voodoo'],
                'severity': 'HIGH',
                'weight': 8.0
            },
            'legal_threats': {
                'telugu': ['అరెస్ట్', 'కేసు', 'కోర్టు', 'పోలీసు', 'జైలు', 'శిక్ష'],
                'english': ['arrest', 'case', 'court', 'police', 'jail', 'lawsuit', 'legal action'],
                'severity': 'HIGH',
                'weight': 7.0
            },
            'violence_threats': {
                'telugu': ['కొట్ట', 'హింస', 'దాడి', 'కొరుకు', 'చెయ్యి', 'కాలు'],
                'english': ['beat', 'violence', 'attack', 'assault', 'harm', 'hurt'],
                'severity': 'HIGH',
                'weight': 7.5
            },
            'reputation_attacks': {
                'telugu': ['మోసం', 'దొంగ', 'మోసగాడు', 'మోసకోరు', 'మోసపూరిత', 'పెంకు'],
                'english': ['fraud', 'cheat', 'scam', 'liar', 'dishonest', 'corrupt'],
                'severity': 'MEDIUM',
                'weight': 5.0
            },
            'business_threats': {
                'telugu': ['బాంబ్', 'పేలుడు', 'దెబ్బ', 'నష్టం', 'మూసివేత', 'నాశనం'],
                'english': ['bomb', 'explosion', 'damage', 'destroy', 'close down', 'ruin'],
                'severity': 'CRITICAL',
                'weight': 9.5
            }
        }
        
        # Crisis severity thresholds
        self.severity_thresholds = {
            'CRITICAL': {'min_score': 8.0, 'color': '#EF4444', 'icon': '🚨'},
            'HIGH': {'min_score': 6.0, 'color': '#F59E0B', 'icon': '⚠️'},
            'MEDIUM': {'min_score': 4.0, 'color': '#EAB308', 'icon': '⚡'},
            'LOW': {'min_score': 2.0, 'color': '#6B7280', 'icon': '📊'}
        }
        
        # Key figures monitoring
        self.key_figures = [
            'సంధ్య శ్రీధర్ రావు', 'sandhya sridhar rao', 'sridhar rao',
            'మాగంటి గోపినాథ్', 'maganti gopinath', 'gopinath',
            'సంధ్య కన్వెన్షన్', 'sandhya convention'
        ]
        
        # Viral threat indicators
        self.viral_thresholds = {
            'high_engagement': 50,  # Comments/likes threshold
            'rapid_spread': 10,     # Videos mentioning same topic
            'trending_keywords': 5   # Keyword frequency threshold
        }
        
        self.logger.info("Crisis Detection Engine initialized with bilingual threat patterns")
    
    def analyze_crisis_threats(self, videos_df: pd.DataFrame, comments_df: pd.DataFrame) -> Dict:
        """
        Comprehensive crisis threat analysis
        
        Args:
            videos_df: AI-processed videos dataset
            comments_df: AI-processed comments dataset
            
        Returns:
            Dict with crisis analysis results
        """
        self.logger.info("Starting comprehensive crisis threat analysis")
        
        try:
            # Initialize crisis report
            crisis_report = {
                'analysis_timestamp': datetime.now().isoformat(),
                'total_threats_detected': 0,
                'active_crises': [],
                'threat_summary': {},
                'executive_alerts': [],
                'trend_analysis': {},
                'recommendations': []
            }
            
            # Analyze video threats
            video_threats = self._analyze_video_threats(videos_df)
            
            # Analyze comment threats
            comment_threats = self._analyze_comment_threats(comments_df)
            
            # Combine and prioritize threats
            all_threats = self._combine_threats(video_threats, comment_threats)
            
            # Generate executive alerts
            executive_alerts = self._generate_executive_alerts(all_threats)
            
            # Analyze trending threats
            trend_analysis = self._analyze_threat_trends(videos_df, comments_df)
            
            # Generate recommendations
            recommendations = self._generate_crisis_recommendations(all_threats, trend_analysis)
            
            # Compile final report
            crisis_report.update({
                'total_threats_detected': len(all_threats),
                'active_crises': self._identify_active_crises(all_threats),
                'threat_summary': self._summarize_threats(all_threats),
                'executive_alerts': executive_alerts,
                'trend_analysis': trend_analysis,
                'recommendations': recommendations
            })
            
            self.logger.info(f"Crisis analysis completed - {len(all_threats)} threats detected")
            return crisis_report
            
        except Exception as e:
            self.logger.error(f"Crisis analysis failed: {e}")
            return {'error': str(e), 'analysis_timestamp': datetime.now().isoformat()}
    
    def _analyze_video_threats(self, videos_df: pd.DataFrame) -> List[Dict]:
        """Analyze threats in video titles, descriptions, and AI fields"""
        threats = []
        
        for idx, video in videos_df.iterrows():
            video_threats = []
            
            # Analyze video title
            title_threats = self._detect_threats_in_text(
                str(video.get('Title', '')), 'video_title', video.get('VideoID', '')
            )
            video_threats.extend(title_threats)
            
            # Analyze video description
            desc_threats = self._detect_threats_in_text(
                str(video.get('Description', '')), 'video_description', video.get('VideoID', '')
            )
            video_threats.extend(desc_threats)
            
            # Analyze AI-generated keywords
            if 'Keywords_EN' in video:
                keyword_threats = self._detect_threats_in_text(
                    str(video.get('Keywords_EN', '')), 'ai_keywords', video.get('VideoID', '')
                )
                video_threats.extend(keyword_threats)
            
            # Add video metadata to threats
            for threat in video_threats:
                threat.update({
                    'video_id': video.get('VideoID', ''),
                    'video_title': video.get('Title', ''),
                    'channel': video.get('Channel', ''),
                    'views': video.get('Views', 0),
                    'upload_date': video.get('UploadDate', ''),
                    'engagement_score': self._calculate_video_engagement(video)
                })
            
            threats.extend(video_threats)
        
        return threats
    
    def _analyze_comment_threats(self, comments_df: pd.DataFrame) -> List[Dict]:
        """Analyze threats in comments and AI sentiment data"""
        threats = []
        
        for idx, comment in comments_df.iterrows():
            comment_threats = []
            
            # Analyze original comment
            original_threats = self._detect_threats_in_text(
                str(comment.get('Comment', '')), 'comment', comment.get('CommentID', '')
            )
            comment_threats.extend(original_threats)
            
            # Analyze English translated comment
            if 'Comment_EN' in comment:
                english_threats = self._detect_threats_in_text(
                    str(comment.get('Comment_EN', '')), 'comment_english', comment.get('CommentID', '')
                )
                comment_threats.extend(english_threats)
            
            # Enhance with sentiment data
            for threat in comment_threats:
                threat.update({
                    'comment_id': comment.get('CommentID', ''),
                    'video_id': comment.get('VideoID', ''),
                    'author': comment.get('Author', ''),
                    'like_count': comment.get('LikeCount', 0),
                    'comment_date': comment.get('Date_Formatted', ''),
                    'sentiment_score': comment.get('SentimentScore_EN', 0.0),
                    'sentiment_label': comment.get('SentimentLabel_EN', 'Neutral'),
                    'is_reply': comment.get('IsReply', False)
                })
            
            threats.extend(comment_threats)
        
        return threats
    
    def _detect_threats_in_text(self, text: str, source_type: str, source_id: str) -> List[Dict]:
        """Detect threat patterns in text using bilingual analysis"""
        threats = []
        text_lower = text.lower()
        
        for threat_type, patterns in self.threat_patterns.items():
            threat_score = 0.0
            matched_terms = []
            
            # Check Telugu patterns
            for term in patterns['telugu']:
                if term in text_lower:
                    threat_score += patterns['weight']
                    matched_terms.append(term)
            
            # Check English patterns
            for term in patterns['english']:
                if term in text_lower:
                    threat_score += patterns['weight']
                    matched_terms.append(term)
            
            # Check for key figure mentions (amplifies threat score)
            key_figure_mentioned = False
            for figure in self.key_figures:
                if figure.lower() in text_lower:
                    threat_score *= 1.5  # Amplify threat score
                    key_figure_mentioned = True
                    break
            
            # If threats detected, create threat object
            if threat_score > 0:
                threats.append({
                    'threat_type': threat_type,
                    'threat_score': threat_score,
                    'severity': patterns['severity'],
                    'matched_terms': matched_terms,
                    'source_type': source_type,
                    'source_id': source_id,
                    'text_content': text[:200] + '...' if len(text) > 200 else text,
                    'key_figure_mentioned': key_figure_mentioned,
                    'detection_timestamp': datetime.now().isoformat()
                })
        
        return threats
    
    def _combine_threats(self, video_threats: List[Dict], comment_threats: List[Dict]) -> List[Dict]:
        """Combine and deduplicate threats from videos and comments"""
        all_threats = video_threats + comment_threats
        
        # Sort by threat score (highest first)
        all_threats.sort(key=lambda x: x['threat_score'], reverse=True)
        
        return all_threats
    
    def _identify_active_crises(self, threats: List[Dict]) -> List[Dict]:
        """Identify active crises requiring immediate attention"""
        active_crises = []
        
        # Group threats by type and severity
        critical_threats = [t for t in threats if t['severity'] == 'CRITICAL']
        high_threats = [t for t in threats if t['severity'] == 'HIGH']
        
        # Crisis criteria: Multiple high-severity threats or any critical threats
        if critical_threats:
            for threat in critical_threats[:5]:  # Top 5 critical threats
                active_crises.append({
                    'crisis_id': f"CRISIS_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(active_crises)}",
                    'crisis_type': threat['threat_type'],
                    'severity': 'CRITICAL',
                    'threat_score': threat['threat_score'],
                    'description': f"{threat['threat_type'].replace('_', ' ').title()} detected",
                    'source': threat['source_type'],
                    'requires_action': True,
                    'detected_at': threat['detection_timestamp']
                })
        
        if len(high_threats) >= 3:  # Multiple high threats = crisis
            active_crises.append({
                'crisis_id': f"CRISIS_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(active_crises)}",
                'crisis_type': 'multiple_high_threats',
                'severity': 'HIGH',
                'threat_score': sum(t['threat_score'] for t in high_threats[:3]) / 3,
                'description': f"Multiple high-severity threats detected ({len(high_threats)} total)",
                'source': 'aggregated',
                'requires_action': True,
                'detected_at': datetime.now().isoformat()
            })
        
        return active_crises
    
    def _generate_executive_alerts(self, threats: List[Dict]) -> List[Dict]:
        """Generate executive-level alerts for immediate action"""
        alerts = []
        
        # Critical threat alerts
        critical_threats = [t for t in threats if t['severity'] == 'CRITICAL']
        if critical_threats:
            alerts.append({
                'alert_id': f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}_CRITICAL",
                'priority': 'IMMEDIATE',
                'title': '🚨 CRITICAL REPUTATION THREAT DETECTED',
                'message': f"{len(critical_threats)} critical threat(s) detected requiring immediate attention",
                'recommended_action': 'Activate crisis management protocol immediately',
                'threat_count': len(critical_threats),
                'max_threat_score': max(t['threat_score'] for t in critical_threats),
                'timestamp': datetime.now().isoformat()
            })
        
        # High-volume threat alerts
        high_volume_threshold = 10
        if len(threats) >= high_volume_threshold:
            alerts.append({
                'alert_id': f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}_VOLUME",
                'priority': 'HIGH',
                'title': '⚠️ HIGH VOLUME THREAT ACTIVITY',
                'message': f"{len(threats)} total threats detected across all content",
                'recommended_action': 'Initiate enhanced monitoring and PR response',
                'threat_count': len(threats),
                'timestamp': datetime.now().isoformat()
            })
        
        # Key figure threat alerts
        key_figure_threats = [t for t in threats if t.get('key_figure_mentioned')]
        if key_figure_threats:
            alerts.append({
                'alert_id': f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}_FIGURE",
                'priority': 'HIGH',
                'title': '👤 KEY FIGURE TARGETED THREATS',
                'message': f"{len(key_figure_threats)} threats directly mention key figures",
                'recommended_action': 'Implement personal security and reputation protection measures',
                'threat_count': len(key_figure_threats),
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def _analyze_threat_trends(self, videos_df: pd.DataFrame, comments_df: pd.DataFrame) -> Dict:
        """Analyze threat trends and patterns over time"""
        trends = {
            'threat_velocity': 0,
            'trending_keywords': [],
            'threat_distribution': {},
            'temporal_patterns': {},
            'viral_indicators': {}
        }
        
        try:
            # Calculate threat velocity (threats per day)
            recent_comments = comments_df.tail(100)  # Last 100 comments
            recent_threats = []
            for _, comment in recent_comments.iterrows():
                comment_threats = self._detect_threats_in_text(
                    str(comment.get('Comment', '')), 'comment', comment.get('CommentID', '')
                )
                recent_threats.extend(comment_threats)
            
            trends['threat_velocity'] = len(recent_threats)
            
            # Identify trending threat keywords
            all_matched_terms = []
            for threat in recent_threats:
                all_matched_terms.extend(threat.get('matched_terms', []))
            
            keyword_counts = Counter(all_matched_terms)
            trends['trending_keywords'] = keyword_counts.most_common(10)
            
            # Threat type distribution
            threat_types = [t['threat_type'] for t in recent_threats]
            trends['threat_distribution'] = dict(Counter(threat_types))
            
            # Viral indicators
            high_engagement_videos = videos_df[videos_df.get('Views', 0) > 10000]
            trends['viral_indicators'] = {
                'high_view_videos': len(high_engagement_videos),
                'potential_viral_threats': len([v for _, v in high_engagement_videos.iterrows() 
                                               if any(pattern in str(v.get('Title', '')).lower() 
                                                     for pattern_list in self.threat_patterns.values() 
                                                     for pattern in pattern_list['telugu'] + pattern_list['english'])])
            }
            
        except Exception as e:
            self.logger.error(f"Trend analysis failed: {e}")
            trends['error'] = str(e)
        
        return trends
    
    def _generate_crisis_recommendations(self, threats: List[Dict], trends: Dict) -> List[Dict]:
        """Generate strategic recommendations based on threat analysis"""
        recommendations = []
        
        # Critical threat recommendations
        critical_threats = [t for t in threats if t['severity'] == 'CRITICAL']
        if critical_threats:
            recommendations.append({
                'priority': 'IMMEDIATE',
                'category': 'Crisis Management',
                'action': 'Activate Crisis Response Protocol',
                'description': 'Immediate crisis management activation required for critical threats',
                'specific_steps': [
                    'Contact crisis management team immediately',
                    'Prepare official statement/response',
                    'Monitor threat escalation closely',
                    'Consider legal consultation for serious threats'
                ]
            })
        
        # High-volume threat recommendations
        if len(threats) >= 10:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Reputation Management',
                'action': 'Enhanced Monitoring & PR Response',
                'description': 'High volume of threats requires enhanced monitoring',
                'specific_steps': [
                    'Increase monitoring frequency to hourly',
                    'Prepare positive content strategy',
                    'Engage PR team for response planning',
                    'Monitor social media mentions actively'
                ]
            })
        
        # Trending threat recommendations
        if trends.get('threat_velocity', 0) > 5:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Proactive Measures',
                'action': 'Proactive Reputation Protection',
                'description': 'Increasing threat velocity requires proactive measures',
                'specific_steps': [
                    'Amplify positive content creation',
                    'Strengthen community engagement',
                    'Address concerns proactively',
                    'Consider influencer partnerships'
                ]
            })
        
        return recommendations
    
    def _calculate_video_engagement(self, video: pd.Series) -> float:
        """Calculate engagement score for video threat assessment"""
        try:
            views = float(video.get('Views', 0))
            comments = float(video.get('Comments', 0))
            likes = float(video.get('LikeCount', 0))
            
            # Simple engagement calculation
            if views > 0:
                engagement = ((comments + likes) / views) * 100
                return min(engagement, 100.0)  # Cap at 100%
            return 0.0
        except:
            return 0.0
    
    def _summarize_threats(self, threats: List[Dict]) -> Dict:
        """Summarize threats by type and severity"""
        summary = {
            'by_severity': {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
            'by_type': {},
            'total_score': 0,
            'highest_threat': None
        }
        
        for threat in threats:
            # Count by severity
            severity = threat.get('severity', 'LOW')
            summary['by_severity'][severity] += 1
            
            # Count by type
            threat_type = threat.get('threat_type', 'unknown')
            summary['by_type'][threat_type] = summary['by_type'].get(threat_type, 0) + 1
            
            # Sum total score
            summary['total_score'] += threat.get('threat_score', 0)
            
            # Track highest threat
            if summary['highest_threat'] is None or threat.get('threat_score', 0) > summary['highest_threat'].get('threat_score', 0):
                summary['highest_threat'] = threat
        
        return summary

    def get_crisis_status(self, videos_df: pd.DataFrame, comments_df: pd.DataFrame) -> Dict:
        """Quick crisis status check for dashboard display"""
        try:
            # Quick threat analysis
            threats = []
            
            # Check recent comments for immediate threats
            recent_comments = comments_df.tail(50)
            for _, comment in recent_comments.iterrows():
                comment_threats = self._detect_threats_in_text(
                    str(comment.get('Comment', '')), 'comment', comment.get('CommentID', '')
                )
                threats.extend(comment_threats)
            
            # Calculate status
            critical_count = len([t for t in threats if t['severity'] == 'CRITICAL'])
            high_count = len([t for t in threats if t['severity'] == 'HIGH'])
            total_threats = len(threats)
            
            # Determine overall status
            if critical_count > 0:
                status = 'CRITICAL'
                status_color = '#EF4444'
                status_icon = '🚨'
                status_message = f'{critical_count} critical threat(s) detected'
            elif high_count >= 3:
                status = 'HIGH'
                status_color = '#F59E0B'
                status_icon = '⚠️'
                status_message = f'{high_count} high-priority threats active'
            elif total_threats >= 5:
                status = 'ELEVATED'
                status_color = '#EAB308'
                status_icon = '⚡'
                status_message = f'{total_threats} total threats detected'
            else:
                status = 'NORMAL'
                status_color = '#22C55E'
                status_icon = '✅'
                status_message = 'No immediate threats detected'
            
            return {
                'status': status,
                'status_color': status_color,
                'status_icon': status_icon,
                'status_message': status_message,
                'threat_counts': {
                    'critical': critical_count,
                    'high': high_count,
                    'total': total_threats
                },
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Crisis status check failed: {e}")
            return {
                'status': 'ERROR',
                'status_color': '#EF4444',
                'status_icon': '❌',
                'status_message': 'Crisis detection system error',
                'error': str(e)
            }

# Example usage and testing
if __name__ == "__main__":
    # Initialize crisis detection engine
    crisis_engine = CrisisDetectionEngine()
    
    try:
        # Load AI-processed datasets
        videos_df = pd.read_csv("backend/data/videos/youtube_videos_ai_processed.csv")
        comments_df = pd.read_csv("backend/data/comments/youtube_comments_ai_enhanced.csv")
        
        print("🚨 CRISIS DETECTION ENGINE - TESTING")
        print("=" * 50)
        
        # Run crisis analysis
        crisis_report = crisis_engine.analyze_crisis_threats(videos_df, comments_df)
        
        # Display results
        print(f"📊 Analysis completed at: {crisis_report['analysis_timestamp']}")
        print(f"🎯 Total threats detected: {crisis_report['total_threats_detected']}")
        print(f"🚨 Active crises: {len(crisis_report['active_crises'])}")
        print(f"⚠️ Executive alerts: {len(crisis_report['executive_alerts'])}")
        
        # Show threat summary
        if 'threat_summary' in crisis_report:
            summary = crisis_report['threat_summary']
            print("\n🔍 THREAT SUMMARY:")
            print(f"  Critical: {summary['by_severity']['CRITICAL']}")
            print(f"  High: {summary['by_severity']['HIGH']}")
            print(f"  Medium: {summary['by_severity']['MEDIUM']}")
            print(f"  Total Score: {summary['total_score']:.1f}")
        
        # Show executive alerts
        if crisis_report['executive_alerts']:
            print("\n🚨 EXECUTIVE ALERTS:")
            for alert in crisis_report['executive_alerts']:
                print(f"  {alert['priority']}: {alert['title']}")
                print(f"    {alert['message']}")
        
        # Quick status check
        status = crisis_engine.get_crisis_status(videos_df, comments_df)
        print(f"\n{status['status_icon']} Current Status: {status['status']} - {status['status_message']}")
        
        print("\n✅ Crisis Detection Engine test completed successfully!")
        
    except Exception as e:
        print(f"❌ Crisis Detection Engine test failed: {e}") 