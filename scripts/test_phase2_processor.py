#!/usr/bin/env python3
"""
Test Phase 2 AI Processor - Percepta Pro v2.0
Quick validation of AI processing components before full dataset processing

Author: Percepta Pro v2.0 Phase 2 Test
Date: 2025-06-29
"""

import pandas as pd
import os
import sys
import logging
from datetime import datetime

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from phase2_ai_processor import PerceptaPhase2Processor
except ImportError as e:
    print(f"❌ Failed to import Phase 2 processor: {e}")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_components():
    """Test basic AI processing components"""
    print("🧪 Testing Basic AI Components")
    print("=" * 50)
    
    try:
        # Initialize processor
        processor = PerceptaPhase2Processor()
        
        # Test translation
        print("🔤 Testing Translation...")
        test_english = "This is a test of the translation system."
        translated = processor.translate_text(test_english, 'te')
        print(f"  Original: {test_english}")
        print(f"  Telugu: {translated}")
        
        # Test sentiment analysis
        print("\n🧠 Testing Sentiment Analysis...")
        positive_text = "This is excellent work, very good quality!"
        negative_text = "This is terrible, worst quality ever!"
        neutral_text = "This is a normal statement."
        
        pos_score, pos_label = processor.analyze_sentiment(positive_text)
        neg_score, neg_label = processor.analyze_sentiment(negative_text)
        neu_score, neu_label = processor.analyze_sentiment(neutral_text)
        
        print(f"  Positive: '{positive_text}' -> {pos_label} ({pos_score:.3f})")
        print(f"  Negative: '{negative_text}' -> {neg_label} ({neg_score:.3f})")
        print(f"  Neutral: '{neutral_text}' -> {neu_label} ({neu_score:.3f})")
        
        # Test keyword extraction
        print("\n🎯 Testing Keyword Extraction...")
        sample_text = "Sridhar Rao Sandhya Convention political controversy legal issues arrest allegations"
        keywords = processor.extract_keywords(sample_text)
        print(f"  Text: {sample_text}")
        print(f"  Keywords: {', '.join(keywords)}")
        
        # Test video ID extraction
        print("\n🆔 Testing Video ID Extraction...")
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ"
        ]
        
        for url in test_urls:
            video_id = processor.extract_video_id(url)
            print(f"  URL: {url}")
            print(f"  Video ID: {video_id}")
        
        print("\n✅ Basic component tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Basic component test failed: {e}")
        return False

def test_sample_video_processing():
    """Test processing of sample videos from our dataset"""
    print("\n🎬 Testing Sample Video Processing")
    print("=" * 50)
    
    try:
        # Load a few sample videos
        videos_file = "backend/data/videos/youtube_videos_final.csv"
        if not os.path.exists(videos_file):
            print(f"❌ Videos file not found: {videos_file}")
            return False
        
        videos_df = pd.read_csv(videos_file)
        print(f"📂 Loaded {len(videos_df)} videos")
        
        # Take first 3 videos for testing
        sample_videos = videos_df.head(3)
        print(f"🔍 Testing with {len(sample_videos)} sample videos")
        
        # Initialize processor
        processor = PerceptaPhase2Processor()
        
        # Process each sample video
        results = []
        for idx, row in sample_videos.iterrows():
            print(f"\n📺 Processing video {idx + 1}: {row.get('Title', 'N/A')[:50]}...")
            
            try:
                result = processor.process_video_row(row)
                results.append(result)
                
                # Print key results
                print(f"  ✅ Transcript EN: {'✓' if result['Transcript_EN'] else '✗'}")
                print(f"  ✅ Summary EN: {'✓' if result['Summary_EN'] else '✗'}")
                print(f"  ✅ Sentiment EN: {result['SentimentLabel_EN']} ({result['SentimentScore_EN']:.3f})")
                print(f"  ✅ Keywords EN: {result['Keywords_EN'][:50]}...")
                
            except Exception as e:
                print(f"  ❌ Processing failed: {e}")
                continue
        
        print(f"\n📊 Sample Processing Results:")
        print(f"  Videos attempted: {len(sample_videos)}")
        print(f"  Videos processed: {len(results)}")
        print(f"  Success rate: {len(results)/len(sample_videos)*100:.1f}%")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"❌ Sample video processing test failed: {e}")
        return False

def main():
    """Run all Phase 2 tests"""
    print("🚀 Phase 2 AI Processor Testing Suite")
    print("=" * 60)
    print(f"📅 Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = []
    
    # Test 1: Basic components
    print("\n" + "=" * 60)
    basic_test = test_basic_components()
    test_results.append(("Basic Components", basic_test))
    
    # Test 2: Sample video processing
    print("\n" + "=" * 60)
    sample_test = test_sample_video_processing()
    test_results.append(("Sample Video Processing", sample_test))
    
    # Final results
    print("\n" + "=" * 60)
    print("🏁 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(test_results)} tests passed")
    
    if passed == len(test_results):
        print("🎉 All tests passed! Phase 2 processor is ready for full dataset processing.")
        print("\nNext steps:")
        print("1. Run: python scripts/phase2_ai_processor.py")
        print("2. Monitor processing logs in scripts/logs/")
        print("3. Check output: backend/data/videos/youtube_videos_ai_processed.csv")
    else:
        print("⚠️ Some tests failed. Please check the errors above before proceeding.")
    
    return passed == len(test_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 