"""
Football Twitter Bot - Configuration Management
Handles loading and managing bot configuration from JSON files and environment variables
"""

import json
import logging
import os
from typing import Dict, List

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        """Initialize configuration from files and environment variables"""
        self.load_settings()
        self.load_journalists()
        self.load_environment_variables()
    
    def load_settings(self):
        """Load general settings from settings.json"""
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Bot behavior settings
            self.check_interval = settings.get('check_interval', 300)  # 5 minutes
            self.tweets_per_check = settings.get('tweets_per_check', 10)
            self.max_posts_per_day = settings.get('max_posts_per_day', 50)
            self.min_post_interval = settings.get('min_post_interval', 300)  # 5 minutes
            
            # AI processing settings
            self.groq_model = settings.get('groq_model', 'llama3-8b-8192')
            self.max_tweet_length = settings.get('max_tweet_length', 280)
            
            # Special formatting settings
            self.here_we_go_accounts = settings.get('here_we_go_accounts', ['FabrizioRomano', 'David_Ornstein'])
            self.transfer_complete_emoji = settings.get('transfer_complete_emoji', '🚨TRANSFER COMPLETED🚨')
            
            logger.info("Settings loaded successfully")
            
        except FileNotFoundError:
            logger.warning("settings.json not found, using default values")
            self._set_default_settings()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing settings.json: {e}")
            self._set_default_settings()
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            self._set_default_settings()
    
    def load_journalists(self):
        """Load journalist configurations from journalists.json"""
        try:
            with open('journalists.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.journalists = data.get('journalists', [])
            
            # Validate journalist data
            valid_journalists = []
            for journalist in self.journalists:
                if self._validate_journalist(journalist):
                    valid_journalists.append(journalist)
                else:
                    logger.warning(f"Invalid journalist configuration: {journalist}")
            
            self.journalists = valid_journalists
            logger.info(f"Loaded {len(self.journalists)} journalist configurations")
            
        except FileNotFoundError:
            logger.error("journalists.json not found")
            self.journalists = []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing journalists.json: {e}")
            self.journalists = []
        except Exception as e:
            logger.error(f"Error loading journalists: {e}")
            self.journalists = []
    
    def load_environment_variables(self):
        """Load sensitive configuration from environment variables"""
        # First, try to load from .env file
        self._load_env_file()
        
        # Groq API key (required)
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            logger.error("GROQ_API_KEY environment variable is required")
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        # Webhook URL for error notifications
        self.webhook_url = os.getenv('WEBHOOK_URL')
        if not self.webhook_url:
            logger.warning("WEBHOOK_URL not set, error notifications disabled")
        
        # Twitter account credentials (for posting)
        self.twitter_username = os.getenv('TWITTER_USERNAME')
        self.twitter_password = os.getenv('TWITTER_PASSWORD')
        self.twitter_email = os.getenv('TWITTER_EMAIL')
        
        # Twitter posting credentials
        self.twitter_posting_mode = os.getenv('TWITTER_POSTING_MODE', 'simulator')
        self.twitter_post_username = os.getenv('TWITTER_POST_USERNAME')
        self.twitter_post_password = os.getenv('TWITTER_POST_PASSWORD')
        self.twitter_post_email = os.getenv('TWITTER_POST_EMAIL')
        
        if not all([self.twitter_username, self.twitter_password]):
            logger.warning("Twitter credentials not fully configured")
    
    def _load_env_file(self):
        """Load environment variables from .env file"""
        try:
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
        except FileNotFoundError:
            pass  # .env file is optional
    
    def _set_default_settings(self):
        """Set default configuration values"""
        self.check_interval = 300  # 5 minutes
        self.tweets_per_check = 10
        self.max_posts_per_day = 50
        self.min_post_interval = 300  # 5 minutes
        self.groq_model = 'llama3-8b-8192'
        self.max_tweet_length = 280
        self.here_we_go_accounts = ['FabrizioRomano', 'David_Ornstein']
        self.transfer_complete_emoji = '🚨TRANSFER COMPLETED🚨'
    
    def _validate_journalist(self, journalist: Dict) -> bool:
        """Validate journalist configuration"""
        required_fields = ['username', 'reliability_score', 'tier']
        
        # Check required fields
        for field in required_fields:
            if field not in journalist:
                return False
        
        # Validate reliability score
        score = journalist['reliability_score']
        if not isinstance(score, (int, float)) or not (0 <= score <= 100):
            return False
        
        # Validate username
        username = journalist['username']
        if not isinstance(username, str) or not username.strip():
            return False
        
        return True
    
    def add_journalist(self, username: str, reliability_score: float, tier: str = 'standard'):
        """Add a new journalist to the configuration"""
        new_journalist = {
            'username': username,
            'reliability_score': reliability_score,
            'tier': tier,
            'enabled': True
        }
        
        if self._validate_journalist(new_journalist):
            self.journalists.append(new_journalist)
            self.save_journalists()
            logger.info(f"Added journalist: {username}")
            return True
        else:
            logger.error(f"Invalid journalist configuration: {new_journalist}")
            return False
    
    def update_journalist_score(self, username: str, new_score: float) -> bool:
        """Update a journalist's reliability score"""
        for journalist in self.journalists:
            if journalist['username'].lower() == username.lower():
                journalist['reliability_score'] = new_score
                self.save_journalists()
                logger.info(f"Updated {username} reliability score to {new_score}")
                return True
        
        logger.warning(f"Journalist {username} not found")
        return False
    
    def remove_journalist(self, username: str) -> bool:
        """Remove a journalist from the configuration"""
        for i, journalist in enumerate(self.journalists):
            if journalist['username'].lower() == username.lower():
                removed = self.journalists.pop(i)
                self.save_journalists()
                logger.info(f"Removed journalist: {username}")
                return True
        
        logger.warning(f"Journalist {username} not found")
        return False
    
    def save_journalists(self):
        """Save journalist configurations to file"""
        try:
            data = {'journalists': self.journalists}
            with open('journalists.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Journalist configurations saved")
        except Exception as e:
            logger.error(f"Error saving journalists: {e}")
    
    def get_enabled_journalists(self) -> List[Dict]:
        """Get list of enabled journalists"""
        return [j for j in self.journalists if j.get('enabled', True)]
