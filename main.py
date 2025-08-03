#!/usr/bin/env python3
"""
Football Twitter Bot - Main Entry Point
Monitors football journalists, rates credibility, and reposts with improved formatting
"""

import asyncio
import logging
import os
import signal
import sys
from datetime import datetime

from bot import FootballTwitterBot
from config import Config
from error_handler import ErrorHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BotManager:
    def __init__(self):
        self.bot = None
        self.running = False
        
    async def start(self):
        """Start the bot with proper error handling"""
        try:
            # Load configuration
            config = Config()
            
            # Initialize error handler
            error_handler = ErrorHandler(config.webhook_url)
            
            # Initialize bot
            self.bot = FootballTwitterBot(config, error_handler)
            
            # Setup signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            logger.info("Starting Football Twitter Bot...")
            await self.bot.initialize()
            
            self.running = True
            logger.info("Bot started successfully!")
            
            # Main bot loop
            while self.running:
                try:
                    await self.bot.run_cycle()
                    await asyncio.sleep(config.check_interval)
                except Exception as e:
                    logger.error(f"Error in bot cycle: {e}")
                    await error_handler.send_error(f"Bot cycle error: {e}")
                    await asyncio.sleep(30)  # Wait before retrying
                    
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            if hasattr(self, 'error_handler'):
                await self.error_handler.send_error(f"Bot startup failed: {e}")
            sys.exit(1)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    async def stop(self):
        """Stop the bot gracefully"""
        self.running = False
        if self.bot:
            await self.bot.cleanup()
        logger.info("Bot stopped")

async def main():
    """Main function"""
    manager = BotManager()
    
    try:
        await manager.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        await manager.stop()

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        sys.exit(1)
    
    # Run the bot
    asyncio.run(main())
