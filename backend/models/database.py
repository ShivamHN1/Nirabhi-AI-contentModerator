"""
Database Handler for Nirabhi

This manages all our data storage needs - from storing analysis results
to keeping track of user preferences and generating helpful reports.

Think of it as the memory of our application - it remembers everything
so we can learn and improve over time.
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

# For now, we'll use a simple in-memory database for the MVP
# In production, this would connect to PostgreSQL or another robust database
from .schemas import (
    ContentAnalysisResponse,
    UserPreferences,
    ToxicityReport,
    ToxicityCategory,
    AnalysisHistory
)

@dataclass
class InMemoryRecord:
    """A simple record for our in-memory database"""
    id: str
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class Database:
    """
    Our friendly database handler.
    
    For this MVP, we're using an in-memory database to keep things simple.
    In a production environment, this would connect to a real database
    like PostgreSQL with proper persistence, indexing, and scaling.
    """
    
    def __init__(self):
        """Initialize our in-memory database"""
        self.connected = False
        
        # Our simple data stores
        self.analysis_history: List[InMemoryRecord] = []
        self.user_preferences: Dict[str, UserPreferences] = {}
        self.user_reports: Dict[str, List[ToxicityReport]] = {}
        
        # Some demo data for testing
        self._setup_demo_data()
    
    async def connect(self):
        """
        Connect to our database.
        For the in-memory version, this just sets up our data structures.
        """
        if self.connected:
            return
        
        print("💾 Connecting to database...")
        
        # In a real app, this would:
        # - Connect to PostgreSQL
        # - Run migrations
        # - Set up connection pooling
        # - Validate schema
        
        # For now, we just simulate this
        await asyncio.sleep(0.1)  # Simulate connection time
        
        self.connected = True
        print("✅ Database connected successfully!")
    
    async def disconnect(self):
        """
        Clean disconnect from our database.
        Always good to clean up after ourselves!
        """
        if not self.connected:
            return
        
        print("👋 Disconnecting from database...")
        
        # In a real app, this would close connection pools
        # For now, we just clear our in-memory data
        
        self.connected = False
        print("✅ Database disconnected cleanly!")
    
    async def store_analysis(
        self,
        original_text: str,
        analysis_result: ContentAnalysisResponse
    ) -> str:
        """
        Store an analysis result for future learning and reporting.
        
        This helps us:
        - Track patterns over time
        - Generate user reports
        - Improve our AI models
        - Provide analytics
        """
        if not self.connected:
            await self.connect()
        
        # Generate a unique ID
        analysis_id = f"analysis_{len(self.analysis_history) + 1}_{int(datetime.utcnow().timestamp())}"
        
        # Create the record
        record = InMemoryRecord(
            id=analysis_id,
            data={
                "original_text": original_text,
                "analysis_result": analysis_result.dict(),
                "user_id": None,  # Could be extracted from request context
            },
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Store it
        self.analysis_history.append(record)
        
        print(f"📊 Stored analysis result: {analysis_id}")
        return analysis_id
    
    async def get_user_reports(self, user_id: str) -> List[ToxicityReport]:
        """
        Generate and return toxicity reports for a user.
        
        This gives users insights into their digital environment
        and helps them make informed decisions about their online safety.
        """
        if not self.connected:
            await self.connect()
        
        # For the MVP, we'll return some sample reports
        # In production, this would analyze real user data
        
        if user_id not in self.user_reports:
            # Generate a sample report
            sample_report = self._generate_sample_report(user_id)
            self.user_reports[user_id] = [sample_report]
        
        return self.user_reports[user_id]
    
    async def update_user_preferences(
        self,
        user_id: str,
        preferences: UserPreferences
    ):
        """
        Update a user's moderation preferences.
        
        Personalization is key to making our system work for everyone!
        """
        if not self.connected:
            await self.connect()
        
        self.user_preferences[user_id] = preferences
        print(f"⚙️ Updated preferences for user: {user_id}")
    
    async def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """
        Get a user's current preferences.
        """
        if not self.connected:
            await self.connect()
        
        return self.user_preferences.get(user_id)
    
    async def get_analysis_history(
        self,
        user_id: Optional[str] = None,
        limit: int = 100
    ) -> List[AnalysisHistory]:
        """
        Get historical analysis data.
        Useful for generating reports and improving our models.
        """
        if not self.connected:
            await self.connect()
        
        # Filter and convert our records
        results = []
        for record in self.analysis_history[-limit:]:  # Get the most recent
            if user_id is None or record.data.get("user_id") == user_id:
                try:
                    analysis_history = AnalysisHistory(
                        id=record.id,
                        user_id=record.data.get("user_id"),
                        original_text=record.data["original_text"],
                        analysis_result=ContentAnalysisResponse(**record.data["analysis_result"]),
                        feedback=record.data.get("feedback"),
                        created_at=record.created_at
                    )
                    results.append(analysis_history)
                except Exception as e:
                    print(f"⚠️ Error converting record {record.id}: {str(e)}")
                    continue
        
        return results
    
    async def get_toxicity_stats(self) -> Dict[str, Any]:
        """
        Get overall toxicity statistics for dashboard and analytics.
        """
        if not self.connected:
            await self.connect()
        
        total_analyses = len(self.analysis_history)
        if total_analyses == 0:
            return {
                "total_analyses": 0,
                "toxic_content_rate": 0.0,
                "category_breakdown": {},
                "average_toxicity_score": 0.0
            }
        
        # Calculate stats from our stored analyses
        toxic_count = 0
        toxicity_scores = []
        category_counts = {}
        
        for record in self.analysis_history:
            try:
                result = record.data["analysis_result"]
                
                if result.get("is_toxic", False):
                    toxic_count += 1
                
                toxicity_scores.append(result.get("toxicity_score", 0.0))
                
                category = result.get("category", "unknown")
                category_counts[category] = category_counts.get(category, 0) + 1
                
            except Exception as e:
                print(f"⚠️ Error processing record for stats: {str(e)}")
                continue
        
        return {
            "total_analyses": total_analyses,
            "toxic_content_rate": (toxic_count / total_analyses) * 100,
            "category_breakdown": category_counts,
            "average_toxicity_score": sum(toxicity_scores) / len(toxicity_scores) if toxicity_scores else 0.0
        }
    
    def _setup_demo_data(self):
        """
        Set up some demo data for testing and demonstration.
        """
        # Add some sample user preferences
        self.user_preferences["demo_user"] = UserPreferences(
            toxicity_threshold=0.6,
            categories_to_filter=[
                ToxicityCategory.HATE_SPEECH,
                ToxicityCategory.CYBERBULLYING,
                ToxicityCategory.THREAT
            ],
            show_explanations=True,
            educational_mode=True,
            wellness_features=True,
            language="en"
        )
    
    def _generate_sample_report(self, user_id: str) -> ToxicityReport:
        """
        Generate a sample toxicity report for demonstration.
        In production, this would analyze real user data.
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)  # Last 30 days
        
        # Generate some realistic sample data
        total_content = 150
        toxic_content = 12
        
        category_breakdown = {
            ToxicityCategory.SAFE: 138,
            ToxicityCategory.INAPPROPRIATE: 7,
            ToxicityCategory.HARASSMENT: 3,
            ToxicityCategory.CYBERBULLYING: 2,
            ToxicityCategory.HATE_SPEECH: 0,
            ToxicityCategory.THREAT: 0
        }
        
        # Calculate wellness score (0-100)
        toxicity_rate = (toxic_content / total_content) * 100
        wellness_score = max(0, 100 - (toxicity_rate * 2))  # Simple calculation
        
        recommendations = [
            "Consider joining more positive communities that align with your interests",
            "Use content filters to reduce exposure to negative content",
            "Take regular breaks from social media to maintain mental health",
            "Report inappropriate content to help keep platforms safe for everyone"
        ]
        
        trend_analysis = (
            "Your digital environment has been relatively healthy this month. "
            f"You encountered toxic content in {toxicity_rate:.1f}% of interactions, "
            "which is below the platform average. Keep up the great work in "
            "choosing positive online spaces!"
        )
        
        return ToxicityReport(
            user_id=user_id,
            report_period_start=start_date,
            report_period_end=end_date,
            total_content_analyzed=total_content,
            toxic_content_detected=toxic_content,
            toxicity_rate=toxicity_rate,
            category_breakdown=category_breakdown,
            trend_analysis=trend_analysis,
            recommendations=recommendations,
            wellness_score=wellness_score
        )
