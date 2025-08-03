#!/usr/bin/env python3
"""
Setup Script for Twitter Posting
Configure credentials for actual Twitter posting
"""

import os
import getpass

def setup_posting_credentials():
    """Interactive setup for Twitter posting credentials"""
    print("=== Twitter Posting Setup ===")
    print("Configure credentials for your bot's Twitter account\n")
    print("IMPORTANT: Use a separate Twitter account for your bot, not your personal account!")
    print("This account will be used to post the rewritten tweets.\n")
    
    print("Options:")
    print("1. Set up real Twitter posting (requires bot account credentials)")
    print("2. Use simulation mode (just logs tweets, doesn't post)")
    print("3. View current settings")
    print("4. Test posting functionality")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        setup_real_posting()
    elif choice == "2":
        setup_simulation_mode()
    elif choice == "3":
        view_current_settings()
    elif choice == "4":
        test_posting()
    else:
        print("Invalid choice")

def setup_real_posting():
    """Set up real Twitter posting credentials"""
    print("\n=== Real Twitter Posting Setup ===")
    print("You'll need credentials for your bot's Twitter account.")
    print("This account will post the rewritten tweets.\n")
    
    username = input("Bot Twitter username (without @): ").strip()
    password = getpass.getpass("Bot Twitter password: ")
    email = input("Bot Twitter email (optional, for verification): ").strip()
    
    if not username or not password:
        print("Username and password are required!")
        return
    
    # Create .env content
    env_content = f"""# Twitter Posting Credentials
TWITTER_POSTING_MODE=real
TWITTER_POST_USERNAME={username}
TWITTER_POST_PASSWORD={password}
"""
    if email:
        env_content += f"TWITTER_POST_EMAIL={email}\n"
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Credentials saved to .env file")
        print("✅ Real Twitter posting enabled")
        print("\nIMPORTANT: Keep your .env file secure and never commit it to version control!")
    except Exception as e:
        print(f"❌ Failed to save credentials: {e}")

def setup_simulation_mode():
    """Set up simulation mode (no real posting)"""
    print("\n=== Simulation Mode Setup ===")
    print("In simulation mode, the bot will process tweets and show you what it would post,")
    print("but won't actually post to Twitter. This is safe for testing.\n")
    
    env_content = """# Twitter Posting Credentials
TWITTER_POSTING_MODE=simulator
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Simulation mode enabled")
        print("✅ Bot will simulate posting without actually posting to Twitter")
    except Exception as e:
        print(f"❌ Failed to save settings: {e}")

def view_current_settings():
    """View current posting settings"""
    print("\n=== Current Settings ===")
    
    try:
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                content = f.read()
            
            if 'TWITTER_POSTING_MODE=real' in content:
                print("📡 Mode: Real Twitter posting")
                if 'TWITTER_POST_USERNAME=' in content:
                    username = [line for line in content.split('\n') if 'TWITTER_POST_USERNAME=' in line]
                    if username:
                        user = username[0].split('=')[1]
                        print(f"🤖 Bot account: @{user}")
                print("⚠️  Bot will post tweets to the configured Twitter account")
            else:
                print("🎭 Mode: Simulation mode")
                print("✅ Bot will simulate posting (safe for testing)")
        else:
            print("⚙️  No configuration found - will use simulation mode by default")
            
    except Exception as e:
        print(f"❌ Error reading settings: {e}")

def test_posting():
    """Test the posting functionality"""
    print("\n=== Testing Posting Functionality ===")
    print("This will test the posting system with a sample tweet...")
    
    import subprocess
    import sys
    
    try:
        # Create a simple test script
        test_script = '''
import asyncio
import os
from twitter_poster import TwitterPoster, TwitterPosterSimulator

async def test():
    posting_mode = os.getenv("TWITTER_POSTING_MODE", "simulator")
    
    if posting_mode == "real" and all([
        os.getenv("TWITTER_POST_USERNAME"),
        os.getenv("TWITTER_POST_PASSWORD")
    ]):
        print("Testing real Twitter posting...")
        poster = TwitterPoster()
    else:
        print("Testing simulation mode...")
        poster = TwitterPosterSimulator()
    
    await poster.initialize()
    success = await poster.test_posting()
    await poster.cleanup()
    
    if success:
        print("✅ Posting test successful!")
    else:
        print("❌ Posting test failed!")

if __name__ == "__main__":
    asyncio.run(test())
'''
        
        with open('test_posting_temp.py', 'w') as f:
            f.write(test_script)
        
        # Run the test
        result = subprocess.run([sys.executable, 'test_posting_temp.py'], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        # Clean up
        os.remove('test_posting_temp.py')
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    try:
        setup_posting_credentials()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")