"""
Error handling and logging system
Centralized error management for the API
"""

import logging
from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class APIException(Exception):
    """Custom API exception class"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

async def api_exception_handler(request: Request, exc: APIException):
    """Handle custom API exceptions"""
    logger.error(f"API Exception: {exc.detail} - Status: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}\nTraceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    logger.warning(f"HTTP Exception: {exc.detail} - Status: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

def log_request(request: Request):
    """Log API requests"""
    logger.info(f"Request: {request.method} {request.url}")

def log_database_error(error: Exception, operation: str):
    """Log database-related errors"""
    logger.error(f"Database error during {operation}: {str(error)}")

def log_data_collection_error(error: Exception, source: str):
    """Log data collection errors"""
    logger.error(f"Data collection error from {source}: {str(error)}")

def log_prediction_error(error: Exception, game_id: int):
    """Log AI prediction errors"""
    logger.error(f"Prediction error for game {game_id}: {str(error)}")

# Success logging
def log_successful_operation(operation: str, details: str = ""):
    """Log successful operations"""
    logger.info(f"Success: {operation} {details}")

if __name__ == "__main__":
    # Test logging system
    print("Testing error handling and logging...")

    # Test different log levels
    logger.info("✅ Info logging working")
    logger.warning("⚠️ Warning logging working")
    logger.error("❌ Error logging working")

    # Test custom functions
    log_successful_operation("Database connection", "- Connected to sports_betting.db")
    log_database_error(Exception("Test error"), "user authentication")

    print("✅ Error handling and logging system ready!")
    print("📝 Check 'app.log' file for logged messages")
