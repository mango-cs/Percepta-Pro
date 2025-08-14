"""
Base Theme Interface and Validation System for Percepta Pro v2.0
"""

from typing import Dict, Any
import json

class ThemeValidator:
    """Validates theme JSON structure"""
    
    REQUIRED_SECTIONS = [
        'designSystem.primaryColors',
        'designSystem.elementStyling.layout',
        'designSystem.elementStyling.navigation',
        'designSystem.elementStyling.cards',
        'designSystem.elementStyling.typography'
    ]
    
    @classmethod
    def validate_theme(cls, theme_data: Dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate theme structure"""
        errors = []
        
        if 'designSystem' not in theme_data:
            errors.append("Missing 'designSystem' root key")
            return False, errors
            
        return len(errors) == 0, errors

class BaseTheme:
    """Base theme class providing standardized access to theme properties"""
    
    def __init__(self, theme_data: Dict[str, Any]):
        """Initialize theme with validated data"""
        is_valid, errors = ThemeValidator.validate_theme(theme_data)
        if not is_valid:
            raise ValueError(f"Invalid theme data: {', '.join(errors)}")
            
        self.data = theme_data
        self.design_system = theme_data['designSystem']
        
    @property
    def colors(self) -> Dict[str, str]:
        """Get all primary colors"""
        return self.design_system['primaryColors']
        
    @property
    def layout(self) -> Dict[str, Any]:
        """Get layout specifications"""
        return self.design_system['elementStyling']['layout']
    
    @property
    def navigation(self) -> Dict[str, Any]:
        """Get navigation specifications"""
        return self.design_system['elementStyling']['navigation']
    
    @property
    def cards(self) -> Dict[str, Any]:
        """Get card specifications"""
        return self.design_system['elementStyling']['cards']
    
    @property
    def typography(self) -> Dict[str, Any]:
        """Get typography specifications"""
        return self.design_system['elementStyling']['typography']
    
    @property
    def buttons(self) -> Dict[str, Any]:
        """Get button specifications"""
        return self.design_system['elementStyling']['buttons']
    
    @property
    def name(self) -> str:
        """Get theme name"""
        return self.design_system.get('name', 'Unnamed Theme')
        
    @property
    def theme_type(self) -> str:
        """Get theme type (dark/light)"""
        return self.design_system.get('theme', 'dark')
        
    # Color Properties
    @property
    def crimzon_red(self) -> str:
        return self.colors['crimzonRed']
        
    @property
    def crimzon_orange(self) -> str:
        return self.colors['crimzonOrange']
        
    @property
    def crimzon_amber(self) -> str:
        return self.colors['crimzonAmber']
        
    @property
    def accent_green(self) -> str:
        return self.colors['accentGreen']
        
    @property
    def background_dark(self) -> str:
        return self.colors['backgroundDark']
        
    @property
    def surface_dark(self) -> str:
        return self.colors['surfaceDark']
        
    @property
    def surface_light(self) -> str:
        return self.colors['surfaceLight']
    
    # Spacing Properties
    @property
    def spacing(self) -> Dict[str, str]:
        """Get spacing scale"""
        return self.design_system['spacing']
    
    # Shadow Properties
    @property
    def shadows(self) -> Dict[str, str]:
        """Get shadow specifications"""
        return self.design_system['shadows']
    
    # Helper Methods
    def get_css_variable(self, path: str, default: str = "") -> str:
        """
        Get a nested value from theme data using dot notation
        
        Args:
            path: Dot-separated path (e.g., 'cards.primaryMetric.background')
            default: Default value if path not found
            
        Returns:
            Value at path or default
        """
        keys = path.split('.')
        current = self.design_system['elementStyling']
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
                
        return current if isinstance(current, str) else default
    
    def to_css_variables(self) -> str:
        """
        Generate CSS custom properties from theme data
        
        Returns:
            CSS string with custom properties
        """
        css_vars = []
        
        # Primary colors
        for color_name, color_value in self.colors.items():
            css_name = color_name.replace('crimzon', 'crimzon-').lower()
            css_vars.append(f"--{css_name}: {color_value};")
        
        # Spacing
        for size_name, size_value in self.spacing.items():
            css_vars.append(f"--spacing-{size_name}: {size_value};")
        
        # Shadows
        for shadow_name, shadow_value in self.shadows.items():
            css_vars.append(f"--shadow-{shadow_name}: {shadow_value};")
        
        return "\n        ".join(css_vars) 