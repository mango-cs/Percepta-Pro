# 🎨 PERCEPTA PRO - UI REFERENCE GUIDE

**Version:** 2.0.1  
**Date:** December 30, 2024  
**Purpose:** Comprehensive UI modification and theme system reference  
**Target:** Development and design consistency  

---

## 🎯 **OVERVIEW**

This document serves as the **definitive reference** for all UI modifications, theme implementations, and design system consistency in Percepta Pro. Use this guide to:
- Make consistent UI changes
- Implement new themes
- Understand the design system architecture
- Maintain visual hierarchy and branding

---

## 🏗️ **DESIGN SYSTEM ARCHITECTURE**

### **Theme System Structure**
```
src/themes/
├── base_theme.py          # Base theme class and structure
├── theme_provider.py      # Theme management and switching
├── crimzon-dark.json      # Original Crimzon theme
├── premium-light.json     # Premium white/blue/green theme
└── themes.json           # Theme registry and metadata
```

### **CSS Integration Points**
```python
# Main CSS injection point
def load_custom_css():
    # Location: reputation_dashboard.py, line ~71
    # Contains all theme variables and styling rules
    
# Theme variable system
:root {
    --primary-color: {theme.primary}
    --secondary-color: {theme.secondary}
    --accent-color: {theme.accent}
    # ... all other variables
}
```

---

## 🎨 **COLOR SYSTEM REFERENCE**

### **Crimzon Dark Theme (Default)**
```css
/* Primary Colors */
--primary-color: #FF4757      /* Crimzon Red */
--secondary-color: #FF6348    /* Crimzon Orange */
--accent-color: #22C55E       /* Success Green */
--warning-color: #FFA502      /* Warning Amber */

/* Background Colors */
--bg-main: #1A1A1A           /* Main background */
--bg-card: #2D2D2D           /* Card backgrounds */
--bg-interactive: #3A3A3A     /* Interactive elements */

/* Text Colors */
--text-primary: #FFFFFF       /* Primary text */
--text-secondary: #CCCCCC     /* Secondary text */
--text-muted: #9CA3AF        /* Muted text */

/* Border Colors */
--border-color: #404040      /* Default borders */
--border-hover: #505050      /* Hover state borders */
```

### **Premium Light Theme (New)**
```css
/* Primary Colors */
--primary-color: #2563EB      /* Professional Blue */
--secondary-color: #059669    /* Success Green */
--accent-color: #DC2626       /* Alert Red */
--warning-color: #D97706      /* Warning Orange */

/* Background Colors */
--bg-main: #FFFFFF           /* Clean white main */
--bg-card: #F8FAFC           /* Light gray cards */
--bg-interactive: #E2E8F0     /* Interactive backgrounds */

/* Text Colors */
--text-primary: #1F2937       /* Dark gray text */
--text-secondary: #4B5563     /* Medium gray text */
--text-muted: #6B7280        /* Light gray text */

/* Border Colors */
--border-color: #E5E7EB      /* Light borders */
--border-hover: #D1D5DB      /* Hover borders */
```

---

## 📐 **SPACING SYSTEM**

### **Spacing Scale (CSS Variables)**
```css
--spacing-xs: 4px      /* Minimal spacing */
--spacing-sm: 8px      /* Small spacing */
--spacing-md: 12px     /* Medium spacing */
--spacing-lg: 16px     /* Large spacing */
--spacing-xl: 20px     /* Extra large spacing */
--spacing-xxl: 24px    /* Double extra large */
--spacing-xxxl: 32px   /* Triple extra large */
```

### **Component Spacing Standards**
```css
/* Navigation Buttons */
padding: 12px 16px;
margin-bottom: 8px;

/* Metric Cards */
padding: 24px;
margin-bottom: 16px;

/* Page Headers */
margin-bottom: 32px;

/* Sections */
margin-bottom: 24px;
```

---

## 🔤 **TYPOGRAPHY SYSTEM**

### **Font Hierarchy**
```css
/* Page Titles */
.page-title {
    font-size: 32px;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: var(--spacing-sm);
}

/* Page Subtitles */
.page-subtitle {
    font-size: 18px;
    font-weight: 600;
    line-height: 1.4;
    margin-bottom: var(--spacing-xxxl);
}

/* Section Headers */
.section-header {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: var(--spacing-lg);
}

/* Metric Values */
.metric-value {
    font-size: 32px;
    font-weight: 700;
    line-height: 1;
}

/* Metric Labels */
.metric-label {
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}
```

---

## 🧩 **COMPONENT REFERENCE**

### **1. Metric Cards**
```python
# Function: create_metric_card()
# Location: reputation_dashboard.py, line ~537
# Purpose: Standardized KPI display cards

def create_metric_card(title, value, change=None, change_type="neutral", icon="📊"):
    return f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-icon">{icon}</span>
            <span class="metric-label">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
        {change_html}
    </div>
    """
```

**CSS Classes:**
```css
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-lg);
}
```

### **2. Navigation Buttons**
```css
.stSidebar .stButton > button {
    background: transparent;
    color: var(--text-muted);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    margin-bottom: var(--spacing-sm);
    transition: all 0.2s ease;
}

.stSidebar .stButton > button:hover {
    background: var(--bg-interactive);
    color: var(--text-primary);
    border-color: var(--border-hover);
}
```

### **3. Page Headers**
```python
# Standard page header format
st.markdown('<h1 class="page-title">📊 Page Title</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Page description and context</p>', unsafe_allow_html=True)
```

### **4. Status Badges**
```css
.status-badge {
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}

.status-positive {
    background: rgba(34, 197, 94, 0.2);
    color: var(--accent-color);
    border: 1px solid var(--accent-color);
}
```

---

