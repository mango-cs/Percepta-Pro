#!/usr/bin/env python3
"""
Test Script for Sridhar Rao YouTube Extractor
============================================

Quick test to verify setup without using API quota.
"""

import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import pandas as pd
        import requests
        from data.videos.schema_v2 import VIDEO_SCHEMA_V2
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_api_key():
    """Test if API key is available"""
    api_key = os.getenv('YOUTUBE_API_KEY')
    if api_key:
        print("✅ YouTube API key found")
        print(f"   Key length: {len(api_key)} characters")
        return True
    else:
        print("❌ YouTube API key not found")
        print("   Set YOUTUBE_API_KEY environment variable")
        return False

def test_directories():
    """Test if required directories exist"""
    required_dirs = [
        "backend/data/videos",
        "scripts/logs"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"⚠️  Creating directory: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
    
    return True

def test_extractor_class():
    """Test if the extractor class can be instantiated"""
    try:
        from sridhar_rao_extractor import SridharRaoExtractor
        
        # Test without API key first
        try:
            extractor = SridharRaoExtractor()
            print("✅ Extractor class initialized successfully")
            
            # Test keywords
            keywords = extractor.get_priority_keywords()
            print(f"✅ Keywords loaded: {len(keywords)} search terms")
            
            # Test channels
            channels = extractor.get_trusted_channels()
            print(f"✅ Trusted channels loaded: {len(channels)} channels")
            
            return True
            
        except ValueError as e:
            if "API key not found" in str(e):
                print("⚠️  Extractor requires API key (expected)")
                return True
            else:
                print(f"❌ Extractor error: {e}")
                return False
                
    except ImportError as e:
        print(f"❌ Cannot import extractor: {e}")
        return False

def test_schema_compatibility():
    """Test schema compatibility"""
    try:
        from data.videos.schema_v2 import VIDEO_SCHEMA_V2
        
        print(f"✅ Schema loaded: {len(VIDEO_SCHEMA_V2)} columns")
        
        # Check for key columns
        required_columns = [
            'VideoID', 'Title', 'Channel', 'RelevanceScore', 
            'TrustLevel', 'ProcessingStatus'
        ]
        
        missing = [col for col in required_columns if col not in VIDEO_SCHEMA_V2]
        if missing:
            print(f"❌ Missing columns: {missing}")
            return False
        
        print("✅ All required columns present in schema")
        return True
        
    except Exception as e:
        print(f"❌ Schema error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Sridhar Rao YouTube Extractor Setup")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("API Key Setup", test_api_key),
        ("Directory Structure", test_directories),
        ("Extractor Class", test_extractor_class),
        ("Schema Compatibility", test_schema_compatibility)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Ready to run extraction.")
        print("   Run: python scripts/sridhar_rao_extractor.py")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
        if not results[1][1]:  # API key test failed
            print("   Most important: Set your YOUTUBE_API_KEY environment variable")
    
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    exit(main()) 