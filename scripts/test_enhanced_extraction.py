#!/usr/bin/env python3
"""
Test Script for Enhanced Telugu Extractor
========================================

Tests the comprehensive bilingual extraction system with sample queries
and validates the precision keyword targeting system.

Author: Percepta Pro v2.0 - Phase 1 Enhanced
"""

import os
import sys
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from scripts.enhanced_telugu_extractor import EnhancedTeluguExtractor
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


def test_keyword_system():
    """Test the comprehensive Telugu keyword system"""
    print("🧪 Testing Enhanced Telugu Keyword System")
    print("=" * 50)
    
    # Initialize without API key for testing
    try:
        # Test keyword generation
        extractor = EnhancedTeluguExtractor.__new__(EnhancedTeluguExtractor)
        keywords = extractor.get_comprehensive_telugu_keywords()
        
        print(f"📋 Total Keywords: {len(keywords)}")
        
        # Analyze by language
        telugu_count = len([k for k in keywords if k['language'] == 'te'])
        english_count = len([k for k in keywords if k['language'] == 'en'])
        
        print(f"🇮🇳 Telugu Keywords: {telugu_count}")
        print(f"🇬🇧 English Keywords: {english_count}")
        
        # Analyze by priority
        priority_analysis = {}
        for keyword in keywords:
            priority = keyword['priority']
            if priority not in priority_analysis:
                priority_analysis[priority] = []
            priority_analysis[priority].append(keyword)
        
        print(f"\n📊 Priority Distribution:")
        for priority in sorted(priority_analysis.keys(), reverse=True):
            count = len(priority_analysis[priority])
            print(f"   Priority {priority}: {count} keywords")
        
        # Show highest priority Telugu terms
        print(f"\n🎯 Critical Telugu Terms (Priority 10):")
        critical_terms = [k for k in keywords if k['priority'] == 10 and k['language'] == 'te']
        for i, term in enumerate(critical_terms[:8], 1):
            print(f"   {i}. {term['query']} ({term['category']})")
        
        # Category analysis
        categories = {}
        for keyword in keywords:
            category = keyword['category']
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        print(f"\n📂 Coverage Categories:")
        for category, count in sorted(categories.items()):
            print(f"   {category}: {count} terms")
        
        print(f"\n✅ Keyword system validation successful!")
        return True
        
    except Exception as e:
        print(f"❌ Keyword system test failed: {e}")
        return False


def test_relevance_scoring():
    """Test the precise relevance scoring system"""
    print("\n🧪 Testing Precise Relevance Scoring")
    print("=" * 50)
    
    try:
        extractor = EnhancedTeluguExtractor.__new__(EnhancedTeluguExtractor)
        
        # Test cases with expected high relevance
        test_cases = [
            {
                "title": "శ్రీధర్ రావు చేతబడి ఆడియో లీక్ వైరల్",
                "channel": "ABN Telugu",
                "description": "మాగంటి గోపీనాథ్ శ్రీధర్ రావు బెదిరింపులు",
                "expected_range": (70, 100),
                "language": "te"
            },
            {
                "title": "Sridhar Rao black magic audio threatens Maganti Gopinath",
                "channel": "TV5 News",
                "description": "Sandhya Convention MD involved in occult practices",
                "expected_range": (60, 90),
                "language": "en"
            },
            {
                "title": "శ్రీధర్ రావు భూకబ్జా కాజ హైద్రా ఆక్రమణ",
                "channel": "Zee Telugu News",
                "description": "గచ్చిబౌలి కట్టడాల కూల్చివేత అరెస్ట్",
                "expected_range": (50, 80),
                "language": "te"
            },
            {
                "title": "Sridhar Rao arrest HYDRAA demolition Gachibowli",
                "channel": "NTV Telugu",
                "description": "Land grab case cheating allegations",
                "expected_range": (40, 70),
                "language": "en"
            },
            {
                "title": "General business news about construction",
                "channel": "Unknown Channel",
                "description": "Regular business content",
                "expected_range": (0, 25),
                "language": "en"
            }
        ]
        
        print("📊 Relevance Score Test Results:")
        all_passed = True
        
        for i, test_case in enumerate(test_cases, 1):
            score = extractor.calculate_precise_relevance(
                test_case["title"], 
                test_case["channel"], 
                test_case["description"],
                test_case["language"]
            )
            
            min_expected, max_expected = test_case["expected_range"]
            passed = min_expected <= score <= max_expected
            
            status = "✅" if passed else "❌"
            print(f"   {i}. {status} Score: {score:.1f} (Expected: {min_expected}-{max_expected})")
            print(f"      Title: {test_case['title'][:50]}...")
            
            if not passed:
                all_passed = False
        
        # Test channel trust levels
        print(f"\n🏆 Channel Trust Level Tests:")
        trust_levels = extractor.get_enhanced_trusted_channels()
        
        high_trust = ["ABN Telugu", "TV5 News", "Zee Telugu News"]
        medium_trust = ["BRK News", "Prime9 News"]
        low_trust = ["Unknown Channel"]
        
        for channel in high_trust:
            trust = trust_levels.get(channel, 0)
            status = "✅" if trust >= 8 else "❌"
            print(f"   {status} {channel}: Trust Level {trust} (High)")
        
        for channel in medium_trust:
            trust = trust_levels.get(channel, 0)
            status = "✅" if 5 <= trust <= 7 else "❌"
            print(f"   {status} {channel}: Trust Level {trust} (Medium)")
        
        for channel in low_trust:
            trust = trust_levels.get(channel, 2)  # Default
            status = "✅" if trust <= 3 else "❌"
            print(f"   {status} {channel}: Trust Level {trust} (Low/Default)")
        
        if all_passed:
            print(f"\n✅ Relevance scoring system validation successful!")
            return True
        else:
            print(f"\n⚠️ Some relevance tests failed - scoring may need adjustment")
            return False
        
    except Exception as e:
        print(f"❌ Relevance scoring test failed: {e}")
        return False


