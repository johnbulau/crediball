"""
Football Twitter Bot - AI Processing Module
Handles AI-powered text analysis and rewriting using Groq API
"""

import asyncio
import json
import logging
import re
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)

class AIProcessor:
    def __init__(self, groq_api_key: str):
        self.api_key = groq_api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama3-8b-8192"
        self.session = None
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def test_connection(self):
        """Test connection to Groq API"""
        try:
            session = await self._get_session()
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": "Test connection"}
                ],
                "max_tokens": 10
            }
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    logger.info("Groq API connection successful")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"Groq API test failed: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error testing Groq API connection: {e}")
            return False
    
    async def is_football_related(self, text: str) -> bool:
        """Determine if a tweet is related to football/soccer"""
        try:
            prompt = f"""
            Analyze this tweet and determine if it's related to football/soccer (the sport played with feet, not American football).

            Consider these as football-related:
            - Player transfers, signings, contract renewals
            - Match results, fixtures, schedules
            - Team news, lineups, injuries
            - Manager appointments, dismissals
            - League news, championships, tournaments
            - Player performance, statistics, awards
            - Stadium news, fan-related content
            - Football clubs, leagues, associations

            Tweet: "{text}"

            Respond with only "YES" if it's football-related, or "NO" if it's not.
            """
            
            response = await self._call_groq_api(prompt, max_tokens=5)
            if response:
                result = response.strip().upper()
                return result == "YES"
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking if tweet is football-related: {e}")
            return False
    
    async def rewrite_tweet(self, original_text: str, journalist_username: str, 
                           reliability_score: float) -> Optional[str]:
        """Rewrite a tweet with improved formatting and clarity"""
        try:
            # Determine if this is a high-tier journalist
            is_high_tier = journalist_username.lower() in ['fabrizioromano', 'david_ornstein']
            
            # Check if it's a "Here We Go" situation
            has_here_we_go = "here we go" in original_text.lower()
            
            prompt = f"""
            Rewrite this football tweet to be clearer, more engaging, and well-formatted. Follow these guidelines:

            1. Make it more concise and impactful
            2. Fix any grammar or formatting issues
            3. Use appropriate emojis (🚨, ⚡, 🔥, ⚽, etc.) but don't overuse them
            4. If it's about a completed transfer and from a high-tier journalist ({journalist_username}), keep "HERE WE GO!" if present
            5. If it's about a completed transfer from other journalists, use "🚨TRANSFER COMPLETED🚨" instead
            6. Maintain the key information and facts
            7. Keep it under 200 characters to leave room for source attribution
            8. Remove any unnecessary hashtags or mentions
            9. Make it sound professional but exciting

            Original tweet: "{original_text}"
            Journalist: {journalist_username}
            Is high-tier journalist: {is_high_tier}
            Has "Here We Go": {has_here_we_go}

            Provide only the rewritten tweet, no explanations.
            """
            
            response = await self._call_groq_api(prompt, max_tokens=150)
            if response:
                # Clean up the response
                rewritten = response.strip()
                
                # Remove quotes if the AI added them
                if rewritten.startswith('"') and rewritten.endswith('"'):
                    rewritten = rewritten[1:-1]
                
                # Ensure it's not too long (leave space for attribution)
                if len(rewritten) > 200:
                    rewritten = rewritten[:197] + "..."
                
                return rewritten
            
            return None
            
        except Exception as e:
            logger.error(f"Error rewriting tweet: {e}")
            return None
    
    async def _call_groq_api(self, prompt: str, max_tokens: int = 150) -> Optional[str]:
        """Make a call to the Groq API"""
        try:
            session = await self._get_session()
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that analyzes and rewrites football/soccer related content. Be concise and accurate."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 1,
                "stream": False
            }
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    return content.strip()
                else:
                    error_text = await response.text()
                    logger.error(f"Groq API error: {response.status} - {error_text}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error("Groq API request timed out")
            return None
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return None
    
    async def cleanup(self):
        """Clean up resources"""
        if self.session and not self.session.closed:
            await self.session.close()
