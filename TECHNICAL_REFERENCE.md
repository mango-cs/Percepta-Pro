# 🎯 PERCEPTA PRO - QUICK REFERENCE GUIDE
## Critical Project Information & Error Prevention

---

## 📊 CURRENT PROJECT STATUS (Always Check First!)

### ✅ COMPLETED PHASES
- **Phase 1**: Enhanced Dataset Foundation ✅ COMPLETE
- **Phase 2**: Bilingual AI Processing ✅ COMPLETE  
- **Phase 2B**: Advanced Comments AI Enhancement ✅ COMPLETE
- **Phase 3A**: Crisis Detection System ✅ COMPLETE
- **Phase 3B**: Executive Reporting System ✅ COMPLETE

### 🎯 CURRENT STATE
- **Version**: v2.0 - Complete Executive Intelligence Platform
- **Last Updated**: June 29, 2025
- **Status**: Production-ready, Phase 2B+3A+3B Executive Intelligence operational
- **Next Step**: Phase 3C (Predictive Analytics) when requested

---

## 📂 CRITICAL FILE STRUCTURE (Exact Paths)

### 🎯 PRIMARY DATASETS (ALWAYS USE THESE)
```
backend/data/videos/youtube_videos_ai_processed.csv    # 596KB, 39 cols, 192 videos - PRIMARY
backend/data/comments/youtube_comments_ai_enhanced.csv # 800KB, 30+ cols, 1,719 comments - PRIMARY (Phase 2B)
backend/data/comments/youtube_comments_final.csv       # 15 cols, 1,525+ comments - LEGACY (use enhanced version)
```

### 📁 LEGACY DATASETS (Reference Only)
```
backend/data/videos/youtube_videos_final.csv          # Phase 1 enhanced (backup)
backend/data/videos/youtube_videos.csv                # Original dataset (backup)
backend/data/comments/youtube_comments.csv            # Original comments (backup)
```

### 🔧 KEY SCRIPTS
```
scripts/phase2_ai_processor.py                        # Complete AI pipeline
scripts/final_dataset_enhancement.py                  # Phase 1 processor
scripts/test_phase2_processor.py                      # Validation suite
reputation_dashboard.py                               # Main Streamlit app
```

### 📋 DOCUMENTATION
```
PROJECT_CONTEXT.md                                    # Technical overview
VERSION_2_CHANGES.md                                  # Implementation history
PHASE_2_COMPLETION_REPORT.md                          # Final completion status
TECHNICAL_REFERENCE.md                                # This file - Technical documentation
```

---

## 🔍 DATASET COLUMN STRUCTURES (Critical for Integration)

### 📹 VIDEOS DATASET (youtube_videos_ai_processed.csv)
**Columns: 39 total**
```
Core Fields:
- VideoID, Title, Channel, UploadDate, Views, Comments, RelevanceScore, TrustLevel

API Enhancement Fields (8):
- PublishedAt_Formatted (dd-mm-yyyy), CategoryId, DefaultLanguage, ChannelId
- LiveBroadcastContent, CommentCount_API, FavoriteCount, ChannelSubscriberCount

AI Processing Fields (10):
- Transcript_EN, Transcript_TE, Summary_EN, Summary_TE
- SentimentScore_EN, SentimentLabel_EN, SentimentScore_TE, SentimentLabel_TE
- Keywords_EN, Keywords_TE

Processing Fields:
- DataHealth, ProcessingStatus, URL, Thumbnail, Duration, Description, etc.
```

### 💬 COMMENTS DATASET (youtube_comments_ai_enhanced.csv) - Phase 2B Enhanced
**Columns: 30+ total**
```
Core Fields:
- VideoID, CommentID, ParentID, IsReply, LikeCount, Author, Comment

Bilingual AI Enhancement Fields (15):
- Comment_EN (improved), SentimentScore_TE/EN, SentimentLabel_TE/EN
- SentimentConfidence_TE/EN, Keywords_TE/EN, CriticalKeywords_TE/EN
- ThreatDetected, ThreatLevel, ThreatTypes, ThreatScore, CriticalPatterns

Processing Fields:
- Date_Formatted, PublishedAt, UpdatedAt, ModerationStatus
- ProcessingStatus, ProcessingTimestamp, AIEnhanced, ReplyCount
```

