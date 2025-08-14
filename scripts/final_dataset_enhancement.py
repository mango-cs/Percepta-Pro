#!/usr/bin/env python3
"""
FINAL CRITICAL ENHANCEMENT - Phase 1 Completion
Adds 8 essential video columns and 4 comment columns for Percepta Pro v2.0

CRITICAL ADDITIONS:
Videos: PublishedAt_Formatted, CategoryId, DefaultLanguage, ChannelId, 
        LiveBroadcastContent, CommentCount_API, FavoriteCount, ChannelSubscriberCount
Comments: Date_Formatted, PublishedAt, UpdatedAt, ModerationStatus

Author: Percepta Pro v2.0 Final Enhancement
Date: 2025-06-29
"""

import pandas as pd
import csv
from datetime import datetime, timedelta
import requests
import time
import os
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalEnhancer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def format_date_to_ddmmyyyy(self, date_string):
        """Convert various date formats to dd-mm-yyyy"""
        if not date_string or date_string == '':
            return ''
            
        try:
            # Handle relative dates like "2 days ago", "1 week ago"
            if 'ago' in str(date_string).lower():
                return self.parse_relative_date(date_string)
            
            # Handle ISO 8601 format from YouTube API
            if 'T' in str(date_string):
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                return dt.strftime('%d-%m-%Y')
            
            # Handle existing dd-mm-yyyy format
            if re.match(r'\d{1,2}-\d{1,2}-\d{4}', str(date_string)):
                return date_string
                
            # Handle yyyy-mm-dd format
            if re.match(r'\d{4}-\d{1,2}-\d{1,2}', str(date_string)):
                dt = datetime.strptime(date_string, '%Y-%m-%d')
                return dt.strftime('%d-%m-%Y')
                
        except Exception as e:
            logger.warning(f"Date parsing error for '{date_string}': {e}")
            
        return date_string
    
    def parse_relative_date(self, relative_date):
        """Parse relative dates like '2 days ago' to dd-mm-yyyy format"""
        try:
            now = datetime.now()
            relative_date = str(relative_date).lower()
            
            if 'day' in relative_date:
                days = int(re.search(r'(\d+)', relative_date).group(1))
                target_date = now - timedelta(days=days)
            elif 'week' in relative_date:
                weeks = int(re.search(r'(\d+)', relative_date).group(1))
                target_date = now - timedelta(weeks=weeks)
            elif 'month' in relative_date:
                months = int(re.search(r'(\d+)', relative_date).group(1))
                target_date = now - timedelta(days=months*30)
            elif 'year' in relative_date:
                years = int(re.search(r'(\d+)', relative_date).group(1))
                target_date = now - timedelta(days=years*365)
            else:
                return relative_date
                
            return target_date.strftime('%d-%m-%Y')
        except Exception:
            return relative_date

    def enhance_videos_final(self, input_file, output_file):
        """Add 8 critical video columns"""
        logger.info("🎬 Starting FINAL videos enhancement...")
        
        # Read current dataset
        df = pd.read_csv(input_file)
        logger.info(f"📊 Loaded {len(df)} videos")
        
        # Add 8 critical columns
        critical_columns = {
            'PublishedAt_Formatted': '',
            'CategoryId': '25',  # Default to News category
            'DefaultLanguage': 'te',  # Default to Telugu
            'ChannelId': '',
            'LiveBroadcastContent': 'none',
            'CommentCount_API': 0,
            'FavoriteCount': 0,
            'ChannelSubscriberCount': 0
        }
        
        for col, default_val in critical_columns.items():
            if col not in df.columns:
                df[col] = default_val
        
        # Format existing UploadDate to proper format
        if 'UploadDate' in df.columns:
            logger.info("📅 Converting dates to dd-mm-yyyy format...")
            df['UploadDate'] = df['UploadDate'].apply(self.format_date_to_ddmmyyyy)
            df['PublishedAt_Formatted'] = df['UploadDate']  # Copy formatted date
        
        # Process videos in batches with API
        video_ids = df['VideoID'].tolist()
        batch_size = 50
        enhanced_count = 0
        
        for i in range(0, len(video_ids), batch_size):
            batch_ids = video_ids[i:i + batch_size]
            logger.info(f"📡 API batch {i//batch_size + 1}: videos {i+1}-{min(i+batch_size, len(video_ids))}")
            
            try:
                # Get video details
                video_request = self.youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(batch_ids),
                    maxResults=50
                )
                video_response = video_request.execute()
                
                # Get channel details for subscriber counts
                channel_ids = []
                video_channel_map = {}
                
                for video in video_response.get('items', []):
                    channel_id = video['snippet']['channelId']
                    video_channel_map[video['id']] = channel_id
                    if channel_id not in channel_ids:
                        channel_ids.append(channel_id)
                
                # Get channel subscriber counts
                channel_subscriber_map = {}
                if channel_ids:
                    try:
                        channel_request = self.youtube.channels().list(
                            part='statistics',
                            id=','.join(channel_ids[:50])  # API limit
                        )
                        channel_response = channel_request.execute()
                        
                        for channel in channel_response.get('items', []):
                            channel_id = channel['id']
                            subscriber_count = channel['statistics'].get('subscriberCount', 0)
                            channel_subscriber_map[channel_id] = subscriber_count
                    except Exception as e:
                        logger.warning(f"Channel API error: {e}")
                
                # Update dataframe with API data
                for video in video_response.get('items', []):
                    video_id = video['id']
                    snippet = video['snippet']
                    statistics = video['statistics']
                    
                    # Find row index
                    row_idx = df[df['VideoID'] == video_id].index
                    if len(row_idx) > 0:
                        row_idx = row_idx[0]
                        
                        # Update with API data
                        df.at[row_idx, 'CategoryId'] = snippet.get('categoryId', '25')
                        df.at[row_idx, 'DefaultLanguage'] = snippet.get('defaultLanguage', 'te')
                        df.at[row_idx, 'ChannelId'] = snippet['channelId']
                        df.at[row_idx, 'LiveBroadcastContent'] = snippet.get('liveBroadcastContent', 'none')
                        df.at[row_idx, 'CommentCount_API'] = statistics.get('commentCount', 0)
                        df.at[row_idx, 'FavoriteCount'] = statistics.get('favoriteCount', 0)
                        
                        # Add channel subscriber count
                        channel_id = video_channel_map[video_id]
                        subscriber_count = channel_subscriber_map.get(channel_id, 0)
                        df.at[row_idx, 'ChannelSubscriberCount'] = subscriber_count
                        
                        enhanced_count += 1
                
                time.sleep(0.1)  # Rate limiting
                
            except HttpError as e:
                logger.warning(f"API error for batch {i//batch_size + 1}: {e}")
            except Exception as e:
                logger.error(f"Error processing batch: {e}")
        
        # Save final enhanced dataset
        df.to_csv(output_file, index=False)
        logger.info(f"✅ FINAL videos dataset saved: {output_file}")
        logger.info(f"📈 Enhanced: {enhanced_count}/{len(df)} videos")
        logger.info(f"📊 Total columns: {len(df.columns)}")
        
        return df

    def enhance_comments_final(self, input_file, output_file):
        """Add 4 critical comment columns"""
        logger.info("💬 Starting FINAL comments enhancement...")
        
        # Read current dataset
        df = pd.read_csv(input_file)
        logger.info(f"📊 Loaded {len(df)} comments")
        
        # Add 4 critical columns
        critical_columns = {
            'Date_Formatted': '',
            'PublishedAt': '',
            'UpdatedAt': '',
            'ModerationStatus': 'published'
        }
        
        for col, default_val in critical_columns.items():
            if col not in df.columns:
                df[col] = default_val
        
        # Format existing Date column
        if 'Date' in df.columns:
            logger.info("📅 Converting comment dates to dd-mm-yyyy format...")
            df['Date_Formatted'] = df['Date'].apply(self.format_date_to_ddmmyyyy)
        
        # Set default values for API fields
        df['PublishedAt'] = df['Date_Formatted']  # Use formatted date as placeholder
        df['UpdatedAt'] = df['Date_Formatted']    # Same as published for most comments
        df['ModerationStatus'] = 'published'      # Most comments are published
        
        # Save enhanced comments dataset
        df.to_csv(output_file, index=False)
        logger.info(f"✅ FINAL comments dataset saved: {output_file}")
        logger.info(f"📊 Total columns: {len(df.columns)}")
        
        return df

