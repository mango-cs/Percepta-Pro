"""
Enhanced Theme Provider System for Percepta Pro v2.0.1
Manages theme loading, switching, and provides theme data with full CSS generation
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any, Optional

class ThemeProvider:
    """Enhanced theme management system for Percepta Pro"""
    
    # Available themes registry
    AVAILABLE_THEMES = {
        "crimzon-dark": "Crimzon Dark",
        "red-crimson": "Red Crimson",
        "cyberpunk": "Cyberpunk",
        "tron": "Tron"
    }
    
    def __init__(self, themes_dir: str = "src/themes"):
        """
        Initialize theme provider
        
        Args:
            themes_dir: Directory containing theme JSON files
        """
        self.themes_dir = Path(themes_dir)
        self._themes_cache: Dict[str, Dict[str, Any]] = {}
        
    def load_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """
        Load and cache a theme by name
        
        Args:
            theme_name: Name of theme to load (without .json extension)
            
        Returns:
            Theme dictionary or None if loading fails
        """
        # Check cache first
        if theme_name in self._themes_cache:
            return self._themes_cache[theme_name]
            
        theme_file = self.themes_dir / f"{theme_name}.json"
        
        if not theme_file.exists():
            st.warning(f"Theme file not found: {theme_file}")
            return None
            
        try:
            with open(theme_file, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
                
            # Validate basic theme structure
            required_keys = ['name', 'colors', 'spacing', 'radius', 'shadows']
            for key in required_keys:
                if key not in theme_data:
                    st.error(f"Invalid theme '{theme_name}': missing '{key}' key")
                    return None
                    
            # Cache and return theme
            self._themes_cache[theme_name] = theme_data
            return theme_data
            
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON in theme '{theme_name}': {e}")
            return None
        except Exception as e:
            st.error(f"Error loading theme '{theme_name}': {e}")
            return None
    
    def get_current_theme_name(self) -> str:
        """Get the current active theme name"""
        return st.session_state.get('current_theme', 'crimzon-dark')
    
    def set_current_theme(self, theme_name: str) -> bool:
        """
        Set the current active theme
        
        Args:
            theme_name: Name of theme to activate
            
        Returns:
            True if theme was set successfully, False otherwise
        """
        theme = self.load_theme(theme_name)
        if theme:
            st.session_state['current_theme'] = theme_name
            return True
        return False
    
    def get_current_theme(self) -> Dict[str, Any]:
        """
        Get the current active theme data
        
        Returns:
            Current theme dictionary
        """
        theme_name = self.get_current_theme_name()
        theme = self.load_theme(theme_name)
        
        if theme:
            return theme
        
        # Fallback to crimzon-dark
        fallback_theme = self.load_theme('crimzon-dark')
        if fallback_theme:
            return fallback_theme
        
        # Ultimate fallback - minimal theme
        return {
            "name": "Fallback Theme",
            "description": "Emergency fallback theme",
            "type": "dark",
            "colors": {
                "primary": "#FF4757",
                "secondary": "#FF6348",
                "accent": "#22C55E",
                "warning": "#FFA502",
                "error": "#FF4757",
                "bg_main": "#1A1A1A",
                "bg_card": "#2D2D2D",
                "bg_interactive": "#3A3A3A",
                "bg_hover": "#4A4A4A",
                "text_primary": "#FFFFFF",
                "text_secondary": "#CCCCCC",
                "text_muted": "#9CA3AF",
                "text_inverse": "#1F2937",
                "border_color": "#404040",
                "border_hover": "#505050",
                "border_focus": "#FF4757"
            },
            "spacing": {"xs": "4px", "sm": "8px", "md": "12px", "lg": "16px", "xl": "20px", "xxl": "24px", "xxxl": "32px"},
            "radius": {"sm": "4px", "md": "8px", "lg": "12px", "xl": "16px"},
            "shadows": {"card": "0 4px 16px rgba(0, 0, 0, 0.2)", "hover": "0 4px 12px rgba(0, 0, 0, 0.4)", "button": "0 2px 8px rgba(0, 0, 0, 0.3)", "focus": "0 0 0 3px rgba(0, 0, 0, 0.1)"},
            "gradients": {"primary": "linear-gradient(135deg, #FF4757 0%, #FF6348 100%)", "secondary": "linear-gradient(135deg, #FF6348 0%, #FFA502 100%)", "accent": "linear-gradient(135deg, #22C55E 0%, #16A34A 100%)"}
        }
    
    def generate_css_variables(self) -> str:
        """
        Generate CSS variables for the current theme
        
        Returns:
            CSS variables string
        """
        theme = self.get_current_theme()
        
        css_vars = []
        
        # Colors
        colors = theme.get('colors', {})
        css_vars.extend([
            f"--primary-color: {colors.get('primary', '#FF4757')};",
            f"--secondary-color: {colors.get('secondary', '#FF6348')};",
            f"--accent-color: {colors.get('accent', '#22C55E')};",
            f"--warning-color: {colors.get('warning', '#FFA502')};",
            f"--error-color: {colors.get('error', '#FF4757')};",
            f"--bg-main: {colors.get('bg_main', '#1A1A1A')};",
            f"--bg-card: {colors.get('bg_card', '#2D2D2D')};",
            f"--bg-interactive: {colors.get('bg_interactive', '#3A3A3A')};",
            f"--bg-hover: {colors.get('bg_hover', '#4A4A4A')};",
            f"--text-primary: {colors.get('text_primary', '#FFFFFF')};",
            f"--text-secondary: {colors.get('text_secondary', '#CCCCCC')};",
            f"--text-muted: {colors.get('text_muted', '#9CA3AF')};",
            f"--text-inverse: {colors.get('text_inverse', '#1F2937')};",
            f"--border-color: {colors.get('border_color', '#404040')};",
            f"--border-hover: {colors.get('border_hover', '#505050')};",
            f"--border-focus: {colors.get('border_focus', '#FF4757')};",
        ])
        
        # Legacy color mappings for backward compatibility
        css_vars.extend([
            f"--crimzon-red: {colors.get('primary', '#FF4757')};",
            f"--crimzon-orange: {colors.get('secondary', '#FF6348')};",
            f"--crimzon-amber: {colors.get('warning', '#FFA502')};",
            f"--accent-green: {colors.get('accent', '#22C55E')};",
        ])
        
        # Spacing
        spacing = theme.get('spacing', {})
        for size_name, size_value in spacing.items():
            css_vars.append(f"--spacing-{size_name}: {size_value};")
        
        # Radius
        radius = theme.get('radius', {})
        for radius_name, radius_value in radius.items():
            css_vars.append(f"--radius-{radius_name}: {radius_value};")
        
        # Shadows
        shadows = theme.get('shadows', {})
        for shadow_name, shadow_value in shadows.items():
            css_vars.append(f"--shadow-{shadow_name}: {shadow_value};")
        
        # Gradients
        gradients = theme.get('gradients', {})
        for gradient_name, gradient_value in gradients.items():
            css_vars.append(f"--gradient-{gradient_name}: {gradient_value};")
        
        css_variables = "\n        ".join(css_vars)
        
        return f"""
    :root {{
        {css_variables}
    }}"""
    
    def get_theme_selector_options(self) -> Dict[str, str]:
        """
        Get available themes for UI selection
        
        Returns:
            Dictionary mapping display names to theme identifiers
        """
        options = {}
        
        for theme_id, display_name in self.AVAILABLE_THEMES.items():
            theme = self.load_theme(theme_id)
            if theme:
                options[display_name] = theme_id
        
        return options
    
    def get_theme_info(self, theme_name: str) -> Dict[str, Any]:
        """
        Get theme information for display
        
        Args:
            theme_name: Name of theme
            
        Returns:
            Dictionary with theme info
        """
        theme = self.load_theme(theme_name)
        if theme:
            return {
                'name': theme.get('name', theme_name),
                'description': theme.get('description', 'No description available'),
                'type': theme.get('type', 'unknown'),
                'author': theme.get('author', 'Unknown'),
                'version': theme.get('version', '1.0.0')
            }
        return {}

# Global theme provider instance
_theme_provider = None

def get_theme_provider() -> ThemeProvider:
    """Get the global theme provider instance"""
    global _theme_provider
    if _theme_provider is None:
        _theme_provider = ThemeProvider()
    return _theme_provider

def get_current_theme() -> Dict[str, Any]:
    """Convenience function to get current theme"""
    return get_theme_provider().get_current_theme()

def generate_theme_css() -> str:
    """Convenience function to generate theme CSS variables"""
    return get_theme_provider().generate_css_variables()

def switch_theme(theme_name: str) -> bool:
    """Convenience function to switch themes"""
    return get_theme_provider().set_current_theme(theme_name) 