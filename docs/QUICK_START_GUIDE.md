# 🚀 Percepta Pro v2.0.2 - Quick Start Guide

Welcome to **Percepta Pro**, the advanced reputation intelligence platform. This guide will get you up and running in minutes.

## ⚡ Quick Launch

### **1. Start the Application**
```bash
# Navigate to project directory
cd Percepta

# Launch Percepta Pro
./start_percepta.bat
```

### **2. Access Dashboard**
- **Main Application**: http://localhost:8501
- **Expected Load Time**: ~10-15 seconds

### **3. Interface Overview**
Once loaded, you'll see:
- **Navigation Sidebar** (left): Page navigation and controls
- **Main Dashboard** (center): Active page content
- **Status Indicators** (top): System health and data status

---

## 🎛️ **Dashboard Modes**

### **Mode Selection**
- **Location**: Top of sidebar under "Dashboard Mode"
- **Basic Mode**: 5 essential pages for general monitoring
- **Advanced Mode**: 9 comprehensive pages with full analytics

| Mode | Best For | Pages Available |
|------|----------|----------------|
| **Basic** | Daily monitoring, Quick insights | Overview, Videos, Comments, Analytics, Settings |
| **Advanced** | Executive analysis, Strategic planning | + Reputation Alerts, Executive Reports, Data Intelligence, Predictive Analytics |

---

## 🌐 **NEW: Language Toggle** 

### **Comment Language Control**
- **Location**: Sidebar, below "Dashboard Mode"
- **Purpose**: Switch between original and translated comments

### **Language Modes**
| Mode | Shows | Best For |
|------|-------|----------|
| **English** (Default) | Translated comments | International audiences, executives |
| **Telugu** | Original mixed-language comments | Native speakers, authentic content |

### **How to Use**
1. **Find Toggle**: Look for "Comments Language" in sidebar
2. **Switch Mode**: 
   - Toggle OFF = English (EN indicator)
   - Toggle ON = Telugu (తెలుగు indicator)
3. **Instant Update**: All pages update immediately
4. **Search**: Search function respects your language selection

---

## 📊 **Page Navigation**

### **Essential Pages**

#### **📊 Overview**
- **Purpose**: Executive dashboard with key metrics
- **Key Metrics**: Total videos, comments, reputation score, sentiment distribution
- **Updates**: Real-time data with language preference applied

#### **💬 Comments** 
- **Purpose**: Deep dive into public discussions
- **Features**: 
  - Language toggle affects all comment display
  - Advanced search and filtering
  - Sentiment analysis and categorization
  - Pagination for large datasets

#### **📈 Analytics**
- **Purpose**: Comprehensive sentiment and trend analysis
- **Charts**: Sentiment timeline, distribution charts, engagement metrics
- **Language Impact**: Charts reflect data from selected language mode

#### **📹 Videos**
- **Purpose**: Video performance and impact analysis
- **Features**: Video catalog, engagement metrics, thumbnail previews

### **Advanced Pages** (Advanced Mode Only)

#### **🔔 Reputation Alerts**
- **Purpose**: Real-time crisis detection and monitoring
- **Features**: Threat assessment, critical alerts, status dashboard

#### **📋 Executive Reports**
- **Purpose**: Strategic intelligence briefings
- **Features**: Automated reports, weekly insights, executive summaries

#### **📂 Data Intelligence** 
- **Purpose**: Comprehensive data analytics
- **Features**: Performance metrics, trend analysis, intelligence overview

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **App Won't Start**
```bash
# Check if Python is installed
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Try manual launch
streamlit run reputation_dashboard.py
```

#### **Data Not Loading**
- **Check**: Data files in `backend/data/` directory
- **Expected**: `youtube_videos_final.csv` and `youtube_comments_ai_enhanced.csv`
- **Fallback**: System automatically uses basic dataset if enhanced unavailable

#### **Language Toggle Not Working**
- **Refresh**: Press F5 to reload the page
- **Check**: Language indicator in sidebar (EN/తెలుగు)
- **Data**: Ensure enhanced comment dataset is available

### **Performance Tips**
- **Browser**: Use Chrome or Firefox for best performance
- **Cache**: Clear browser cache if experiencing slow loading
- **Data**: Language switching is instant, no page reload needed

---

## 📱 **Interface Tips**

### **Navigation Best Practices**
1. **Start with Overview**: Get familiar with overall metrics
2. **Use Language Toggle**: Switch based on your audience needs
3. **Explore Advanced Mode**: Access full analytics capabilities
4. **Check Alerts**: Monitor reputation status regularly

### **Search and Filtering**
- **Comments Search**: Respects your selected language mode
- **Sentiment Filters**: Available across all analytical pages
- **Date Ranges**: Use sort options for temporal analysis

### **Visual Indicators**
- **Green**: Positive metrics, good performance
- **Red**: Alerts, critical issues, negative sentiment
- **Orange**: Neutral metrics, moderate performance

---

## 🎯 **Getting the Most Value**

### **Daily Workflow**
1. **Morning**: Check Overview for overnight changes
2. **Monitor**: Review Reputation Alerts for any issues
3. **Analyze**: Use Comments page to understand public sentiment
4. **Language Switch**: Toggle between modes for comprehensive view

### **Weekly Review**
1. **Executive Reports**: Generate strategic intelligence briefings
2. **Analytics**: Review trend analysis and performance metrics
3. **Language Comparison**: Compare sentiment across both language modes

### **Executive Presentation**
- **Use Advanced Mode**: Full feature set for C-suite presentations
- **Language Selection**: Choose appropriate mode for your audience
- **Export Data**: Use browser print function for static reports

---

## 📞 **Support & Documentation**

### **Additional Resources**
- **Technical Reference**: `TECHNICAL_REFERENCE.md`
- **Project Overview**: `CURRENT_PROJECT_STATE_DECEMBER_2024.md`
- **Full Documentation**: `docs/` directory

### **Getting Help**
- **UI Issues**: Check browser console for errors
- **Data Questions**: Review data files in `backend/data/`
- **Feature Requests**: Document in project issue tracker

---

**🎯 Ready to monitor your reputation intelligence? Launch the app and start exploring!**

*Updated for Percepta Pro v2.0.2 with Language Toggle Feature* 