def main():
    # Configuration
    API_KEY = "AIzaSyClXhVz8WRPxTRYLH3gJ0MxhkyzHQtwumo"
    
    # File paths
    videos_input = "backend/data/videos/youtube_videos_enhanced.csv"
    videos_output = "backend/data/videos/youtube_videos_final.csv"
    comments_input = "backend/data/comments/youtube_comments.csv"
    comments_output = "backend/data/comments/youtube_comments_final.csv"
    
    try:
        enhancer = FinalEnhancer(API_KEY)
        
        logger.info("🚀 PERCEPTA PRO v2.0 - FINAL ENHANCEMENT")
        logger.info("=" * 50)
        
        # Enhance videos dataset
        if os.path.exists(videos_input):
            videos_df = enhancer.enhance_videos_final(videos_input, videos_output)
            logger.info(f"🎬 Videos: {len(videos_df.columns)} columns")
        else:
            logger.error(f"❌ Videos file not found: {videos_input}")
        
        # Enhance comments dataset
        if os.path.exists(comments_input):
            comments_df = enhancer.enhance_comments_final(comments_input, comments_output)
            logger.info(f"💬 Comments: {len(comments_df.columns)} columns")
        else:
            logger.error(f"❌ Comments file not found: {comments_input}")
        
        logger.info("=" * 50)
        logger.info("🎉 PHASE 1 FINAL ENHANCEMENT COMPLETE!")
        logger.info("📋 Videos: +8 columns | Comments: +4 columns")
        logger.info("🎯 READY FOR PHASE 2: AI PROCESSING PIPELINE")
        
    except Exception as e:
        logger.error(f"❌ Enhancement failed: {e}")
        raise

if __name__ == "__main__":
    main() 