def test_api_key_validation():
    """Test API key handling and validation"""
    print("\n🧪 Testing API Key Validation")
    print("=" * 50)
    
    # Test without API key
    os.environ.pop('YOUTUBE_API_KEY', None)
    
    try:
        extractor = EnhancedTeluguExtractor()
        print("❌ Should have failed without API key")
        return False
    except ValueError as e:
        print("✅ Correctly caught missing API key error")
    
    # Test with sample API key format
    os.environ['YOUTUBE_API_KEY'] = 'test_key_format_validation'
    
    try:
        extractor = EnhancedTeluguExtractor()
        print("✅ API key initialization successful")
        
        # Test extractor properties
        print(f"📍 Output file: {extractor.output_file}")
        print(f"🔗 Base URL: {extractor.base_url}")
        print(f"📊 Stats initialized: {bool(extractor.stats)}")
        
        return True
        
    except Exception as e:
        print(f"❌ API key validation failed: {e}")
        return False


def test_schema_compliance():
    """Test v2.0 schema compliance"""
    print("\n🧪 Testing v2.0 Schema Compliance")
    print("=" * 50)
    
    try:
        from backend.data.videos.schema_v2 import VIDEO_SCHEMA_V2
        
        print(f"📋 Schema loaded with {len(VIDEO_SCHEMA_V2)} columns")
        
        # Verify critical columns are present
        critical_columns = [
            'VideoID', 'Title', 'Channel', 'UploadDate', 'RelevanceScore', 
            'TrustLevel', 'Transcript_EN', 'Transcript_TE', 
            'SentimentScore_EN', 'SentimentScore_TE', 'DataHealth'
        ]
        
        missing_columns = [col for col in critical_columns if col not in VIDEO_SCHEMA_V2]
        
        if missing_columns:
            print(f"❌ Missing critical columns: {missing_columns}")
            return False
        
        print(f"✅ All critical bilingual columns present")
        
        # Show bilingual columns
        bilingual_columns = [col for col in VIDEO_SCHEMA_V2 if '_EN' in col or '_TE' in col]
        print(f"🌐 Bilingual columns ({len(bilingual_columns)}):")
        for col in bilingual_columns:
            lang = "Telugu" if "_TE" in col else "English"
            print(f"   📝 {col} ({lang})")
        
        return True
        
    except ImportError as e:
        print(f"❌ Schema import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False


def run_comprehensive_tests():
    """Run all validation tests"""
    print("🚀 ENHANCED TELUGU EXTRACTOR - COMPREHENSIVE TESTING")
    print("=" * 70)
    print("🎯 Testing bilingual precision extraction system")
    print(f"⏰ Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Schema Compliance", test_schema_compliance),
        ("Telugu Keywords", test_keyword_system),
        ("Relevance Scoring", test_relevance_scoring),
        ("API Key Handling", test_api_key_validation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Enhanced extractor ready for production!")
        return True
    else:
        print("⚠️ Some tests failed. Please review before production use.")
        return False


def main():
    """Main test execution"""
    success = run_comprehensive_tests()
    
    if success:
        print("\n✅ Enhanced Telugu Extractor validation complete!")
        print("🚀 Ready to run with your YouTube API key!")
        print("\n💡 Usage:")
        print("   export YOUTUBE_API_KEY='your_api_key_here'")
        print("   python scripts/enhanced_telugu_extractor.py")
        return 0
    else:
        print("\n❌ Validation failed. Please fix issues before proceeding.")
        return 1


if __name__ == "__main__":
    exit(main()) 