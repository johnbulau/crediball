"""
Twitter Poster - Browser Automation for Posting Tweets
Uses Playwright for automated Twitter posting
"""

import asyncio
import logging
import os
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

logger = logging.getLogger(__name__)

class TwitterPoster:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.logged_in = False
        
        # Get credentials from environment
        self.username = os.getenv('TWITTER_POST_USERNAME')
        self.password = os.getenv('TWITTER_POST_PASSWORD')
        self.email = os.getenv('TWITTER_POST_EMAIL')
    
    async def initialize(self):
        """Initialize browser and login to Twitter"""
        try:
            if not all([self.username, self.password]):
                raise ValueError("Twitter posting credentials not configured")
            
            playwright = await async_playwright().start()
            
            # Launch browser in headless mode
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            # Create context with user agent
            self.context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            self.page = await self.context.new_page()
            
            # Login to Twitter
            await self._login()
            
            logger.info("Twitter poster initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter poster: {e}")
            await self.cleanup()
            raise
    
    async def _login(self):
        """Login to Twitter"""
        try:
            logger.info("Logging in to Twitter...")
            
            # Go to Twitter login page
            await self.page.goto('https://twitter.com/i/flow/login', wait_until='networkidle')
            
            # Wait for username field and enter username
            username_selector = 'input[autocomplete="username"]'
            await self.page.wait_for_selector(username_selector, timeout=10000)
            await self.page.fill(username_selector, self.username)
            await self.page.click('div[role="button"]:has-text("Next")')
            
            # Check if email verification is required
            try:
                await self.page.wait_for_selector('input[data-testid="ocfEnterTextTextInput"]', timeout=5000)
                if self.email:
                    await self.page.fill('input[data-testid="ocfEnterTextTextInput"]', self.email)
                    await self.page.click('div[role="button"]:has-text("Next")')
                else:
                    raise ValueError("Email verification required but no email provided")
            except:
                # Email verification not required, continue
                pass
            
            # Wait for password field and enter password
            password_selector = 'input[autocomplete="current-password"]'
            await self.page.wait_for_selector(password_selector, timeout=10000)
            await self.page.fill(password_selector, self.password)
            await self.page.click('div[role="button"]:has-text("Log in")')
            
            # Wait for successful login (home page)
            await self.page.wait_for_url('https://twitter.com/home', timeout=15000)
            
            self.logged_in = True
            logger.info("Successfully logged in to Twitter")
            
        except Exception as e:
            logger.error(f"Failed to login to Twitter: {e}")
            raise
    
    async def post_tweet(self, text: str) -> bool:
        """Post a tweet"""
        if not self.logged_in:
            logger.error("Not logged in to Twitter")
            return False
        
        try:
            logger.info(f"Posting tweet: {text[:50]}...")
            
            # Go to home page if not already there
            await self.page.goto('https://twitter.com/home', wait_until='networkidle')
            
            # Find and click the tweet compose button
            compose_button = 'a[aria-label="Post"], div[aria-label="Post"]'
            await self.page.wait_for_selector(compose_button, timeout=10000)
            await self.page.click(compose_button)
            
            # Wait for compose modal to appear
            await asyncio.sleep(2)
            
            # Find the tweet text area
            text_area = 'div[data-testid="tweetTextarea_0"]'
            await self.page.wait_for_selector(text_area, timeout=10000)
            
            # Clear any existing text and enter the tweet
            await self.page.click(text_area)
            await self.page.keyboard.press('Control+a')  # Select all
            await self.page.keyboard.press('Delete')     # Delete existing text
            await self.page.type(text_area, text)
            
            # Wait a moment for the text to be processed
            await asyncio.sleep(1)
            
            # Find and click the post button
            post_button = 'div[data-testid="tweetButtonInline"]'
            await self.page.wait_for_selector(post_button, timeout=5000)
            
            # Check if the post button is enabled
            is_disabled = await self.page.locator(post_button).get_attribute('aria-disabled')
            if is_disabled == 'true':
                logger.error("Post button is disabled - tweet may be too long or empty")
                return False
            
            await self.page.click(post_button)
            
            # Wait for the tweet to be posted (modal should disappear)
            await asyncio.sleep(3)
            
            logger.info("Tweet posted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return False
    
    async def test_posting(self) -> bool:
        """Test posting functionality with a test tweet"""
        test_text = f"Test post from Football Twitter Bot - {asyncio.get_event_loop().time()}"
        return await self.post_tweet(test_text)
    
    async def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            logger.info("Twitter poster cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# Alternative simpler posting class for testing
class TwitterPosterSimulator:
    """Simulator for testing without actual posting"""
    
    def __init__(self):
        self.logged_in = False
    
    async def initialize(self):
        """Simulate initialization"""
        logger.info("Twitter poster simulator initialized")
        self.logged_in = True
    
    async def post_tweet(self, text: str) -> bool:
        """Simulate posting a tweet"""
        logger.info(f"SIMULATED POST: {text}")
        await asyncio.sleep(1)  # Simulate posting delay
        return True
    
    async def test_posting(self) -> bool:
        """Test simulated posting"""
        return await self.post_tweet("Test post from simulator")
    
    async def cleanup(self):
        """Cleanup simulator"""
        logger.info("Twitter poster simulator cleanup completed")