### 💬 LEGACY COMMENTS DATASET (youtube_comments_final.csv) - Phase 2A
**Columns: 15 total (kept for compatibility)**
```
Core Fields: VideoID, CommentID, Author, Comment, Comment_EN
Basic Enhancement: Date_Formatted, Sentiment, SentLabel
```

---

## ⚠️ COMMON ERRORS & SOLUTIONS

### 🚨 Dashboard Integration Errors
**Error**: `FileNotFoundError: youtube_videos.csv`
**Solution**: Dashboard MUST load AI-enhanced datasets:
```python
videos_path = Path("backend/data/videos/youtube_videos_ai_processed.csv")
comments_path = Path("backend/data/comments/youtube_comments_final.csv")
```

**Error**: `KeyError: 'Upload Date'` or similar column errors
**Solution**: Handle both old and new column names:
```python
# Handle different date column names
if 'UploadDate' in videos_df.columns:
    videos_df['Upload Date'] = pd.to_datetime(videos_df['UploadDate'], errors='coerce')
elif 'Upload Date' in videos_df.columns:
    videos_df['Upload Date'] = pd.to_datetime(videos_df['Upload Date'], errors='coerce')
```

### 🔧 AI Processing Errors
**Error**: "The expanded size of the tensor (XXX) must match the existing size (514)"
**Solution**: Text truncation + fallback to keyword-based analysis (ALREADY IMPLEMENTED)

**Error**: "Subtitles are disabled for this video"
**Solution**: Expected behavior - graceful handling without stopping (ALREADY IMPLEMENTED)

**Error**: "Translation failed: timed out"
**Solution**: Retry mechanisms with timeout handling (ALREADY IMPLEMENTED)

### 💾 System Resource Errors
**Error**: Multiple Python processes consuming memory
**Solution**: Kill processes before starting: `taskkill /f /im python.exe`

**Error**: Dashboard loading slowly
**Solution**: Use cached data loading: `@st.cache_data` decorator applied

---

## 🎯 DASHBOARD INTEGRATION CHECKLIST

### ✅ ALWAYS VERIFY THESE WHEN UPDATING DASHBOARD:
1. **Data Source**: Uses `youtube_videos_ai_processed.csv` and `youtube_comments_final.csv`
2. **Column Handling**: Supports both old and new column names
3. **Sentiment Analysis**: Uses `SentimentScore_EN` and `SentimentLabel_EN` when available
4. **Date Processing**: Handles `Date_Formatted` (dd-mm-yyyy format)
5. **AI Features**: Integrates AI insights (transcripts, summaries, keywords)
6. **Error Handling**: Graceful fallbacks for missing columns/data

### 🔍 QUICK VERIFICATION COMMANDS:
```python
# Check if dashboard loads correct files
videos_df, comments_df = load_reputation_data()
print(f"Videos shape: {videos_df.shape}")  # Should be (192, 39)
print(f"Comments shape: {comments_df.shape}")  # Should be (1525+, 15)
print(f"Video columns: {len(videos_df.columns)}")  # Should be 39
print(f"Comment columns: {len(comments_df.columns)}")  # Should be 15
```

---

## 🧠 AI PROCESSING STATUS

### ✅ FULLY IMPLEMENTED COMPONENTS:
1. **Google Translate API**: Telugu-English translation with timeout handling
2. **Sentiment Analysis**:
   - English: cardiffnlp/twitter-roberta-base-sentiment-latest
   - Telugu: nlptown/bert-base-multilingual-uncased-sentiment
   - Fallback: Keyword-based analysis
3. **YouTube Transcript API**: Graceful handling of missing subtitles
4. **Keyword Extraction**: Bilingual term identification
5. **Content Summarization**: Smart summaries from descriptions/transcripts

### 📊 PROCESSING RESULTS:
- **Success Rate**: 95%+ with comprehensive error handling
- **Videos Processed**: 192/192 (100% completion)
- **Critical Content**: చేతబడి, అరెస్ట్, మాగంటి content captured
- **Bilingual Coverage**: Telugu 57.3% + English 71.9%

---

## 🚀 QUICK TROUBLESHOOTING GUIDE

### 🔥 EMERGENCY FIXES:
```bash
# 1. Kill all Python processes if system is slow
taskkill /f /im python.exe

# 2. Restart dashboard
streamlit run reputation_dashboard.py

# 3. Check data files exist
dir backend\data\videos\youtube_videos_ai_processed.csv
dir backend\data\comments\youtube_comments_final.csv

# 4. Verify Python dependencies
pip install -r requirements.txt
```

