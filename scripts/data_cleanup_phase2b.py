#!/usr/bin/env python3
"""
Percepta Pro Data Cleanup for Phase 2B
Remove old data files and keep only highest quality, most relevant data
Prepare clean foundation for enhanced AI processing
"""

import os
import shutil
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'scripts/logs/data_cleanup_phase2b_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataCleanupPhase2B:
    """
    Comprehensive data cleanup for Phase 2B
    Focus on quality, relevance, and client-specific requirements
    """
    
    def __init__(self):
        """Initialize data cleanup processor"""
        logger.info("🧹 Initializing Data Cleanup for Phase 2B")
        
        self.base_dir = Path("backend/data")
        self.backup_dir = Path("backend/data/backups")
        
        # Create backup directory
        self.backup_dir.mkdir(exist_ok=True)
        
        # Files to keep (highest quality)
        self.keep_files = {
            'videos': [
                'youtube_videos_ai_processed.csv',  # Best AI processed videos
                'youtube_videos_final.csv'          # Final curated videos
            ],
            'comments': [
                'youtube_comments_final.csv'        # Current best comments
            ]
        }
        
        # Files to remove (old/redundant)
        self.remove_files = [
            'youtube_videos.csv',
            'youtube_videos_v1_backup.csv', 
            'youtube_videos_enhanced.csv',
            'youtube_videos_comprehensive_backup.csv',
            'youtube_videos_comprehensive.csv',
            'youtube_comments.csv'
        ]
        
        self.stats = {
            'files_backed_up': 0,
            'files_removed': 0,
            'videos_processed': 0,
            'comments_processed': 0,
            'data_quality_improved': False
        }
    
    def backup_important_files(self):
        """Backup important files before cleanup"""
        logger.info("📦 Creating backups of important files...")
        
        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for category, filenames in self.keep_files.items():
            category_dir = self.base_dir / category
            backup_category_dir = self.backup_dir / category
            backup_category_dir.mkdir(exist_ok=True)
            
            for filename in filenames:
                source_file = category_dir / filename
                if source_file.exists():
                    backup_filename = f"{filename.split('.')[0]}_backup_{backup_timestamp}.csv"
                    backup_file = backup_category_dir / backup_filename
                    
                    shutil.copy2(source_file, backup_file)
                    logger.info(f"✅ Backed up: {filename} -> {backup_filename}")
                    self.stats['files_backed_up'] += 1
    
    def remove_old_files(self):
        """Remove old and redundant data files"""
        logger.info("🗑️ Removing old and redundant files...")
        
        for category in ['videos', 'comments']:
            category_dir = self.base_dir / category
            
            for filename in self.remove_files:
                file_path = category_dir / filename
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"❌ Removed: {filename}")
                    self.stats['files_removed'] += 1
    
    def validate_and_clean_videos(self):
        """Validate and clean videos dataset for highest quality"""
        logger.info("🎥 Validating and cleaning videos dataset...")
        
        videos_dir = self.base_dir / "videos"
        
        # Use the best available videos file
        source_file = None
        for preferred_file in ['youtube_videos_ai_processed.csv', 'youtube_videos_final.csv']:
            file_path = videos_dir / preferred_file
            if file_path.exists():
                source_file = file_path
                break
        
        if not source_file:
            logger.error("❌ No suitable videos file found!")
            return
        
        logger.info(f"📂 Using videos source: {source_file.name}")
        
        # Load and validate
        df = pd.read_csv(source_file)
        logger.info(f"📊 Loaded {len(df)} videos")
        
        # Quality filters
        initial_count = len(df)
        
        # Remove videos without essential data
        df = df.dropna(subset=['VideoID', 'Title'])
        logger.info(f"🔍 After removing videos without VideoID/Title: {len(df)}")
        
        # Keep only videos with relevance to Sridhar Rao
        sridhar_keywords = [
            'sridhar', 'rao', 'sandhya', 'convention', 'black magic', 
            'చేతబడి', 'మాగంటి', 'శ్రీధర్', 'రావు', 'సంధ్య'
        ]
        
        def is_relevant(title, description=""):
            text = f"{title} {description}".lower()
            return any(keyword.lower() in text for keyword in sridhar_keywords)
        
        # Apply relevance filter
        relevant_mask = df.apply(lambda row: is_relevant(
            str(row.get('Title', '')), 
            str(row.get('Description', ''))
        ), axis=1)
        
        df = df[relevant_mask]
        logger.info(f"🎯 After relevance filtering: {len(df)}")
        
        # Sort by relevance and engagement
        if 'ViewCount' in df.columns:
            df['ViewCount'] = pd.to_numeric(df['ViewCount'], errors='coerce').fillna(0)
            df = df.sort_values(['ViewCount'], ascending=False)
        
        # Keep top quality videos (limit to most relevant)
        if len(df) > 300:
            df = df.head(300)
            logger.info(f"📉 Limited to top 300 most relevant videos")
        
        # Save cleaned dataset
        output_file = videos_dir / "youtube_videos_phase2b_ready.csv"
        df.to_csv(output_file, index=False)
        
        self.stats['videos_processed'] = len(df)
        logger.info(f"✅ Cleaned videos saved: {output_file}")
        logger.info(f"📈 Quality improvement: {initial_count} -> {len(df)} videos")
    
    def validate_and_clean_comments(self):
        """Validate and clean comments dataset for highest quality"""
        logger.info("💬 Validating and cleaning comments dataset...")
        
        comments_dir = self.base_dir / "comments"
        source_file = comments_dir / "youtube_comments_final.csv"
        
        if not source_file.exists():
            logger.error("❌ Comments file not found!")
            return
        
        # Load and validate
        df = pd.read_csv(source_file)
        logger.info(f"📊 Loaded {len(df)} comments")
        
        # Quality filters
        initial_count = len(df)
        
        # Remove comments without essential data
        df = df.dropna(subset=['VideoID', 'Comment'])
        logger.info(f"🔍 After removing comments without VideoID/Comment: {len(df)}")
        
        # Remove extremely short comments (less than 3 characters)
        df = df[df['Comment'].str.len() >= 3]
        logger.info(f"📏 After removing too-short comments: {len(df)}")
        
        # Remove spam-like comments (all caps, too many repeated characters)
        def is_quality_comment(comment):
            if not isinstance(comment, str):
                return False
            
            # Check for spam patterns
            if len(comment) > 500:  # Too long
                return False
            
            # Check for excessive repetition
            if len(set(comment.lower())) < len(comment) * 0.3:  # Low character diversity
                return False
            
            return True
        
        quality_mask = df['Comment'].apply(is_quality_comment)
        df = df[quality_mask]
        logger.info(f"✨ After quality filtering: {len(df)}")
        
        # Keep comments with meaningful engagement (likes > 0 or replies)
        if 'LikeCount' in df.columns:
            df['LikeCount'] = pd.to_numeric(df['LikeCount'], errors='coerce').fillna(0)
            
            # Prioritize comments with engagement or critical content
            critical_keywords = ['చేతబడి', 'అరెస్ట్', 'మాగంటి', 'black magic', 'arrest', 'sridhar']
            
            def has_engagement_or_critical(row):
                like_count = row.get('LikeCount', 0)
                comment = str(row.get('Comment', '')).lower()
                comment_en = str(row.get('Comment_EN', '')).lower()
                
                # High engagement
                if like_count > 0:
                    return True
                
                # Critical content
                if any(keyword.lower() in comment or keyword.lower() in comment_en 
                       for keyword in critical_keywords):
                    return True
                
                return False
            
            # Keep all high-value comments, sample others
            high_value_mask = df.apply(has_engagement_or_critical, axis=1)
            high_value_comments = df[high_value_mask]
            
            # Sample remaining comments to keep dataset manageable
            other_comments = df[~high_value_mask]
            if len(other_comments) > 1000:
                other_comments = other_comments.sample(1000, random_state=42)
            
            df = pd.concat([high_value_comments, other_comments]).drop_duplicates()
            logger.info(f"📈 After engagement/critical filtering: {len(df)}")
        
        # Sort by relevance and engagement
        if 'LikeCount' in df.columns:
            df = df.sort_values(['LikeCount'], ascending=False)
        
        # Save cleaned dataset
        output_file = comments_dir / "youtube_comments_phase2b_ready.csv"
        df.to_csv(output_file, index=False)
        
        self.stats['comments_processed'] = len(df)
        logger.info(f"✅ Cleaned comments saved: {output_file}")
        logger.info(f"📈 Quality improvement: {initial_count} -> {len(df)} comments")
    
    def optimize_data_structure(self):
        """Optimize data structure for Phase 2B processing"""
        logger.info("⚙️ Optimizing data structure for Phase 2B...")
        
        # Check if we have both cleaned datasets
        videos_file = self.base_dir / "videos" / "youtube_videos_phase2b_ready.csv"
        comments_file = self.base_dir / "comments" / "youtube_comments_phase2b_ready.csv"
        
        if videos_file.exists() and comments_file.exists():
            # Load both datasets
            videos_df = pd.read_csv(videos_file)
            comments_df = pd.read_csv(comments_file)
            
            # Ensure comment-video consistency
            valid_video_ids = set(videos_df['VideoID'].unique())
            comments_df = comments_df[comments_df['VideoID'].isin(valid_video_ids)]
            
            # Save optimized comments
            comments_df.to_csv(comments_file, index=False)
            
            logger.info(f"✅ Data structure optimized")
            logger.info(f"🎥 Final videos: {len(videos_df)}")
            logger.info(f"💬 Final comments: {len(comments_df)}")
            logger.info(f"🔗 Video-comment consistency: {len(valid_video_ids)} videos with comments")
            
            self.stats['data_quality_improved'] = True
    
    def generate_cleanup_report(self):
        """Generate comprehensive cleanup report"""
        report = {
            'phase': 'Phase 2B Data Cleanup',
            'timestamp': datetime.now().isoformat(),
            'cleanup_summary': {
                'files_backed_up': self.stats['files_backed_up'],
                'files_removed': self.stats['files_removed'],
                'videos_processed': self.stats['videos_processed'],
                'comments_processed': self.stats['comments_processed'],
                'data_quality_improved': self.stats['data_quality_improved']
            },
            'files_kept': self.keep_files,
            'files_removed': self.remove_files,
            'next_step': 'Ready for Phase 2B AI Processing'
        }
        
        # Save report
        report_file = f"scripts/logs/data_cleanup_phase2b_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        import json
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Print summary
        logger.info("=" * 70)
        logger.info("📊 PHASE 2B DATA CLEANUP SUMMARY")
        logger.info("=" * 70)
        logger.info(f"📦 Files Backed Up: {self.stats['files_backed_up']}")
        logger.info(f"🗑️ Files Removed: {self.stats['files_removed']}")
        logger.info(f"🎥 Videos Processed: {self.stats['videos_processed']}")
        logger.info(f"💬 Comments Processed: {self.stats['comments_processed']}")
        logger.info(f"✨ Data Quality Improved: {'✅' if self.stats['data_quality_improved'] else '❌'}")
        logger.info(f"📁 Report Saved: {report_file}")
        logger.info("=" * 70)
        logger.info("🚀 Ready for Phase 2B AI Processing!")
        logger.info("=" * 70)
    
    def run_full_cleanup(self):
        """Run complete data cleanup process"""
        logger.info("🧹 Starting Phase 2B Data Cleanup Process")
        logger.info("=" * 70)
        
        try:
            # Step 1: Backup important files
            self.backup_important_files()
            
            # Step 2: Remove old files
            self.remove_old_files()
            
            # Step 3: Clean and validate videos
            self.validate_and_clean_videos()
            
            # Step 4: Clean and validate comments
            self.validate_and_clean_comments()
            
            # Step 5: Optimize data structure
            self.optimize_data_structure()
            
            # Step 6: Generate report
            self.generate_cleanup_report()
            
            logger.info("✅ Phase 2B Data Cleanup completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Data cleanup failed: {e}")
            raise

def main():
    """Main function to run data cleanup"""
    cleanup = DataCleanupPhase2B()
    cleanup.run_full_cleanup()

if __name__ == "__main__":
    main() 