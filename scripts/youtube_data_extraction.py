#!/usr/bin/env python3
"""
Percepta Pro v2.0 - Comprehensive YouTube Data Extraction
=======================================================

Specialized extraction script for Sridhar Rao (Sandhya Convention MD) 
based on detailed client profile and 25 years of research intelligence.

Target: 300-500 relevant videos across Telugu and English channels
Focus: Recent controversies, legal issues, political connections

Author: Percepta Development Team
Usage: python scripts/youtube_data_extraction.py
"""

import os
import sys
import pandas as pd
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import requests
from urllib.parse import quote_plus

# Add backend to path for schema imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from data.videos.schema_v2 import (
        VIDEO_SCHEMA_V2, 
        calculate_relevance_score, 
        determine_trust_level,
        VideoSchemaValidator
    )
except ImportError:
    print("❌ Error: Could not import schema_v2. Please ensure backend/data/videos/schema_v2.py exists.")
    sys.exit(1)


class SridharRaoYouTubeExtractor:
    """Specialized YouTube data extractor for Sridhar Rao coverage"""
    
    def __init__(self, api_key: str = None):
        """Initialize the extractor with YouTube API key"""
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("❌ YouTube API key not found. Set YOUTUBE_API_KEY environment variable.")
        
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.output_file = "backend/data/videos/youtube_videos.csv"
        self.backup_file = f"backend/data/videos/youtube_videos_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Setup logging
        self._setup_logging()
        
        # Extraction statistics
        self.stats = {
            "start_time": datetime.now(),
            "total_searches": 0,
            "total_videos_found": 0,
            "relevant_videos": 0,
            "duplicates_skipped": 0,
            "api_calls": 0,
            "errors": 0
        }
        
        # Rate limiting
        self.request_delay = 0.1  # 100ms between requests
        self.daily_quota_used = 0
        self.max_daily_quota = 10000  # YouTube API daily limit
        
    def _setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = "scripts/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = f"{log_dir}/extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_search_keywords(self) -> List[Dict[str, Any]]:
        """
        Get comprehensive search keywords based on client intelligence
        Organized by priority and controversy type
        """
        
        # HIGH PRIORITY: Recent Major Scandals (June 2025)
        high_priority_keywords = [
            {
                "query": "සංධ්‍ය ශ්‍රීධර් රාවු ආඩියෝ ලීක්",
                "category": "black_magic_audio",
                "priority": 10,
                "description": "Black magic audio leak (Telugu)"
            },
            {
                "query": "Sridhar Rao black magic audio",
                "category": "black_magic_audio", 
                "priority": 10,
                "description": "Black magic audio leak (English)"
            },
            {
                "query": "Maganti Gopinath Sridhar Rao death",
                "category": "black_magic_audio",
                "priority": 10,
                "description": "Maganti Gopinath death connection"
            },
            {
                "query": "සංධ්‍ය කන්වෙන්ශන් ශ්‍රීධර් රාවු ක්‍ෂුද්‍ර පූජා",
                "category": "black_magic_audio",
                "priority": 10,
                "description": "Sandhya Convention occult practices (Telugu)"
            }
        ]
        
        # MEDIUM-HIGH PRIORITY: Recent Legal Issues (2025)
        medium_high_keywords = [
            {
                "query": "Sridhar Rao HYDRAA demolition",
                "category": "land_grab_2025",
                "priority": 9,
                "description": "HYDRAA demolitions 2025"
            },
            {
                "query": "සංධ්‍ය ශ්‍රීධර් රාවු ගච්චිබෝව්ලි",
                "category": "land_grab_2025", 
                "priority": 9,
                "description": "Gachibowli land issues (Telugu)"
            },
            {
                "query": "Sridhar Rao arrest 2025",
                "category": "legal_2025",
                "priority": 9,
                "description": "2025 arrests and legal issues"
            },
            {
                "query": "Sandhya Convention land grab",
                "category": "land_grab_2025",
                "priority": 9,
                "description": "Land grabbing allegations"
            }
        ]
        
        # MEDIUM PRIORITY: Historical Controversies (2023-2024)
        medium_keywords = [
            {
                "query": "Sridhar Rao cheating case",
                "category": "legal_historical",
                "priority": 7,
                "description": "Historical cheating cases"
            },
            {
                "query": "Sridhar Rao Delhi arrest 2023",
                "category": "legal_historical",
                "priority": 7,
                "description": "2023 Delhi arrest"
            },
            {
                "query": "සංධ්‍ය කන්ස්ට්‍රක්ශන් ශ්‍රීධර් රාවු",
                "category": "business_disputes",
                "priority": 6,
                "description": "Sandhya Construction disputes (Telugu)"
            },
            {
                "query": "Sridhar Rao phone tapping case",
                "category": "political_connections",
                "priority": 6,
                "description": "Phone tapping investigation"
            }
        ]
        
        # LOWER PRIORITY: General Business Coverage
        lower_keywords = [
            {
                "query": "Sandhya Convention MD Sridhar Rao",
                "category": "business_general",
                "priority": 5,
                "description": "General business coverage"
            },
            {
                "query": "සංධ්‍ය කන්වෙන්ශන් එම්ඩී",
                "category": "business_general",
                "priority": 5,
                "description": "Sandhya Convention MD (Telugu)"
            },
            {
                "query": "Sridhar Rao real estate",
                "category": "business_general",
                "priority": 4,
                "description": "Real estate business coverage"
            }
        ]
        
        # Combine all keywords, sorted by priority
        all_keywords = high_priority_keywords + medium_high_keywords + medium_keywords + lower_keywords
        return sorted(all_keywords, key=lambda x: x['priority'], reverse=True)
    
    def get_channel_priorities(self) -> Dict[str, int]:
        """
        Get channel trust levels based on client intelligence
        
        Returns:
            Dict mapping channel names to trust levels (0-10)
        """
        return {
            # Tier 1: High Trust Mainstream (9-10)
            "ABN Telugu": 10,
            "TV5 News": 10, 
            "Zee Telugu News": 10,
            "NTV Telugu": 10,
            
            # Tier 2: Medium-High Trust Regional (7-8)
            "Raj News Telugu": 8,
            "CVR News Telugu": 8,
            "CVR News": 8,
            "BRK News": 7,
            "BIG TV Live": 7,
            "BIG TV": 7,
            
            # Tier 3: Secondary Sources (5-6)
            "Mirror TV Telugu": 6,
            "MirrorTV Plus": 6,
            "Prime9 News": 6,
            "Mahaa News": 6,
            "T News Telugu": 6,
            "V6 News Telugu": 6,
            
            # Tier 4: Lower Priority (3-4)
            "ANN Telugu": 4,
            "Tolivelugu": 4,
            "99TV Telugu": 4,
            "10TV News Telugu": 4,
            
            # Default for unrecognized channels
            "_default": 2
        }
    
    def calculate_sridhar_relevance(self, title: str, channel: str, description: str = "") -> float:
        """
        Calculate relevance score specifically for Sridhar Rao content
        
        Args:
            title: Video title
            channel: Channel name
            description: Video description
            
        Returns:
            Relevance score (0-100)
        """
        score = 0.0
        text = f"{title} {description}".lower()
        
        # HIGH VALUE: Recent major scandals (40 points max)
        black_magic_terms = [
            "black magic", "ක්‍ෂුද්‍ර පූජා", "occult", "ritual", "death threat",
            "maganti gopinath", "audio leak", "ආඩියෝ ලීක්"
        ]
        for term in black_magic_terms:
            if term.lower() in text:
                score += 8.0  # Up to 40 points total
        
        # HIGH VALUE: Legal issues (30 points max)
        legal_terms = [
            "arrest", "case", "court", "police", "fir", "cheating", 
            "fraud", "land grab", "hydraa", "demolition"
        ]
        for term in legal_terms:
            if term.lower() in text:
                score += 5.0  # Up to 30 points total
        
        # MEDIUM VALUE: Business/Political (20 points max)
        business_terms = [
            "sandhya convention", "sandhya construction", "real estate",
            "brs", "political", "controversy"
        ]
        for term in business_terms:
            if term.lower() in text:
                score += 4.0  # Up to 20 points total
        
        # MEDIUM VALUE: Name variations (15 points max)
        name_terms = [
            "sridhar rao", "ශ්‍රීධර් රාවු", "sreedhar rao", "sridhar", "ශ්‍රීධර්"
        ]
        for term in name_terms:
            if term.lower() in text:
                score += 3.0  # Up to 15 points total
        
        # Channel trust bonus (0-10 points)
        channel_priorities = self.get_channel_priorities()
        channel_score = channel_priorities.get(channel, channel_priorities["_default"])
        score += channel_score
        
        # Recent content bonus (0-15 points based on upload date)
        # This would be implemented when we have upload date info
        
        return min(score, 100.0)  # Cap at 100
    
    def search_youtube_videos(self, query: str, max_results: int = 50, 
                            published_after: str = None) -> List[Dict[str, Any]]:
        """
        Search YouTube videos using the API
        
        Args:
            query: Search query
            max_results: Maximum results to return
            published_after: ISO date string for filtering recent content
            
        Returns:
            List of video data dictionaries
        """
        self.logger.info(f"🔍 Searching: '{query}' (max: {max_results})")
        
        try:
            # Build search parameters
            params = {
                'part': 'snippet,statistics',
                'q': query,
                'type': 'video',
                'maxResults': min(max_results, 50),  # API limit per request
                'order': 'relevance',
                'key': self.api_key,
                'regionCode': 'IN',  # Focus on Indian content
                'relevanceLanguage': 'te'  # Telugu language preference
            }
            
            if published_after:
                params['publishedAfter'] = published_after
            
            # Make API request
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            self.api_calls += 1
            self.daily_quota_used += 100  # Each search costs ~100 quota units
            
            data = response.json()
            videos = []
            
            # Process each video
            for item in data.get('items', []):
                try:
                    video_data = self._process_video_item(item)
                    if video_data:
                        videos.append(video_data)
                except Exception as e:
                    self.logger.warning(f"Error processing video item: {e}")
                    continue
            
            # Rate limiting
            time.sleep(self.request_delay)
            
            self.logger.info(f"📊 Found {len(videos)} videos for query: '{query}'")
            return videos
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ API request failed for query '{query}': {e}")
            self.stats["errors"] += 1
            return []
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in search for '{query}': {e}")
            self.stats["errors"] += 1
            return []
    
    def _process_video_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single video item from YouTube API response
        
        Args:
            item: Video item from API response
            
        Returns:
            Processed video data or None if not relevant
        """
        try:
            snippet = item['snippet']
            video_id = item['id']['videoId']
            
            # Extract basic info
            title = snippet.get('title', '').strip()
            channel = snippet.get('channelTitle', '').strip()
            description = snippet.get('description', '').strip()
            upload_date = snippet.get('publishedAt', '')[:10]  # YYYY-MM-DD format
            thumbnail = snippet.get('thumbnails', {}).get('default', {}).get('url', '')
            
            # Calculate relevance score
            relevance_score = self.calculate_sridhar_relevance(title, channel, description)
            
            # Filter out low relevance content
            if relevance_score < 15.0:  # Minimum threshold for Sridhar Rao content
                return None
            
            # Get additional statistics if available
            view_count = 0
            comment_count = 0
            
            # Create video data structure
            video_data = {
                'video_id': video_id,
                'title': title,
                'channel': channel,
                'description': description,
                'upload_date': upload_date,
                'thumbnail_url': thumbnail,
                'view_count': view_count,
                'comment_count': comment_count,
                'relevance_score': relevance_score,
                'youtube_url': f"https://www.youtube.com/watch?v={video_id}"
            }
            
            return video_data
            
        except Exception as e:
            self.logger.warning(f"Error processing video item: {e}")
            return None
    
    def get_video_statistics(self, video_ids: List[str]) -> Dict[str, Dict[str, int]]:
        """
        Get detailed statistics for a batch of videos
        
        Args:
            video_ids: List of video IDs
            
        Returns:
            Dictionary mapping video IDs to their statistics
        """
        if not video_ids:
            return {}
        
        try:
            # Batch video IDs (API allows up to 50 per request)
            batch_size = 50
            all_stats = {}
            
            for i in range(0, len(video_ids), batch_size):
                batch_ids = video_ids[i:i + batch_size]
                
                params = {
                    'part': 'statistics',
                    'id': ','.join(batch_ids),
                    'key': self.api_key
                }
                
                response = requests.get(f"{self.base_url}/videos", params=params)
                response.raise_for_status()
                
                self.api_calls += 1
                self.daily_quota_used += 1  # Statistics call costs 1 quota unit
                
                data = response.json()
                
                for item in data.get('items', []):
                    video_id = item['id']
                    stats = item.get('statistics', {})
                    
                    all_stats[video_id] = {
                        'view_count': int(stats.get('viewCount', 0)),
                        'comment_count': int(stats.get('commentCount', 0)),
                        'like_count': int(stats.get('likeCount', 0))
                    }
                
                time.sleep(self.request_delay)
            
            return all_stats
            
        except Exception as e:
            self.logger.error(f"Error fetching video statistics: {e}")
            return {}
    
    def process_extracted_videos(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process extracted videos into v2.0 schema format
        
        Args:
            videos: Raw video data from API
            
        Returns:
            Processed videos matching schema
        """
        self.logger.info(f"🔄 Processing {len(videos)} extracted videos...")
        
        # Get video statistics in batches
        video_ids = [v['video_id'] for v in videos]
        video_stats = self.get_video_statistics(video_ids)
        
        processed_videos = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        for video_data in videos:
            try:
                video_id = video_data['video_id']
                
                # Get statistics
                stats = video_stats.get(video_id, {})
                views = stats.get('view_count', 0)
                comments = stats.get('comment_count', 0)
                
                # Calculate final scores
                relevance_score = video_data['relevance_score']
                channel = video_data['channel']
                trust_level = 1 if self.get_channel_priorities().get(channel, 0) >= 7 else 0
                
                # Calculate data health
                data_health = self._calculate_data_health(
                    video_data['title'], 
                    channel, 
                    video_data['upload_date'], 
                    views, 
                    comments
                )
                
                # Create v2.0 schema record
                processed_video = {
                    'VideoID': video_id,
                    'Title': video_data['title'],
                    'Channel': channel,
                    'UploadDate': video_data['upload_date'],
                    'Fetched_Date': today,
                    'Views': views,
                    'Comments': comments,
                    'RelevanceScore': round(relevance_score, 2),
                    'TrustLevel': trust_level,
                    'Transcript_EN': "",  # To be filled by AI processing
                    'Transcript_TE': "",  # To be filled by AI processing
                    'Summary_EN': "",     # To be filled by AI processing
                    'Summary_TE': "",     # To be filled by AI processing
                    'SentimentScore_EN': 0.0,  # To be filled by AI processing
                    'SentimentLabel_EN': "",   # To be filled by AI processing
                    'SentimentScore_TE': 0.0,  # To be filled by AI processing
                    'SentimentLabel_TE': "",   # To be filled by AI processing
                    'Keywords_EN': "",    # To be filled by AI processing
                    'Keywords_TE': "",    # To be filled by AI processing
                    'DataHealth': round(data_health, 2),
                    'ProcessingStatus': "pending"
                }
                
                processed_videos.append(processed_video)
                self.stats["relevant_videos"] += 1
                
            except Exception as e:
                self.logger.error(f"Error processing video {video_data.get('video_id', 'unknown')}: {e}")
                self.stats["errors"] += 1
                continue
        
        self.logger.info(f"✅ Successfully processed {len(processed_videos)} videos")
        return processed_videos
    
    def _calculate_data_health(self, title: str, channel: str, upload_date: str, 
                              views: int, comments: int) -> float:
        """Calculate data health score for a video"""
        score = 0.0
        
        # Title quality (25 points)
        if title and len(title.strip()) > 10:
            score += 25
        elif title:
            score += 10
        
        # Channel quality (25 points)
        channel_trust = self.get_channel_priorities().get(channel, 2)
        score += (channel_trust / 10) * 25
        
        # Date quality (20 points)
        if upload_date:
            try:
                datetime.strptime(upload_date, "%Y-%m-%d")
                score += 20
            except ValueError:
                score += 5
        
        # Engagement metrics (30 points)
        if views > 0:
            score += 10
            if views > 1000:
                score += 5
            if views > 10000:
                score += 5
        
        if comments > 0:
            score += 10
        
        return min(score, 100.0)
    
    def remove_duplicates(self, videos: List[Dict[str, Any]], 
                         existing_videos: List[str] = None) -> List[Dict[str, Any]]:
        """
        Remove duplicate videos based on VideoID
        
        Args:
            videos: List of video records
            existing_videos: List of existing video IDs to avoid
            
        Returns:
            Deduplicated video list
        """
        existing_ids = set(existing_videos) if existing_videos else set()
        seen_ids = set()
        unique_videos = []
        
        for video in videos:
            video_id = video['VideoID']
            
            if video_id in existing_ids:
                self.stats["duplicates_skipped"] += 1
                continue
                
            if video_id in seen_ids:
                self.stats["duplicates_skipped"] += 1
                continue
            
            seen_ids.add(video_id)
            unique_videos.append(video)
        
        self.logger.info(f"🔄 Removed {len(videos) - len(unique_videos)} duplicates")
        return unique_videos
    
    def save_extracted_data(self, videos: List[Dict[str, Any]], backup_existing: bool = True):
        """
        Save extracted videos to CSV file
        
        Args:
            videos: Processed video records
            backup_existing: Whether to backup existing data
        """
        if not videos:
            self.logger.warning("No videos to save")
            return
        
        try:
            # Backup existing data if requested
            if backup_existing and os.path.exists(self.output_file):
                os.rename(self.output_file, self.backup_file)
                self.logger.info(f"📦 Backed up existing data to: {self.backup_file}")
            
            # Create DataFrame and save
            df = pd.DataFrame(videos)
            
            # Ensure schema compliance
            for col in VIDEO_SCHEMA_V2:
                if col not in df.columns:
                    df[col] = ""
            
            # Reorder columns to match schema
            df = df[VIDEO_SCHEMA_V2]
            
            # Save to file
            df.to_csv(self.output_file, index=False)
            self.logger.info(f"💾 Saved {len(videos)} videos to: {self.output_file}")
            
            # Validate saved data
            validator = VideoSchemaValidator()
            results = validator.validate_dataframe(df)
            
            if results["valid"]:
                self.logger.info("✅ Data validation passed!")
            else:
                self.logger.warning("⚠️ Data validation warnings found")
                for warning in results["warnings"]:
                    self.logger.warning(f"   • {warning}")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving data: {e}")
            raise
    
    def run_comprehensive_extraction(self, max_videos_per_query: int = 50, 
                                   focus_recent_months: int = 6) -> Dict[str, Any]:
        """
        Run comprehensive extraction for Sridhar Rao content
        
        Args:
            max_videos_per_query: Maximum videos per search query
            focus_recent_months: Number of recent months to prioritize
            
        Returns:
            Extraction report
        """
        self.logger.info("🚀 Starting Comprehensive Sridhar Rao Content Extraction")
        self.logger.info("=" * 80)
        
        # Calculate date filter for recent content
        recent_date = (datetime.now() - timedelta(days=focus_recent_months * 30)).isoformat() + 'Z'
        
        try:
            # Get keywords and channel priorities
            keywords = self.get_search_keywords()
            all_videos = []
            
            # Load existing video IDs to avoid duplicates
            existing_ids = []
            if os.path.exists(self.output_file):
                try:
                    existing_df = pd.read_csv(self.output_file)
                    existing_ids = existing_df['VideoID'].tolist() if 'VideoID' in existing_df.columns else []
                    self.logger.info(f"📂 Found {len(existing_ids)} existing videos to avoid duplicates")
                except Exception as e:
                    self.logger.warning(f"Could not load existing data: {e}")
            
            # Process each keyword by priority
            for keyword_data in keywords:
                query = keyword_data['query']
                priority = keyword_data['priority']
                category = keyword_data['category']
                
                self.logger.info(f"🔍 Processing Priority {priority} - {category}: '{query}'")
                
                # Check quota limits
                if self.daily_quota_used >= self.max_daily_quota * 0.9:  # 90% of quota
                    self.logger.warning("⚠️ Approaching daily API quota limit, stopping extraction")
                    break
                
                # Search for recent content first (higher priority)
                if priority >= 8:  # High priority searches get recent filter
                    recent_videos = self.search_youtube_videos(
                        query, 
                        max_results=max_videos_per_query,
                        published_after=recent_date
                    )
                    all_videos.extend(recent_videos)
                    self.stats["total_searches"] += 1
                
                # Search for all-time content
                all_time_videos = self.search_youtube_videos(
                    query, 
                    max_results=max_videos_per_query // 2  # Fewer for all-time to save quota
                )
                all_videos.extend(all_time_videos)
                self.stats["total_searches"] += 1
                self.stats["total_videos_found"] += len(all_time_videos)
                
                # Rate limiting between queries
                time.sleep(self.request_delay * 2)
            
            self.logger.info(f"🎯 Raw extraction complete: {len(all_videos)} videos found")
            
            # Process and clean the data
            processed_videos = self.process_extracted_videos(all_videos)
            unique_videos = self.remove_duplicates(processed_videos, existing_ids)
            
            # Save the data
            if unique_videos:
                self.save_extracted_data(unique_videos)
            
            # Generate final report
            report = self._generate_extraction_report(unique_videos)
            
            self.logger.info("🎉 Extraction completed successfully!")
            return report
            
        except Exception as e:
            self.logger.error(f"❌ Extraction failed: {e}")
            self.stats["errors"] += 1
            return self._generate_extraction_report([])
    
    def _generate_extraction_report(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive extraction report"""
        end_time = datetime.now()
        duration = (end_time - self.stats["start_time"]).total_seconds()
        
        # Analyze extracted videos
        if videos:
            df = pd.DataFrame(videos)
            
            # Channel analysis
            channel_counts = df['Channel'].value_counts().head(10).to_dict()
            
            # Relevance analysis
            high_relevance = len(df[df['RelevanceScore'] >= 50])
            medium_relevance = len(df[(df['RelevanceScore'] >= 25) & (df['RelevanceScore'] < 50)])
            low_relevance = len(df[df['RelevanceScore'] < 25])
            
            # Trust analysis
            trusted_sources = len(df[df['TrustLevel'] == 1])
            
            # Date analysis
            recent_videos = len(df[df['UploadDate'] >= '2025-01-01'])
            
        else:
            channel_counts = {}
            high_relevance = medium_relevance = low_relevance = 0
            trusted_sources = recent_videos = 0
        
        report = {
            "extraction_summary": {
                "start_time": self.stats["start_time"].isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": round(duration, 1),
                "status": "success" if self.stats["errors"] == 0 else "completed_with_errors"
            },
            "api_usage": {
                "total_api_calls": self.api_calls,
                "quota_used": self.daily_quota_used,
                "quota_remaining": self.max_daily_quota - self.daily_quota_used
            },
            "extraction_stats": {
                "total_searches": self.stats["total_searches"],
                "raw_videos_found": self.stats["total_videos_found"],
                "relevant_videos_extracted": len(videos),
                "duplicates_skipped": self.stats["duplicates_skipped"],
                "errors_encountered": self.stats["errors"]
            },
            "content_analysis": {
                "high_relevance_videos": high_relevance,
                "medium_relevance_videos": medium_relevance,
                "low_relevance_videos": low_relevance,
                "trusted_source_videos": trusted_sources,
                "recent_2025_videos": recent_videos
            },
            "top_channels": channel_counts,
            "recommendations": [
                "Review high-relevance videos for immediate analysis",
                "Prioritize trusted source content for reputation monitoring",
                "Set up automated monitoring for new content",
                "Consider deeper analysis of recent controversy coverage"
            ]
        }
        
        return report


def main():
    """Main extraction function"""
    print("🚀 Sridhar Rao YouTube Content Extraction")
    print("=" * 50)
    
    try:
        # Initialize extractor
        extractor = SridharRaoYouTubeExtractor()
        
        # Run comprehensive extraction
        report = extractor.run_comprehensive_extraction(
            max_videos_per_query=30,  # Conservative to manage quota
            focus_recent_months=6     # Focus on last 6 months
        )
        
        # Display final report
        print("\n" + "="*80)
        print("📋 EXTRACTION COMPLETION REPORT")
        print("="*80)
        
        print(f"⏱️  Duration: {report['extraction_summary']['duration_seconds']}s")
        print(f"📊 Videos Extracted: {report['extraction_stats']['relevant_videos_extracted']}")
        print(f"🎯 High Relevance: {report['content_analysis']['high_relevance_videos']}")
        print(f"✅ Trusted Sources: {report['content_analysis']['trusted_source_videos']}")
        print(f"📅 Recent (2025): {report['content_analysis']['recent_2025_videos']}")
        print(f"🔄 API Calls: {report['api_usage']['total_api_calls']}")
        print(f"📈 Quota Used: {report['api_usage']['quota_used']}")
        
        if report['top_channels']:
            print(f"\n🎬 Top Channels:")
            for channel, count in list(report['top_channels'].items())[:5]:
                print(f"   • {channel}: {count} videos")
        
        print(f"\n✅ Status: {report['extraction_summary']['status'].upper()}")
        
        if report['extraction_stats']['errors_encountered'] > 0:
            print(f"⚠️  Errors: {report['extraction_stats']['errors_encountered']}")
        
        print("\n🎯 Ready for Phase 2: AI Processing Pipeline!")
        
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 