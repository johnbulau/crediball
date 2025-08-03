#!/usr/bin/env python3
"""
Render.com Setup Helper Script
Helps configure the bot for first-time deployment on Render
"""

import asyncio
import json
import os
import sys
from datetime import datetime

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🚀 Football Twitter Bot - Render.com Setup")
    print("=" * 60)
    print()

def check_environment():
    """Check if required environment variables are set"""
    print("📋 Checking Environment Variables...")
    
    required_vars = [
        'GROQ_API_KEY',
        'TWITTER_POST_USERNAME', 
        'TWITTER_POST_PASSWORD'
    ]
    
    optional_vars = [
        'TWITTER_POST_EMAIL',
        'WEBHOOK_URL',
        'TWITTER_POSTING_MODE'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
        else:
            print(f"  ✅ {var}: Set")
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
        else:
            print(f"  ✅ {var}: Set")
    
    if missing_required:
        print(f"\n❌ Missing Required Variables:")
        for var in missing_required:
            print(f"  - {var}")
        print("\nPlease set these in your Render service environment variables.")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing Optional Variables:")
        for var in missing_optional:
            print(f"  - {var}")
        print("These are optional but recommended for full functionality.")
    
    return True

def check_config_files():
    """Check if configuration files exist and are valid"""
    print("\n📁 Checking Configuration Files...")
    
    files_to_check = [
        ('journalists.json', 'Journalist configurations'),
        ('settings.json', 'Bot settings')
    ]
    
    all_good = True
    
    for filename, description in files_to_check:
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                print(f"  ✅ {filename}: Valid ({description})")
                
                if filename == 'journalists.json':
                    journalists = data.get('journalists', [])
                    enabled = [j for j in journalists if j.get('enabled', True)]
                    print(f"     📊 {len(journalists)} total, {len(enabled)} enabled")
                    
            except json.JSONDecodeError:
                print(f"  ❌ {filename}: Invalid JSON format")
                all_good = False
            except Exception as e:
                print(f"  ❌ {filename}: Error reading file ({e})")
                all_good = False
        else:
            print(f"  ❌ {filename}: File not found")
            all_good = False
    
    return all_good

async def test_connections():
    """Test connections to external services"""
    print("\n🔗 Testing External Connections...")
    
    # Test Groq API
    try:
        from ai_processor import AIProcessor
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key:
            ai = AIProcessor(groq_key)
            await ai.test_connection()
            print("  ✅ Groq API: Connected")
        else:
            print("  ❌ Groq API: No API key set")
    except Exception as e:
        print(f"  ❌ Groq API: Connection failed ({e})")
    
    # Check twscrape accounts
    try:
        from twscrape import API
        api = API()
        # Try to get accounts - method name may vary by version
        try:
            accounts = await api.pool.accounts_info()
        except AttributeError:
            # Fallback method names
            try:
                accounts = list(await api.pool.get_all())
            except:
                accounts = []
        
        if accounts:
            active_accounts = [acc for acc in accounts if getattr(acc, 'active', True)]
            print(f"  ✅ Twitter Scraping: {len(active_accounts)}/{len(accounts)} accounts active")
        else:
            print("  ⚠️  Twitter Scraping: No accounts configured")
            print("     Run 'python setup_twitter_accounts.py' after deployment")
    except Exception as e:
        print(f"  ❌ Twitter Scraping: Error checking accounts ({e})")

def show_deployment_checklist():
    """Show post-deployment checklist"""
    print("\n" + "=" * 60)
    print("📋 POST-DEPLOYMENT CHECKLIST")
    print("=" * 60)
    print()
    print("After your bot is deployed on Render:")
    print()
    print("1. 🐦 Setup Twitter Accounts for Scraping:")
    print("   - Access your Render service console")
    print("   - Run: python setup_twitter_accounts.py")
    print("   - Add at least one Twitter account")
    print()
    print("2. 📊 Monitor Bot Activity:")
    print("   - Check Render logs for bot cycles")
    print("   - Look for successful tweet processing")
    print("   - Watch for error messages")
    print()
    print("3. 🔧 Fine-tune Configuration:")
    print("   - Adjust journalists.json as needed")
    print("   - Update settings.json for posting frequency")
    print("   - Set up webhook notifications (optional)")
    print()
    print("4. 🎯 Test Posting:")
    print("   - Monitor for successful posts")
    print("   - Verify AI rewriting quality")
    print("   - Check rate limiting compliance")
    print()
    print("5. 💰 Monitor Costs:")
    print("   - Groq API usage")
    print("   - Render service costs")
    print("   - Consider upgrading plan if needed")
    print()

async def main():
    """Main setup function"""
    print_banner()
    
    # Check environment
    env_ok = check_environment()
    
    # Check config files
    config_ok = check_config_files()
    
    # Test connections
    await test_connections()
    
    # Overall status
    print("\n" + "=" * 60)
    if env_ok and config_ok:
        print("🎉 SETUP STATUS: READY FOR DEPLOYMENT")
        print("✅ All checks passed! Your bot is ready for Render.com")
    else:
        print("⚠️  SETUP STATUS: NEEDS ATTENTION")
        print("❌ Some issues need to be resolved before deployment")
    print("=" * 60)
    
    # Show checklist
    show_deployment_checklist()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)