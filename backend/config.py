"""
Configuration Settings for Nirabhi

This file contains all the configurable settings for our application.
It makes it easy to adjust behavior without changing code, and helps
us manage different environments (development, staging, production).
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or defaults.
    
    This uses Pydantic's BaseSettings to automatically load configuration
    from environment variables, making it easy to deploy in different environments.
    """
    
    # Application Information
    app_name: str = Field(default="Nirabhi AI Content Moderator", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    reload: bool = Field(default=True, env="RELOAD")  # Auto-reload for development
    
    # API Configuration
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001"
        ],
        env="CORS_ORIGINS"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./nirabhi.db",  # Simple SQLite for MVP
        env="DATABASE_URL"
    )
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")  # Log SQL queries
    
    # Redis Configuration (for caching and background tasks)
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # AI Model Configuration
    toxicity_model_name: str = Field(
        default="unitary/toxic-bert",
        env="TOXICITY_MODEL_NAME"
    )
    use_gpu: bool = Field(default=False, env="USE_GPU")  # Set to True if GPU available
    model_cache_dir: str = Field(default="./model_cache", env="MODEL_CACHE_DIR")
    
    # Content Analysis Settings
    max_text_length: int = Field(default=10000, env="MAX_TEXT_LENGTH")
    default_toxicity_threshold: float = Field(default=0.7, env="DEFAULT_TOXICITY_THRESHOLD")
    analysis_timeout_seconds: int = Field(default=30, env="ANALYSIS_TIMEOUT_SECONDS")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_burst: int = Field(default=10, env="RATE_LIMIT_BURST")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")  # json or text
    log_file: str = Field(default="nirabhi.log", env="LOG_FILE")
    
    # Security Settings
    secret_key: str = Field(
        default="your-secret-key-change-this-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Feature Flags
    enable_analytics: bool = Field(default=True, env="ENABLE_ANALYTICS")
    enable_user_feedback: bool = Field(default=True, env="ENABLE_USER_FEEDBACK")
    enable_wellness_features: bool = Field(default=True, env="ENABLE_WELLNESS_FEATURES")
    enable_educational_mode: bool = Field(default=True, env="ENABLE_EDUCATIONAL_MODE")
    
    # External API Keys (if needed)
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # Monitoring and Observability
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    # Content Moderation Policies
    strict_mode: bool = Field(default=False, env="STRICT_MODE")
    family_friendly_mode: bool = Field(default=False, env="FAMILY_FRIENDLY_MODE")
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"  # Load from .env file if present
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def get_database_url(self) -> str:
        """
        Get the properly formatted database URL.
        Handles different database types and environments.
        """
        if self.environment == "production":
            # In production, we'd typically use PostgreSQL
            if not self.database_url.startswith("postgresql://"):
                return f"postgresql://user:password@localhost/nirabhi"
        
        return self.database_url
    
    def is_development(self) -> bool:
        """Check if we're running in development mode"""
        return self.environment.lower() in ["development", "dev", "local"]
    
    def is_production(self) -> bool:
        """Check if we're running in production mode"""
        return self.environment.lower() in ["production", "prod"]
    
    def get_cors_origins(self) -> List[str]:
        """
        Get CORS origins based on environment.
        More permissive in development, strict in production.
        """
        if self.is_development():
            return self.cors_origins + ["*"]  # Allow all in dev
        return self.cors_origins
    
    def get_log_level(self) -> str:
        """Get appropriate log level for the environment"""
        if self.is_development():
            return "DEBUG"
        elif self.is_production():
            return "WARNING"
        return self.log_level

# Create a global settings instance
settings = Settings()

# Environment-specific configurations
def get_development_settings() -> Settings:
    """Get settings optimized for development"""
    dev_settings = Settings(
        environment="development",
        debug=True,
        reload=True,
        log_level="DEBUG",
        database_echo=True,
        rate_limit_per_minute=1000,  # More permissive for testing
    )
    return dev_settings

def get_production_settings() -> Settings:
    """Get settings optimized for production"""
    prod_settings = Settings(
        environment="production",
        debug=False,
        reload=False,
        log_level="WARNING",
        database_echo=False,
        rate_limit_per_minute=60,
    )
    return prod_settings

def get_testing_settings() -> Settings:
    """Get settings optimized for testing"""
    test_settings = Settings(
        environment="testing",
        database_url="sqlite:///:memory:",  # In-memory database for tests
        log_level="ERROR",  # Reduce noise during tests
        rate_limit_per_minute=10000,  # No rate limiting in tests
        enable_analytics=False,  # Disable analytics in tests
    )
    return test_settings

# Utility functions for common configuration needs
def get_ai_model_config() -> dict:
    """Get AI model configuration"""
    return {
        "model_name": settings.toxicity_model_name,
        "use_gpu": settings.use_gpu,
        "cache_dir": settings.model_cache_dir,
        "max_length": settings.max_text_length,
        "timeout": settings.analysis_timeout_seconds
    }

def get_security_config() -> dict:
    """Get security-related configuration"""
    return {
        "secret_key": settings.secret_key,
        "algorithm": settings.algorithm,
        "token_expire_minutes": settings.access_token_expire_minutes,
        "rate_limit_per_minute": settings.rate_limit_per_minute,
        "rate_limit_burst": settings.rate_limit_burst
    }

def get_feature_flags() -> dict:
    """Get all feature flags"""
    return {
        "analytics": settings.enable_analytics,
        "user_feedback": settings.enable_user_feedback,
        "wellness_features": settings.enable_wellness_features,
        "educational_mode": settings.enable_educational_mode,
        "metrics": settings.enable_metrics,
        "strict_mode": settings.strict_mode,
        "family_friendly_mode": settings.family_friendly_mode
    }

# Print configuration summary (useful for debugging)
def print_config_summary():
    """Print a summary of current configuration"""
    print(f"""
🛡️ Nirabhi Configuration Summary
================================
Environment: {settings.environment}
Debug Mode: {settings.debug}
Host: {settings.host}:{settings.port}
Database: {settings.get_database_url()}
AI Model: {settings.toxicity_model_name}
Log Level: {settings.get_log_level()}
Features: {', '.join(f for f, enabled in get_feature_flags().items() if enabled)}
================================
    """)

if __name__ == "__main__":
    # Test our configuration
    print_config_summary()
    
    # Show how different environments work
    print("\n🔧 Development Settings:")
    dev = get_development_settings()
    print(f"  Debug: {dev.debug}, Log Level: {dev.log_level}")
    
    print("\n🚀 Production Settings:")
    prod = get_production_settings()
    print(f"  Debug: {prod.debug}, Log Level: {prod.log_level}")
    
    print("\n🧪 Testing Settings:")
    test = get_testing_settings()
    print(f"  Database: {test.database_url}, Analytics: {test.enable_analytics}")
