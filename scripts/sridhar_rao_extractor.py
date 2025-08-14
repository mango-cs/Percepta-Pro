#!/usr/bin/env python3
"""
Sridhar Rao YouTube Content Extractor
===================================

Specialized extraction for Sridhar Rao (Sandhya Convention MD) based on 
detailed client intelligence and controversy mapping.

Usage: python scripts/sridhar_rao_extractor.py
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


class SridharRaoExtractor:
    """YouTube extractor specifically for Sridhar Rao content"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key not found. Set YOUTUBE_API_KEY environment variable.")
        
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.output_file = "backend/data/videos/youtube_videos_extracted.csv"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Stats
        self.stats = {
            "videos_found": 0,
            "relevant_videos": 0,
            "api_calls": 0,
            "errors": 0
        }
    
    def get_priority_keywords(self) -> List[Dict[str, Any]]:
        """Get high-priority search keywords based on client intelligence"""
        return [
            # HIGH PRIORITY: June 2025 Black Magic Audio Leak
            {"query": "Sridhar Rao black magic audio", "priority": 10, "category": "scandal_2025"},
            {"query": "సంධ్య శ్రీధర్ రావు ఆడియో లీక్", "priority": 10, "category": "scandal_2025"},
            {"query": "Maganti Gopinath Sridhar Rao death", "priority": 10, "category": "scandal_2025"},
            {"query": "Sandhya Convention occult practices", "priority": 9, "category": "scandal_2025"},
            
            # HIGH PRIORITY: 2025 Legal Issues
            {"query": "Sridhar Rao HYDRAA demolition", "priority": 9, "category": "legal_2025"},
            {"query": "Sridhar Rao land grab Gachibowli", "priority": 9, "category": "legal_2025"},
            {"query": "Sridhar Rao arrest 2025", "priority": 9, "category": "legal_2025"},
            
            # MEDIUM PRIORITY: Historical Controversies
            {"query": "Sridhar Rao cheating case", "priority": 7, "category": "legal_historical"},
            {"query": "Sridhar Rao Delhi arrest 2023", "priority": 7, "category": "legal_historical"},
            {"query": "Sandhya Convention MD controversy", "priority": 6, "category": "business_disputes"},
            
            # LOWER PRIORITY: General Coverage
            {"query": "Sandhya Convention Sridhar Rao", "priority": 5, "category": "general"},
            {"query": "సంధ్య కన్వెన్షన్ శ్రీధర్ రావు", "priority": 5, "category": "general"},
        ]
    
    def get_trusted_channels(self) -> Dict[str, int]:
        """Get channel trust levels based on client intelligence"""
        return {
            # Tier 1: High Trust (9-10)
            "ABN Telugu": 10,
            "TV5 News": 10,
            "Zee Telugu News": 10,
            "NTV Telugu": 10,
            
            # Tier 2: Medium Trust (7-8)
            "Raj News Telugu": 8,
            "CVR News Telugu": 8,
            "BRK News": 7,
            "BIG TV Live": 7,
            
            # Default for others
            "_default": 3
        }
    
    def calculate_relevance(self, title: str, channel: str, description: str = "") -> float:
        """Calculate relevance score for Sridhar Rao content"""
        score = 0.0
        text = f"{title} {description}".lower()
        
        # Recent scandal keywords (high value)
        scandal_terms = ["black magic", "audio leak", "maganti gopinath", "occult", "death threat"]
        for term in scandal_terms:
            if term in text:
                score += 15.0
        
        # Legal keywords (medium-high value)
        legal_terms = ["arrest", "case", "court", "cheating", "fraud", "land grab", "hydraa"]
        for term in legal_terms:
            if term in text:
                score += 10.0
        
        # Name variations (medium value)
        name_terms = ["sridhar rao", "sreedhar rao", "శ్రీధర్ రావు"]
        for term in name_terms:
            if term in text:
                score += 8.0
        
        # Business terms (lower value)
        business_terms = ["sandhya convention", "sandhya construction"]
        for term in business_terms:
            if term in text:
                score += 5.0
        
        # Channel trust bonus
        channel_trust = self.get_trusted_channels().get(channel, 3)
        score += channel_trust
        
        return min(score, 100.0)
    
    def search_videos(self, query: str, max_results: int = 25) -> List[Dict[str, Any]]:
        """Search YouTube for videos"""
        self.logger.info(f"Searching: '{query}'")
        
        try:
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'order': 'relevance',
                'key': self.api_key,
                'regionCode': 'IN',
                'relevanceLanguage': 'te'
            }
            
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            self.stats["api_calls"] += 1
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video_data = self._process_video(item)
                if video_data:
                    videos.append(video_data)
            
            self.logger.info(f"Found {len(videos)} videos")
            return videos
            
        except Exception as e:
            self.logger.error(f"Search failed for '{query}': {e}")
            self.stats["errors"] += 1
            return []
    
    def _process_video(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single video from API response"""
        try:
            snippet = item['snippet']
            video_id = item['id']['videoId']
            
            title = snippet.get('title', '').strip()
            channel = snippet.get('channelTitle', '').strip()
            description = snippet.get('description', '').strip()
            upload_date = snippet.get('publishedAt', '')[:10]
            
            # Calculate relevance
            relevance = self.calculate_relevance(title, channel, description)
            
            # Filter low relevance content
            if relevance < 20.0:
                return None
            
            return {
                'video_id': video_id,
                'title': title,
                'channel': channel,
                'description': description,
                'upload_date': upload_date,
                'relevance_score': relevance,
                'youtube_url': f"https://www.youtube.com/watch?v={video_id}"
            }
            
        except Exception as e:
            self.logger.warning(f"Error processing video: {e}")
            return None
    
    def get_video_stats(self, video_ids: List[str]) -> Dict[str, Dict[str, int]]:
        """Get video statistics"""
        if not video_ids:
            return {}
        
        try:
            # Process in batches of 50
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
                        'comment_count': int(stats.get('commentCount', 0))
                    }
                
                time.sleep(0.1)  # Rate limiting
            
            return all_stats
            
        except Exception as e:
            self.logger.error(f"Error getting video stats: {e}")
            return {}
    
    def process_to_schema(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process videos to v2.0 schema format"""
        self.logger.info(f"Processing {len(videos)} videos to schema...")
        
        # Get video statistics
        video_ids = [v['video_id'] for v in videos]
        video_stats = self.get_video_stats(video_ids)
        
        processed = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        for video in videos:
            try:
                video_id = video['video_id']
                stats = video_stats.get(video_id, {})
                
                # Calculate trust level
                channel = video['channel']
                trust_levels = self.get_trusted_channels()
                trust_level = 1 if trust_levels.get(channel, 0) >= 7 else 0
                
                # Create schema record
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
                    'DataHealth': 85.0,  # Default high health for extracted data
                    'ProcessingStatus': "pending"
                }
                
                processed.append(record)
                self.stats["relevant_videos"] += 1
                
            except Exception as e:
                self.logger.error(f"Error processing video {video.get('video_id')}: {e}")
                continue
        
        return processed
    
    def save_data(self, videos: List[Dict[str, Any]]):
        """Save processed videos to CSV"""
        if not videos:
            self.logger.warning("No videos to save")
            return
        
        try:
            df = pd.DataFrame(videos)
            
            # Ensure schema compliance
            for col in VIDEO_SCHEMA_V2:
                if col not in df.columns:
                    df[col] = ""
            
            df = df[VIDEO_SCHEMA_V2]
            df.to_csv(self.output_file, index=False)
            
            self.logger.info(f"Saved {len(videos)} videos to {self.output_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")
            raise
    
    def run_extraction(self, max_videos_per_query: int = 25):
        """Run the complete extraction process"""
        self.logger.info("Starting Sridhar Rao content extraction...")
        
        keywords = self.get_priority_keywords()
        all_videos = []
        
        # Process keywords by priority
        for keyword_data in keywords:
            query = keyword_data['query']
            priority = keyword_data['priority']
            
            self.logger.info(f"Processing priority {priority}: {query}")
            
            videos = self.search_videos(query, max_videos_per_query)
            all_videos.extend(videos)
            self.stats["videos_found"] += len(videos)
            
            time.sleep(0.2)  # Rate limiting
        
        # Remove duplicates
        unique_videos = []
        seen_ids = set()
        
        for video in all_videos:
            video_id = video['video_id']
            if video_id not in seen_ids:
                seen_ids.add(video_id)
                unique_videos.append(video)
        
        self.logger.info(f"Found {len(unique_videos)} unique videos after deduplication")
        
        # Process to schema and save
        processed_videos = self.process_to_schema(unique_videos)
        self.save_data(processed_videos)
        
        # Generate report
        self._print_report(processed_videos)
        
        return processed_videos
    
    def _print_report(self, videos: List[Dict[str, Any]]):
        """Print extraction report"""
        if not videos:
            print("No videos extracted")
            return
        
        df = pd.DataFrame(videos)
        
        print("\n" + "="*60)
        print("SRIDHAR RAO EXTRACTION REPORT")
        print("="*60)
        print(f"Total Videos Extracted: {len(videos)}")
        print(f"API Calls Made: {self.stats['api_calls']}")
        print(f"Errors Encountered: {self.stats['errors']}")
        
        print(f"\nRelevance Distribution:")
        high_rel = len(df[df['RelevanceScore'] >= 50])
        med_rel = len(df[(df['RelevanceScore'] >= 30) & (df['RelevanceScore'] < 50)])
        low_rel = len(df[df['RelevanceScore'] < 30])
        print(f"  High Relevance (50+): {high_rel}")
        print(f"  Medium Relevance (30-49): {med_rel}")
        print(f"  Lower Relevance (<30): {low_rel}")
        
        print(f"\nTrusted Sources: {len(df[df['TrustLevel'] == 1])}")
        
        print(f"\nTop Channels:")
        channel_counts = df['Channel'].value_counts().head(5)
        for channel, count in channel_counts.items():
            print(f"  {channel}: {count}")
        
        print(f"\nRecent Content (2025): {len(df[df['UploadDate'] >= '2025-01-01'])}")
        print(f"\nData saved to: {self.output_file}")
        print("="*60)


def main():
    """Main function"""
    print("Sridhar Rao YouTube Content Extractor")
    print("=====================================")
    
    try:
        extractor = SridharRaoExtractor()
        videos = extractor.run_extraction(max_videos_per_query=30)
        
        print(f"\nExtraction completed successfully!")
        print(f"Total relevant videos: {len(videos)}")
        print("Ready for AI processing pipeline!")
        
        return 0
        
    except Exception as e:
        print(f"Extraction failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 