#!/usr/bin/env python3
"""
GitHub Repository Preparation Script
Prepares the project for deployment by creating necessary files and cleaning up
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

def print_banner():
    print("=" * 60)
    print("📦 Preparing Football Twitter Bot for GitHub & Render")
    print("=" * 60)
    print()

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment variables
.env
.env.local
.env.production

# Logs
*.log
logs/

# Database files
*.db
*.sqlite
*.sqlite3
accounts.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Replit specific
replit.nix
.replit
uv.lock

# Runtime files
attached_assets/
bot.log

# Temporary files
*.tmp
*.temp
"""
    
    try:
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .gitignore: {e}")
        return False

def cleanup_files():
    """Clean up files that shouldn't be in the repository"""
    files_to_remove = [
        'bot.log',
        'accounts.db',
        '.env'
    ]
    
    dirs_to_remove = [
        '__pycache__',
        'attached_assets'
    ]
    
    print("🧹 Cleaning up repository...")
    
    # Remove files
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"  ✅ Removed {file}")
            except Exception as e:
                print(f"  ⚠️  Could not remove {file}: {e}")
    
    # Remove directories
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  ✅ Removed {dir_name}/")
            except Exception as e:
                print(f"  ⚠️  Could not remove {dir_name}/: {e}")

def check_essential_files():
    """Check that all essential files are present"""
    essential_files = [
        'main.py',
        'bot.py',
        'config.py',
        'ai_processor.py',
        'twitter_manager.py',
        'twitter_poster.py',
        'error_handler.py',
        'journalists.json',
        'settings.json',
        'Dockerfile',
        'requirements-render.txt',
        'render.yaml',
        'RENDER_DEPLOYMENT.md'
    ]
    
    print("📋 Checking essential files...")
    all_present = True
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ Missing: {file}")
            all_present = False
    
    return all_present

def show_deployment_instructions():
    """Show final deployment instructions"""
    print("\n" + "=" * 60)
    print("🚀 DEPLOYMENT INSTRUCTIONS")
    print("=" * 60)
    print()
    print("1. 📤 Push to GitHub:")
    print("   git init")
    print("   git add .")
    print('   git commit -m "Football Twitter Bot - Ready for deployment"')
    print("   git remote add origin https://github.com/johnbulau/football-twitter-bot.git")
    print("   git push -u origin main")
    print()
    print("2. 🌐 Deploy on Render.com:")
    print("   - Go to render.com and create account")
    print("   - Click 'New +' → 'Worker'")
    print("   - Connect your GitHub repository")
    print("   - Service will auto-deploy using render.yaml")
    print()
    print("3. 🔑 Set Environment Variables in Render:")
    print("   - GROQ_API_KEY (required)")
    print("   - TWITTER_POST_USERNAME (required)")
    print("   - TWITTER_POST_PASSWORD (required)")
    print("   - TWITTER_POST_EMAIL (optional)")
    print("   - WEBHOOK_URL (optional)")
    print()
    print("4. 🐦 After Deployment:")
    print("   - Access Render console")
    print("   - Run: python setup_twitter_accounts.py")
    print("   - Add Twitter accounts for scraping")
    print()
    print("5. 📊 Monitor:")
    print("   - Check Render logs for bot activity")
    print("   - Monitor error notifications")
    print("   - Watch for successful posts")
    print()
    print("📖 For detailed instructions: see RENDER_DEPLOYMENT.md")
    print("=" * 60)

def main():
    """Main preparation function"""
    print_banner()
    
    # Create .gitignore
    gitignore_ok = create_gitignore()
    
    # Cleanup files
    cleanup_files()
    
    # Check essential files
    files_ok = check_essential_files()
    
    print("\n" + "=" * 60)
    if gitignore_ok and files_ok:
        print("✅ REPOSITORY READY FOR GITHUB & RENDER!")
        print("All files prepared for deployment")
    else:
        print("⚠️  REPOSITORY NEEDS ATTENTION")
        print("Some issues need to be resolved")
    print("=" * 60)
    
    # Show deployment instructions
    show_deployment_instructions()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Preparation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Preparation failed: {e}")
        sys.exit(1)