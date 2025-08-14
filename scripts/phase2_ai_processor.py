#!/usr/bin/env python3
"""
PHASE 2 AI PROCESSING PIPELINE - Percepta Pro v2.0
Bilingual AI processing for reputation monitoring with Telugu-English precision

PHASE 2A: Language Foundation
- Transcript extraction and processing
- High-accuracy Telugu-English translation
- Language detection and classification

PHASE 2B: Sentiment Intelligence  
- Multi-layered bilingual sentiment analysis
- Reputation scoring algorithm
- Temporal trend analysis

PHASE 2C: Executive Intelligence
- Advanced analytics engine
- Crisis detection system
- Predictive modeling

Author: Percepta Pro v2.0 Phase 2
Date: 2025-06-29
"""

import pandas as pd
import os
import logging
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json
import re

# AI and NLP libraries
pipeline = None
whisper = None
openai = None

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_API_AVAILABLE = True
except ImportError as e:
    print(f"Warning: YouTube transcript API not available: {e}")
    TRANSCRIPT_API_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Transformers not available: {e}")
    TRANSFORMERS_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OpenAI not available: {e}")
    OPENAI_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Whisper not available: {e}")
    WHISPER_AVAILABLE = False

# Google Translation API
try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Google Translator not available: {e}")
    TRANSLATOR_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'scripts/logs/phase2_ai_processing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PerceptaPhase2Processor:
    """
    Percepta Pro Phase 2 AI Processing Pipeline
    Handles bilingual transcript extraction, translation, and sentiment analysis
    """
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        Initialize Phase 2 AI Processor
        
        Args:
            api_keys: Dictionary containing API keys (openai, youtube)
        """
        self.api_keys = api_keys or {}
        self.translator = None
        self.sentiment_analyzer = None
        self.whisper_model = None
        self.telugu_sentiment_model = None
        
        # Initialize processing components
        self._initialize_components()
        
        # Processing statistics
        self.stats = {
            'videos_processed': 0,
            'transcripts_extracted': 0,
            'translations_completed': 0,
            'sentiment_analyses': 0,
            'errors': [],
            'start_time': datetime.now()
        }
        
        logger.info("🚀 Percepta Phase 2 AI Processor initialized")
    
    def _initialize_components(self):
        """Initialize AI processing components"""
        try:
            # Initialize translator
            if TRANSLATOR_AVAILABLE:
                self.translator = Translator()
                logger.info("Google Translator initialized")
            else:
                logger.warning("Google Translator not available - translation disabled")
            
            # Initialize English sentiment analyzer
            if TRANSFORMERS_AVAILABLE and pipeline is not None:
                try:
                    self.sentiment_analyzer = pipeline(
                        "sentiment-analysis",
                        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                        return_all_scores=True
                    )
                    logger.info("English sentiment analyzer initialized")
                except Exception as e:
                    # Fallback to basic sentiment analyzer
                    try:
                        self.sentiment_analyzer = pipeline("sentiment-analysis")
                        logger.info("Basic sentiment analyzer initialized (fallback)")
                    except Exception as e2:
                        logger.warning(f"Sentiment analyzer not available: {e2}")
                        self.sentiment_analyzer = None
            else:
                logger.warning("Transformers not available - sentiment analysis limited")
            
            # Initialize Whisper for audio processing
            if WHISPER_AVAILABLE and whisper is not None:
                try:
                    self.whisper_model = whisper.load_model("base")
                    logger.info("Whisper audio model initialized")
                except Exception as e:
                    logger.warning(f"Whisper model loading failed: {e}")
                    self.whisper_model = None
            else:
                logger.warning("Whisper not available - audio processing disabled")
                
            # Initialize Telugu sentiment (if available)
            if TRANSFORMERS_AVAILABLE and pipeline is not None:
                try:
                    # Use multilingual model that supports Telugu
                    self.telugu_sentiment_model = pipeline(
                        "sentiment-analysis",
                        model="nlptown/bert-base-multilingual-uncased-sentiment",
                        return_all_scores=True
                    )
                    logger.info("Telugu sentiment analyzer initialized")
                except Exception as e:
                    logger.warning(f"Telugu sentiment model not available: {e}")
                    self.telugu_sentiment_model = None
            else:
                logger.warning("Telugu sentiment analysis not available")
                self.telugu_sentiment_model = None
                
        except Exception as e:
            logger.error(f"Component initialization error: {e}")
            # Don't raise - allow processor to continue with limited functionality
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def extract_transcript(self, video_url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract transcript from YouTube video
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Tuple of (english_transcript, telugu_transcript)
        """
        if not TRANSCRIPT_API_AVAILABLE:
            logger.warning("YouTube transcript API not available - transcript extraction disabled")
            return None, None
            
        video_id = self.extract_video_id(video_url)
        if not video_id:
            logger.warning(f"Could not extract video ID from URL: {video_url}")
            return None, None
        
        try:
            # Try to get transcript in multiple languages
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            
            english_transcript = None
            telugu_transcript = None
            
            # Look for English transcript
            try:
                en_transcript = transcripts.find_transcript(['en', 'en-US', 'en-GB'])
                english_transcript = ' '.join([item['text'] for item in en_transcript.fetch()])
                logger.info(f"English transcript extracted for {video_id}")
            except Exception:
                logger.debug(f"No English transcript for {video_id}")
            
            # Look for Telugu transcript
            try:
                te_transcript = transcripts.find_transcript(['te', 'hi'])  # Telugu or Hindi
                telugu_transcript = ' '.join([item['text'] for item in te_transcript.fetch()])
                logger.info(f"Telugu transcript extracted for {video_id}")
            except Exception:
                logger.debug(f"No Telugu transcript for {video_id}")
            
            # If no transcript available, try auto-generated
            if not english_transcript and not telugu_transcript:
                try:
                    auto_transcript = transcripts.find_generated_transcript(['en'])
                    english_transcript = ' '.join([item['text'] for item in auto_transcript.fetch()])
                    logger.info(f"Auto-generated English transcript for {video_id}")
                except Exception:
                    logger.debug(f"No auto-generated transcript for {video_id}")
            
            return english_transcript, telugu_transcript
            
        except Exception as e:
            logger.error(f"Transcript extraction failed for {video_id}: {e}")
            return None, None
    
    def translate_text(self, text: str, target_lang: str = 'en') -> Optional[str]:
        """
        Translate text with high accuracy
        
        Args:
            text: Text to translate
            target_lang: Target language ('en' or 'te')
            
        Returns:
            Translated text or None if failed
        """
        if not text or not text.strip():
            return None
        
        if not self.translator:
            logger.warning("Translator not available - skipping translation")
            return None
        
        try:
            # Limit text length for API efficiency
            if len(text) > 5000:
                text = text[:5000] + "..."
            
            result = self.translator.translate(text, dest=target_lang)
            translated = result.text
            
            logger.debug(f"Translated text to {target_lang}: {text[:50]}...")
            return translated
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return None
    
    def analyze_sentiment(self, text: str, language: str = 'en') -> Tuple[float, str]:
        """
        Analyze sentiment with bilingual support
        
        Args:
            text: Text to analyze
            language: Language of text ('en' or 'te')
            
        Returns:
            Tuple of (sentiment_score, sentiment_label)
            Score: -1.0 (negative) to 1.0 (positive)
            Label: 'Positive', 'Negative', or 'Neutral'
        """
        if not text or not text.strip():
            return 0.0, 'Neutral'
        
        # Check if we have appropriate analyzer
        if language == 'te' and self.telugu_sentiment_model:
            analyzer = self.telugu_sentiment_model
        elif self.sentiment_analyzer:
            analyzer = self.sentiment_analyzer
        else:
            # Basic sentiment fallback using keyword matching
            logger.debug("No sentiment analyzer available - using keyword fallback")
            return self._basic_sentiment_analysis(text)
        
        try:
            # Limit text length
            if len(text) > 512:
                text = text[:512] + "..."
            
            results = analyzer(text)
            
            # Convert results to standardized format
            if isinstance(results[0], list):
                results = results[0]
            
            # Find the highest confidence sentiment
            best_result = max(results, key=lambda x: x['score'])
            label = best_result['label']
            confidence = best_result['score']
            
            # Normalize labels and scores
            if label.upper() in ['POSITIVE', 'POS', '5 stars', '4 stars']:
                sentiment_score = confidence
                sentiment_label = 'Positive'
            elif label.upper() in ['NEGATIVE', 'NEG', '1 star', '2 stars']:
                sentiment_score = -confidence
                sentiment_label = 'Negative'
            else:
                sentiment_score = 0.0
                sentiment_label = 'Neutral'
            
            logger.debug(f"Sentiment analyzed: {sentiment_label} ({sentiment_score:.3f})")
            return sentiment_score, sentiment_label
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return self._basic_sentiment_analysis(text)
    
    def _basic_sentiment_analysis(self, text: str) -> Tuple[float, str]:
        """
        Basic sentiment analysis using keyword matching
        Fallback when AI models are not available
        """
        text_lower = text.lower()
        
        # Positive keywords (English + Telugu)
        positive_keywords = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'best', 'fantastic',
            'చాలా బాగుంది', 'అద్భుతం', 'చాలా మంచిది', 'బాగుంది'
        ]
        
        # Negative keywords (English + Telugu)
        negative_keywords = [
            'bad', 'terrible', 'awful', 'worst', 'horrible', 'hate',
            'చెత్త', 'దారుణం', 'మోసం', 'అరెస్ట్', 'కేసు', 'అవినీతి'
        ]
        
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        if positive_count > negative_count:
            return 0.6, 'Positive'
        elif negative_count > positive_count:
            return -0.6, 'Negative'
        else:
            return 0.0, 'Neutral'
    
    def extract_keywords(self, text: str, language: str = 'en', max_keywords: int = 10) -> List[str]:
        """
        Extract key terms and phrases from text
        
        Args:
            text: Text to analyze
            language: Language of text
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of extracted keywords
        """
        if not text or not text.strip():
            return []
        
        try:
            # Simple keyword extraction using word frequency
            # Remove common stop words and clean text
            import string
            
            # Telugu stop words (basic set)
            telugu_stop_words = {
                'అని', 'అయి', 'అయ్యారు', 'అద్దు', 'ఇది', 'ఈ', 'ఆ', 'వా', 'మా', 'నా',
                'చే', 'కి', 'లో', 'తో', 'కు', 'గా', 'వరకు', 'దగ్గర', 'వైపు'
            }
            
            # English stop words (basic set)
            english_stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
                'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
            }
            
            # Clean and tokenize text
            text = text.lower().translate(str.maketrans('', '', string.punctuation))
            words = text.split()
            
            # Filter out stop words
            if language == 'te':
                words = [w for w in words if w not in telugu_stop_words and len(w) > 2]
            else:
                words = [w for w in words if w not in english_stop_words and len(w) > 2]
            
            # Count frequency and get top keywords
            from collections import Counter
            word_freq = Counter(words)
            keywords = [word for word, count in word_freq.most_common(max_keywords)]
            
            logger.debug(f"✅ Extracted {len(keywords)} keywords from {language} text")
            return keywords
            
        except Exception as e:
            logger.error(f"❌ Keyword extraction failed: {e}")
            return []
    
    def process_video_row(self, row: pd.Series) -> Dict[str, any]:
        """
        Process a single video row through the AI pipeline
        
        Args:
            row: Video data row from DataFrame
            
        Returns:
            Dictionary with processed AI fields
        """
        result = {
            'VideoID': row.get('VideoID', ''),
            'Transcript_EN': None,
            'Transcript_TE': None,
            'Summary_EN': None,
            'Summary_TE': None,
            'SentimentScore_EN': 0.0,
            'SentimentScore_TE': 0.0,
            'SentimentLabel_EN': 'Neutral',
            'SentimentLabel_TE': 'Neutral',
            'Keywords_EN': '',
            'Keywords_TE': ''
        }
        
        try:
            video_url = row.get('URL', '')
            title = row.get('Title', '')
            description = row.get('Description', '')
            
            logger.info(f"Processing video: {title[:50]}...")
            
            # Step 1: Extract transcripts
            transcript_en, transcript_te = self.extract_transcript(video_url)
            result['Transcript_EN'] = transcript_en
            result['Transcript_TE'] = transcript_te
            
            if transcript_en:
                self.stats['transcripts_extracted'] += 1
            
            # Step 2: Generate summaries from transcripts or description
            content_en = transcript_en or description or title
            if content_en and len(content_en) > 100:
                # Simple summary: take first 200 characters
                result['Summary_EN'] = content_en[:200] + "..." if len(content_en) > 200 else content_en
            elif title:
                # Use title as minimum summary
                result['Summary_EN'] = title
            
            # If we have Telugu transcript, process it
            if transcript_te:
                result['Summary_TE'] = transcript_te[:200] + "..." if len(transcript_te) > 200 else transcript_te
            elif content_en and self.translator:
                # Translate English content to Telugu
                translated_content = self.translate_text(content_en[:500], 'te')
                if translated_content:
                    result['Summary_TE'] = translated_content
                    if not transcript_te:  # Only set transcript if we don't have one
                        result['Transcript_TE'] = translated_content
                    self.stats['translations_completed'] += 1
            
            # Step 3: Sentiment analysis
            if content_en:
                score_en, label_en = self.analyze_sentiment(content_en, 'en')
                result['SentimentScore_EN'] = score_en
                result['SentimentLabel_EN'] = label_en
                self.stats['sentiment_analyses'] += 1
            
            if result['Summary_TE']:
                score_te, label_te = self.analyze_sentiment(result['Summary_TE'], 'te')
                result['SentimentScore_TE'] = score_te
                result['SentimentLabel_TE'] = label_te
                self.stats['sentiment_analyses'] += 1
            
            # Step 4: Keyword extraction
            if content_en:
                keywords_en = self.extract_keywords(content_en, 'en')
                result['Keywords_EN'] = ', '.join(keywords_en[:10])
            
            if result['Summary_TE']:
                keywords_te = self.extract_keywords(result['Summary_TE'], 'te')
                result['Keywords_TE'] = ', '.join(keywords_te[:10])
            
            self.stats['videos_processed'] += 1
            logger.info(f"Video processed successfully: {title[:30]}...")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Video processing failed: {e}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return result
    
    def process_videos_dataset(self, videos_file: str, output_file: str = None, batch_size: int = 10):
        """
        Process entire videos dataset through AI pipeline
        
        Args:
            videos_file: Path to videos CSV file
            output_file: Path to save processed results
            batch_size: Number of videos to process in each batch
        """
        try:
            # Load videos dataset
            logger.info(f"📂 Loading videos dataset: {videos_file}")
            videos_df = pd.read_csv(videos_file)
            logger.info(f"📊 Loaded {len(videos_df)} videos for processing")
            
            # Prepare output file
            if not output_file:
                output_file = videos_file.replace('.csv', '_ai_processed.csv')
            
            processed_rows = []
            
            # Process videos in batches
            for i in range(0, len(videos_df), batch_size):
                batch = videos_df.iloc[i:i+batch_size]
                logger.info(f"🔄 Processing batch {i//batch_size + 1}/{(len(videos_df)-1)//batch_size + 1}")
                
                for idx, row in batch.iterrows():
                    try:
                        # Process video through AI pipeline
                        ai_results = self.process_video_row(row)
                        
                        # Merge with original row data
                        processed_row = row.to_dict()
                        processed_row.update(ai_results)
                        processed_rows.append(processed_row)
                        
                        # Save progress every 5 videos
                        if len(processed_rows) % 5 == 0:
                            temp_df = pd.DataFrame(processed_rows)
                            temp_df.to_csv(output_file.replace('.csv', '_temp.csv'), index=False)
                            logger.info(f"💾 Progress saved: {len(processed_rows)} videos processed")
                        
                    except Exception as e:
                        logger.error(f"❌ Failed to process video at index {idx}: {e}")
                        continue
                
                # Brief pause between batches
                time.sleep(2)
            
            # Save final results
            if processed_rows:
                final_df = pd.DataFrame(processed_rows)
                final_df.to_csv(output_file, index=False)
                logger.info(f"✅ AI processing complete! Saved to: {output_file}")
                
                # Clean up temp file
                temp_file = output_file.replace('.csv', '_temp.csv')
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                # Print processing statistics
                self._print_processing_stats()
                
            else:
                logger.error("❌ No videos were successfully processed")
                
        except Exception as e:
            logger.error(f"❌ Dataset processing failed: {e}")
            raise
    
    def _print_processing_stats(self):
        """Print processing statistics"""
        end_time = datetime.now()
        duration = end_time - self.stats['start_time']
        
        print("\n" + "="*60)
        print("🎉 PHASE 2 AI PROCESSING COMPLETE")
        print("="*60)
        print(f"📊 Videos Processed: {self.stats['videos_processed']}")
        print(f"🎤 Transcripts Extracted: {self.stats['transcripts_extracted']}")
        print(f"🌐 Translations Completed: {self.stats['translations_completed']}")
        print(f"🧠 Sentiment Analyses: {self.stats['sentiment_analyses']}")
        print(f"⏱️ Processing Time: {duration}")
        print(f"❌ Errors: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print("\n⚠️ Error Summary:")
            for error in self.stats['errors'][-5:]:  # Show last 5 errors
                print(f"   • {error}")
        
        print("="*60)

def main():
    """Main execution function"""
    
    # Configuration
    VIDEOS_FILE = "backend/data/videos/youtube_videos_final.csv"
    OUTPUT_FILE = "backend/data/videos/youtube_videos_ai_processed.csv"
    BATCH_SIZE = 5  # Process 5 videos at a time
    
    # API keys (add your keys here)
    api_keys = {
        'openai': os.getenv('OPENAI_API_KEY'),
        'youtube': os.getenv('YOUTUBE_API_KEY')
    }
    
    try:
        print("🚀 Starting Percepta Pro Phase 2 AI Processing Pipeline")
        print("="*60)
        
        # Initialize processor
        processor = PerceptaPhase2Processor(api_keys)
        
        # Check if input file exists
        if not os.path.exists(VIDEOS_FILE):
            print(f"❌ Videos file not found: {VIDEOS_FILE}")
            print("Please ensure Phase 1 is complete and the file exists.")
            return
        
        # Start processing
        processor.process_videos_dataset(
            videos_file=VIDEOS_FILE,
            output_file=OUTPUT_FILE,
            batch_size=BATCH_SIZE
        )
        
        print(f"✅ Phase 2 processing complete! Results saved to: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ Phase 2 processing failed: {e}")
        logger.error(f"Fatal error in main: {e}")

if __name__ == "__main__":
    main() 