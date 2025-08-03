"""
Football Twitter Bot - Error Handling Module
Handles error reporting and webhook notifications
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)

class ErrorHandler:
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self.session = None
        self.error_count = 0
        self.last_error_time = None
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def send_error(self, error_message: str, error_type: str = "ERROR", 
                        include_timestamp: bool = True):
        """Send error notification via webhook"""
        try:
            self.error_count += 1
            self.last_error_time = datetime.now()
            
            # Log the error locally
            logger.error(f"[{error_type}] {error_message}")
            
            # Send webhook notification if configured
            if self.webhook_url:
                await self._send_webhook_notification(error_message, error_type, include_timestamp)
            else:
                logger.warning("Webhook URL not configured, error notification not sent")
                
        except Exception as e:
            logger.error(f"Error in error handler: {e}")
    
    async def _send_webhook_notification(self, error_message: str, error_type: str, 
                                       include_timestamp: bool):
        """Send notification to webhook endpoint"""
        try:
            session = await self._get_session()
            
            # Prepare the payload
            payload = {
                "error_type": error_type,
                "message": error_message,
                "error_count": self.error_count,
                "bot_name": "Football Twitter Bot"
            }
            
            if include_timestamp:
                payload["timestamp"] = datetime.now().isoformat()
            
            # Send to webhook
            async with session.post(
                self.webhook_url,
                json=payload,
                timeout=10
            ) as response:
                if response.status == 200:
                    logger.debug("Error notification sent successfully")
                else:
                    logger.warning(f"Webhook notification failed: {response.status}")
                    
        except asyncio.TimeoutError:
            logger.warning("Webhook notification timed out")
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
    
    async def send_info(self, message: str):
        """Send informational message via webhook"""
        await self.send_error(message, error_type="INFO")
    
    async def send_warning(self, message: str):
        """Send warning message via webhook"""
        await self.send_error(message, error_type="WARNING")
    
    async def send_critical(self, message: str):
        """Send critical error message via webhook"""
        await self.send_error(message, error_type="CRITICAL")
    
    async def send_startup_notification(self):
        """Send notification when bot starts up"""
        message = f"Football Twitter Bot started successfully at {datetime.now().isoformat()}"
        await self.send_info(message)
    
    async def send_shutdown_notification(self):
        """Send notification when bot shuts down"""
        message = f"Football Twitter Bot shutting down at {datetime.now().isoformat()}"
        await self.send_info(message)
    
    async def send_daily_summary(self, posts_count: int, errors_count: int):
        """Send daily summary via webhook"""
        message = f"Daily Summary - Posts: {posts_count}, Errors: {errors_count}"
        await self.send_info(message)
    
    def get_error_stats(self) -> dict:
        """Get error statistics"""
        return {
            "total_errors": self.error_count,
            "last_error_time": self.last_error_time.isoformat() if self.last_error_time else None,
            "webhook_configured": self.webhook_url is not None
        }
    
    async def test_webhook(self) -> bool:
        """Test webhook connectivity"""
        if not self.webhook_url:
            logger.warning("No webhook URL configured for testing")
            return False
        
        try:
            test_message = "Webhook test from Football Twitter Bot"
            await self._send_webhook_notification(test_message, "TEST", True)
            logger.info("Webhook test completed")
            return True
        except Exception as e:
            logger.error(f"Webhook test failed: {e}")
            return False
    
    async def cleanup(self):
        """Clean up resources"""
        try:
            if self.session and not self.session.closed:
                await self.session.close()
            logger.debug("Error handler cleanup completed")
        except Exception as e:
            logger.error(f"Error during error handler cleanup: {e}")

# Custom exception classes for different types of errors
class TwitterAPIError(Exception):
    """Raised when Twitter API operations fail"""
    pass

class AIProcessingError(Exception):
    """Raised when AI processing fails"""
    pass

class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass

class RateLimitError(Exception):
    """Raised when rate limits are exceeded"""
    pass
