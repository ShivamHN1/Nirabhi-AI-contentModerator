"""
Beautiful Logging for Nirabhi

Because good logs make debugging a joy instead of a nightmare!
This sets up colorful, informative logging that helps us understand
what's happening in our application.
"""

import sys
import logging
from typing import Optional
from loguru import logger
from rich.console import Console
from rich.logging import RichHandler

def setup_logger(log_level: str = "INFO") -> logging.Logger:
    """
    Set up a beautiful, informative logger for our application.
    
    This creates logs that are:
    - Colorful and easy to read
    - Informative with context
    - Properly formatted
    - Fun to look at (yes, logs can be fun!)
    """
    
    # Remove the default loguru handler
    logger.remove()
    
    # Create a rich console for beautiful output
    console = Console()
    
    # Add a custom format that's both informative and pretty
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Add the new handler with our custom format
    logger.add(
        sys.stdout,
        format=log_format,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Also add a file handler for persistent logging
    logger.add(
        "nirabhi.log",
        format=log_format,
        level=log_level,
        rotation="10 MB",  # Rotate when file gets too big
        retention="7 days",  # Keep logs for a week
        compression="zip",  # Compress old logs
        backtrace=True,
        diagnose=True
    )
    
    # Create a standard logger that plays nice with other libraries
    class InterceptHandler(logging.Handler):
        """
        Intercept standard logging calls and route them through loguru
        """
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Set up the interceptor for standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Silence some noisy third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("transformers").setLevel(logging.WARNING)
    
    # Return the loguru logger (it works great as a standard logger too!)
    return logger

def log_api_call(endpoint: str, method: str, user_id: Optional[str] = None):
    """
    Log an API call in a consistent, informative way.
    """
    user_info = f" (user: {user_id})" if user_id else ""
    logger.info(f"🔗 API Call: {method} {endpoint}{user_info}")

def log_analysis_start(text_preview: str, user_id: Optional[str] = None):
    """
    Log the start of a content analysis.
    """
    preview = text_preview[:50] + "..." if len(text_preview) > 50 else text_preview
    user_info = f" for user {user_id}" if user_id else ""
    logger.info(f"🔍 Starting analysis{user_info}: '{preview}'")

def log_analysis_complete(toxicity_score: float, category: str, processing_time_ms: float):
    """
    Log the completion of a content analysis.
    """
    logger.info(
        f"✅ Analysis complete: {toxicity_score:.3f} toxicity "
        f"({category}) in {processing_time_ms:.1f}ms"
    )

def log_error_with_context(error: Exception, context: str):
    """
    Log an error with helpful context information.
    """
    logger.error(f"❌ Error in {context}: {str(error)}", exc_info=True)

def log_startup_banner():
    """
    Log a beautiful startup banner because first impressions matter!
    """
    banner = """
🛡️  Nirabhi - AI-Powered Content Moderator
   Creating safer digital spaces through intelligent analysis
   
   Ready to make the internet a kinder place! ✨
    """
    logger.info(banner)

def log_shutdown_message():
    """
    Log a friendly shutdown message.
    """
    logger.info("👋 Nirabhi is shutting down. Thanks for making the internet safer!")

# Example usage and testing
if __name__ == "__main__":
    # Test our logger setup
    test_logger = setup_logger("DEBUG")
    
    log_startup_banner()
    
    # Test different log levels
    logger.debug("🔍 This is a debug message - for developer eyes only!")
    logger.info("ℹ️ This is an info message - general information")
    logger.warning("⚠️ This is a warning - something might be wrong")
    logger.error("❌ This is an error - something went wrong")
    
    # Test API logging
    log_api_call("/analyze", "POST", "user123")
    
    # Test analysis logging
    log_analysis_start("This is some test content for analysis", "user123")
    log_analysis_complete(0.2, "safe", 156.7)
    
    # Test error logging
    try:
        # Intentionally cause an error
        1 / 0
    except Exception as e:
        log_error_with_context(e, "testing error logging")
    
    logger.info("🎉 Logger testing complete!")
