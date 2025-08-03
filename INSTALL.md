# Installation Guide

## Prerequisites
- Python 3.8 or higher
- Git
- Twitter account for posting

## Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/football-twitter-bot.git
   cd football-twitter-bot
   ```

2. **Install Python dependencies**
   ```bash
   pip install aiohttp groq playwright trafilatura twscrape
   ```

3. **Install browser dependencies (for real posting)**
   ```bash
   playwright install-deps
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run the bot**
   ```bash
   python main.py
   ```

## Getting API Keys

### Groq API (Free)
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for free account
3. Create API key in API Keys section
4. Add to .env file

### Twitter Account
- Use your posting account credentials
- Enable 2FA is recommended
- Use app-specific password if available

## Troubleshooting

**Browser dependencies missing?**
```bash
playwright install-deps
```

**Python version issues?**
- Ensure Python 3.8+ is installed
- Use virtual environment if needed

**API connection problems?**
- Check your Groq API key
- Verify internet connection
- Check rate limits