## 🎛️ **THEME IMPLEMENTATION GUIDE**

### **1. Creating a New Theme**

**Step 1: Create Theme JSON**
```json
{
    "name": "Theme Name",
    "description": "Theme description",
    "type": "light|dark",
    "colors": {
        "primary": "#HEX",
        "secondary": "#HEX",
        "accent": "#HEX",
        "warning": "#HEX",
        "bg_main": "#HEX",
        "bg_card": "#HEX",
        "bg_interactive": "#HEX",
        "text_primary": "#HEX",
        "text_secondary": "#HEX",
        "text_muted": "#HEX",
        "border_color": "#HEX",
        "border_hover": "#HEX"
    },
    "spacing": {
        "xs": "4px",
        "sm": "8px",
        "md": "12px",
        "lg": "16px",
        "xl": "20px",
        "xxl": "24px",
        "xxxl": "32px"
    },
    "radius": {
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "xl": "16px"
    }
}
```

**Step 2: Register in Theme Provider**
```python
# Add to theme_provider.py
AVAILABLE_THEMES = {
    "crimzon-dark": "Crimzon Dark",
    "premium-light": "Premium Light",
    "your-theme": "Your Theme Name"
}
```

### **2. Theme Switching Logic**
```python
# Location: theme_provider.py
def apply_theme(theme_name):
    """Apply theme to application"""
    theme_config = load_theme(theme_name)
    css_variables = generate_css_variables(theme_config)
    st.markdown(f"<style>{css_variables}</style>", unsafe_allow_html=True)
```

---

## 🔧 **MODIFICATION GUIDELINES**

### **Making UI Changes**

**1. Color Changes**
- Always use CSS variables, never hardcoded colors
- Update theme JSON files, not direct CSS
- Test changes across all themes

**2. Spacing Changes**
- Use predefined spacing variables
- Maintain consistent rhythm
- Consider responsive behavior

**3. Typography Changes**
- Follow established hierarchy
- Maintain readability standards
- Test across different screen sizes

**4. Component Changes**
- Update component functions, not individual instances
- Maintain accessibility standards
- Document changes in this guide

### **Testing Checklist**
- [ ] Works across all themes
- [ ] Maintains responsive design
- [ ] Follows accessibility standards
- [ ] Consistent with design system
- [ ] No hardcoded colors/spacing
- [ ] Cross-browser compatibility

---

## 📍 **KEY LOCATIONS IN CODEBASE**

### **CSS and Styling**
```
reputation_dashboard.py
├── Line 71-530: load_custom_css() function
├── Contains all CSS variables and styling rules
└── Theme integration point

src/themes/
├── base_theme.py: Theme structure definitions
├── theme_provider.py: Theme management logic
└── *.json: Theme configuration files
```

### **Component Functions**
```
reputation_dashboard.py
├── Line 537: create_metric_card()
├── Line 803: create_sidebar()
├── Line 1230: create_top_mode_selector()
└── Individual page functions (show_*_page)
```

### **Page Header Patterns**
```python
# Standard implementation across all pages
st.markdown('<h1 class="page-title">ICON Title</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Description</p>', unsafe_allow_html=True)
```

---

## 🎨 **DESIGN TOKENS**

### **Border Radius**
```css
--radius-sm: 4px    /* Small elements */
--radius-md: 8px    /* Buttons, inputs */
--radius-lg: 12px   /* Cards, containers */
--radius-xl: 16px   /* Large containers */
```

### **Shadows**
```css
--shadow-card: 0 2px 8px rgba(0, 0, 0, 0.1);
--shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.15);
--shadow-button: 0 1px 3px rgba(0, 0, 0, 0.1);
```

### **Transitions**
```css
--transition-fast: 0.15s ease;
--transition-normal: 0.2s ease;
--transition-slow: 0.3s ease;
```

---

## 🔍 **DEBUGGING UI ISSUES**

### **Common Issues and Solutions**

**1. Color Not Applying**
- Check if CSS variable is defined
- Verify theme JSON structure
- Ensure theme is properly loaded

**2. Spacing Inconsistencies**
- Use spacing variables instead of hardcoded values
- Check for !important overrides
- Verify responsive behavior

**3. Theme Not Switching**
- Check session state management
- Verify theme provider logic
- Ensure CSS is being regenerated

### **Debug Tools**
```python
# Add to debug theme loading
st.write(f"Current theme: {st.session_state.get('theme', 'crimzon-dark')}")
st.write(f"Available themes: {get_available_themes()}")
```

---

## 📝 **MAINTENANCE GUIDELINES**

### **When Adding New Components**
1. Define component in separate function
2. Use CSS variables for all styling
3. Add to this reference guide
4. Test across all themes
5. Document usage examples

### **When Modifying Existing Components**
1. Check all usage locations
2. Maintain backward compatibility
3. Update this reference guide
4. Test visual consistency
5. Update component documentation

### **Theme Maintenance**
1. Keep theme JSONs synchronized
2. Test new components with all themes
3. Maintain color contrast ratios
4. Document theme-specific considerations

---

## 🎯 **QUICK REFERENCE CHECKLIST**

### **Before Making UI Changes**
- [ ] Read this reference guide
- [ ] Identify affected components
- [ ] Check theme compatibility
- [ ] Plan responsive behavior

### **During Implementation**
- [ ] Use CSS variables only
- [ ] Follow spacing standards
- [ ] Maintain typography hierarchy
- [ ] Test with multiple themes

### **After Implementation**
- [ ] Test all themes
- [ ] Verify responsive design
- [ ] Update documentation
- [ ] Check accessibility

---

**🎨 This guide serves as the single source of truth for all UI modifications in Percepta Pro**

**Always refer to this document before making styling changes to ensure consistency and maintainability.** 