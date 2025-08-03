#!/usr/bin/env python3
"""
Health Check Script for Render Deployment
Provides a simple HTTP endpoint to check bot status
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from aiohttp import web
from config import Config
from ai_processor import AIProcessor

logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self):
        self.config = Config()
        groq_key = self.config.groq_api_key or ""
        self.ai_processor = AIProcessor(groq_key)
        self.start_time = datetime.now()
        
    async def health_check(self, request):
        """Health check endpoint"""
        try:
            # Check AI processor connection
            ai_status = await self._check_ai_connection()
            
            # Get basic status
            uptime = datetime.now() - self.start_time
            
            status = {
                "status": "healthy" if ai_status else "degraded",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": int(uptime.total_seconds()),
                "components": {
                    "ai_processor": "healthy" if ai_status else "unhealthy",
                    "config": "healthy" if len(self.config.journalists) > 0 else "unhealthy"
                },
                "stats": {
                    "journalists_configured": len(self.config.journalists),
                    "enabled_journalists": len(self.config.get_enabled_journalists())
                }
            }
            
            return web.json_response(status)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return web.json_response({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }, status=500)
    
    async def _check_ai_connection(self):
        """Check if AI processor is working"""
        try:
            await self.ai_processor.test_connection()
            return True
        except:
            return False

async def init_app():
    """Initialize the web application"""
    health_checker = HealthChecker()
    app = web.Application()
    app.router.add_get('/health', health_checker.health_check)
    app.router.add_get('/', health_checker.health_check)
    return app

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        app = asyncio.run(init_app())
        web.run_app(app, host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error(f"Health check server failed to start: {e}")
        sys.exit(1)