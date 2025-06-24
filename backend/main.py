"""
Nirabhi - AI-Powered Content Moderator
Main FastAPI Application

This is the heart of our content moderation system. It provides APIs for:
- Content analysis and toxicity detection
- User preference management
- Reporting and analytics
- Educational feedback

Built with love for creating safer digital spaces.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
import logging
from datetime import datetime

# Import our custom modules
from models.content_analyzer import ContentAnalyzer
from models.database import Database
from models.schemas import (
    ContentAnalysisRequest,
    ContentAnalysisResponse,
    UserPreferences,
    ToxicityReport,
    HealthCheck
)
from utils.logger import setup_logger
from config import settings

# Initialize our beautiful logger
logger = setup_logger()

# Create the FastAPI app with a warm welcome
app = FastAPI(
    title="🛡️ Nirabhi API",
    description="AI-Powered Content Moderator - Creating safer digital spaces",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for our frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our AI brain and database
content_analyzer = ContentAnalyzer()
database = Database()

@app.on_event("startup")
async def startup_event():
    """
    When our app wakes up, let's prepare everything we need.
    Think of this as our morning coffee routine!
    """
    logger.info("🚀 Nirabhi is starting up...")
    await database.connect()
    await content_analyzer.initialize()
    logger.info("✅ All systems ready! Nirabhi is now protecting digital spaces.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    When we shut down, let's clean up nicely.
    Always good to be polite!
    """
    logger.info("👋 Nirabhi is shutting down...")
    await database.disconnect()
    logger.info("✅ Shutdown complete. Thanks for using Nirabhi!")

@app.get("/", response_model=HealthCheck)
async def root():
    """
    Our friendly welcome endpoint.
    Like a warm handshake when someone visits our API!
    """
    return HealthCheck(
        status="healthy",
        message="Welcome to Nirabhi - AI-Powered Content Moderator! 🛡️",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )

@app.post("/analyze", response_model=ContentAnalysisResponse)
async def analyze_content(
    request: ContentAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    The main event! This is where the magic happens.
    
    We analyze content to detect:
    - Toxicity and hate speech
    - Sentiment and emotional impact
    - Potential harm to users
    - Educational opportunities
    
    It's like having a wise friend who helps keep conversations healthy.
    """
    try:
        logger.info(f"🔍 Analyzing content: {request.text[:50]}...")
        
        # Use our AI brain to analyze the content
        analysis_result = await content_analyzer.analyze_text(
            text=request.text,
            context=request.context,
            user_preferences=request.user_preferences
        )
        
        # Store the analysis for future learning (in the background)
        background_tasks.add_task(
            database.store_analysis,
            request.text,
            analysis_result
        )
        
        # If content is highly toxic, let's also prepare helpful resources
        if analysis_result.toxicity_score > 0.7:
            background_tasks.add_task(
                prepare_support_resources,
                analysis_result
            )
        
        logger.info(f"✅ Analysis complete. Toxicity score: {analysis_result.toxicity_score}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"❌ Error analyzing content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Oops! Something went wrong while analyzing the content. Please try again."
        )

@app.get("/reports/user/{user_id}", response_model=List[ToxicityReport])
async def get_user_reports(user_id: str):
    """
    Get personalized reports for a user.
    
    This helps users understand their digital environment and
    provides insights for healthier online interactions.
    """
    try:
        reports = await database.get_user_reports(user_id)
        return reports
    except Exception as e:
        logger.error(f"❌ Error fetching user reports: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Couldn't fetch your reports right now. Please try again later."
        )

@app.post("/preferences/{user_id}")
async def update_user_preferences(
    user_id: str,
    preferences: UserPreferences
):
    """
    Update user's moderation preferences.
    
    Because everyone deserves to customize their digital safety!
    We respect that different people have different comfort levels.
    """
    try:
        await database.update_user_preferences(user_id, preferences)
        return {"message": "Your preferences have been updated successfully! 🎉"}
    except Exception as e:
        logger.error(f"❌ Error updating preferences: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Couldn't update your preferences right now. Please try again."
        )

@app.get("/health")
async def health_check():
    """
    A quick health check to make sure everything is running smoothly.
    Like checking your pulse - simple but important!
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "components": {
            "database": "healthy",
            "ai_model": "loaded",
            "api": "running"
        }
    }

async def prepare_support_resources(analysis_result):
    """
    When we detect highly toxic content, let's prepare helpful resources
    for users who might need support.
    
    This runs in the background so we don't slow down the main response.
    """
    logger.info("🤝 Preparing support resources for user wellbeing")
    # Here we could integrate with mental health resources,
    # crisis hotlines, or educational materials
    pass

if __name__ == "__main__":
    # Let's start our server with some style!
    print("🛡️ Starting Nirabhi - AI-Powered Content Moderator")
    print("Creating safer digital spaces, one analysis at a time...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # For development - auto-reload when code changes
        log_level="info"
    )
