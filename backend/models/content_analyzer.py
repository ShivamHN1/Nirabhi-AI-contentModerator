"""
The AI Brain of Nirabhi - Content Analyzer

This is where the magic happens! Our content analyzer uses multiple AI models
to understand and evaluate text content for toxicity, sentiment, and harm.

It's like having a wise, patient teacher who can instantly understand
the emotional impact and safety of any piece of text.
"""

import re
import time
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

# AI and ML libraries
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch

# Our custom models
from .schemas import (
    ContentAnalysisResponse,
    ToxicityCategory,
    SeverityLevel,
    UserPreferences
)

class ContentAnalyzer:
    """
    The heart of our AI system - analyzes content for toxicity and provides
    helpful feedback to create safer digital spaces.
    """
    
    def __init__(self):
        """
        Initialize our AI analyzer.
        We start empty but ready to learn!
        """
        self.toxicity_classifier = None
        self.sentiment_analyzer = None
        self.is_initialized = False
        
        # Precompiled regex patterns for quick detection
        self.hate_speech_patterns = self._compile_hate_speech_patterns()
        self.threat_patterns = self._compile_threat_patterns()
        self.profanity_patterns = self._compile_profanity_patterns()
        
        # Support resources for users who need help
        self.support_resources = self._load_support_resources()
    
    async def initialize(self):
        """
        Wake up our AI models and get them ready for action!
        This is like warming up before a workout.
        """
        if self.is_initialized:
            return
            
        try:
            print("🧠 Loading AI models for content analysis...")
            
            # Load a lightweight but effective toxicity detection model
            # Using DistilBERT for speed while maintaining accuracy
            self.toxicity_classifier = pipeline(
                "text-classification",
                model="unitary/toxic-bert",
                device=0 if torch.cuda.is_available() else -1,
                return_all_scores=True
            )
            
            # Initialize VADER sentiment analyzer (great for social media text!)
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            
            self.is_initialized = True
            print("✅ AI models loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading AI models: {str(e)}")
            # Fallback to rule-based analysis if models fail to load
            self.toxicity_classifier = None
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            self.is_initialized = True
            print("⚠️ Using fallback rule-based analysis")
    
    async def analyze_text(
        self,
        text: str,
        context: Optional[str] = None,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> ContentAnalysisResponse:
        """
        The main analysis function - where we examine text and provide insights.
        
        This is like having a conversation with the text to understand:
        - Is it harmful or toxic?
        - What emotions does it carry?
        - How can we help make it better?
        """
        start_time = time.time()
        
        if not self.is_initialized:
            await self.initialize()
        
        # Clean and prepare the text
        cleaned_text = self._preprocess_text(text)
        
        # Run multiple analysis methods
        toxicity_analysis = await self._analyze_toxicity(cleaned_text)
        sentiment_analysis = self._analyze_sentiment(cleaned_text)
        pattern_analysis = self._analyze_patterns(cleaned_text)
        
        # Combine all our insights
        combined_score = self._combine_analysis_scores(
            toxicity_analysis,
            sentiment_analysis,
            pattern_analysis
        )
        
        # Determine the primary category and severity
        category = self._determine_category(
            toxicity_analysis,
            pattern_analysis,
            combined_score
        )
        
        severity = self._determine_severity(combined_score, category)
        
        # Generate helpful explanations and suggestions
        explanation = self._generate_explanation(
            category,
            combined_score,
            text
        )
        
        suggestions = self._generate_suggestions(
            category,
            text,
            user_preferences
        )
        
        # Get support resources if needed
        support_resources = None
        if combined_score > 0.7 or category in [
            ToxicityCategory.THREAT,
            ToxicityCategory.CYBERBULLYING,
            ToxicityCategory.HATE_SPEECH
        ]:
            support_resources = self.support_resources
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        return ContentAnalysisResponse(
            text=text,
            toxicity_score=combined_score,
            is_toxic=combined_score > 0.5,  # Default threshold
            category=category,
            severity=severity,
            sentiment_score=sentiment_analysis['compound'],
            confidence=self._calculate_confidence(toxicity_analysis, pattern_analysis),
            explanation=explanation,
            suggestions=suggestions,
            support_resources=support_resources,
            analysis_timestamp=datetime.utcnow(),
            processing_time_ms=processing_time
        )
    
    def _preprocess_text(self, text: str) -> str:
        """
        Clean up the text for better analysis.
        Like washing vegetables before cooking!
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Normalize some common internet language
        text = re.sub(r'(.)\1{3,}', r'\1\1', text)  # Reduce repeated characters
        
        return text
    
    async def _analyze_toxicity(self, text: str) -> Dict[str, float]:
        """
        Use our AI model to detect toxicity.
        This is the main AI-powered analysis.
        """
        if not self.toxicity_classifier:
            # Fallback to simple rule-based analysis
            return self._rule_based_toxicity_analysis(text)
        
        try:
            # Run the text through our toxicity classifier
            results = self.toxicity_classifier(text)
            
            # Convert results to our format
            scores = {}
            for result in results[0]:  # results is a list of lists
                label = result['label'].lower()
                score = result['score']
                
                if 'toxic' in label or 'hate' in label:
                    scores['toxicity'] = score
                elif 'severe' in label:
                    scores['severe_toxicity'] = score
                elif 'obscene' in label:
                    scores['obscene'] = score
                elif 'threat' in label:
                    scores['threat'] = score
                elif 'insult' in label:
                    scores['insult'] = score
            
            return scores
            
        except Exception as e:
            print(f"⚠️ AI model error, using fallback: {str(e)}")
            return self._rule_based_toxicity_analysis(text)
    
    def _rule_based_toxicity_analysis(self, text: str) -> Dict[str, float]:
        """
        Fallback analysis using patterns and rules.
        Sometimes the old ways are reliable!
        """
        text_lower = text.lower()
        scores = {
            'toxicity': 0.0,
            'severe_toxicity': 0.0,
            'obscene': 0.0,
            'threat': 0.0,
            'insult': 0.0
        }
        
        # Check for hate speech patterns
        hate_matches = sum(1 for pattern in self.hate_speech_patterns 
                          if pattern.search(text_lower))
        if hate_matches > 0:
            scores['toxicity'] = min(0.3 + (hate_matches * 0.2), 1.0)
        
        # Check for threats
        threat_matches = sum(1 for pattern in self.threat_patterns 
                           if pattern.search(text_lower))
        if threat_matches > 0:
            scores['threat'] = min(0.4 + (threat_matches * 0.3), 1.0)
            scores['severe_toxicity'] = max(scores['severe_toxicity'], 0.7)
        
        # Check for profanity
        profanity_matches = sum(1 for pattern in self.profanity_patterns 
                              if pattern.search(text_lower))
        if profanity_matches > 0:
            scores['obscene'] = min(0.2 + (profanity_matches * 0.2), 1.0)
            scores['insult'] = min(0.3 + (profanity_matches * 0.1), 1.0)
        
        return scores
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Understand the emotional tone of the text.
        Are people being kind or mean?
        """
        return self.sentiment_analyzer.polarity_scores(text)
    
    def _analyze_patterns(self, text: str) -> Dict[str, bool]:
        """
        Look for specific patterns that indicate different types of problems.
        """
        text_lower = text.lower()
        
        return {
            'has_hate_speech': any(pattern.search(text_lower) 
                                  for pattern in self.hate_speech_patterns),
            'has_threats': any(pattern.search(text_lower) 
                              for pattern in self.threat_patterns),
            'has_profanity': any(pattern.search(text_lower) 
                                for pattern in self.profanity_patterns),
            'excessive_caps': len(re.findall(r'[A-Z]{4,}', text)) > 2,
            'excessive_punctuation': len(re.findall(r'[!?]{3,}', text)) > 0
        }
    
    def _combine_analysis_scores(
        self,
        toxicity_analysis: Dict[str, float],
        sentiment_analysis: Dict[str, float],
        pattern_analysis: Dict[str, bool]
    ) -> float:
        """
        Combine all our analysis methods into one final toxicity score.
        Like mixing ingredients to make the perfect recipe!
        """
        # Start with the main toxicity score
        base_score = toxicity_analysis.get('toxicity', 0.0)
        
        # Boost score based on severe toxicity
        if toxicity_analysis.get('severe_toxicity', 0.0) > 0.5:
            base_score = max(base_score, 0.8)
        
        # Factor in threats (very serious!)
        if toxicity_analysis.get('threat', 0.0) > 0.3:
            base_score = max(base_score, 0.9)
        
        # Consider sentiment - very negative sentiment can indicate toxicity
        sentiment_score = sentiment_analysis.get('compound', 0.0)
        if sentiment_score < -0.5:
            base_score = max(base_score, abs(sentiment_score) * 0.6)
        
        # Pattern-based adjustments
        if pattern_analysis.get('has_threats'):
            base_score = max(base_score, 0.85)
        if pattern_analysis.get('has_hate_speech'):
            base_score = max(base_score, 0.75)
        if pattern_analysis.get('excessive_caps') and pattern_analysis.get('has_profanity'):
            base_score = min(base_score + 0.2, 1.0)
        
        return min(base_score, 1.0)
    
    def _determine_category(
        self,
        toxicity_analysis: Dict[str, float],
        pattern_analysis: Dict[str, bool],
        combined_score: float
    ) -> ToxicityCategory:
        """
        Figure out what type of toxicity we're dealing with.
        """
        if combined_score < 0.3:
            return ToxicityCategory.SAFE
        
        # Check for specific threat patterns
        if (pattern_analysis.get('has_threats') or 
            toxicity_analysis.get('threat', 0.0) > 0.4):
            return ToxicityCategory.THREAT
        
        # Check for hate speech
        if (pattern_analysis.get('has_hate_speech') or
            combined_score > 0.7):
            return ToxicityCategory.HATE_SPEECH
        
        # Check for cyberbullying indicators
        if (toxicity_analysis.get('insult', 0.0) > 0.5 and
            combined_score > 0.6):
            return ToxicityCategory.CYBERBULLYING
        
        # Check for harassment
        if combined_score > 0.5:
            return ToxicityCategory.HARASSMENT
        
        # Default to inappropriate for mild toxicity
        return ToxicityCategory.INAPPROPRIATE
    
    def _determine_severity(
        self,
        combined_score: float,
        category: ToxicityCategory
    ) -> SeverityLevel:
        """
        How serious is this content?
        """
        if category == ToxicityCategory.THREAT:
            return SeverityLevel.CRITICAL
        
        if combined_score >= 0.8:
            return SeverityLevel.HIGH
        elif combined_score >= 0.6:
            return SeverityLevel.MEDIUM
        elif combined_score >= 0.3:
            return SeverityLevel.LOW
        else:
            return SeverityLevel.LOW
    
    def _generate_explanation(
        self,
        category: ToxicityCategory,
        score: float,
        text: str
    ) -> str:
        """
        Explain to users why content was flagged.
        Education is key to building better digital habits!
        """
        if category == ToxicityCategory.SAFE:
            return "This content appears to be safe and appropriate for most audiences."
        
        explanations = {
            ToxicityCategory.HATE_SPEECH: (
                "This content contains language that may be hurtful or discriminatory "
                "towards individuals or groups based on their identity."
            ),
            ToxicityCategory.CYBERBULLYING: (
                "This content contains language that could be perceived as bullying, "
                "intimidating, or meant to cause emotional harm to someone."
            ),
            ToxicityCategory.HARASSMENT: (
                "This content contains language that may be considered harassing "
                "or repeatedly targeting someone in a negative way."
            ),
            ToxicityCategory.THREAT: (
                "This content contains language that could be interpreted as a threat "
                "or expression of intent to cause harm."
            ),
            ToxicityCategory.INAPPROPRIATE: (
                "This content contains language that may not be appropriate "
                "for all audiences or contexts."
            )
        }
        
        base_explanation = explanations.get(
            category,
            "This content has been flagged for potential toxicity."
        )
        
        if score < 0.5:
            return base_explanation + " The content is borderline and context may be important."
        elif score < 0.7:
            return base_explanation + " The content shows moderate signs of toxicity."
        else:
            return base_explanation + " The content shows strong indicators of toxicity."
    
    def _generate_suggestions(
        self,
        category: ToxicityCategory,
        text: str,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Provide helpful suggestions for improving content.
        We want to teach, not just punish!
        """
        if category == ToxicityCategory.SAFE:
            return ["Great job! This content promotes positive communication."]
        
        suggestions = []
        
        base_suggestions = {
            ToxicityCategory.HATE_SPEECH: [
                "Consider using more inclusive language that doesn't target or demean groups of people",
                "Think about how your words might affect someone from the group you're discussing",
                "Try expressing your viewpoint without using language that could hurt others"
            ],
            ToxicityCategory.CYBERBULLYING: [
                "Consider how the recipient might feel reading this message",
                "Try expressing disagreement without personal attacks",
                "Think about whether this comment builds up or tears down the conversation"
            ],
            ToxicityCategory.HARASSMENT: [
                "Consider giving the person space rather than continuing to engage negatively",
                "Try focusing on the topic rather than the person",
                "Ask yourself if this comment is constructive or just venting"
            ],
            ToxicityCategory.THREAT: [
                "Express disagreement or frustration without mentioning harm",
                "Consider taking a break before responding when you're angry",
                "Remember that threats can have serious legal and personal consequences"
            ]
        }
        
        suggestions.extend(base_suggestions.get(category, [
            "Consider rephrasing your message in a more positive way",
            "Think about the impact your words might have on others",
            "Try expressing your thoughts with more empathy and understanding"
        ]))
        
        # Add general wellness suggestions
        suggestions.append("Remember: kind words can make someone's day better!")
        
        return suggestions[:3]  # Keep it concise
    
    def _calculate_confidence(
        self,
        toxicity_analysis: Dict[str, float],
        pattern_analysis: Dict[str, bool]
    ) -> float:
        """
        How confident are we in our analysis?
        Honesty about uncertainty is important!
        """
        confidence = 0.5  # Base confidence
        
        # Higher confidence if we have clear AI model results
        if toxicity_analysis.get('toxicity', 0.0) > 0.1:
            confidence += 0.3
        
        # Higher confidence if patterns match
        pattern_matches = sum(1 for v in pattern_analysis.values() if v)
        confidence += min(pattern_matches * 0.1, 0.2)
        
        return min(confidence, 0.95)  # Never be 100% confident
    
    def _compile_hate_speech_patterns(self) -> List[re.Pattern]:
        """
        Compile regex patterns for detecting hate speech.
        These are basic patterns - real systems would use more sophisticated detection.
        """
        patterns = [
            r'\b(hate|despise|loathe)\s+(you|them|those)\b',
            r'\b(kill|die|death)\s+(yourself|yourselves)\b',
            r'\b(stupid|idiot|moron)\s+(people|person)\b',
        ]
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def _compile_threat_patterns(self) -> List[re.Pattern]:
        """
        Compile regex patterns for detecting threats.
        """
        patterns = [
            r'\b(going\s+to|gonna|will)\s+(kill|hurt|harm|beat|destroy)\b',
            r'\b(watch\s+out|be\s+careful|you\s+better)\b',
            r'\bor\s+else\b',
        ]
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def _compile_profanity_patterns(self) -> List[re.Pattern]:
        """
        Compile basic profanity detection patterns.
        This is a simplified version - production systems would use comprehensive lists.
        """
        # Basic pattern matching for demonstration
        # Real systems would use more sophisticated profanity databases
        patterns = [
            r'\b[a-z]*sh[i1]t[a-z]*\b',
            r'\b[a-z]*d[a4]mn[a-z]*\b',
            r'\b[a-z]*cr[a4]p[a-z]*\b',
        ]
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def _load_support_resources(self) -> List[Dict[str, str]]:
        """
        Load mental health and support resources for users who need help.
        """
        return [
            {
                "name": "Crisis Text Line",
                "description": "Free 24/7 support via text message",
                "contact": "Text HOME to 741741",
                "url": "https://www.crisistextline.org/"
            },
            {
                "name": "National Suicide Prevention Lifeline",
                "description": "Free and confidential support 24/7",
                "contact": "988",
                "url": "https://suicidepreventionlifeline.org/"
            },
            {
                "name": "StopBullying.gov",
                "description": "Resources for dealing with cyberbullying",
                "contact": "Online resources",
                "url": "https://www.stopbullying.gov/"
            }
        ]
