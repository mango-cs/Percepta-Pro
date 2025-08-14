# Percepta Pro v2.0.2 🎯
## Advanced Reputation Intelligence Platform

![Percepta Pro](assets/images/percepta_logo.png)

Percepta Pro is a comprehensive reputation monitoring and intelligence platform built with Streamlit and Python. It provides real-time sentiment analysis, predictive analytics, and executive-grade reporting for reputation management.

## 🌟 Key Features

### **🔍 Intelligent Monitoring**
- **Real-time Tracking**: Monitor YouTube videos and comments continuously
- **Bilingual Language Support**: **NEW** - Toggle between English (translated) and Telugu (original) comments
- **Advanced Analytics**: 200+ videos and 1,500+ comments processed with AI enhancement

### **🧠 AI-Powered Intelligence**
- **Sentiment Analysis**: Advanced bilingual sentiment analysis (Telugu + English)
- **Predictive Analytics**: ML-powered reputation forecasting and trend analysis
- **Crisis Detection**: Real-time reputation threat monitoring with 98 critical alerts managed
- **Comment Language Toggle**: **NEW** - Switch between original mixed-language comments and English translations

### **📊 Executive Dashboard**
- **Professional Interface**: Crimzon design system with executive-grade polish
- **Dual Mode Support**: Advanced (9 pages) and Basic (5 pages) interface modes
- **Real-time Metrics**: Live reputation scoring and sentiment tracking
- **Strategic Reports**: Automated intelligence briefings and executive summaries

## 🚀 Quick Start

### **Launch Application**
```bash
# Clone the repository
git clone [repository-url]
cd percepta

# Install dependencies
pip install -r requirements.txt

# Launch Percepta Pro
./start_percepta.bat
```

### **Access Dashboard**
- **Main Application**: http://localhost:8501
- **Debug Console**: Available via debug_navigation_app.py

## 🎛️ Interface Modes

| Mode | Pages | Target Audience | Key Features |
|------|-------|----------------|--------------|
| **Advanced** | 9 pages | C-Suite Executives | Complete feature set with predictive analytics |
| **Basic** | 5 pages | General Users | Streamlined monitoring interface |

## 🌐 Language Support

### **NEW: Comment Language Toggle**
- **English Mode** (Default): View translated English comments
- **Telugu Mode**: View original comments (Telugu + Telugu-written-in-English)
- **Toggle Location**: Sidebar, below "Dashboard Mode"
- **Real-time Switching**: Instantly changes across all pages

## 📁 Project Structure

```
percepta/
├── reputation_dashboard.py   # Main production dashboard (237KB)
├── start_percepta.bat       # Application launcher
├── src/                     # Source code modules
│   ├── dashboard/          # Dashboard components
│   ├── core/              # Core business logic  
│   ├── analytics/         # Analytics engines
│   ├── themes/            # Theme system
│   ├── utils/             # Utilities
│   └── data_processing/   # Data processing logic
├── backend/data/           # Data storage
│   ├── videos/            # Video datasets
│   └── comments/          # Comment datasets (with bilingual support)
├── docs/                   # Documentation
├── scripts/               # Processing scripts
├── tests/                 # Test files
└── assets/                # Static assets
```

## 🔧 Technical Specifications

- **Framework**: Streamlit + Python
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **AI/ML**: Custom sentiment analysis models
- **Language Support**: Telugu/English bilingual processing
- **Storage**: CSV-based with real-time analytics
- **Deployment**: Local hosting with production-ready interface

## 📈 Performance Metrics

- **Processing Capacity**: 200+ videos, 1,500+ comments
- **Language Coverage**: Bilingual (Telugu/English) with translation support
- **Analytics Models**: 4 operational ML models
- **Crisis Alerts**: 666 threats identified, 98 critical alerts managed
- **Real-time Updates**: Live sentiment tracking and reputation scoring

## 🎯 Current Status

**Version**: 2.0.2 (Language Toggle Update)  
**Status**: ✅ **Production Ready**  
**Last Updated**: December 2024  
**Key Update**: Added bilingual comment language toggle functionality

## 🚀 Recent Updates

### **v2.0.2 - Language Toggle Feature**
- ✅ Added bilingual comment language toggle
- ✅ English/Telugu mode switching across all pages
- ✅ Enhanced data loading with language preference support
- ✅ Improved search functionality for selected language
- ✅ Real-time language switching without page reload

### **v2.0.1 - UI Refinements**
- ✅ Executive-grade interface polish
- ✅ Seamless navigation improvements
- ✅ Enhanced visual hierarchy
- ✅ Professional color scheme optimization

## 📞 Support

For technical support or feature requests, please refer to the documentation in the `docs/` directory or check the project's issue tracker.

---

**Built with ❤️ for Advanced Reputation Intelligence** 