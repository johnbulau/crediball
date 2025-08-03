# Football Twitter Bot ⚽

A sophisticated Python-based Twitter bot that monitors top football journalists, analyzes their credibility, and reposts content with enhanced formatting and reliability scoring. Built using only free APIs and services.

## Features

- **Free Operation**: Uses twscrape for Twitter data and Groq API for AI processing
- **Journalist Monitoring**: Tracks multiple football journalists with configurable reliability scores  
- **AI-Powered Content**: Analyzes and rewrites posts for better clarity and engagement
- **Credibility Scoring**: Displays reliability scores for each source
- **Smart Formatting**: Special handling for "Here We Go" posts and transfer news
- **Error Reporting**: Webhook notifications for monitoring and debugging
- **Rate Limiting**: Prevents API abuse and Twitter restrictions

## Quick Start

### 1. Get Your Free API Keys

**Groq API (Free AI Processing)**
- Visit https://console.groq.com/
- Sign up for free account
- Create API key in the API Keys section
- Free tier: 1,000 requests/day, 6,000 tokens/minute

### 2. Run the Setup

The bot is ready to run! Use the bot manager for easy setup:

```bash
python bot_manager.py
```

This will show you a menu to:
- Add/remove journalists and update their reliability scores
- Set up Twitter accounts for data access
- View current settings
- Start the bot

### 3. Add Twitter Accounts

Before the bot can fetch tweets, you need to add Twitter accounts:

```bash
python setup_twitter_accounts.py
```

**Important**: Use secondary Twitter accounts, not your personal ones.

### 4. Test the Bot (Optional)

Test how the bot processes tweets before going live:

```bash
python test_tweet.py "https://x.com/FabrizioRomano/status/1951901347219206602"
```

Or use the bot manager:
```bash
python bot_manager.py
# Choose option 8 for tweet testing
```

### 5. Start Monitoring

```bash
python main.py
```

The bot will start monitoring all configured journalists and posting improved versions of their football-related tweets.

## Example Output

**Original Tweet** (Fabrizio Romano):
```
🚨⚪️ Kylian Mbappé to Real Madrid, HERE WE GO! Every document has been signed, sealed and completed.

Real Madrid, set to announce Mbappé as new signing next week after winning the Champions League.

Mbappé made his decision in February; he can now be considered new Real player.
```

**Bot's Repost**:
```
🚨⚪️ MBAPPE TO REAL MADRID! HERE WE GO!🚨
Kylian Mbappé has officially signed for Real Madrid. All documents are completed, and the club will announce the transfer next week. Mbappé made his decision back in February.

Source - @FabrizioRomano
[Reliability Score: 🟢 - 99.9%]
```

## Configuration

### Pre-configured Journalists

The bot comes with 15+ top football journalists already configured:

- **Tier 1 (90%+)**: Fabrizio Romano (99.9%), David Ornstein (99.5%), James Robson (95%)
- **Tier 2 (70-90%)**: Sky Sports, The Athletic, Guardian reporters
- **Tier 3-4 (20-70%)**: Lower reliability sources like The Sun (20%)

### Easy Management

Use the bot manager to easily:
- Add new journalists: `python bot_manager.py` → Option 2
- Update reliability scores: `python bot_manager.py` → Option 3
- View all journalists: `python bot_manager.py` → Option 5

### Settings

All settings are in `settings.json`:
- **Rate Limiting**: Max 50 posts/day, 5-minute intervals
- **AI Model**: Llama3-8b-8192 (free via Groq)
- **Special Formatting**: "HERE WE GO" for tier-1 journalists, "TRANSFER COMPLETED" for others

## Advanced Features

### Webhook Notifications
Set `WEBHOOK_URL` environment variable to receive error notifications and status updates.

### Rate Limiting
- Maximum 50 posts per day
- 5-minute minimum interval between posts
- Automatic daily reset

### Content Filtering
- Only processes football-related content
- Excludes American football
- Filters retweets and replies
- Minimum engagement thresholds

## Troubleshooting

### "No active accounts" Error
This means you need to add Twitter accounts:
```bash
python setup_twitter_accounts.py
```

### Rate Limiting Issues
- Wait for rate limits to reset (usually 15 minutes)
- Reduce `check_interval` in settings.json
- Add more Twitter accounts for better distribution

### API Errors
- Check your Groq API key is valid
- Ensure you have free quota remaining
- Verify internet connection

## Security Notes

- Never commit API keys to version control
- Use secondary Twitter accounts for scraping
- Keep webhook URLs secure
- Monitor rate limits to avoid account restrictions

## Installation (Manual)

If you prefer manual setup:

1. **Install Dependencies**
```bash
pip install aiohttp twscrape groq
```

2. **Set Environment Variables**
```bash
export GROQ_API_KEY="your_groq_api_key_here"
export WEBHOOK_URL="your_webhook_url_here"  # Optional
```

3. **Add Twitter Accounts**
```bash
python setup_twitter_accounts.py
```

4. **Configure Journalists** (Optional)
Edit `journalists.json` to add/remove journalists or modify their reliability scores.

5. **Start the Bot**
```bash
python main.py
```

## File Structure

```
football-twitter-bot/
├── main.py                 # Main bot entry point
├── bot.py                  # Core bot logic  
├── ai_processor.py         # Groq AI integration
├── twitter_manager.py      # Twitter data handling
├── config.py              # Configuration management
├── error_handler.py        # Error reporting
├── bot_manager.py         # Easy management interface
├── setup_twitter_accounts.py # Twitter account setup
├── journalists.json        # Journalist configurations
├── settings.json          # Bot settings
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Disclaimer

This bot is for educational purposes. Ensure compliance with Twitter's Terms of Service and rate limiting guidelines. Use responsibly and respect content creators' rights.
