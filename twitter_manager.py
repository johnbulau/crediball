"""
Football Twitter Bot - Twitter Management Module
Handles Twitter scraping and posting using twscrape library
"""

import asyncio
import logging
import os
import random
from typing import Dict, List, Optional

# Note: twscrape needs to be installed via pip
try:
    from twscrape import API, gather
    from twscrape.models import Tweet
except ImportError:
    logger = logging.getLogger(__name__)
    logger.error("twscrape library not found. Install with: pip install twscrape")
    raise

from twitter_poster import TwitterPoster, TwitterPosterSimulator

logger = logging.getLogger(__name__)

class TwitterManager:
    def __init__(self):
        self.api = None
        self.poster = None
        self.initialized = False
        self.posting_enabled = False
    
    async def initialize(self):
        """Initialize the Twitter API client and poster"""
        try:
            # Initialize scraping API
            self.api = API()
            
            # Initialize posting system
            posting_mode = os.getenv('TWITTER_POSTING_MODE', 'simulator')
            
            if posting_mode == 'real' and all([
                os.getenv('TWITTER_POST_USERNAME'),
                os.getenv('TWITTER_POST_PASSWORD')
            ]):
                try:
                    logger.info("Initializing real Twitter poster...")
                    self.poster = TwitterPoster()
                    await self.poster.initialize()
                    self.posting_enabled = True
                    logger.info("Real Twitter posting enabled")
                except Exception as e:
                    logger.warning(f"Real Twitter posting failed to initialize: {e}")
                    logger.info("Falling back to simulation mode...")
                    self.poster = TwitterPosterSimulator()
                    await self.poster.initialize()
                    self.posting_enabled = False
                    logger.info("Twitter posting in simulation mode (fallback)")
            else:
                logger.info("Initializing Twitter poster simulator...")
                self.poster = TwitterPosterSimulator()
                await self.poster.initialize()
                self.posting_enabled = False
                logger.info("Twitter posting in simulation mode")
            
            logger.info("Twitter manager initialized")
            self.initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter manager: {e}")
            raise
    
    async def get_user_tweets(self, username: str, limit: int = 10) -> List[Dict]:
        """Get recent tweets from a specific user"""
        if not self.initialized:
            raise RuntimeError("Twitter manager not initialized")
        
        try:
            logger.debug(f"Fetching tweets from {username}")
            
            # Search for tweets from the specific user
            search_query = f"from:{username}"
            tweets = []
            
            async for tweet in self.api.search(search_query, limit=limit):
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.rawContent,
                    'created_at': tweet.date,
                    'username': tweet.user.username,
                    'user_id': tweet.user.id,
                    'retweet_count': tweet.retweetCount,
                    'like_count': tweet.likeCount,
                    'reply_count': tweet.replyCount,
                    'url': tweet.url
                }
                tweets.append(tweet_data)
            
            logger.debug(f"Found {len(tweets)} tweets from {username}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error fetching tweets from {username}: {e}")
            return []
    
    async def post_tweet(self, text: str) -> bool:
        """Post a tweet to the bot account"""
        if not self.initialized:
            raise RuntimeError("Twitter manager not initialized")
        
        try:
            logger.info(f"Posting tweet: {text[:50]}...")
            
            # Use the poster to actually post the tweet
            success = await self.poster.post_tweet(text)
            
            if success:
                if self.posting_enabled:
                    logger.info("Tweet posted successfully to Twitter")
                else:
                    logger.info("Tweet simulated successfully (simulation mode)")
            else:
                logger.error("Failed to post tweet")
            
            return success
            
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False
    
    async def search_tweets(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for tweets matching a query"""
        if not self.initialized:
            raise RuntimeError("Twitter manager not initialized")
        
        try:
            logger.debug(f"Searching tweets with query: {query}")
            
            tweets = []
            async for tweet in self.api.search(query, limit=limit):
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.rawContent,
                    'created_at': tweet.date,
                    'username': tweet.user.username,
                    'user_id': tweet.user.id,
                    'retweet_count': tweet.retweetCount,
                    'like_count': tweet.likeCount,
                    'reply_count': tweet.replyCount,
                    'url': tweet.url
                }
                tweets.append(tweet_data)
            
            logger.debug(f"Found {len(tweets)} tweets for query: {query}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []
    
    async def get_user_info(self, username: str) -> Optional[Dict]:
        """Get information about a Twitter user"""
        if not self.initialized:
            raise RuntimeError("Twitter manager not initialized")
        
        try:
            user = await self.api.user_by_login(username)
            if user:
                return {
                    'id': user.id,
                    'username': user.username,
                    'display_name': user.displayname,
                    'description': user.description,
                    'followers_count': user.followersCount,
                    'following_count': user.friendsCount,
                    'tweet_count': user.statusesCount,
                    'verified': user.verified,
                    'created_at': user.created,
                    'profile_image_url': user.profileImageUrl
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting user info for {username}: {e}")
            return None
    
    async def cleanup(self):
        """Clean up resources"""
        try:
            if self.poster:
                await self.poster.cleanup()
            if self.api:
                # Close any open connections
                pass
            logger.info("Twitter manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during Twitter manager cleanup: {e}")

# Alternative implementation note:
# If twscrape doesn't work properly, you can replace this with other solutions like:
# 1. Using selenium/playwright for browser automation
# 2. Using alternative libraries like snscrape (if working)
# 3. Using third-party APIs like twitterapi.io (paid but cheap)

class TwitterManagerFallback:
    """Fallback Twitter manager using browser automation if twscrape fails"""
    
    def __init__(self):
        self.driver = None
        self.initialized = False
    
    async def initialize(self):
        """Initialize browser automation"""
        try:
            # This would use selenium or playwright
            # Implementation would depend on chosen browser automation tool
            logger.warning("Using fallback Twitter manager - functionality limited")
            self.initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize fallback Twitter manager: {e}")
            raise
    
    async def get_user_tweets(self, username: str, limit: int = 10) -> List[Dict]:
        """Fallback method to get tweets"""
        # Browser automation implementation would go here
        logger.warning("Fallback Twitter manager - tweet fetching not implemented")
        return []
    
    async def post_tweet(self, text: str) -> bool:
        """Fallback method to post tweets"""
        # Browser automation implementation would go here
        logger.warning("Fallback Twitter manager - tweet posting not implemented")
        return False
