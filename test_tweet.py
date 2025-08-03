#!/usr/bin/env python3
"""
Tweet Testing Script
Test the bot's AI processing on specific tweets
"""

import asyncio
import sys
import re
from typing import Dict, Optional

from ai_processor import AIProcessor
from config import Config
from twitter_manager import TwitterManager

class TweetTester:
    def __init__(self):
        self.config = Config()
        self.ai_processor = AIProcessor(self.config.groq_api_key)
        self.twitter_manager = TwitterManager()
    
    def extract_tweet_id_from_url(self, url: str) -> Optional[str]:
        """Extract tweet ID from Twitter URL"""
        patterns = [
            r'twitter\.com/\w+/status/(\d+)',
            r'x\.com/\w+/status/(\d+)',
            r'/status/(\d+)',
            r'(\d{19})',  # Direct tweet ID (19 digits)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_journalist_by_username(self, username: str) -> Optional[Dict]:
        """Find journalist configuration by username"""
        username_lower = username.lower()
        for journalist in self.config.journalists:
            if journalist['username'].lower() == username_lower:
                return journalist
        return None
    
    async def test_tweet_processing(self, tweet_url_or_text: str, username: str = None):
        """Test tweet processing with either URL or direct text"""
        print("=== Tweet Processing Test ===\n")
        
        # Check if it's a URL or direct text
        tweet_id = self.extract_tweet_id_from_url(tweet_url_or_text)
        
        if tweet_id:
            print(f"Detected tweet ID: {tweet_id}")
            # For now, we'll simulate the tweet content since we need Twitter accounts
            # In real scenario, this would fetch the actual tweet
            if "1951901347219206602" in tweet_id:
                # Example tweet content for testing
                tweet_text = """🚨⚪️ Kylian Mbappé to Real Madrid, HERE WE GO! Every document has been signed, sealed and completed.

Real Madrid, set to announce Mbappé as new signing next week after winning the Champions League.

Mbappé made his decision in February; he can now be considered new Real player."""
                original_username = "FabrizioRomano"
                print(f"Using example tweet from @{original_username}")
            else:
                print("❌ For testing, please use the example tweet URL or provide direct text")
                return
        else:
            # Direct text provided
            tweet_text = tweet_url_or_text
            original_username = username or "CrediBall"
            print(f"Testing with provided text from @{original_username}")
        
        print(f"\n📝 Original Tweet:")
        print("-" * 50)
        print(tweet_text)
        print("-" * 50)
        
        # Get journalist info
        journalist = self.get_journalist_by_username(original_username)
        if not journalist:
            print(f"⚠️  Journalist @{original_username} not found in config, using defaults")
            journalist = {
                'username': original_username,
                'reliability_score': 100.0,
                'tier': 'tier1'
            }
        
        print(f"\n👤 Journalist Info:")
        print(f"   Username: @{journalist['username']}")
        print(f"   Reliability: {journalist['reliability_score']}%")
        print(f"   Tier: {journalist['tier']}")
        
        # Test AI initialization
        print(f"\n🤖 Testing AI Connection...")
        try:
            ai_connected = await self.ai_processor.test_connection()
            if ai_connected:
                print("✅ AI connection successful")
            else:
                print("❌ AI connection failed")
                return
        except Exception as e:
            print(f"❌ AI connection error: {e}")
            return
        
        # Test football detection
        print(f"\n⚽ Testing Football Detection...")
        try:
            is_football = await self.ai_processor.is_football_related(tweet_text)
            if is_football:
                print("✅ Tweet detected as football-related")
            else:
                print("❌ Tweet not detected as football-related")
                return
        except Exception as e:
            print(f"❌ Football detection error: {e}")
            return
        
        # Test tweet rewriting
        print(f"\n✏️  Testing Tweet Rewriting...")
        try:
            rewritten = await self.ai_processor.rewrite_tweet(
                tweet_text, 
                journalist['username'], 
                journalist['reliability_score']
            )
            
            if rewritten:
                print("✅ Tweet rewriting successful")
                print(f"\n📝 Rewritten Tweet:")
                print("-" * 50)
                print(rewritten)
                print("-" * 50)
            else:
                print("❌ Tweet rewriting failed")
                return
        except Exception as e:
            print(f"❌ Tweet rewriting error: {e}")
            return
        
        # Format final tweet
        print(f"\n📋 Formatting Final Tweet...")
        final_tweet = self._format_final_tweet(
            rewritten,
            journalist['username'],
            journalist['reliability_score'],
            journalist.get('tier', 'tier2')
        )
        
        print(f"\n🎯 Final Bot Tweet:")
        print("=" * 60)
        print(final_tweet)
        print("=" * 60)
        
        # Show character count
        char_count = len(final_tweet)
        print(f"\n📊 Character Count: {char_count}/280")
        if char_count > 280:
            print("⚠️  Warning: Tweet exceeds 280 character limit!")
        else:
            print("✅ Tweet within character limit")
        
        print(f"\n✅ Test completed successfully!")
    
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

async def main():
    """Main function"""
    print("=== Football Twitter Bot - Tweet Tester ===")
    print("Test how the bot processes specific tweets\n")
    
    if len(sys.argv) > 1:
        # Use command line argument
        tweet_input = sys.argv[1]
        username = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Interactive mode
        print("Enter a tweet URL or paste tweet text:")
        tweet_input = input("> ").strip()
        
        if not tweet_input:
            print("No input provided. Using example tweet.")
            tweet_input = "https://x.com/FabrizioRomano/status/1951901347219206602"
        
        # Ask for username if not URL
        if not re.search(r'(twitter|x)\.com', tweet_input):
            username = input("Enter journalist username (optional): ").strip()
            username = username if username else None
        else:
            username = None
    
    tester = TweetTester()
    try:
        await tester.test_tweet_processing(tweet_input, username)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)