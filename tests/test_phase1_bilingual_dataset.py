#!/usr/bin/env python3
"""
Enhanced Bilingual Phase 1 Dataset Validator for Percepta Pro
============================================================

Validates that the comprehensive bilingual dataset produced by
scripts/enhanced_telugu_extractor.py meets all quality standards
for Telugu + English content analysis.

Author: Percepta Pro v2.0 - Enhanced Bilingual System
"""

import pytest
import pandas as pd
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from data.videos.schema_v2 import VIDEO_SCHEMA_V2
except ImportError:
    print("❌ Error: Could not import schema_v2")
    sys.exit(1)


class BilingualDatasetValidator:
    """Enhanced validator for bilingual Telugu+English datasets"""
    
    def __init__(self, csv_path: str, max_fail: int = 20):
        self.csv_path = csv_path
        self.max_fail = max_fail
        self.errors = {}
        self.df = None
        self.results = {}
        
        # Load expected configuration
        self.expected_channels = {
            # Tier 1: Highest Trust Telugu News
            "ABN Telugu": 10, "TV5 News": 10, "Zee Telugu News": 10, 
            "NTV Telugu": 10, "ETV Telangana": 10,
            # Tier 2: High Trust Regional  
            "Raj News Telugu": 9, "CVR News Telugu": 9, "CVR News": 9,
            "T News Telugu": 8, "V6 News Telugu": 8, "Mahaa News": 8,
            # Tier 3: Medium-High Trust
            "BRK News": 7, "BIG TV Live": 7, "Prime9 News": 7
        }
        
        # Expected Telugu terms for content validation
        self.telugu_indicators = [
            "శ్రీధర్", "సంధ్య", "కన్వెన్షన్", "రావు", "చేతబడి", "కబ్జా",
            "మోసం", "అరెస్ట్", "హైడ్రా", "గచ్చిబౌలి", "ఆడియో లీక్"
        ]
    
    def load_dataset(self) -> bool:
        """Load and validate basic dataset structure"""
        try:
            if not os.path.exists(self.csv_path):
                self.errors['file_missing'] = f"Dataset file not found: {self.csv_path}"
                return False
            
            self.df = pd.read_csv(self.csv_path)
            
            if self.df.empty:
                self.errors['empty_dataset'] = "Dataset is empty"
                return False
            
            return True
            
        except Exception as e:
            self.errors['load_error'] = f"Failed to load dataset: {e}"
            return False
    
    def test_schema_compliance(self) -> bool:
        """Test 1: Complete v2.0 schema compliance"""
        print("🧪 Testing Schema Compliance...")
        
        # Check column count
        if len(self.df.columns) != len(VIDEO_SCHEMA_V2):
            self.errors['schema_column_count'] = f"Expected {len(VIDEO_SCHEMA_V2)} columns, got {len(self.df.columns)}"
            return False
        
        # Check column names and order
        missing_cols = []
        wrong_order = []
        
        for i, expected_col in enumerate(VIDEO_SCHEMA_V2):
            if i >= len(self.df.columns):
                missing_cols.append(expected_col)
            elif self.df.columns[i] != expected_col:
                wrong_order.append(f"Position {i}: expected '{expected_col}', got '{self.df.columns[i]}'")
        
        if missing_cols:
            self.errors['schema_missing_columns'] = missing_cols
            return False
        
        if wrong_order:
            self.errors['schema_wrong_order'] = wrong_order
            return False
        
        # Check bilingual columns specifically
        bilingual_cols = [col for col in VIDEO_SCHEMA_V2 if '_EN' in col or '_TE' in col]
        if len(bilingual_cols) != 10:
            self.errors['schema_bilingual_incomplete'] = f"Expected 10 bilingual columns, found {len(bilingual_cols)}"
            return False
        
        self.results['schema_compliance'] = True
        print("✅ Schema compliance: PASSED")
        return True
    
    def test_row_count_sanity(self, min_rows: int = 50, max_rows: int = 1200) -> bool:
        """Test 2: Reasonable dataset size"""
        print("🧪 Testing Row Count Sanity...")
        
        row_count = len(self.df)
        
        if row_count < min_rows:
            self.errors['row_count_too_low'] = f"Only {row_count} rows, expected at least {min_rows}"
            return False
        
        if row_count > max_rows:
            self.errors['row_count_too_high'] = f"{row_count} rows exceeds maximum {max_rows}"
            return False
        
        self.results['row_count'] = row_count
        print(f"✅ Row count sanity: {row_count} rows (within {min_rows}-{max_rows})")
        return True
    
    def test_duplicate_check(self) -> bool:
        """Test 3: No duplicate VideoIDs"""
        print("🧪 Testing Duplicate VideoIDs...")
        
        duplicates = self.df[self.df.duplicated(subset=['VideoID'], keep=False)]
        
        if not duplicates.empty:
            duplicate_count = len(duplicates)
            self.errors['duplicate_videoids'] = f"Found {duplicate_count} duplicate VideoIDs"
            
            # Save duplicate errors
            self._save_error_csv('duplicate_errors.csv', duplicates)
            return False
        
        self.results['duplicates'] = 0
        print("✅ Duplicate check: 0 duplicates found")
        return True
    
    def test_bilingual_coverage(self) -> bool:
        """Test 4: ENHANCED - Bilingual content coverage"""
        print("🧪 Testing Bilingual Coverage...")
        
        telugu_content_count = 0
        english_content_count = 0
        
        for idx, row in self.df.iterrows():
            title = str(row['Title']).lower()
            
            # Check for Telugu content
            if any(term in title for term in self.telugu_indicators):
                telugu_content_count += 1
            
            # Check for English content
            if any(term in title for term in ['sridhar rao', 'sandhya convention', 'black magic']):
                english_content_count += 1
        
        total_rows = len(self.df)
        telugu_percentage = (telugu_content_count / total_rows) * 100
        english_percentage = (english_content_count / total_rows) * 100
        
        # Validate coverage ratios
        if telugu_percentage < 30:  # At least 30% Telugu content
            self.errors['low_telugu_coverage'] = f"Telugu content only {telugu_percentage:.1f}% (expected >30%)"
            return False
        
        if english_percentage < 15:  # At least 15% English content
            self.errors['low_english_coverage'] = f"English content only {english_percentage:.1f}% (expected >15%)"
            return False
        
        self.results['bilingual_coverage'] = {
            'telugu_content_percentage': round(telugu_percentage, 1),
            'english_content_percentage': round(english_percentage, 1)
        }
        
        print(f"✅ Bilingual coverage: Telugu {telugu_percentage:.1f}%, English {english_percentage:.1f}%")
        return True
    
    def test_relevance_trust_ranges(self) -> bool:
        """Test 5: Relevance and Trust value ranges"""
        print("🧪 Testing Relevance & Trust Ranges...")
        
        range_errors = []
        
        for idx, row in self.df.iterrows():
            relevance = row['RelevanceScore']
            trust = row['TrustLevel']
            
            # Check RelevanceScore range
            if not (0 <= relevance <= 100):
                range_errors.append({
                    'VideoID': row['VideoID'],
                    'Error': f"RelevanceScore {relevance} out of range (0-100)",
                    'Title': row['Title'][:50]
                })
            
            # Check TrustLevel values
            if trust not in [0, 1]:
                range_errors.append({
                    'VideoID': row['VideoID'],
                    'Error': f"TrustLevel {trust} not in [0, 1]",
                    'Channel': row['Channel']
                })
        
        if range_errors:
            self.errors['range_errors'] = f"Found {len(range_errors)} range errors"
            self._save_error_csv('range_errors.csv', pd.DataFrame(range_errors))
            return False
        
        # Check relevance distribution
        high_relevance = len(self.df[self.df['RelevanceScore'] >= 50])
        avg_relevance = self.df['RelevanceScore'].mean()
        
        self.results['relevance_stats'] = {
            'high_relevance_count': high_relevance,
            'average_relevance': round(avg_relevance, 2)
        }
        
        print(f"✅ Relevance & Trust ranges: Valid (avg relevance: {avg_relevance:.1f})")
        return True
    
    def test_channel_quality_distribution(self) -> bool:
        """Test 6: ENHANCED - Channel quality and trust distribution"""
        print("🧪 Testing Channel Quality Distribution...")
        
        channel_counts = self.df['Channel'].value_counts()
        trusted_channels = 0
        total_from_trusted = 0
        
        for channel, count in channel_counts.items():
            if channel in self.expected_channels:
                trusted_channels += 1
                total_from_trusted += count
        
        trusted_percentage = (total_from_trusted / len(self.df)) * 100
        
        if trusted_percentage < 40:  # At least 40% from trusted sources
            self.errors['low_trusted_sources'] = f"Only {trusted_percentage:.1f}% from trusted sources (expected >40%)"
            return False
        
        # Check top channels
        top_channels = channel_counts.head(10)
        quality_channels = sum(1 for ch in top_channels.index if ch in self.expected_channels)
        
        self.results['channel_quality'] = {
            'trusted_percentage': round(trusted_percentage, 1),
            'quality_channels_in_top10': quality_channels,
            'total_channels': len(channel_counts)
        }
        
        print(f"✅ Channel quality: {trusted_percentage:.1f}% from trusted sources, {quality_channels}/10 top channels are quality")
        return True
    
    def _save_error_csv(self, filename: str, error_df: pd.DataFrame):
        """Save error details to CSV file"""
        error_dir = os.path.join(os.path.dirname(self.csv_path), '..', '..', 'tests', 'errors')
        os.makedirs(error_dir, exist_ok=True)
        
        error_path = os.path.join(error_dir, filename)
        error_df.to_csv(error_path, index=False)
        print(f"   📄 Error details saved to: {error_path}")
    
    def run_all_tests(self) -> bool:
        """Run complete validation suite"""
        print("🚀 ENHANCED BILINGUAL DATASET VALIDATOR")
        print("=" * 60)
        print(f"📊 Validating: {self.csv_path}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if not self.load_dataset():
            print("❌ Failed to load dataset")
            return False
        
        print(f"📋 Dataset loaded: {len(self.df)} rows, {len(self.df.columns)} columns")
        print()
        
        # Run core tests
        tests = [
            self.test_schema_compliance,
            self.test_row_count_sanity,
            self.test_duplicate_check,
            self.test_bilingual_coverage,
            self.test_relevance_trust_ranges,
            self.test_channel_quality_distribution
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")
                failed += 1
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        
        for error_type, error_msg in self.errors.items():
            print(f"❌ {error_type}: {error_msg}")
        
        print(f"\n🎯 Test Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED! Dataset is ready for Phase 2!")
            return True
        else:
            print(f"⚠️ {failed} test(s) failed. Check error files for details.")
            return False


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Enhanced Bilingual Dataset Validator')
    parser.add_argument('--csv', default='backend/data/videos/youtube_videos_comprehensive.csv', 
                       help='Path to CSV file to validate')
    parser.add_argument('--max-fail', type=int, default=20, 
                       help='Maximum failures to show per test')
    parser.add_argument('--min-rows', type=int, default=50, 
                       help='Minimum expected rows')
    parser.add_argument('--max-rows', type=int, default=1200, 
                       help='Maximum expected rows')
    
    args = parser.parse_args()
    
    validator = BilingualDatasetValidator(args.csv, args.max_fail)
    success = validator.run_all_tests()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())


# Pytest Integration
class TestPhase1Dataset:
    """Pytest integration for the bilingual dataset validator"""
    
    @pytest.fixture
    def validator(self):
        csv_path = 'backend/data/videos/youtube_videos_comprehensive.csv'
        validator = BilingualDatasetValidator(csv_path)
        validator.load_dataset()
        return validator
    
    def test_schema_compliance(self, validator):
        assert validator.test_schema_compliance()
    
    def test_row_count_sanity(self, validator):
        assert validator.test_row_count_sanity()
    
    def test_duplicate_check(self, validator):
        assert validator.test_duplicate_check()
    
    def test_bilingual_coverage(self, validator):
        assert validator.test_bilingual_coverage()
    
    def test_relevance_trust_ranges(self, validator):
        assert validator.test_relevance_trust_ranges()
    
    def test_channel_quality_distribution(self, validator):
        assert validator.test_channel_quality_distribution() 