"""
Football Twitter Bot - Main Bot Logic
Handles monitoring, processing, and posting of football-related content
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set

from ai_processor import AIProcessor
from config import Config
from error_handler import ErrorHandler
from twitter_manager import TwitterManager

logger = logging.getLogger(__name__)

class FootballTwitterBot:
    def __init__(self, config: Config, error_handler: ErrorHandler):
        self.config = config
        self.error_handler = error_handler
        self.ai_processor = AIProcessor(config.groq_api_key)
        self.twitter_manager = TwitterManager()
        
        # Track processed tweets to avoid duplicates
        self.processed_tweets: Set[str] = set()
        self.last_check_time = datetime.now()
        
        # Rate limiting
        self.last_post_time = 0
        self.post_count_today = 0
        self.daily_reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    async def initialize(self):
        """Initialize the bot components"""
        try:
            logger.info("Initializing bot components...")
            
            # Initialize Twitter manager
            await self.twitter_manager.initialize()
            
            # Test AI processor
            await self.ai_processor.test_connection()
            
            logger.info("Bot initialization complete")
            
        except Exception as e:
            logger.error(f"Bot initialization failed: {e}")
            await self.error_handler.send_error(f"Bot initialization failed: {e}")
            raise
    
    async def run_cycle(self):
        """Run one cycle of monitoring and processing"""
        try:
            logger.info("Starting bot cycle...")
            
            # Reset daily post count if needed
            self._check_daily_reset()
            
            # Check if we've hit daily posting limit
            if self.post_count_today >= self.config.max_posts_per_day:
                logger.info(f"Daily posting limit reached ({self.config.max_posts_per_day})")
                return
            
            # Monitor each journalist
            for journalist in self.config.journalists:
                try:
                    await self._monitor_journalist(journalist)
                    await asyncio.sleep(2)  # Small delay between journalists
                except Exception as e:
                    logger.error(f"Error monitoring {journalist['username']}: {e}")
                    await self.error_handler.send_error(
                        f"Error monitoring {journalist['username']}: {e}"
                    )
            
            logger.info("Bot cycle completed")
            
        except Exception as e:
            logger.error(f"Error in bot cycle: {e}")
            await self.error_handler.send_error(f"Bot cycle error: {e}")
    
    async def _monitor_journalist(self, journalist: Dict):
        """Monitor a specific journalist for new tweets"""
        try:
            username = journalist['username']
            logger.info(f"Monitoring {username}...")
            
            # Get recent tweets from the journalist
            tweets = await self.twitter_manager.get_user_tweets(
                username, 
                limit=self.config.tweets_per_check
            )
            
            if not tweets:
                logger.debug(f"No tweets found for {username}")
                return
            
            # Process each tweet
            for tweet in tweets:
                try:
                    # Skip if already processed
                    if tweet['id'] in self.processed_tweets:
                        continue
                    
                    # Skip if tweet is too old
                    if not self._is_recent_tweet(tweet):
                        continue
                    
                    # Check if it's football-related
                    is_football = await self.ai_processor.is_football_related(tweet['text'])
                    
                    if is_football:
                        await self._process_football_tweet(tweet, journalist)
                    
                    # Mark as processed
                    self.processed_tweets.add(tweet['id'])
                    
                    # Limit processed tweets cache size
                    if len(self.processed_tweets) > 10000:
                        # Keep only the most recent 5000
                        self.processed_tweets = set(list(self.processed_tweets)[-5000:])
                
                except Exception as e:
                    logger.error(f"Error processing tweet {tweet.get('id', 'unknown')}: {e}")
                    await self.error_handler.send_error(
                        f"Error processing tweet from {username}: {e}"
                    )
        
        except Exception as e:
            logger.error(f"Error monitoring {username}: {e}")
            raise
    
    async def _process_football_tweet(self, tweet: Dict, journalist: Dict):
        """Process a football-related tweet"""
        try:
            logger.info(f"Processing football tweet from {journalist['username']}")
            
            # Check rate limiting
            if not self._can_post():
                logger.info("Rate limiting: Cannot post yet")
                return
            
            # Analyze and rewrite the tweet
            rewritten_text = await self.ai_processor.rewrite_tweet(
                tweet['text'],
                journalist['username'],
                journalist['reliability_score']
            )
            
            if not rewritten_text:
                logger.warning("Failed to rewrite tweet")
                return
            
            # Add source attribution and reliability score
            formatted_tweet = self._format_final_tweet(
                rewritten_text,
                journalist['username'],
                journalist['reliability_score'],
                journalist.get('tier', 'unknown')
            )
            
            # Post the tweet
            success = await self.twitter_manager.post_tweet(formatted_tweet)
            
            if success:
                self.last_post_time = time.time()
                self.post_count_today += 1
                logger.info(f"Successfully posted tweet from {journalist['username']}")
            else:
                logger.error("Failed to post tweet")
                await self.error_handler.send_error(
                    f"Failed to post tweet from {journalist['username']}"
                )
        
        except Exception as e:
            logger.error(f"Error processing football tweet: {e}")
            await self.error_handler.send_error(f"Error processing football tweet: {e}")
    
    def _format_final_tweet(self, rewritten_text: str, username: str, 
                           reliability_score: float, tier: str) -> str:
        """Format the final tweet with source and reliability score"""
        # Determine reliability emoji and color
        if reliability_score >= 90:
            reliability_emoji = "🟢"
        elif reliability_score >= 70:
            reliability_emoji = "🟡"
        elif reliability_score >= 50:
            reliability_emoji = "🟠"
        else:
            reliability_emoji = "🔴"
        
        # Format the tweet
        formatted_tweet = f"{rewritten_text}\n\n"
        formatted_tweet += f"Source - @{username}\n"
        formatted_tweet += f"[Reliability Score: {reliability_emoji} - {reliability_score}%]"
        
        # Ensure tweet doesn't exceed character limit
        if len(formatted_tweet) > 280:
            # Truncate the rewritten text to fit
            max_rewritten_length = 280 - len(f"\n\nSource - @{username}\n[Reliability Score: {reliability_emoji} - {reliability_score}%]")
            if max_rewritten_length > 50:  # Ensure minimum content length
                rewritten_text = rewritten_text[:max_rewritten_length-3] + "..."
                formatted_tweet = f"{rewritten_text}\n\n"
                formatted_tweet += f"Source - @{username}\n"
                formatted_tweet += f"[Reliability Score: {reliability_emoji} - {reliability_score}%]"
        
        return formatted_tweet
    
    def _is_recent_tweet(self, tweet: Dict) -> bool:
        """Check if tweet is recent enough to process"""
        try:
            # Assuming tweet has created_at field
            # For twscrape, this might be in different format
            # Adjust based on actual tweet structure
            return True  # For now, process all tweets found
        except:
            return True
    
    def _can_post(self) -> bool:
        """Check if we can post (rate limiting)"""
        current_time = time.time()
        
        # Check minimum interval between posts
        if current_time - self.last_post_time < self.config.min_post_interval:
            return False
        
        # Check daily posting limit
        if self.post_count_today >= self.config.max_posts_per_day:
            return False
        
        return True
    
    def _check_daily_reset(self):
        """Reset daily counters if needed"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if today_start > self.daily_reset_time:
            self.post_count_today = 0
            self.daily_reset_time = today_start
            logger.info("Daily post count reset")
    
    async def cleanup(self):
        """Clean up resources"""
        try:
            if self.twitter_manager:
                await self.twitter_manager.cleanup()
            logger.info("Bot cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
