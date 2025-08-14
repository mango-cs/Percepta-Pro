#!/usr/bin/env python3
"""
Critical Dataset Enhancement Script - Phase 1 Completion
Adds 8 critical video columns and 4 comment columns for Percepta Pro v2.0

VIDEOS ENHANCEMENT (8 columns):
- PublishedAt_Formatted: Proper dd-mm-yyyy format
- CategoryId: Content category (25=News, etc.)
- DefaultLanguage: API-declared primary language  
- ChannelId: Unique channel identifier
- LiveBroadcastContent: Live/upcoming/none status
- CommentCount_API: API's accurate comment count
- FavoriteCount: Video favorites (engagement metric)
- ChannelSubscriberCount: Channel authority metric

COMMENTS ENHANCEMENT (4 columns):
- Date_Formatted: Proper dd-mm-yyyy format
- PublishedAt: API timestamp for precise ordering
- UpdatedAt: When comment was last modified
- ModerationStatus: Published/held for review/rejected

Author: Percepta Pro v2.0 Phase 1 Final
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

class DatasetEnhancer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.video_batch_size = 50  # YouTube API allows max 50 video IDs per request
        self.comment_batch_size = 100  # Comment pagination limit
        
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
                target_date = now - timedelta(days=months*30)  # Approximate
            elif 'year' in relative_date:
                years = int(re.search(r'(\d+)', relative_date).group(1))
                target_date = now - timedelta(days=years*365)  # Approximate
            else:
                return relative_date
                
            return target_date.strftime('%d-%m-%Y')
        except Exception:
            return relative_date

    def get_video_details_batch(self, video_ids):
        """Get enhanced video details for batch of video IDs"""
        try:
            # Get video details
            video_request = self.youtube.videos().list(
                part='snippet,statistics,status,liveStreamingDetails',
                id=','.join(video_ids),
                maxResults=50
            )
            video_response = video_request.execute()
            
            # Get channel details for subscriber counts
            channel_ids = []
            video_channel_map = {}
            
            for video in video_response.get('items', []):
                channel_id = video['snippet']['channelId']
                channel_ids.append(channel_id)
                video_channel_map[video['id']] = channel_id
            
            # Remove duplicates
            unique_channel_ids = list(set(channel_ids))
            
            # Get channel subscriber counts
            channel_subscriber_map = {}
            if unique_channel_ids:
                channel_request = self.youtube.channels().list(
                    part='statistics',
                    id=','.join(unique_channel_ids)
                )
                channel_response = channel_request.execute()
                
                for channel in channel_response.get('items', []):
                    channel_id = channel['id']
                    subscriber_count = channel['statistics'].get('subscriberCount', 0)
                    channel_subscriber_map[channel_id] = subscriber_count
            
            # Process video data
            enhanced_data = {}
            for video in video_response.get('items', []):
                video_id = video['id']
                snippet = video['snippet']
                statistics = video['statistics']
                status = video.get('status', {})
                live_details = video.get('liveStreamingDetails', {})
                
                # Format published date
                published_at = snippet.get('publishedAt', '')
                published_formatted = self.format_date_to_ddmmyyyy(published_at)
                
                # Get channel subscriber count
                channel_id = snippet['channelId']
                subscriber_count = channel_subscriber_map.get(channel_id, 0)
                
                enhanced_data[video_id] = {
                    'PublishedAt_Formatted': published_formatted,
                    'CategoryId': snippet.get('categoryId', ''),
                    'DefaultLanguage': snippet.get('defaultLanguage', ''),
                    'ChannelId': channel_id,
                    'LiveBroadcastContent': snippet.get('liveBroadcastContent', 'none'),
                    'CommentCount_API': statistics.get('commentCount', 0),
                    'FavoriteCount': statistics.get('favoriteCount', 0),
                    'ChannelSubscriberCount': subscriber_count
                }
            
            return enhanced_data
            
        except HttpError as e:
            logger.error(f"YouTube API error in batch request: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error getting video details: {e}")
            return {}

    def enhance_videos_dataset(self, input_file, output_file):
        """Enhance videos dataset with 8 critical columns"""
        logger.info("🎬 Starting videos dataset enhancement...")
        
        # Read current dataset
        df = pd.read_csv(input_file)
        logger.info(f"📊 Loaded {len(df)} videos from {input_file}")
        
        # Initialize new columns
        new_columns = [
            'PublishedAt_Formatted', 'CategoryId', 'DefaultLanguage', 'ChannelId',
            'LiveBroadcastContent', 'CommentCount_API', 'FavoriteCount', 'ChannelSubscriberCount'
        ]
        
        for col in new_columns:
            if col not in df.columns:
                df[col] = ''
        
        # Process videos in batches
        video_ids = df['VideoID'].tolist()
        processed_count = 0
        
        for i in range(0, len(video_ids), self.video_batch_size):
            batch_ids = video_ids[i:i + self.video_batch_size]
            logger.info(f"📡 Processing batch {i//self.video_batch_size + 1}: videos {i+1}-{min(i+self.video_batch_size, len(video_ids))}")
            
            # Get enhanced data for this batch
            enhanced_data = self.get_video_details_batch(batch_ids)
            
            # Update dataframe
            for video_id in batch_ids:
                if video_id in enhanced_data:
                    row_idx = df[df['VideoID'] == video_id].index[0]
                    for col, value in enhanced_data[video_id].items():
                        df.at[row_idx, col] = value
                    processed_count += 1
            
            # Rate limiting
            time.sleep(0.1)
        
        # Also format existing UploadDate column
        if 'UploadDate' in df.columns:
            df['UploadDate'] = df['UploadDate'].apply(self.format_date_to_ddmmyyyy)
        
        # Save enhanced dataset
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Enhanced videos dataset saved: {output_file}")
        logger.info(f"📈 Successfully processed: {processed_count}/{len(df)} videos")
        
        return df

    def get_comment_details_batch(self, video_ids):
        """Get enhanced comment details for batch of video IDs"""
        enhanced_comments = {}
        
        for video_id in video_ids:
            try:
                comment_request = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=self.comment_batch_size,
                    order='relevance'
                )
                comment_response = comment_request.execute()
                
                for comment_thread in comment_response.get('items', []):
                    top_comment = comment_thread['snippet']['topLevelComment']['snippet']
                    comment_id = comment_thread['snippet']['topLevelComment']['id']
                    
                    # Format dates
                    published_at = top_comment.get('publishedAt', '')
                    updated_at = top_comment.get('updatedAt', '')
                    published_formatted = self.format_date_to_ddmmyyyy(published_at)
                    
                    enhanced_comments[comment_id] = {
                        'Date_Formatted': published_formatted,
                        'PublishedAt': published_at,
                        'UpdatedAt': updated_at,
                        'ModerationStatus': top_comment.get('moderationStatus', 'published')
                    }
                    
                    # Process replies if any
                    if 'replies' in comment_thread:
                        for reply in comment_thread['replies']['comments']:
                            reply_snippet = reply['snippet']
                            reply_id = reply['id']
                            
                            reply_published_at = reply_snippet.get('publishedAt', '')
                            reply_updated_at = reply_snippet.get('updatedAt', '')
                            reply_published_formatted = self.format_date_to_ddmmyyyy(reply_published_at)
                            
                            enhanced_comments[reply_id] = {
                                'Date_Formatted': reply_published_formatted,
                                'PublishedAt': reply_published_at,
                                'UpdatedAt': reply_updated_at,
                                'ModerationStatus': reply_snippet.get('moderationStatus', 'published')
                            }
                
                time.sleep(0.1)  # Rate limiting
                
            except HttpError as e:
                if 'commentsDisabled' in str(e):
                    logger.info(f"Comments disabled for video {video_id}")
                else:
                    logger.warning(f"Error getting comments for {video_id}: {e}")
            except Exception as e:
                logger.error(f"Error processing comments for {video_id}: {e}")
        
        return enhanced_comments

    def enhance_comments_dataset(self, input_file, output_file):
        """Enhance comments dataset with 4 critical columns"""
        logger.info("💬 Starting comments dataset enhancement...")
        
        # Read current dataset
        df = pd.read_csv(input_file)
        logger.info(f"📊 Loaded {len(df)} comments from {input_file}")
        
        # Initialize new columns
        new_columns = ['Date_Formatted', 'PublishedAt', 'UpdatedAt', 'ModerationStatus']
        
        for col in new_columns:
            if col not in df.columns:
                df[col] = ''
        
        # Format existing Date column first
        if 'Date' in df.columns:
            df['Date_Formatted'] = df['Date'].apply(self.format_date_to_ddmmyyyy)
        
        # Get unique video IDs for API enhancement
        unique_video_ids = df['VideoID'].dropna().unique().tolist()
        
        # Process videos in smaller batches for comments
        processed_videos = 0
        
        for i in range(0, len(unique_video_ids), 5):  # Smaller batches for comments
            batch_video_ids = unique_video_ids[i:i + 5]
            logger.info(f"📡 Processing comment batch {i//5 + 1}: videos {i+1}-{min(i+5, len(unique_video_ids))}")
            
            # Get enhanced comment data
            enhanced_comments = self.get_comment_details_batch(batch_video_ids)
            
            # Update dataframe based on CommentID where available
            for comment_id, enhancement_data in enhanced_comments.items():
                matching_rows = df[df['CommentID'] == comment_id]
                if not matching_rows.empty:
                    row_idx = matching_rows.index[0]
                    for col, value in enhancement_data.items():
                        df.at[row_idx, col] = value
            
            processed_videos += len(batch_video_ids)
            time.sleep(0.2)  # Rate limiting
        
        # Fill missing ModerationStatus with 'published' (most comments are published)
        df['ModerationStatus'] = df['ModerationStatus'].fillna('published')
        
        # Save enhanced dataset
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Enhanced comments dataset saved: {output_file}")
        logger.info(f"📈 Processed comments for: {processed_videos} videos")
        
        return df

def main():
    # Configuration
    API_KEY = "AIzaSyClXhVz8WRPxTRYLH3gJ0MxhkyzHQtwumo"  # User's YouTube API key
    
    # File paths
    videos_input = "backend/data/videos/youtube_videos_enhanced.csv"
    videos_output = "backend/data/videos/youtube_videos_final.csv"
    comments_input = "backend/data/comments/youtube_comments.csv"
    comments_output = "backend/data/comments/youtube_comments_enhanced.csv"
    
    try:
        # Initialize enhancer
        enhancer = DatasetEnhancer(API_KEY)
        
        logger.info("🚀 PERCEPTA PRO v2.0 - CRITICAL DATASET ENHANCEMENT")
        logger.info("=" * 60)
        
        # Enhance videos dataset
        if os.path.exists(videos_input):
            videos_df = enhancer.enhance_videos_dataset(videos_input, videos_output)
            logger.info(f"✅ Videos enhanced: {len(videos_df)} records with {len(videos_df.columns)} columns")
        else:
            logger.error(f"❌ Videos input file not found: {videos_input}")
        
        # Enhance comments dataset  
        if os.path.exists(comments_input):
            comments_df = enhancer.enhance_comments_dataset(comments_input, comments_output)
            logger.info(f"✅ Comments enhanced: {len(comments_df)} records with {len(comments_df.columns)} columns")
        else:
            logger.error(f"❌ Comments input file not found: {comments_input}")
        
        logger.info("=" * 60)
        logger.info("🎉 PHASE 1 ENHANCEMENT COMPLETE!")
        logger.info("📋 Added 8 critical video columns + 4 comment columns")
        logger.info("🎯 Ready for Phase 2: AI Processing Pipeline")
        
    except Exception as e:
        logger.error(f"❌ Enhancement failed: {e}")
        raise

if __name__ == "__main__":
    main() 