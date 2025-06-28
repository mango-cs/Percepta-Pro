# Percepta Pro - Enterprise Reputation Analytics Platform

**C-suite-ready analytics portal for YouTube data analysis**

## 🚀 Project Status: **PRODUCTION READY**

- ✅ **Frontend**: NIXPACKS deployment with React/Next.js 14
- ✅ **Backend**: FastAPI with Python startup script
- ✅ **Deployment**: Railway cloud platform
- ✅ **Authentication**: NextAuth.js with JWT
- ✅ **Analytics**: Real-time sentiment analysis & metrics

## 📁 Project Structure

```
Percepta/
├── backend/                 # FastAPI Backend
│   ├── src/                 # Source code
│   │   ├── app.py          # Main FastAPI application
│   │   ├── auth/           # Authentication modules
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── data/               # CSV data files
│   ├── start.py            # Railway startup script
│   ├── requirements.txt    # Python dependencies
│   └── railway.json        # Railway deployment config
│
├── frontend/               # Next.js Frontend
│   ├── src/                # Source code
│   │   ├── app/            # App router
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   └── lib/            # Utilities
│   ├── public/             # Static assets
│   ├── package.json        # Dependencies
│   ├── nixpacks.toml       # NIXPACKS build config
│   └── railway.json        # Railway deployment config
│
└── README.md               # Project documentation
```

## 🎯 Key Features

### **Analytics Dashboard**
- **Overview Metrics**: Videos, comments, sentiment percentages
- **Timeline Data**: Daily sentiment trends and comment volume
- **Video Analytics**: Performance metrics with sentiment analysis
- **Word Clouds**: Positive/negative sentiment visualization
- **Search & Export**: Full-text search with CSV/JSON export

### **Authentication & Security**
- **NextAuth.js**: GitHub OAuth + credentials authentication
- **JWT Tokens**: Secure API access with role-based permissions
- **User Roles**: Admin, PR Manager, Analyst, Viewer
- **Route Protection**: Middleware-based access control

### **Technical Stack**
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Zustand
- **Backend**: FastAPI, Pandas, Pydantic, Uvicorn
- **Deployment**: Railway (NIXPACKS + Python)
- **Data**: CSV-based with real-time processing

## 🚀 Deployment

### **Railway Configuration**
Both services are deployed on Railway with optimized configurations:

**Frontend (NIXPACKS)**:
```toml
[phases.build]
cmd = "npm install --legacy-peer-deps && npm run build"

[phases.start]
cmd = "npm start"
```

**Backend (Python)**:
```python
# start.py - Custom startup script
os.chdir('src')  # Fix import paths
uvicorn.run("app:app", host="0.0.0.0", port=PORT)
```

### **Health Checks**
- **Frontend**: `/api/health` - Service status
- **Backend**: `/health` - Service + data loader status

## 🔧 Development

### **Frontend Setup**
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

### **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python start.py
```

## 📊 Data Processing

The system processes YouTube analytics data:
- **Videos**: `Youtube-Full-List-FInal.csv`
- **Comments**: `all_comments_with_replies.csv`

Automatic sentiment analysis and metrics calculation on startup.

## 🎯 API Endpoints

### **Authentication**
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Current user profile

### **Analytics**
- `GET /metrics/overview` - Dashboard overview
- `GET /metrics/timeline` - Sentiment timeline
- `GET /metrics/videos` - Video analytics
- `GET /comments` - Video comments
- `GET /wordcloud` - Word cloud data
- `GET /export` - Data export

## 🏢 Enterprise Features

**Built for C-suite decision making**:
- Real-time reputation monitoring
- Risk assessment metrics
- Viral threat detection
- Actionable intelligence reporting
- Audit logging & compliance

---

**Percepta Pro** - Transforming YouTube analytics into executive-ready insights. 