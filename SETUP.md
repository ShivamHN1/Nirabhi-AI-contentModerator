# 🛡️ Nirabhi Setup Guide

Welcome to Nirabhi! This guide will help you set up the AI-powered content moderator on your system.

## 🚀 Quick Start

### Prerequisites

Make sure you have the following installed:
- **Python 3.9+** (for backend)
- **Node.js 18+** (for frontend)
- **Git** (for version control)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nirabhi-ai-moderator.git
cd nirabhi-ai-moderator
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Application Settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Server Configuration
HOST=0.0.0.0
PORT=8000

# AI Model Configuration
TOXICITY_MODEL_NAME=unitary/toxic-bert
USE_GPU=false

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_WELLNESS_FEATURES=true
ENABLE_EDUCATIONAL_MODE=true

# Security (change in production!)
SECRET_KEY=your-secret-key-change-this-in-production
```

### AI Models

The system uses lightweight AI models that work well without GPU:
- **VADER Sentiment Analysis** - For emotional tone detection
- **Rule-based Patterns** - For quick toxicity detection
- **Optional: Transformer Models** - For advanced analysis (requires more resources)

## 🎯 Features Overview

### 🔍 Content Analysis
- Real-time toxicity detection
- Sentiment analysis
- Category classification (hate speech, cyberbullying, etc.)
- Confidence scoring
- Educational explanations

### 🎨 User Interface
- Beautiful, responsive design
- Dark/light mode toggle
- Real-time feedback
- Educational suggestions
- Support resources

### 📊 Analytics
- Personal wellness dashboard
- Usage statistics
- Content analysis history
- Trend insights

### ⚙️ Customization
- Adjustable sensitivity levels
- Personal preference settings
- Category filtering
- Educational mode toggle

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📁 Project Structure

```
nirabhi-ai-moderator/
├── backend/                 # Python FastAPI backend
│   ├── models/             # AI models and data schemas
│   │   ├── content_analyzer.py  # Main AI analysis engine
│   │   ├── database.py     # Database operations
│   │   └── schemas.py      # Data models
│   ├── utils/              # Utility functions
│   │   └── logger.py       # Logging configuration
│   ├── main.py            # FastAPI application
│   ├── config.py          # Configuration settings
│   └── requirements.txt   # Python dependencies
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.tsx        # Main application
│   │   └── index.tsx      # Entry point
│   ├── public/            # Static assets
│   └── package.json       # Node dependencies
└── README.md              # Project documentation
```

## 🚀 Deployment

### Development
- Backend: `python main.py` (auto-reload enabled)
- Frontend: `npm start` (hot reload enabled)

### Production

#### Backend (using Gunicorn)
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend (build and serve)
```bash
npm run build
# Serve the build folder with your preferred web server
```

#### Docker (Optional)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Backend: Change `PORT` in `.env` file
   - Frontend: Use `PORT=3001 npm start`

2. **AI Model Loading Issues**
   - Models download automatically on first run
   - Ensure stable internet connection
   - Check disk space (models can be 100MB+)

3. **CORS Errors**
   - Ensure backend is running on port 8000
   - Check `cors_origins` in `config.py`

4. **Dependencies Issues**
   - Update pip: `pip install --upgrade pip`
   - Clear npm cache: `npm cache clean --force`

### Performance Tips

1. **Backend Optimization**
   - Set `USE_GPU=true` if you have a compatible GPU
   - Increase worker processes for production
   - Use Redis for caching (optional)

2. **Frontend Optimization**
   - Run `npm run build` for production
   - Enable gzip compression on your server
   - Use a CDN for static assets

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the `/docs` folder
- **Community**: Join our Discord server
- **Email**: team@nirabhi.ai

## 🎉 What's Next?

After setup, you can:
1. **Test the analyzer** with sample content
2. **Explore the dashboard** to see analytics
3. **Customize preferences** to match your needs
4. **Check wellness reports** for insights
5. **Contribute** to the project on GitHub

---

Thank you for using Nirabhi! Together, we're making the internet a safer, kinder place. 💙
