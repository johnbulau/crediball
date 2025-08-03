#!/usr/bin/env python3
"""
Bot Management Script
Simple interface to manage the football Twitter bot
"""

import asyncio
import json
import sys
from config import Config

class BotManager:
    def __init__(self):
        self.config = Config()
    
    def show_menu(self):
        """Display the main menu"""
        print("\n=== Football Twitter Bot Manager ===")
        print("1. Start the bot")
        print("2. Add journalist")
        print("3. Update journalist score")
        print("4. Remove journalist")
        print("5. List journalists")
        print("6. View settings")
        print("7. Setup Twitter accounts")
        print("8. Test tweet processing")
        print("9. Configure posting")
        print("10. Exit")
        
    def add_journalist(self):
        """Add a new journalist"""
        print("\n=== Add New Journalist ===")
        username = input("Twitter username (without @): ").strip()
        
        try:
            score = float(input("Reliability score (0-100): ").strip())
            if not (0 <= score <= 100):
                print("Score must be between 0 and 100!")
                return
        except ValueError:
            print("Invalid score format!")
            return
        
        tier = input("Tier (tier1/tier2/tier3/tier4): ").strip().lower()
        if tier not in ['tier1', 'tier2', 'tier3', 'tier4']:
            tier = 'tier2'  # Default
        
        if self.config.add_journalist(username, score, tier):
            print(f"✓ Added @{username} with {score}% reliability")
        else:
            print("✗ Failed to add journalist")
    
    def update_score(self):
        """Update a journalist's reliability score"""
        print("\n=== Update Journalist Score ===")
        self.list_journalists()
        
        username = input("\nEnter username to update: ").strip()
        try:
            new_score = float(input("New reliability score (0-100): ").strip())
            if not (0 <= new_score <= 100):
                print("Score must be between 0 and 100!")
                return
        except ValueError:
            print("Invalid score format!")
            return
        
        if self.config.update_journalist_score(username, new_score):
            print(f"✓ Updated @{username} score to {new_score}%")
        else:
            print("✗ Journalist not found")
    
    def remove_journalist(self):
        """Remove a journalist"""
        print("\n=== Remove Journalist ===")
        self.list_journalists()
        
        username = input("\nEnter username to remove: ").strip()
        if self.config.remove_journalist(username):
            print(f"✓ Removed @{username}")
        else:
            print("✗ Journalist not found")
    
    def list_journalists(self):
        """List all journalists"""
        print("\n=== Current Journalists ===")
        for i, journalist in enumerate(self.config.journalists, 1):
            status = "✓" if journalist.get('enabled', True) else "✗"
            score = journalist['reliability_score']
            tier = journalist.get('tier', 'unknown')
            
            # Color code based on score
            if score >= 90:
                emoji = "🟢"
            elif score >= 70:
                emoji = "🟡"
            elif score >= 50:
                emoji = "🟠"
            else:
                emoji = "🔴"
            
            print(f"{i:2}. {status} @{journalist['username']:20} {emoji} {score:5.1f}% ({tier})")
    
    def view_settings(self):
        """Display current settings"""
        print("\n=== Current Settings ===")
        print(f"Check interval: {self.config.check_interval} seconds")
        print(f"Max posts per day: {self.config.max_posts_per_day}")
        print(f"Min post interval: {self.config.min_post_interval} seconds")
        print(f"AI model: {self.config.groq_model}")
        print(f"Groq API key: {'✓ Set' if self.config.groq_api_key else '✗ Missing'}")
        print(f"Webhook URL: {'✓ Set' if self.config.webhook_url else '✗ Not set'}")
        print(f"Total journalists: {len(self.config.journalists)}")
    
    def setup_twitter_accounts(self):
        """Run the Twitter account setup script"""
        print("\n=== Setting up Twitter Accounts ===")
        print("Running Twitter account setup script...")
        import subprocess
        try:
            subprocess.run([sys.executable, "setup_twitter_accounts.py"], check=True)
        except subprocess.CalledProcessError:
            print("✗ Twitter setup failed")
        except FileNotFoundError:
            print("✗ Setup script not found")
    
    def test_tweet_processing(self):
        """Test tweet processing functionality"""
        print("\n=== Test Tweet Processing ===")
        print("Choose test method:")
        print("1. Test with the example Mbappé tweet")
        print("2. Test with custom tweet text")
        print("3. Test with tweet URL")
        
        choice = input("Enter choice (1-3): ").strip()
        
        import subprocess
        
        if choice == "1":
            # Test with example tweet
            try:
                subprocess.run([sys.executable, "test_tweet.py", "https://x.com/FabrizioRomano/status/1951901347219206602"], check=True)
            except subprocess.CalledProcessError:
                print("✗ Test failed")
        elif choice == "2":
            # Test with custom text
            print("\nPaste your tweet text:")
            tweet_text = input("> ").strip()
            if not tweet_text:
                print("✗ No text provided")
                return
            
            username = input("Journalist username (optional): ").strip()
            
            try:
                args = [sys.executable, "test_tweet.py", tweet_text]
                if username:
                    args.append(username)
                subprocess.run(args, check=True)
            except subprocess.CalledProcessError:
                print("✗ Test failed")
        elif choice == "3":
            # Test with URL
            url = input("Enter tweet URL: ").strip()
            if not url:
                print("✗ No URL provided")
                return
            
            try:
                subprocess.run([sys.executable, "test_tweet.py", url], check=True)
            except subprocess.CalledProcessError:
                print("✗ Test failed")
        else:
            print("Invalid choice")
    
    def configure_posting(self):
        """Configure Twitter posting settings"""
        print("\n=== Configure Twitter Posting ===")
        print("Run the posting setup script...")
        import subprocess
        try:
            subprocess.run([sys.executable, "setup_posting.py"], check=True)
        except subprocess.CalledProcessError:
            print("✗ Posting setup failed")
        except FileNotFoundError:
            print("✗ Setup script not found")
    
    def start_bot(self):
        """Start the main bot"""
        print("\n=== Starting Bot ===")
        print("The bot will start monitoring journalists...")
        print("Press Ctrl+C to stop the bot")
        
        try:
            import subprocess
            subprocess.run([sys.executable, "main.py"], check=True)
        except subprocess.CalledProcessError:
            print("✗ Bot failed to start")
        except KeyboardInterrupt:
            print("\n✓ Bot stopped by user")
    
    def run(self):
        """Main menu loop"""
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (1-10): ").strip()
            
            if choice == "1":
                self.start_bot()
            elif choice == "2":
                self.add_journalist()
            elif choice == "3":
                self.update_score()
            elif choice == "4":
                self.remove_journalist()
            elif choice == "5":
                self.list_journalists()
            elif choice == "6":
                self.view_settings()
            elif choice == "7":
                self.setup_twitter_accounts()
            elif choice == "8":
                self.test_tweet_processing()
            elif choice == "9":
                self.configure_posting()
            elif choice == "10":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    manager = BotManager()
    try:
        manager.run()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")