#!/usr/bin/env python3
"""
Percepta Pro v2.0 - Initial Data Cleaning Script
==============================================

One-off script to clean and migrate existing YouTube videos data 
from v1.0 format to enhanced v2.0 schema with AI-ready structure.

Author: Percepta Development Team
Version: 2.0
Usage: python scripts/clean_initial_videos.py
"""

import pandas as pd
import re
import sys
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Optional, Tuple

# Add backend to path for schema imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from data.videos.schema_v2 import (
        VIDEO_SCHEMA_V2, 
        calculate_relevance_score, 
        determine_trust_level,
        VideoSchemaValidator,
        create_empty_dataframe
    )
except ImportError:
    print("Error: Could not import schema_v2. Please ensure backend/data/videos/schema_v2.py exists.")
    sys.exit(1)


class VideoDataCleaner:
    """Handles cleaning and migration of video data to v2.0 schema"""
    
    def __init__(self):
        self.input_file = "backend/data/videos/youtube_videos.csv"
        self.output_file = "backend/data/videos/youtube_videos.csv"
        self.backup_file = "backend/data/videos/youtube_videos_v1_backup.csv"
        
    def extract_video_id(self, url: str) -> str:
        """
        Extract YouTube video ID from URL
        
        Args:
            url: YouTube video URL
            
        Returns:
            11-character video ID or empty string if invalid
        """
        if not url:
            return ""
        
        try:
            # Handle different YouTube URL formats
            if "youtube.com/watch" in url:
                parsed = urlparse(url)
                return parse_qs(parsed.query).get('v', [''])[0]
            elif "youtu.be/" in url:
                return url.split('/')[-1].split('?')[0]
            elif len(url) == 11:  # Already a video ID
                return url
        except Exception:
            pass
        
        return ""
    
    def parse_relative_date(self, date_str: str, reference_date: datetime = None) -> str:
        """
        Convert relative date strings to ISO 8601 format
        
        Args:
            date_str: Relative date like "1 day ago", "4 days ago"
            reference_date: Reference date for calculation (defaults to today)
            
        Returns:
            ISO 8601 formatted date string (YYYY-MM-DD)
        """
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")
        
        if reference_date is None:
            reference_date = datetime.now()
        
        date_str = date_str.lower().strip()
        
        try:
            # Handle "X time_unit ago" format
            if "ago" in date_str:
                parts = date_str.replace("ago", "").strip().split()
                if len(parts) >= 2:
                    number = int(parts[0])
                    unit = parts[1]
                    
                    if "second" in unit:
                        delta = timedelta(seconds=number)
                    elif "minute" in unit:
                        delta = timedelta(minutes=number)
                    elif "hour" in unit:
                        delta = timedelta(hours=number)
                    elif "day" in unit:
                        delta = timedelta(days=number)
                    elif "week" in unit:
                        delta = timedelta(weeks=number)
                    elif "month" in unit:
                        delta = timedelta(days=number * 30)  # Approximate
                    elif "year" in unit:
                        delta = timedelta(days=number * 365)  # Approximate
                    else:
                        delta = timedelta(days=1)  # Default to 1 day
                    
                    result_date = reference_date - delta
                    return result_date.strftime("%Y-%m-%d")
            
            # Handle "Streamed X time_unit ago" format
            if "streamed" in date_str:
                # Remove "streamed" and process as normal
                cleaned = date_str.replace("streamed", "").strip()
                return self.parse_relative_date(cleaned, reference_date)
            
            # Try to parse as existing ISO date
            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                pass
            
            # Default fallback
            return reference_date.strftime("%Y-%m-%d")
            
        except Exception:
            # If all else fails, return today's date
            return reference_date.strftime("%Y-%m-%d")
    
    def clean_title(self, title: str) -> str:
        """
        Clean and normalize video titles
        
        Args:
            title: Raw video title
            
        Returns:
            Cleaned title
        """
        if not title:
            return ""
        
        # Basic cleaning
        title = title.strip()
        
        # Remove excessive whitespace
        title = re.sub(r'\s+', ' ', title)
        
        # Limit length to schema maximum
        if len(title) > 200:
            title = title[:197] + "..."
        
        return title
    
    def extract_metrics(self, views_str: str = "", comments_str: str = "") -> Tuple[int, int]:
        """
        Extract numeric values from view and comment strings
        
        Args:
            views_str: Views string (if available)
            comments_str: Comments string (if available)
            
        Returns:
            Tuple of (views, comments) as integers
        """
        def extract_number(text: str) -> int:
            if not text:
                return 0
            try:
                # Extract numbers from text
                numbers = re.findall(r'\d+', str(text).replace(',', ''))
                return int(numbers[0]) if numbers else 0
            except (ValueError, IndexError):
                return 0
        
        views = extract_number(views_str)
        comments = extract_number(comments_str)
        
        return views, comments
    
    def load_existing_data(self) -> pd.DataFrame:
        """
        Load existing video data from CSV
        
        Returns:
            DataFrame with existing data
        """
        try:
            df = pd.read_csv(self.input_file)
            print(f"✅ Loaded {len(df)} existing videos from {self.input_file}")
            return df
        except FileNotFoundError:
            print(f"❌ Input file not found: {self.input_file}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading existing data: {e}")
            sys.exit(1)
    
    def backup_existing_data(self, df: pd.DataFrame):
        """
        Create backup of existing data
        
        Args:
            df: DataFrame to backup
        """
        try:
            df.to_csv(self.backup_file, index=False)
            print(f"📦 Created backup: {self.backup_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not create backup: {e}")
    
    def migrate_to_v2_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Migrate DataFrame from v1.0 to v2.0 schema
        
        Args:
            df: Input DataFrame with v1.0 schema
            
        Returns:
            DataFrame with v2.0 schema
        """
        print("🔄 Migrating data to v2.0 schema...")
        
        # Create new DataFrame with v2.0 schema
        new_df = create_empty_dataframe()
        
        # Today's date for fetched_date
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Process each row
        migrated_rows = []
        duplicates_removed = 0
        processed_video_ids = set()
        
        for idx, row in df.iterrows():
            try:
                # Extract video ID from URL
                video_id = self.extract_video_id(row.get('URL', ''))
                
                # Skip if no valid video ID
                if not video_id or len(video_id) != 11:
                    print(f"⚠️  Row {idx+1}: Invalid video ID, skipping")
                    continue
                
                # Check for duplicates
                if video_id in processed_video_ids:
                    duplicates_removed += 1
                    print(f"🔄 Row {idx+1}: Duplicate video ID {video_id}, skipping")
                    continue
                
                processed_video_ids.add(video_id)
                
                # Clean and extract data
                title = self.clean_title(row.get('Title', ''))
                channel = str(row.get('Channel', '')).strip()
                upload_date = self.parse_relative_date(row.get('Upload Date', ''))
                
                # Extract metrics (not available in current data, so set to 0)
                views, comments = 0, 0
                
                # Calculate scores
                relevance_score = calculate_relevance_score(title, channel)
                trust_level = determine_trust_level(channel)
                
                # Calculate data health score
                data_health = self._calculate_data_health(title, channel, upload_date)
                
                # Create migrated row
                migrated_row = {
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
                
                migrated_rows.append(migrated_row)
                
            except Exception as e:
                print(f"⚠️  Row {idx+1}: Error processing - {e}")
                continue
        
        # Create new DataFrame
        if migrated_rows:
            new_df = pd.DataFrame(migrated_rows)
            print(f"✅ Successfully migrated {len(migrated_rows)} videos")
            if duplicates_removed > 0:
                print(f"🧹 Removed {duplicates_removed} duplicate entries")
        else:
            print("❌ No valid data to migrate")
            
        return new_df
    
    def _calculate_data_health(self, title: str, channel: str, upload_date: str) -> float:
        """
        Calculate data health score based on available information
        
        Args:
            title: Video title
            channel: Channel name
            upload_date: Upload date
            
        Returns:
            Data health score (0-100)
        """
        score = 0.0
        
        # Title quality (40 points)
        if title and len(title.strip()) > 0:
            score += 20
            if len(title.strip()) > 10:  # Meaningful title
                score += 20
        
        # Channel quality (30 points)
        if channel and len(channel.strip()) > 0:
            score += 30
        
        # Date quality (30 points)
        if upload_date:
            try:
                datetime.strptime(upload_date, "%Y-%m-%d")
                score += 30
            except ValueError:
                score += 10  # Partial credit for having some date
        
        return min(score, 100.0)
    
    def validate_migrated_data(self, df: pd.DataFrame) -> bool:
        """
        Validate migrated data against v2.0 schema
        
        Args:
            df: Migrated DataFrame
            
        Returns:
            True if validation passes, False otherwise
        """
        print("🔍 Validating migrated data...")
        
        validator = VideoSchemaValidator()
        results = validator.validate_dataframe(df)
        
        if results["valid"]:
            print("✅ Data validation passed!")
            print(f"📊 Statistics:")
            for key, value in results["stats"].items():
                print(f"   • {key}: {value}")
        else:
            print("❌ Data validation failed!")
            print("🚨 Errors:")
            for error in results["errors"]:
                print(f"   • {error}")
        
        if results["warnings"]:
            print("⚠️  Warnings:")
            for warning in results["warnings"]:
                print(f"   • {warning}")
        
        return results["valid"]
    
    def save_cleaned_data(self, df: pd.DataFrame):
        """
        Save cleaned data to output file
        
        Args:
            df: Cleaned DataFrame
        """
        try:
            df.to_csv(self.output_file, index=False)
            print(f"💾 Saved cleaned data to {self.output_file}")
            print(f"📈 Final dataset: {len(df)} videos with {len(df.columns)} columns")
        except Exception as e:
            print(f"❌ Error saving cleaned data: {e}")
            sys.exit(1)
    
    def run_cleaning_process(self):
        """
        Run the complete data cleaning process
        """
        print("🚀 Starting Percepta Pro v2.0 Data Migration")
        print("=" * 50)
        
        # Step 1: Load existing data
        existing_df = self.load_existing_data()
        
        # Step 2: Create backup
        self.backup_existing_data(existing_df)
        
        # Step 3: Migrate to v2.0 schema
        migrated_df = self.migrate_to_v2_schema(existing_df)
        
        if migrated_df.empty:
            print("❌ Migration failed - no valid data produced")
            sys.exit(1)
        
        # Step 4: Validate migrated data
        if not self.validate_migrated_data(migrated_df):
            print("❌ Migration failed validation")
            sys.exit(1)
        
        # Step 5: Save cleaned data
        self.save_cleaned_data(migrated_df)
        
        print("\n🎉 Data migration completed successfully!")
        print(f"📁 Original data backed up to: {self.backup_file}")
        print(f"📁 Clean v2.0 data saved to: {self.output_file}")
        print(f"📊 Ready for AI processing pipeline")


def main():
    """Main function to run the cleaning process"""
    
    # Ensure we're in the right directory
    if not os.path.exists("backend/data/videos"):
        print("❌ Error: Please run this script from the project root directory")
        print("   Expected structure: backend/data/videos/")
        sys.exit(1)
    
    # Create and run cleaner
    cleaner = VideoDataCleaner()
    
    try:
        cleaner.run_cleaning_process()
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 