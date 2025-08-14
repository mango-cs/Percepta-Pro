#!/usr/bin/env python3
"""
Enhanced Bilingual YouTube Extractor for Sridhar Rao
==================================================

High-precision Telugu + English extraction with accurate keyword targeting
based on 20 years of media intelligence and actual Telugu terminology usage.

Critical Requirements:
- Perfect bilingual functionality (Telugu + English)
- Accurate data classification and grading
- Precise relevance scoring (no assumptions)
- Comprehensive coverage of all controversy categories

Usage: python scripts/enhanced_telugu_extractor.py
Author: Percepta Pro v2.0 - Phase 1 Enhanced
"""

import os
import sys
import pandas as pd
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from data.videos.schema_v2 import VIDEO_SCHEMA_V2, calculate_relevance_score, determine_trust_level
except ImportError:
    print("Error: Could not import schema_v2")
    sys.exit(1)


class EnhancedTeluguExtractor:
    """Enhanced bilingual YouTube extractor with precise Telugu keyword targeting"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key not found. Set YOUTUBE_API_KEY environment variable.")
        
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.output_file = "backend/data/videos/youtube_videos_comprehensive.csv"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Enhanced stats tracking
        self.stats = {
            "videos_found": 0,
            "relevant_videos": 0,
            "api_calls": 0,
            "errors": 0,
            "telugu_videos": 0,
            "english_videos": 0,
            "high_relevance_videos": 0,
            "trusted_source_videos": 0
        }
    
    def get_comprehensive_telugu_keywords(self) -> List[Dict[str, Any]]:
        """
        Comprehensive Telugu keywords based on actual media usage analysis
        Organized by controversy type and priority level
        """
        return [
            # HIGHEST PRIORITY: Black Magic Audio Leak (June 2025) - Telugu Primary Terms
            {"query": "శ్రీధర్ రావు చేతబడి", "priority": 10, "category": "black_magic_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు క్షుద్ర పూజలు", "priority": 10, "category": "black_magic_primary", "language": "te"},
            {"query": "మాగంటి గోపీనాథ్ శ్రీధర్ రావు", "priority": 10, "category": "black_magic_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు ఆడియో లీక్", "priority": 10, "category": "black_magic_primary", "language": "te"},
            {"query": "సంధ్య కన్వెన్షన్ చేతబడి", "priority": 10, "category": "black_magic_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు చంపేశా", "priority": 10, "category": "black_magic_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు బెదిరింపులు", "priority": 10, "category": "black_magic_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు ఆడియో వైరల్", "priority": 10, "category": "black_magic_primary", "language": "te"},
            
            # HIGH PRIORITY: English Black Magic Coverage
            {"query": "Sridhar Rao black magic audio", "priority": 9, "category": "black_magic_english", "language": "en"},
            {"query": "Maganti Gopinath Sridhar Rao death", "priority": 9, "category": "black_magic_english", "language": "en"},
            {"query": "Sandhya Convention occult practices", "priority": 9, "category": "black_magic_english", "language": "en"},
            {"query": "Sridhar Rao threatening audio", "priority": 9, "category": "black_magic_english", "language": "en"},
            
            # HIGH PRIORITY: 2025 Legal Issues - Telugu Primary
            {"query": "శ్రీధర్ రావు భూకబ్జా", "priority": 9, "category": "legal_2025_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు కబ్జా", "priority": 9, "category": "legal_2025_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు హైడ్రా", "priority": 9, "category": "legal_2025_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు అరెస్ట్", "priority": 9, "category": "legal_2025_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు గచ్చిబౌలి", "priority": 9, "category": "legal_2025_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు కట్టడాల కూల్చివేత", "priority": 9, "category": "legal_2025_primary", "language": "te"},
            {"query": "సంధ్య కన్వెన్షన్ కబ్జా", "priority": 9, "category": "legal_2025_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు ఆక్రమణ", "priority": 9, "category": "legal_2025_primary", "language": "te"},
            
            # HIGH PRIORITY: 2025 Legal Issues - English
            {"query": "Sridhar Rao HYDRAA demolition", "priority": 8, "category": "legal_2025_english", "language": "en"},
            {"query": "Sridhar Rao land grab Gachibowli", "priority": 8, "category": "legal_2025_english", "language": "en"},
            {"query": "Sridhar Rao arrest 2025", "priority": 8, "category": "legal_2025_english", "language": "en"},
            {"query": "Sandhya Convention demolition", "priority": 8, "category": "legal_2025_english", "language": "en"},
            
            # MEDIUM-HIGH PRIORITY: Historical Legal Cases - Telugu Primary
            {"query": "శ్రీధర్ రావు మోసం", "priority": 8, "category": "legal_historical_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు కేసు", "priority": 8, "category": "legal_historical_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు ఎఫ్‌ఐఆర్", "priority": 8, "category": "legal_historical_primary", "language": "te"},
            {"query": "సంధ్య కన్వెన్షన్ మోసం", "priority": 8, "category": "legal_historical_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు తీవ్ర ఆరోపణలు", "priority": 8, "category": "legal_historical_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు బెయిల్", "priority": 7, "category": "legal_historical_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు జైలు", "priority": 7, "category": "legal_historical_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు పోలీసుల ఫిర్యాదు", "priority": 7, "category": "legal_historical_primary", "language": "te"},
            
            # MEDIUM PRIORITY: English Legal Historical
            {"query": "Sridhar Rao cheating case", "priority": 7, "category": "legal_historical_english", "language": "en"},
            {"query": "Sridhar Rao Delhi arrest 2023", "priority": 7, "category": "legal_historical_english", "language": "en"},
            {"query": "Sridhar Rao fraud allegations", "priority": 7, "category": "legal_historical_english", "language": "en"},
            {"query": "Sandhya Convention cheating", "priority": 7, "category": "legal_historical_english", "language": "en"},
            
            # MEDIUM PRIORITY: Political Connections - Telugu Primary
            {"query": "శ్రీధర్ రావు రాజకీయ సంబంధాలు", "priority": 6, "category": "political_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు ఫోన్ ట్యాపింగ్", "priority": 6, "category": "political_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు బిఆర్‌ఎస్", "priority": 6, "category": "political_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు ఆరోపణలు", "priority": 6, "category": "political_primary", "language": "te"},
            
            # MEDIUM PRIORITY: Business Disputes - Telugu Primary  
            {"query": "సంధ్య కన్వెన్షన్ వివాదాలు", "priority": 6, "category": "business_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు రియల్ ఎస్టేట్ వివాదాలు", "priority": 6, "category": "business_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు నిర్మాణ వివాదాలు", "priority": 6, "category": "business_primary", "language": "te"},
            {"query": "సంధ్య కన్స్ట్రక్షన్స్ వివాదాలు", "priority": 6, "category": "business_primary", "language": "te"},
            
            # LOWER-MEDIUM PRIORITY: Other Controversies - Telugu Primary
            {"query": "శ్రీధర్ రావు లైంగిక దాడి", "priority": 5, "category": "other_controversies_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు దాడి", "priority": 5, "category": "other_controversies_primary", "language": "te"},
            {"query": "శ్రీధర్ రావు కొట్లాట", "priority": 5, "category": "other_controversies_primary", "language": "te"},
            {"query": "సంధ్య కన్వెన్షన్ సమస్యలు", "priority": 5, "category": "other_controversies_primary", "language": "te"},
            
            # GENERAL COVERAGE: Business Names - Telugu
            {"query": "సంధ్య కన్వెన్షన్ ఎండీ", "priority": 4, "category": "business_general", "language": "te"},
            {"query": "సంధ్య కన్స్ట్రక్షన్స్ శ్రీధర్", "priority": 4, "category": "business_general", "language": "te"},
            {"query": "సంధ్య రియల్టర్స్ శ్రీధర్", "priority": 4, "category": "business_general", "language": "te"},
            {"query": "సంధ్య హోటల్స్ శ్రీధర్", "priority": 4, "category": "business_general", "language": "te"},
            {"query": "సంధ్య డైరెక్టర్", "priority": 4, "category": "business_general", "language": "te"},
            {"query": "సంధ్య ఓనర్", "priority": 4, "category": "business_general", "language": "te"},
            
            # GENERAL COVERAGE: English Business
            {"query": "Sandhya Convention MD Sridhar Rao", "priority": 4, "category": "business_general", "language": "en"},
            {"query": "Sandhya Construction Sridhar Rao", "priority": 4, "category": "business_general", "language": "en"},
            {"query": "Sandhya Realtors Sridhar Rao", "priority": 4, "category": "business_general", "language": "en"},
            
            # REGIONAL NEWS COVERAGE: Telugu
            {"query": "శ్రీధర్ రావు వార్తలు", "priority": 3, "category": "news_regional", "language": "te"},
            {"query": "శ్రీధర్ రావు బ్రేకింగ్ న్యూస్", "priority": 3, "category": "news_regional", "language": "te"},
            {"query": "శ్రీధర్ రావు హైదరాబాద్", "priority": 3, "category": "news_regional", "language": "te"},
            {"query": "శ్రీధర్ రావు తెలంగాణ", "priority": 3, "category": "news_regional", "language": "te"},
            
            # ALTERNATIVE NAME SPELLINGS: Telugu
            {"query": "శ్రీధర్ రావు", "priority": 3, "category": "name_variants", "language": "te"},
            {"query": "సంధ్య శ్రీధర్ రావు", "priority": 3, "category": "name_variants", "language": "te"},
            {"query": "శ్రీధర్", "priority": 2, "category": "name_variants", "language": "te"},
            {"query": "సంధ్య", "priority": 2, "category": "name_variants", "language": "te"}
        ]
    
    def get_enhanced_trusted_channels(self) -> Dict[str, int]:
        """Enhanced channel trust levels with comprehensive Telugu media coverage"""
        return {
            # Tier 1: Highest Trust Telugu News (9-10)
            "ABN Telugu": 10,
            "TV5 News": 10,
            "Zee Telugu News": 10, 
            "NTV Telugu": 10,
            "ETV Telangana": 10,
            
            # Tier 2: High Trust Regional (8-9)
            "Raj News Telugu": 9,
            "CVR News Telugu": 9,
            "CVR News": 9,
            "T News Telugu": 8,
            "V6 News Telugu": 8,
            "Mahaa News": 8,
            "Mahaa News Telangana": 8,
            
            # Tier 3: Medium-High Trust (7-8)
            "BRK News": 7,
            "BIG TV Live": 7,
            "BIG TV": 7,
            "Prime9 News": 7,
            "Prime9 Telangana": 7,
            "ANN Telugu": 7,
            
            # Tier 4: Medium Trust (5-6)
            "Mirror TV Telugu": 6,
            "MirrorTV Plus": 6,
            "99TV Telugu": 6,
            "10TV News Telugu": 6,
            "Tolivelugu": 6,
            "Kaloji Tv": 5,
            
            # Tier 5: Lower Trust but Relevant (3-4)
            "Shanarthi Telangana": 4,
            "Wild Wolf Telugu": 4,
            "Mana ToliVelugu Tv": 4,
            "News on Face": 4,
            "All in 1 Media": 3,
            
            # Default for unrecognized
            "_default": 2
        }
    
    def calculate_precise_relevance(self, title: str, channel: str, description: str = "", language: str = "mixed") -> float:
        """
        ENHANCED PRECISE relevance calculation with accurate Telugu term recognition
        Based on actual media usage patterns - NO ASSUMPTIONS, only verified scoring
        """
        score = 0.0
        text = f"{title} {description}".lower()
        
        # CRITICAL MULTIPLIER: Recent Black Magic Scandal Terms (40+ points possible)
        black_magic_telugu_critical = ["చేతబడి", "క్షుద్ర పూజలు", "ఆడియో లీక్"]
        black_magic_telugu_high = ["చంపేశా", "చంపించాడు", "బెదిరింపులు", "వైరల్"]
        black_magic_english_critical = ["black magic", "occult", "audio leak"]
        black_magic_english_high = ["threatening", "death threat", "viral audio"]
        
        # Critical terms get maximum weight
        for term in black_magic_telugu_critical:
            if term in text:
                score += 15.0  # 45 points possible for Telugu critical
                
        for term in black_magic_telugu_high:
            if term in text:
                score += 10.0  # 40 points possible for Telugu high-impact
                
        for term in black_magic_english_critical:
            if term in text:
                score += 12.0  # 36 points possible for English critical
                
        for term in black_magic_english_high:
            if term in text:
                score += 8.0   # 24 points possible for English high-impact
        
        # HIGH IMPACT: Legal/Criminal Terms (30+ points possible)
        legal_telugu_critical = ["అరెస్ట్", "భూకబ్జా", "కబ్జా", "హైడ్రా"]
        legal_telugu_standard = ["మోసం", "కేసు", "ఎఫ్‌ఐఆర్", "ఆక్రమణ", "కట్టడాల కూల్చివేత"]
        legal_english_critical = ["arrest", "land grab", "hydraa", "demolition"]
        legal_english_standard = ["case", "cheating", "fraud", "fir"]
        
        for term in legal_telugu_critical:
            if term in text:
                score += 8.0   # 32 points possible
                
        for term in legal_telugu_standard:
            if term in text:
                score += 5.0   # 25 points possible
                
        for term in legal_english_critical:
            if term in text:
                score += 6.0   # 24 points possible
                
        for term in legal_english_standard:
            if term in text:
                score += 3.0   # 12 points possible
        
        # ESSENTIAL: Name Recognition with precise matching (25+ points possible)
        name_telugu_exact = ["శ్రీధర్ రావు"]
        name_telugu_partial = ["శ్రీధర్", "మాగంటి గోపీనాథ్"]
        name_english_exact = ["sridhar rao", "sreedhar rao"]
        name_english_partial = ["maganti gopinath"]
        
        # Exact name matches get highest priority
        for term in name_telugu_exact:
            if term in text:
                score += 12.0  # Telugu exact names critical
                
        for term in name_telugu_partial:
            if term in text:
                score += 8.0   # Telugu partial names important
                
        for term in name_english_exact:
            if term in text:
                score += 12.0  # English exact names high priority (boosted for accuracy)
                
        for term in name_english_partial:
            if term in text:
                score += 6.0   # English partial names medium
        
        # BUSINESS CONTEXT: Company Terms (15+ points possible)
        business_telugu_primary = ["సంధ్య కన్వెన్షన్"]
        business_telugu_secondary = ["సంధ్య కన్స్ట్రక్షన్స్", "సంధ్య రియల్టర్స్", "సంధ్య హోటల్స్", "ఎండీ"]
        business_english_primary = ["sandhya convention"]
        business_english_secondary = ["sandhya construction", "sandhya realtors", "sandhya hotels"]
        
        for term in business_telugu_primary:
            if term in text:
                score += 6.0   # Primary business terms
                
        for term in business_telugu_secondary:
            if term in text:
                score += 3.0   # Secondary business terms
                
        for term in business_english_primary:
            if term in text:
                score += 5.0
                
        for term in business_english_secondary:
            if term in text:
                score += 2.5
        
        # GEOGRAPHIC/NEWS CONTEXT (10+ points possible)
        context_telugu_critical = ["వార్తలు", "బ్రేకింగ్ న్యూస్"]
        context_telugu_location = ["హైదరాబాద్", "తెలంగాణ", "గచ్చిబౌలి"]
        context_english = ["hyderabad", "telangana", "gachibowli", "news", "breaking"]
        
        for term in context_telugu_critical:
            if term in text:
                score += 3.0   # News context important
                
        for term in context_telugu_location:
            if term in text:
                score += 2.0   # Location context
                
        for term in context_english:
            if term in text:
                score += 1.5   # English context terms
        
        # CHANNEL TRUST MULTIPLIER (Enhanced weighting)
        channel_trust = self.get_enhanced_trusted_channels().get(channel, 2)
        if channel_trust >= 9:
            score += 12.0  # Top tier channels get significant boost
        elif channel_trust >= 7:
            score += 8.0   # High trust channels
        elif channel_trust >= 5:
            score += 4.0   # Medium trust
        else:
            score += channel_trust  # Low trust gets minimal boost
        
        # LANGUAGE PRECISION BONUS: Telugu content accuracy bonus
        telugu_indicators = ["శ్రీధర్", "సంధ్య", "కన్వెన్షన్", "రావు", "చేతబడి", "కబ్జా"]
        telugu_match_count = sum(1 for term in telugu_indicators if term in text)
        
        if telugu_match_count >= 3:
            score += 5.0   # High Telugu accuracy
        elif telugu_match_count >= 2:
            score += 3.0   # Medium Telugu accuracy
        elif telugu_match_count >= 1:
            score += 1.0   # Basic Telugu presence
        
        # ENGLISH CRITICAL CONTENT COMBINATION BONUS: For high-impact English coverage
        english_critical_indicators = ["sridhar rao", "black magic", "audio", "maganti gopinath"]
        english_match_count = sum(1 for term in english_critical_indicators if term in text)
        
        if english_match_count >= 3:
            score += 3.0   # High English critical accuracy bonus
        elif english_match_count >= 2:
            score += 1.5   # Medium English accuracy bonus
        
        return min(score, 100.0)  # Cap at 100
    
    def search_videos(self, query: str, max_results: int = 20, language: str = "mixed") -> List[Dict[str, Any]]:
        """Enhanced search with language-specific parameters"""
        self.logger.info(f"🔍 Searching ({language}): '{query}'")
        
        try:
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'order': 'relevance',
                'key': self.api_key,
                'regionCode': 'IN'
            }
            
            # Language-specific optimizations
            if language == "te":
                params['relevanceLanguage'] = 'te'
            elif language == "en":
                params['relevanceLanguage'] = 'en'
            
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            self.stats["api_calls"] += 1
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video_data = self._process_video(item, language)
                if video_data:
                    videos.append(video_data)
            
            self.logger.info(f"📊 Found {len(videos)} relevant videos")
            return videos
            
        except Exception as e:
            self.logger.error(f"❌ Search failed for '{query}': {e}")
            self.stats["errors"] += 1
            return []
    
    def _process_video(self, item: Dict[str, Any], language: str = "mixed") -> Optional[Dict[str, Any]]:
        """Enhanced video processing with precise relevance filtering"""
        try:
            snippet = item['snippet']
            video_id = item['id']['videoId']
            
            title = snippet.get('title', '').strip()
            channel = snippet.get('channelTitle', '').strip()
            description = snippet.get('description', '').strip()
            upload_date = snippet.get('publishedAt', '')[:10]
            
            # Calculate precise relevance
            relevance = self.calculate_precise_relevance(title, channel, description, language)
            
            # Higher threshold for quality - no low-relevance content
            if relevance < 25.0:
                return None
            
            # Track language distribution
            if language == "te":
                self.stats["telugu_videos"] += 1
            elif language == "en":
                self.stats["english_videos"] += 1
            
            if relevance >= 50.0:
                self.stats["high_relevance_videos"] += 1
            
            return {
                'video_id': video_id,
                'title': title,
                'channel': channel,
                'description': description,
                'upload_date': upload_date,
                'relevance_score': relevance,
                'primary_language': language,
                'youtube_url': f"https://www.youtube.com/watch?v={video_id}"
            }
            
        except Exception as e:
            self.logger.warning(f"⚠️ Error processing video: {e}")
            return None
    
    def run_comprehensive_extraction(self, max_videos_per_query: int = 20):
        """Run comprehensive bilingual extraction with precise targeting"""
        self.logger.info("🚀 Starting Enhanced Bilingual Sridhar Rao Extraction")
        self.logger.info("=" * 70)
        
        keywords = self.get_comprehensive_telugu_keywords()
        all_videos = []
        
        # Process by priority groups for optimal API usage
        priority_groups = {
            "Critical (10)": [k for k in keywords if k['priority'] == 10],
            "High (9)": [k for k in keywords if k['priority'] == 9], 
            "Medium-High (8)": [k for k in keywords if k['priority'] == 8],
            "Medium (6-7)": [k for k in keywords if k['priority'] in [6, 7]],
            "Lower (3-5)": [k for k in keywords if k['priority'] in [3, 4, 5]],
            "Broad (2)": [k for k in keywords if k['priority'] == 2]
        }
        
        for group_name, group_keywords in priority_groups.items():
            self.logger.info(f"\n📋 Processing {group_name} Keywords: {len(group_keywords)} terms")
            
            for keyword_data in group_keywords:
                query = keyword_data['query']
                priority = keyword_data['priority']
                category = keyword_data['category']
                language = keyword_data['language']
                
                self.logger.info(f"🎯 P{priority} ({language}): {category} - '{query}'")
                
                videos = self.search_videos(query, max_videos_per_query, language)
                all_videos.extend(videos)
                self.stats["videos_found"] += len(videos)
                
                # Adaptive rate limiting based on priority
                if priority >= 9:
                    time.sleep(0.3)  # Slower for high priority
                else:
                    time.sleep(0.2)
        
        # Enhanced deduplication
        unique_videos = self._enhanced_deduplication(all_videos)
        
        # Process to schema
        processed_videos = self.process_to_schema(unique_videos)
        
        # Save data
        self.save_enhanced_data(processed_videos)
        
        # Generate comprehensive report
        self._generate_bilingual_report(processed_videos)
        
        return processed_videos
    
    def _enhanced_deduplication(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhanced deduplication preserving highest relevance scores"""
        video_map = {}
        
        for video in videos:
            video_id = video['video_id']
            if video_id in video_map:
                # Keep video with higher relevance score
                if video['relevance_score'] > video_map[video_id]['relevance_score']:
                    video_map[video_id] = video
            else:
                video_map[video_id] = video
        
        unique_videos = list(video_map.values())
        duplicates_removed = len(videos) - len(unique_videos)
        
        self.logger.info(f"🔄 Removed {duplicates_removed} duplicates, {len(unique_videos)} unique videos remain")
        return unique_videos
    
    def process_to_schema(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process videos to enhanced v2.0 schema"""
        self.logger.info(f"⚙️ Processing {len(videos)} videos to v2.0 schema...")
        
        # Get video statistics
        video_ids = [v['video_id'] for v in videos]
        video_stats = self.get_video_stats(video_ids)
        
        processed = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        for video in videos:
            try:
                video_id = video['video_id']
                stats = video_stats.get(video_id, {})
                
                # Enhanced trust level calculation
                channel = video['channel']
                trust_levels = self.get_enhanced_trusted_channels()
                trust_level = 1 if trust_levels.get(channel, 0) >= 7 else 0
                
                if trust_level == 1:
                    self.stats["trusted_source_videos"] += 1
                
                # Create enhanced schema record
                record = {
                    'VideoID': video_id,
                    'Title': video['title'],
                    'Channel': channel,
                    'UploadDate': video['upload_date'],
                    'Fetched_Date': today,
                    'Views': stats.get('view_count', 0),
                    'Comments': stats.get('comment_count', 0),
                    'RelevanceScore': round(video['relevance_score'], 2),
                    'TrustLevel': trust_level,
                    'Transcript_EN': "",
                    'Transcript_TE': "",
                    'Summary_EN': "",
                    'Summary_TE': "",
                    'SentimentScore_EN': 0.0,
                    'SentimentLabel_EN': "",
                    'SentimentScore_TE': 0.0,
                    'SentimentLabel_TE': "",
                    'Keywords_EN': "",
                    'Keywords_TE': "",
                    'DataHealth': 90.0,  # High health for extracted data
                    'ProcessingStatus': "pending"
                }
                
                processed.append(record)
                self.stats["relevant_videos"] += 1
                
            except Exception as e:
                self.logger.error(f"❌ Error processing video {video.get('video_id')}: {e}")
                continue
        
        return processed
    
    def get_video_stats(self, video_ids: List[str]) -> Dict[str, Dict[str, int]]:
        """Get comprehensive video statistics"""
        if not video_ids:
            return {}
        
        try:
            all_stats = {}
            batch_size = 50
            
            for i in range(0, len(video_ids), batch_size):
                batch_ids = video_ids[i:i + batch_size]
                
                params = {
                    'part': 'statistics',
                    'id': ','.join(batch_ids),
                    'key': self.api_key
                }
                
                response = requests.get(f"{self.base_url}/videos", params=params)
                response.raise_for_status()
                
                self.stats["api_calls"] += 1
                data = response.json()
                
                for item in data.get('items', []):
                    video_id = item['id']
                    stats = item.get('statistics', {})
                    
                    all_stats[video_id] = {
                        'view_count': int(stats.get('viewCount', 0)),
                        'comment_count': int(stats.get('commentCount', 0)),
                        'like_count': int(stats.get('likeCount', 0))
                    }
                
                time.sleep(0.1)
            
            return all_stats
            
        except Exception as e:
            self.logger.error(f"❌ Error getting video statistics: {e}")
            return {}
    
    def save_enhanced_data(self, videos: List[Dict[str, Any]]):
        """Save enhanced dataset with validation"""
        if not videos:
            self.logger.warning("⚠️ No videos to save")
            return
        
        try:
            df = pd.DataFrame(videos)
            
            # Ensure complete schema compliance
            for col in VIDEO_SCHEMA_V2:
                if col not in df.columns:
                    df[col] = ""
            
            df = df[VIDEO_SCHEMA_V2]
            df.to_csv(self.output_file, index=False)
            
            self.logger.info(f"💾 Saved {len(videos)} videos to {self.output_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving data: {e}")
            raise
    
    def _generate_bilingual_report(self, videos: List[Dict[str, Any]]):
        """Generate comprehensive bilingual extraction report"""
        if not videos:
            print("❌ No videos extracted")
            return
        
        df = pd.DataFrame(videos)
        
        print("\n" + "="*80)
        print("🎯 ENHANCED BILINGUAL EXTRACTION REPORT - SRIDHAR RAO")
        print("="*80)
        
        # Basic Stats
        print(f"📊 Total Videos Extracted: {len(videos)}")
        print(f"🔄 API Calls Made: {self.stats['api_calls']}")
        print(f"⚠️ Errors Encountered: {self.stats['errors']}")
        
        # Language Distribution
        print(f"\n🌐 Language Distribution:")
        print(f"   📝 Telugu-focused searches: {self.stats['telugu_videos']} videos")
        print(f"   📝 English-focused searches: {self.stats['english_videos']} videos")
        
        # Relevance Analysis
        print(f"\n📈 Relevance Distribution:")
        high_rel = len(df[df['RelevanceScore'] >= 50])
        med_rel = len(df[(df['RelevanceScore'] >= 35) & (df['RelevanceScore'] < 50)])
        low_rel = len(df[df['RelevanceScore'] < 35])
        print(f"   🎯 High Relevance (50+): {high_rel} videos")
        print(f"   📊 Medium Relevance (35-49): {med_rel} videos")
        print(f"   📉 Lower Relevance (<35): {low_rel} videos")
        
        # Trust Analysis
        print(f"\n🏆 Source Quality:")
        print(f"   ✅ Trusted Sources (TrustLevel=1): {self.stats['trusted_source_videos']} videos")
        print(f"   ⚠️ Other Sources: {len(videos) - self.stats['trusted_source_videos']} videos")
        
        # Top Channels
        print(f"\n📺 Top Contributing Channels:")
        channel_counts = df['Channel'].value_counts().head(8)
        for i, (channel, count) in enumerate(channel_counts.items(), 1):
            trust_indicator = "✅" if self.get_enhanced_trusted_channels().get(channel, 0) >= 7 else "⚠️"
            print(f"   {i}. {trust_indicator} {channel}: {count} videos")
        
        # Temporal Analysis
        print(f"\n📅 Temporal Distribution:")
        recent_2025 = len(df[df['UploadDate'] >= '2025-01-01'])
        recent_2024 = len(df[df['UploadDate'] >= '2024-01-01'])
        print(f"   🔥 Recent (2025): {recent_2025} videos")
        print(f"   📊 Last Year (2024+): {recent_2024} videos")
        
        # Quality Metrics
        avg_relevance = df['RelevanceScore'].mean()
        max_relevance = df['RelevanceScore'].max()
        print(f"\n📊 Quality Metrics:")
        print(f"   📈 Average Relevance: {avg_relevance:.1f}")
        print(f"   🎯 Maximum Relevance: {max_relevance:.1f}")
        
        print(f"\n💾 Data saved to: {self.output_file}")
        print(f"🎯 Ready for Phase 2: AI Processing Pipeline!")
        print("="*80)


def main():
    """Main execution function"""
    print("🚀 Enhanced Bilingual YouTube Extractor for Sridhar Rao")
    print("=" * 60)
    print("🎯 Precision bilingual extraction with comprehensive Telugu coverage")
    print("📋 Based on 20 years of media intelligence and actual terminology usage")
    print()
    
    try:
        extractor = EnhancedTeluguExtractor()
        
        print("⚙️ Configuration:")
        print(f"   📝 Telugu keywords prioritized")
        print(f"   🏆 {len(extractor.get_enhanced_trusted_channels())} trusted channels")
        print(f"   🎯 {len(extractor.get_comprehensive_telugu_keywords())} search terms")
        print()
        
        videos = extractor.run_comprehensive_extraction(max_videos_per_query=25)
        
        print(f"\n🎉 Extraction completed successfully!")
        print(f"📊 Total relevant videos: {len(videos)}")
        print(f"🎯 High-precision bilingual dataset ready for AI processing!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 