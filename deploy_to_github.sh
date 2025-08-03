#!/bin/bash

echo "🚀 Deploying Football Twitter Bot to GitHub..."
echo "Repository: https://github.com/johnbulau/football-twitter-bot"
echo ""

# Initialize git repository
echo "📦 Initializing Git repository..."
git init

# Add all files
echo "📁 Adding files to repository..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Football Twitter Bot - Ready for Render.com deployment

Features:
- Complete Twitter bot with AI processing (Groq API)
- Browser automation for real posting (Playwright)
- Docker containerization for Render.com
- 24/7 monitoring of football journalists
- Credibility scoring and content rewriting
- Rate limiting and error handling
- Comprehensive deployment setup"

# Add remote repository
echo "🔗 Adding GitHub remote..."
git remote add origin https://github.com/johnbulau/football-twitter-bot.git

# Push to GitHub
echo "⬆️ Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully deployed to GitHub!"
echo "🌐 Repository URL: https://github.com/johnbulau/football-twitter-bot"
echo ""
echo "🚀 Next steps:"
echo "1. Go to render.com and create an account"
echo "2. Create a new Worker service"
echo "3. Connect your GitHub repository"
echo "4. Set environment variables (GROQ_API_KEY, Twitter credentials)"
echo "5. Deploy and monitor logs"
echo ""
echo "📖 See RENDER_DEPLOYMENT.md for detailed instructions"