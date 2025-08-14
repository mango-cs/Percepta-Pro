"""
Test Script for Percepta Pro Theme System
Verifies that the theme system loads and provides correct values
"""

import json
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append('..')
sys.path.append('../..')

try:
    from base_theme import BaseTheme, ThemeValidator
    from theme_provider import ThemeProvider, get_current_theme
    print("✅ Theme system imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_theme_loading():
    """Test loading the crimzon-dark theme"""
    print("\n🔧 Testing Theme Loading...")
    
    # Test direct JSON loading
    try:
        with open('crimzon-dark.json', 'r') as f:
            theme_data = json.load(f)
        print("✅ JSON file loaded successfully")
    except Exception as e:
        print(f"❌ JSON loading failed: {e}")
        return False
    
    # Test theme validation
    try:
        is_valid, errors = ThemeValidator.validate_theme(theme_data)
        if is_valid:
            print("✅ Theme validation passed")
        else:
            print(f"❌ Theme validation failed: {errors}")
            return False
    except Exception as e:
        print(f"❌ Theme validation error: {e}")
        return False
    
    # Test BaseTheme creation
    try:
        theme = BaseTheme(theme_data)
        print("✅ BaseTheme object created successfully")
        print(f"   - Theme name: {theme.name}")
        print(f"   - Theme type: {theme.theme_type}")
        print(f"   - Crimzon red: {theme.crimzon_red}")
        print(f"   - Background dark: {theme.background_dark}")
    except Exception as e:
        print(f"❌ BaseTheme creation failed: {e}")
        return False
    
    return True

def test_theme_provider():
    """Test the theme provider system"""
    print("\n🔄 Testing Theme Provider...")
    
    try:
        provider = ThemeProvider()
        print("✅ ThemeProvider created successfully")
        
        # Test theme discovery
        themes = provider.discover_themes()
        print(f"✅ Discovered themes: {list(themes.keys())}")
        
        # Test theme loading
        theme = provider.load_theme('crimzon-dark')
        if theme:
            print("✅ Crimzon-dark theme loaded successfully")
            print(f"   - Primary colors: {theme.colors}")
        else:
            print("❌ Failed to load crimzon-dark theme")
            return False
            
    except Exception as e:
        print(f"❌ Theme provider test failed: {e}")
        return False
    
    return True

def test_css_generation():
    """Test CSS generation from theme"""
    print("\n🎨 Testing CSS Generation...")
    
    try:
        provider = ThemeProvider()
        css = provider.generate_css()
        
        # Check if CSS contains expected variables
        expected_vars = [
            '--crimzon-red: #FF4757',
            '--crimzon-orange: #FF6348',
            '--accent-green: #2ED573',
            '--bg-main: #1A1A1A'
        ]
        
        all_found = True
        for var in expected_vars:
            if var in css:
                print(f"✅ Found: {var}")
            else:
                print(f"❌ Missing: {var}")
                all_found = False
        
        if all_found:
            print("✅ CSS generation test passed")
        else:
            print("❌ CSS generation test failed")
            return False
            
    except Exception as e:
        print(f"❌ CSS generation test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Percepta Pro Theme System Test Suite")
    print("=" * 50)
    
    tests = [
        test_theme_loading,
        test_theme_provider,
        test_css_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Theme system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 