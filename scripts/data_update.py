#!/usr/bin/env python3
"""
Percepta Pro v2.0 - Automated Data Update Pipeline
=================================================

Daily scheduled script for fetching new YouTube videos and comments
related to Sandhya Convention MD Sridhar Rao with automated processing.

Author: Percepta Development Team
Version: 2.0
Usage: python scripts/data_update.py [--dry-run] [--verbose]
"""

import pandas as pd
import sys
import os
import argparse
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import json
import time
import requests
from urllib.parse import quote

# Add backend to path for schema imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from data.videos.schema_v2 import (
        VIDEO_SCHEMA_V2, 
        calculate_relevance_score, 
        determine_trust_level,
        VideoSchemaValidator,
        SRIDHAR_RAO_KEYWORDS
    )
except ImportError:
    print("Error: Could not import schema_v2. Please ensure backend/data/videos/schema_v2.py exists.")
    sys.exit(1)


class DataUpdatePipeline:
    """Automated data update pipeline for Percepta Pro v2.0"""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        
        # File paths
        self.videos_file = "backend/data/videos/youtube_videos.csv"
        self.comments_file = "backend/data/comments/youtube_comments.csv"
        self.log_file = f"scripts/logs/data_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Pipeline statistics
        self.stats = {
            "start_time": datetime.now(),
            "videos_processed": 0,
            "new_videos_found": 0,
            "duplicates_skipped": 0,
            "errors_encountered": 0,
            "processing_time": 0.0
        }
        
        # Setup logging
        self._setup_logging()
        
        # Search configuration
        self.search_queries = self._build_search_queries()
        self.relevance_threshold = 25.0  # Minimum relevance score to include
        
    def _setup_logging(self):
        """Setup logging configuration"""
        os.makedirs("scripts/logs", exist_ok=True)
        
        logging.basicConfig(
            level=logging.DEBUG if self.verbose else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _build_search_queries(self) -> List[str]:
        """
        Build search queries based on keywords
        
        Returns:
            List of search query strings
        """
        # Primary search terms with high relevance
        primary_queries = [
            "సంధ్య శ్రీధర్ రావు",
            "sandhya sridhar rao",
            "sandhya convention sridhar",
            "సంధ్య కన్వెన్షన్ శ్రీధర్"
        ]
        
        # Secondary queries for broader coverage
        secondary_queries = [
            "మాగంటి గోపీనాథ్ సంధ్య",
            "maganti gopinath sridhar",
            "gachibowli builder controversy",
            "sandhya convention hyderabad"
        ]
        
        # Combine and limit queries
        all_queries = primary_queries + secondary_queries
        return all_queries[:6]  # Limit to prevent API overuse
        
    def load_existing_data(self) -> Tuple[pd.DataFrame, set]:
        """
        Load existing video data and extract video IDs
        
        Returns:
            Tuple of (DataFrame, set of existing video IDs)
        """
        try:
            if os.path.exists(self.videos_file):
                df = pd.read_csv(self.videos_file)
                existing_ids = set(df['VideoID'].dropna()) if 'VideoID' in df.columns else set()
                self.logger.info(f"Loaded {len(df)} existing videos, {len(existing_ids)} unique IDs")
                return df, existing_ids
            else:
                self.logger.warning(f"Videos file not found: {self.videos_file}")
                # Create empty DataFrame with v2.0 schema
                df = pd.DataFrame(columns=VIDEO_SCHEMA_V2)
                return df, set()
        except Exception as e:
            self.logger.error(f"Error loading existing data: {e}")
            return pd.DataFrame(columns=VIDEO_SCHEMA_V2), set()
    
    def simulate_youtube_search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Simulate YouTube search API call (stub implementation)
        
        In production, this would use YouTube Data API v3
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of video data dictionaries
        """
        self.logger.info(f"🔍 Simulating search for: '{query}' (max: {max_results})")
        
        # For now, return empty list as this is a foundation stub
        # In production, implement actual YouTube API calls here
        
        simulated_results = []
        
        # Simulate finding some new videos based on patterns in existing data
        if "sridhar" in query.lower() or "సంధ్య" in query:
            # Generate some realistic-looking dummy data for testing
            base_time = datetime.now()
            
            for i in range(min(3, max_results)):  # Simulate finding 0-3 new videos
                video_id = f"SIMUL{int(time.time())}{i:02d}"[-11:]  # Generate fake video ID
                
                simulated_video = {
                    "video_id": video_id,
                    "title": f"Sample Video {i+1} - {query[:20]}... Discussion",
                    "channel": "Sample News Channel",
                    "upload_date": (base_time - timedelta(days=i+1)).strftime("%Y-%m-%d"),
                    "view_count": (i+1) * 1000,
                    "comment_count": (i+1) * 50,
                    "thumbnail_url": f"https://example.com/thumb_{video_id}.jpg"
                }
                
                simulated_results.append(simulated_video)
        
        self.logger.info(f"📊 Simulated search returned {len(simulated_results)} results")
        return simulated_results
    
    def fetch_new_videos(self, existing_video_ids: set) -> List[Dict[str, Any]]:
        """
        Fetch new videos from multiple search queries
        
        Args:
            existing_video_ids: Set of existing video IDs to avoid duplicates
            
        Returns:
            List of new video data
        """
        self.logger.info("🚀 Starting video discovery process...")
        
        all_new_videos = []
        processed_video_ids = set()
        
        for query in self.search_queries:
            try:
                self.logger.info(f"🔍 Processing query: {query}")
                
                # Simulate API call (replace with real YouTube API in production)
                search_results = self.simulate_youtube_search(query, max_results=20)
                
                for video_data in search_results:
                    video_id = video_data.get("video_id", "")
                    
                    # Skip if already exists or already processed
                    if video_id in existing_video_ids or video_id in processed_video_ids:
                        self.stats["duplicates_skipped"] += 1
                        continue
                    
                    # Calculate relevance score
                    title = video_data.get("title", "")
                    channel = video_data.get("channel", "")
                    relevance_score = calculate_relevance_score(title, channel)
                    
                    # Skip if relevance is too low
                    if relevance_score < self.relevance_threshold:
                        self.logger.debug(f"Skipping low relevance video: {title[:50]}... (score: {relevance_score:.1f})")
                        continue
                    
                    # Add to results
                    processed_video_ids.add(video_id)
                    all_new_videos.append(video_data)
                    self.stats["new_videos_found"] += 1
                    
                    self.logger.info(f"✅ Found relevant video: {title[:50]}... (score: {relevance_score:.1f})")
                
                # Rate limiting simulation
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error processing query '{query}': {e}")
                self.stats["errors_encountered"] += 1
                continue
        
        self.logger.info(f"🎯 Discovery complete: {len(all_new_videos)} new relevant videos found")
        return all_new_videos
    
    def process_video_data(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw video data into v2.0 schema format
        
        Args:
            video_data: Raw video data from search
            
        Returns:
            Processed video data matching v2.0 schema
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Extract and clean data
        video_id = video_data.get("video_id", "")
        title = video_data.get("title", "").strip()
        channel = video_data.get("channel", "").strip()
        upload_date = video_data.get("upload_date", today)
        views = int(video_data.get("view_count", 0))
        comments = int(video_data.get("comment_count", 0))
        
        # Calculate scores
        relevance_score = calculate_relevance_score(title, channel)
        trust_level = determine_trust_level(channel)
        
        # Calculate data health
        data_health = self._calculate_data_health(title, channel, upload_date, views, comments)
        
        # Create processed record
        processed_video = {
            'VideoID': video_id,
            'Title': title,
            'Channel': channel,
            'UploadDate': upload_date,
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
        
        return processed_video
    
    def _calculate_data_health(self, title: str, channel: str, upload_date: str, 
                              views: int, comments: int) -> float:
        """
        Calculate data health score for new video
        
        Args:
            title: Video title
            channel: Channel name  
            upload_date: Upload date
            views: View count
            comments: Comment count
            
        Returns:
            Data health score (0-100)
        """
        score = 0.0
        
        # Title quality (25 points)
        if title and len(title.strip()) > 10:
            score += 25
        elif title:
            score += 10
        
        # Channel quality (25 points)
        if channel and len(channel.strip()) > 0:
            score += 25
        
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
        
        if comments > 0:
            score += 10
            if comments > 10:
                score += 5
        
        return min(score, 100.0)
    
    def append_new_videos(self, existing_df: pd.DataFrame, new_videos: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Append new videos to existing DataFrame
        
        Args:
            existing_df: Existing video DataFrame
            new_videos: List of new video data
            
        Returns:
            Updated DataFrame with new videos
        """
        if not new_videos:
            self.logger.info("No new videos to append")
            return existing_df
        
        self.logger.info(f"📝 Processing {len(new_videos)} new videos...")
        
        processed_videos = []
        for video_data in new_videos:
            try:
                processed_video = self.process_video_data(video_data)
                processed_videos.append(processed_video)
                self.stats["videos_processed"] += 1
            except Exception as e:
                self.logger.error(f"Error processing video {video_data.get('video_id', 'unknown')}: {e}")
                self.stats["errors_encountered"] += 1
                continue
        
        if processed_videos:
            new_df = pd.DataFrame(processed_videos)
            
            # Ensure schema compliance
            for col in VIDEO_SCHEMA_V2:
                if col not in new_df.columns:
                    new_df[col] = ""
            
            # Reorder columns to match schema
            new_df = new_df[VIDEO_SCHEMA_V2]
            
            # Append to existing data
            if not existing_df.empty:
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                updated_df = new_df
            
            self.logger.info(f"✅ Successfully processed {len(processed_videos)} new videos")
            return updated_df
        
        return existing_df
    
    def validate_updated_data(self, df: pd.DataFrame) -> bool:
        """
        Validate updated dataset
        
        Args:
            df: Updated DataFrame
            
        Returns:
            True if validation passes
        """
        self.logger.info("🔍 Validating updated dataset...")
        
        validator = VideoSchemaValidator()
        results = validator.validate_dataframe(df)
        
        if results["valid"]:
            self.logger.info("✅ Data validation passed!")
            for key, value in results["stats"].items():
                self.logger.info(f"   • {key}: {value}")
        else:
            self.logger.error("❌ Data validation failed!")
            for error in results["errors"]:
                self.logger.error(f"   • {error}")
        
        if results["warnings"]:
            for warning in results["warnings"]:
                self.logger.warning(f"   • {warning}")
        
        return results["valid"]
    
    def save_updated_data(self, df: pd.DataFrame):
        """
        Save updated dataset to file
        
        Args:
            df: Updated DataFrame
        """
        if self.dry_run:
            self.logger.info(f"🔄 DRY RUN: Would save {len(df)} videos to {self.videos_file}")
            return
        
        try:
            # Create backup of existing file
            if os.path.exists(self.videos_file):
                backup_file = f"{self.videos_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.rename(self.videos_file, backup_file)
                self.logger.info(f"📦 Created backup: {backup_file}")
            
            # Save updated data
            df.to_csv(self.videos_file, index=False)
            self.logger.info(f"💾 Saved updated dataset: {len(df)} videos")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving updated data: {e}")
            raise
    
    def generate_pipeline_report(self) -> Dict[str, Any]:
        """
        Generate pipeline execution report
        
        Returns:
            Dictionary with pipeline statistics and health metrics
        """
        end_time = datetime.now()
        self.stats["end_time"] = end_time
        self.stats["processing_time"] = (end_time - self.stats["start_time"]).total_seconds()
        
        report = {
            "pipeline_execution": {
                "start_time": self.stats["start_time"].isoformat(),
                "end_time": self.stats["end_time"].isoformat(),
                "processing_time_seconds": self.stats["processing_time"],
                "status": "success" if self.stats["errors_encountered"] == 0 else "completed_with_errors"
            },
            "data_processing": {
                "videos_processed": self.stats["videos_processed"],
                "new_videos_found": self.stats["new_videos_found"],
                "duplicates_skipped": self.stats["duplicates_skipped"],
                "errors_encountered": self.stats["errors_encountered"]
            },
            "search_configuration": {
                "queries_used": len(self.search_queries),
                "relevance_threshold": self.relevance_threshold,
                "search_queries": self.search_queries
            },
            "next_actions": [
                "Run AI processing pipeline for new videos",
                "Update sentiment analysis for recent content",
                "Generate weekly data health report"
            ]
        }
        
        return report
    
    def run_pipeline(self):
        """
        Execute the complete data update pipeline
        """
        self.logger.info("🚀 Starting Percepta Pro v2.0 Data Update Pipeline")
        self.logger.info("=" * 60)
        
        try:
            # Step 1: Load existing data
            existing_df, existing_ids = self.load_existing_data()
            
            # Step 2: Fetch new videos
            new_videos = self.fetch_new_videos(existing_ids)
            
            if not new_videos:
                self.logger.info("📊 No new relevant videos found")
                return self.generate_pipeline_report()
            
            # Step 3: Process and append new videos
            updated_df = self.append_new_videos(existing_df, new_videos)
            
            # Step 4: Validate updated data
            if not self.validate_updated_data(updated_df):
                raise Exception("Data validation failed")
            
            # Step 5: Save updated data
            self.save_updated_data(updated_df)
            
            # Step 6: Generate report
            report = self.generate_pipeline_report()
            
            self.logger.info("🎉 Pipeline execution completed successfully!")
            self.logger.info(f"📊 Summary: {self.stats['new_videos_found']} new videos, {self.stats['errors_encountered']} errors")
            
            return report
            
        except Exception as e:
            self.logger.error(f"❌ Pipeline execution failed: {e}")
            self.stats["errors_encountered"] += 1
            return self.generate_pipeline_report()


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Percepta Pro v2.0 Data Update Pipeline")
    parser.add_argument('--dry-run', action='store_true', help='Run without making changes')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Ensure we're in the right directory
    if not os.path.exists("backend/data/videos"):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Create and run pipeline
    pipeline = DataUpdatePipeline(dry_run=args.dry_run, verbose=args.verbose)
    
    try:
        report = pipeline.run_pipeline()
        
        # Print summary
        print("\n" + "="*60)
        print("📋 PIPELINE EXECUTION SUMMARY")
        print("="*60)
        print(f"Status: {report['pipeline_execution']['status']}")
        print(f"Processing time: {report['pipeline_execution']['processing_time_seconds']:.1f}s")
        print(f"New videos: {report['data_processing']['new_videos_found']}")
        print(f"Errors: {report['data_processing']['errors_encountered']}")
        
        if args.verbose:
            print(f"\nFull report saved to: {pipeline.log_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 