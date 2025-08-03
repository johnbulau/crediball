# Manual Deployment Guide

Since Git operations are restricted in Replit, here's how to manually deploy your Football Twitter Bot to GitHub and Render.com.

## Method 1: Download and Upload to GitHub (Recommended)

### Step 1: Download Your Project
1. In Replit, go to the Files panel
2. Click the three dots menu (⋮) next to "Files"
3. Select "Download as zip"
4. Save the zip file to your computer

### Step 2: Create GitHub Repository
1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name it: `football-twitter-bot`
4. Make it **Public** (so Render can access it for free)
5. Don't initialize with README, .gitignore, or license (we have these files)
6. Click "Create repository"

### Step 3: Upload to GitHub
1. Extract the downloaded zip file
2. Remove these files from the folder (they shouldn't be in the repo):
   - `replit.nix`
   - `.replit`
   - `uv.lock`
   - Any `.pyc` files in `__pycache__/`
3. Go to your new GitHub repository
4. Click "uploading an existing file"
5. Drag and drop all the project files
6. Write commit message: "Football Twitter Bot - Ready for Render deployment"
7. Click "Commit changes"

## Method 2: Manual Git Commands (On Your Local Machine)

If you have Git installed on your computer:

```bash
# Download and extract the project files first, then:
cd football-twitter-bot
git init
git add .
git commit -m "Football Twitter Bot - Ready for Render deployment"
git remote add origin https://github.com/johnbulau/football-twitter-bot.git
git push -u origin main
```

## Step 4: Deploy on Render.com

### Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Verify your email

### Create Worker Service
1. Click "New +" in Render dashboard  
2. Select "Worker"
3. Connect your GitHub account if not already connected
4. Select your `football-twitter-bot` repository
5. Configure the service:
   - **Service Name**: `football-twitter-bot`
   - **Plan**: Starter ($7/month minimum for 24/7 operation)
   - **Auto-Deploy**: Yes (recommended)

### Set Environment Variables
In the Environment tab, add these variables:

**Required:**
- `GROQ_API_KEY` = `your_groq_api_key_here`
- `TWITTER_POST_USERNAME` = `your_bot_twitter_username`
- `TWITTER_POST_PASSWORD` = `your_bot_twitter_password`

**Optional but Recommended:**
- `TWITTER_POST_EMAIL` = `your_bot_twitter_email`
- `WEBHOOK_URL` = `your_discord_webhook_url`

### Deploy
1. Click "Create Worker Service"
2. Render will automatically detect the `render.yaml` file
3. It will build the Docker container with all browser dependencies
4. Monitor the deployment logs

## Step 5: Post-Deployment Setup

### Add Twitter Accounts for Scraping
1. Once deployed, go to your service dashboard
2. Open the "Console" tab
3. Run this command:
   ```bash
   python setup_twitter_accounts.py
   ```
4. Follow the prompts to add at least one Twitter account for scraping

### Monitor Your Bot
1. Check the "Logs" tab for bot activity
2. Look for successful cycles and tweet processing
3. Set up webhook notifications for errors

## Expected Costs

- **Render Worker (Starter)**: $7/month for 24/7 operation
- **Groq API**: Free tier includes significant usage
- **Total**: ~$7-10/month for continuous operation

## Troubleshooting

### Common Issues:
1. **"No active accounts" warnings**: Add Twitter accounts via console
2. **Groq API errors**: Verify your API key is correct
3. **Browser errors**: The Docker container should handle this automatically
4. **Memory issues**: Consider upgrading to Standard plan ($25/month)

### Getting Help:
- Check service logs in Render dashboard
- Review error notifications via webhook
- Use the health check endpoint to monitor status

## Success Indicators

Your bot is working correctly when you see:
- Regular "Bot cycle completed" messages in logs
- Successful tweet processing and AI rewriting
- Posts appearing on your bot's Twitter account
- No repeated error messages

The bot will run continuously, checking for new tweets every 5 minutes and posting enhanced content with credibility scores.