### 🧪 QUICK TESTS:
```python
# Test data loading
import pandas as pd
videos = pd.read_csv("backend/data/videos/youtube_videos_ai_processed.csv")
comments = pd.read_csv("backend/data/comments/youtube_comments_final.csv")
print(f"✅ Videos: {len(videos)} rows, {len(videos.columns)} columns")
print(f"✅ Comments: {len(comments)} rows, {len(comments.columns)} columns")

# Test AI fields presence
ai_fields = ['Transcript_EN', 'Summary_EN', 'SentimentScore_EN', 'Keywords_EN']
for field in ai_fields:
    if field in videos.columns:
        print(f"✅ {field}: {videos[field].notna().sum()} entries")
```

---

## 📋 PHASE 3 IMPLEMENTATION STATUS

### ✅ PHASE 3A: CRISIS DETECTION SYSTEM - COMPLETE
- **Real-time Threat Monitoring**: 666 threats detected across 192 videos
- **Executive Crisis Dashboard**: 🚨 Crisis Detection Center page added
- **Bilingual Threat Patterns**: Telugu + English threat analysis
- **Critical Threat Categories**: Death threats, black magic, legal issues, violence, reputation attacks
- **Executive Alerts**: Immediate/High/Medium priority classifications
- **Strategic Recommendations**: Automated crisis response guidance
- **Status**: OPERATIONAL - Critical threats detected and managed

### ✅ PHASE 3B: EXECUTIVE REPORTING SYSTEM - COMPLETE
- **Automated Intelligence Briefings**: Daily/Weekly/Executive summary reports
- **Executive Reports Dashboard**: 📋 Executive Reports page with multiple report types
- **Strategic Analytics**: Performance metrics, trend analysis, forecasting
- **Action Item Generation**: Automated task assignments with priorities
- **Export Capabilities**: JSON/TXT export for all report types
- **Intelligence Integration**: Crisis data integration for comprehensive reporting
- **Status**: OPERATIONAL - Executive-grade automated reporting active

### 🚀 NEXT IMPLEMENTATION TARGETS (Phase 3C+):
1. **Predictive Analytics**: Reputation forecasting models ⏳ NEXT
2. **API Development**: External system integration
3. **Mobile Optimization**: Responsive design enhancements
4. **Advanced Analytics**: Trend prediction algorithms
5. **Real-time Notifications**: Email/SMS alert systems

---

## 🔒 CRITICAL REMINDERS (NEVER FORGET!)

### ⚠️ ALWAYS REMEMBER:
1. **Primary Datasets**: Only use `youtube_videos_ai_processed.csv` and `youtube_comments_final.csv`
2. **Column Compatibility**: Handle both old and new column names in dashboard
3. **Error Handling**: All AI processing has comprehensive fallbacks implemented
4. **Resource Management**: Kill Python processes if system becomes slow
5. **Data Quality**: 95%+ processing success rate - errors are expected and handled
6. **Bilingual Support**: All features must support both Telugu and English

### 🎯 PROJECT ESSENTIALS:
- **Subject**: Sandhya Convention MD Sridhar Rao reputation monitoring
- **Critical Content**: చేతబడి (black magic), అరెస్ట్ (arrest), మాగంటి గోపినాథ్ (key figure)
- **Data Sources**: 192 videos, 1,525+ comments, premium Telugu channels
- **Technology Stack**: Streamlit, Transformers, Google Translate, YouTube APIs

---

## 📞 QUICK COMMAND REFERENCE

### 🚀 ESSENTIAL COMMANDS:
```bash
# Launch dashboard
streamlit run reputation_dashboard.py

# Run AI processing (if needed)
python scripts/phase2_ai_processor.py

# Run tests
python scripts/test_phase2_processor.py

# System cleanup
taskkill /f /im python.exe

# Check file sizes
dir backend\data\videos\*.csv
dir backend\data\comments\*.csv
```

---

**🎯 REMEMBER: Always check this file first for project status, file paths, and error solutions!**

**Last Updated**: June 29, 2025  
**Project Status**: Phase 1-2 Complete, Phase 3 Ready  
**Critical Files**: AI-processed datasets integrated, dashboard operational 