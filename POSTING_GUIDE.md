# Twitter Posting Guide

## Overview

The Football Twitter Bot now supports **real Twitter posting** in addition to simulation mode. You can configure the bot to actually post tweets to a Twitter account using browser automation.

## How It Works

### Two Modes Available

1. **Simulation Mode** (Default & Safe)
   - Bot processes tweets and shows what it would post
   - No actual posting to Twitter
   - Perfect for testing and development

2. **Real Posting Mode**
   - Bot actually posts tweets to a configured Twitter account
   - Uses browser automation (Playwright) to post tweets
   - Requires a dedicated bot Twitter account

## Quick Setup

### Option 1: Simulation Mode (Recommended for Testing)
```bash
python setup_posting.py
# Choose option 2: "Use simulation mode"
```

### Option 2: Real Posting Mode
```bash
python setup_posting.py
# Choose option 1: "Set up real Twitter posting"
# Follow the prompts to enter your bot account credentials
```

### Option 3: Via Bot Manager
```bash
python bot_manager.py
# Choose option 9: "Configure posting"
```

## Important Notes

### For Real Posting
- **Use a separate Twitter account** for your bot, NOT your personal account
- The bot account should be dedicated solely to the football bot
- Keep your credentials secure (they're stored in `.env` file)
- The `.env` file is automatically ignored by git for security

### Security
- Never share your `.env` file
- Never commit credentials to version control
- Use strong passwords for your bot account
- Consider enabling 2FA on your bot account (may require additional setup)

## Testing

### Test Posting Functionality
```bash
python test_posting_system.py
```

### Test Via Bot Manager
```bash
python bot_manager.py
# Choose option 8: "Test tweet processing"
```

### Test Individual Tweets
```bash
python test_tweet.py "Your custom tweet text here"
```

## Environment Variables

The bot uses these environment variables for posting:

```bash
# Posting mode: "simulator" or "real"
TWITTER_POSTING_MODE=simulator

# For real posting (only needed if mode=real)
TWITTER_POST_USERNAME=your_bot_username
TWITTER_POST_PASSWORD=your_bot_password
TWITTER_POST_EMAIL=your_bot_email  # Optional, for verification
```

## How the Bot Posts

### Processing Flow
1. **Monitor** journalists' tweets
2. **Filter** for football content
3. **Analyze** with AI (Groq) for credibility and rewriting
4. **Format** with special styling (HERE WE GO, etc.)
5. **Post** to Twitter (real or simulated)

### Posting Features
- **Rate limiting**: Maximum 50 posts per day
- **Minimum intervals**: 5 minutes between posts
- **Special formatting**: "HERE WE GO" for tier-1 journalists
- **Reliability scores**: Displayed with each post
- **Error handling**: Webhook notifications for issues

### Safety Features
- **Simulation mode** by default
- **Rate limiting** to prevent spam
- **Error logging** and notifications
- **Content filtering** for quality control

## Troubleshooting

### Common Issues

#### "No active accounts" warnings
This is normal - it refers to Twitter scraping accounts (twscrape), not posting accounts.

#### Browser automation fails
- Ensure Playwright dependencies are installed
- Check internet connection
- Verify Twitter credentials
- Twitter may require manual verification occasionally

#### Posts not appearing
- Check if account is suspended or limited
- Verify credentials are correct
- Check Twitter's posting limits
- Review bot logs for errors

### Getting Help
1. Check the logs in `bot.log`
2. Test with simulation mode first
3. Use the bot manager for diagnostics
4. Review error messages carefully

## File Structure

```
├── twitter_poster.py          # Main posting logic
├── setup_posting.py           # Interactive setup script
├── test_posting_system.py     # Posting tests
├── bot_manager.py             # Management interface
├── .env                       # Credentials (auto-created)
└── POSTING_GUIDE.md          # This guide
```

## Next Steps

1. **Start with simulation mode** to test the system
2. **Configure a bot account** if you want real posting
3. **Run the bot** and monitor its behavior
4. **Review posts** before switching to real mode
5. **Set up monitoring** for any issues

The bot is designed to be safe and easy to use. Always test in simulation mode first!