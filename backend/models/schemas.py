"""
Data Models and Schemas for Nirabhi API

These are the blueprints that define how our data looks and behaves.
Think of them as the DNA of our API - they ensure everything is
structured, validated, and easy to understand.

Each model represents a different piece of our content moderation puzzle.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ToxicityCategory(str, Enum):
    """
    Different types of toxic content we can identify.
    Each category helps us provide more specific feedback to users.
    """
    HATE_SPEECH = "hate_speech"
    CYBERBULLYING = "cyberbullying"
    HARASSMENT = "harassment"
    THREAT = "threat"
    SPAM = "spam"
    MISINFORMATION = "misinformation"
    INAPPROPRIATE = "inappropriate"
    SAFE = "safe"

class SeverityLevel(str, Enum):
    """
    How severe is the toxic content?
    This helps us respond appropriately to different situations.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ContentAnalysisRequest(BaseModel):
    """
    What users send us when they want content analyzed.
    Like giving us a piece of text and asking "Is this okay?"
    """
    text: str = Field(
        ...,
        description="The content to analyze for toxicity",
        min_length=1,
        max_length=10000
    )
    context: Optional[str] = Field(
        None,
        description="Additional context that might help with analysis"
    )
    user_preferences: Optional[Dict[str, Any]] = Field(
        None,
        description="User's personal moderation preferences"
    )
    
    @validator('text')
    def text_must_not_be_empty(cls, v):
        """Make sure we actually have content to analyze"""
        if not v.strip():
            raise ValueError('Text content cannot be empty')
        return v.strip()

class ContentAnalysisResponse(BaseModel):
    """
    What we send back after analyzing content.
    It's like a detailed report card for the text.
    """
    text: str = Field(..., description="The original text that was analyzed")
    
    # Core Analysis Results
    toxicity_score: float = Field(
        ...,
        description="Overall toxicity score (0.0 = safe, 1.0 = highly toxic)",
        ge=0.0,
        le=1.0
    )
    
    is_toxic: bool = Field(
        ...,
        description="Whether the content is considered toxic"
    )
    
    category: ToxicityCategory = Field(
        ...,
        description="Primary category of toxicity (if any)"
    )
    
    severity: SeverityLevel = Field(
        ...,
        description="How severe the toxicity is"
    )
    
    # Detailed Analysis
    sentiment_score: float = Field(
        ...,
        description="Sentiment analysis (-1.0 = very negative, 1.0 = very positive)",
        ge=-1.0,
        le=1.0
    )
    
    confidence: float = Field(
        ...,
        description="How confident we are in our analysis",
        ge=0.0,
        le=1.0
    )
    
    # Educational and Helpful Information
    explanation: str = Field(
        ...,
        description="Human-friendly explanation of why content was flagged"
    )
    
    suggestions: List[str] = Field(
        default_factory=list,
        description="Helpful suggestions for improving the content"
    )
    
    support_resources: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Mental health or support resources if needed"
    )
    
    # Metadata
    analysis_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this analysis was performed"
    )
    
    processing_time_ms: Optional[float] = Field(
        None,
        description="How long the analysis took in milliseconds"
    )

class UserPreferences(BaseModel):
    """
    How each user wants their content moderated.
    Because everyone deserves a personalized experience!
    """
    toxicity_threshold: float = Field(
        0.7,
        description="Toxicity score threshold for flagging content",
        ge=0.0,
        le=1.0
    )
    
    categories_to_filter: List[ToxicityCategory] = Field(
        default_factory=lambda: [
            ToxicityCategory.HATE_SPEECH,
            ToxicityCategory.CYBERBULLYING,
            ToxicityCategory.HARASSMENT,
            ToxicityCategory.THREAT
        ],
        description="Which categories of toxic content to filter"
    )
    
    show_explanations: bool = Field(
        True,
        description="Whether to show explanations for flagged content"
    )
    
    educational_mode: bool = Field(
        True,
        description="Whether to provide educational feedback"
    )
    
    wellness_features: bool = Field(
        True,
        description="Whether to enable mental health and wellness features"
    )
    
    language: str = Field(
        "en",
        description="Preferred language for responses",
        regex="^[a-z]{2}$"
    )

class ToxicityReport(BaseModel):
    """
    A comprehensive report about toxicity patterns.
    Like a health checkup for your digital environment.
    """
    user_id: str = Field(..., description="User this report belongs to")
    
    report_period_start: datetime = Field(
        ...,
        description="Start of the reporting period"
    )
    
    report_period_end: datetime = Field(
        ...,
        description="End of the reporting period"
    )
    
    # Statistics
    total_content_analyzed: int = Field(
        ..., 
        description="Total pieces of content analyzed"
    )
    
    toxic_content_detected: int = Field(
        ...,
        description="Number of toxic content pieces detected"
    )
    
    toxicity_rate: float = Field(
        ...,
        description="Percentage of content that was toxic",
        ge=0.0,
        le=100.0
    )
    
    # Category Breakdown
    category_breakdown: Dict[ToxicityCategory, int] = Field(
        default_factory=dict,
        description="Count of each toxicity category detected"
    )
    
    # Trends and Insights
    trend_analysis: Optional[str] = Field(
        None,
        description="Analysis of trends in the user's digital environment"
    )
    
    recommendations: List[str] = Field(
        default_factory=list,
        description="Personalized recommendations for safer browsing"
    )
    
    wellness_score: float = Field(
        ...,
        description="Overall digital wellness score (0-100)",
        ge=0.0,
        le=100.0
    )

class HealthCheck(BaseModel):
    """
    Simple health check response to make sure our API is alive and well.
    """
    status: str = Field(..., description="Current system status")
    message: str = Field(..., description="Friendly status message")
    timestamp: datetime = Field(..., description="When this check was performed")
    version: str = Field(..., description="Current API version")

class AnalysisHistory(BaseModel):
    """
    Historical record of content analysis.
    Helps us learn and improve over time.
    """
    id: str = Field(..., description="Unique identifier for this analysis")
    user_id: Optional[str] = Field(None, description="User who requested the analysis")
    original_text: str = Field(..., description="The content that was analyzed")
    analysis_result: ContentAnalysisResponse = Field(..., description="The analysis results")
    feedback: Optional[str] = Field(None, description="User feedback on the analysis")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class ErrorResponse(BaseModel):
    """
    When things go wrong, we want to communicate clearly and helpfully.
    """
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-friendly error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    support_contact: str = Field(
        default="team@nirabhi.ai",
        description="How to get help with this error"
    )
