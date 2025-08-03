# Render.com Deployment Guide

This guide will help you deploy your Football Twitter Bot to Render.com for continuous 24/7 operation with browser automation support.

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Push your bot code to a GitHub repository
3. **API Keys**: Prepare your Groq API key and Twitter account credentials
4. **Twitter Accounts**: Set up at least one Twitter account for data scraping

## Step 1: Prepare Your Repository

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Football Twitter Bot"
   git remote add origin https://github.com/johnbulau/football-twitter-bot.git
   git push -u origin main
   ```

## Step 2: Deploy on Render

1. **Create New Service**:
   - Go to your Render dashboard
   - Click "New +" → "Worker"
   - Connect your GitHub repository

2. **Configure Service**:
   - **Name**: `football-twitter-bot`
   - **Environment**: Docker
   - **Plan**: Starter ($7/month) or higher for reliable operation
   - **Auto-Deploy**: Enable (recommended)

3. **Set Environment Variables**:
   Add these in the Environment tab:

   **Required Variables**:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   TWITTER_POSTING_MODE=real
   TWITTER_POST_USERNAME=your_bot_twitter_username
   TWITTER_POST_PASSWORD=your_bot_twitter_password
   ```

   **Optional Variables**:
   ```
   TWITTER_POST_EMAIL=your_bot_twitter_email
   WEBHOOK_URL=your_discord_webhook_url_for_errors
   ```

## Step 3: Setup Twitter Accounts for Scraping

After deployment, you'll need to add Twitter accounts for data scraping:

1. **Access your service console** on Render
2. **Run the setup script**:
   ```bash
   python setup_twitter_accounts.py
   ```
3. **Add at least one Twitter account** following the prompts
4. **Verify the account** is working properly

## Step 4: Monitor and Manage

### Viewing Logs
- Go to your service dashboard
- Click on "Logs" tab to see real-time bot activity
- Monitor for successful tweet processing and any errors

### Managing Configuration
Update these files in your repository and push changes:

- `journalists.json` - Add/remove journalists to monitor
- `settings.json` - Adjust bot behavior, posting limits, keywords

### Key Settings to Adjust:
```json
{
  "check_interval": 300,          // Check every 5 minutes
  "max_posts_per_day": 50,        // Maximum posts per day
  "min_post_interval": 300,       // 5 minutes between posts
  "tweets_per_check": 10          // Tweets to check per journalist
}
```

## Step 5: Scaling and Optimization

### Performance Tips:
1. **Monitor Resource Usage**: Check CPU and memory usage in Render dashboard
2. **Adjust Check Intervals**: Increase intervals if hitting rate limits
3. **Upgrade Plan**: Consider higher plans for better performance

### Cost Optimization:
- **Starter Plan ($7/month)**: Good for testing and light usage
- **Standard Plan ($25/month)**: Recommended for production use
- **Pro Plan ($85/month)**: For high-volume operations

## Troubleshooting

### Common Issues:

**1. "No active accounts" warnings**:
- Run `python setup_twitter_accounts.py` to add Twitter accounts
- Verify account credentials are correct

**2. Browser automation failures**:
- The Docker container includes all browser dependencies
- Check logs for specific Playwright errors

**3. Groq API errors**:
- Verify your GROQ_API_KEY is set correctly
- Check Groq API usage limits

**4. Memory issues**:
- Consider upgrading to Standard plan for more RAM
- Monitor memory usage in Render dashboard

### Support Channels:
- Check service logs first
- Use webhook notifications for error monitoring
- Review bot.log for detailed error information

## Security Best Practices

1. **Never commit credentials** to your repository
2. **Use environment variables** for all sensitive data
3. **Enable two-factor authentication** on Render account
4. **Use dedicated Twitter accounts** for the bot (not personal accounts)
5. **Monitor webhook notifications** for suspicious activity

## Monitoring and Maintenance

### Daily Checks:
- Verify bot is processing tweets successfully
- Check error notifications via webhook
- Monitor posting rate and engagement

### Weekly Maintenance:
- Review journalist reliability scores
- Update journalists.json if needed
- Check Groq API usage and costs

### Monthly Tasks:
- Analyze bot performance metrics
- Consider adjusting posting strategies
- Review and update blocked keywords

## Advanced Configuration

### Custom Webhook Notifications:
Set up Discord or Slack webhooks for error monitoring:
```
WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
```

### Custom Posting Schedule:
Modify settings.json to control when the bot posts:
```json
{
  "posting_hours": {
    "start": 6,  // Start posting at 6 AM
    "end": 23    // Stop posting at 11 PM
  }
}
```

Your bot is now ready for 24/7 operation on Render.com with full browser automation support!