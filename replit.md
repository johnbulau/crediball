# Football Twitter Bot

## Overview

A Python-based Twitter bot that monitors football journalists, analyzes their credibility, and reposts content with improved formatting. The bot uses free APIs (twscrape for Twitter data, Groq for AI processing) to track multiple football journalists, rate their reliability, and rewrite posts for better clarity and engagement. It includes smart formatting for transfer news, rate limiting to prevent API abuse, and error reporting via webhooks.

## Recent Changes (August 2025)

✓ Completed full bot implementation with all core features
✓ Integrated Groq API for free AI processing (Llama3-8b-8192 model)
✓ Built comprehensive Twitter management system using twscrape
✓ **NEW: Added real Twitter posting functionality with browser automation**
✓ **NEW: Created posting setup system with simulation and real modes**
✓ **NEW: Implemented Playwright-based tweet posting with credential management**
✓ Created user-friendly management tools (bot_manager.py, setup_posting.py)
✓ Configured 15+ pre-loaded football journalists with reliability scores
✓ Implemented smart formatting for "Here We Go" posts and transfer completions
✓ Added comprehensive error handling and webhook notifications
✓ Created complete documentation and setup guides
✓ **NEW: Built posting safety features with rate limiting and simulation mode**
✓ **NEW: Created complete Render.com deployment setup with Docker container**
✓ **NEW: Built deployment scripts and health checking for 24/7 operation**
✓ **NEW: Added GitHub preparation tools and comprehensive deployment guide**

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Components

**Bot Architecture**: Modular design with separate components for AI processing, Twitter management, configuration, and error handling. The main bot orchestrates all components through async/await patterns.

**AI Processing**: Uses Groq API with Llama3-8b-8192 model for text analysis and rewriting. Implements connection testing and session management for reliable API communication.

**Twitter Integration**: Built on twscrape library for scraping Twitter data without official API costs. Handles user tweet fetching, rate limiting, and content filtering. **NEW: Includes Playwright-based posting system for real Twitter posting with browser automation.**

**Configuration Management**: JSON-based configuration system with settings.json for bot behavior and journalists.json for source management. Supports environment variable overrides.

**Error Handling**: Centralized error reporting with webhook notifications for monitoring. Tracks error counts and timestamps for debugging.

**Rate Limiting**: Multi-level rate limiting including posts per day, minimum intervals between posts, and API request throttling to prevent service abuse.

**Content Processing**: Special handling for "Here We Go" posts from tier-1 journalists, transfer completion announcements, and customizable emoji formatting.

### Data Management

**In-Memory Storage**: Uses sets and dictionaries to track processed tweets, rate limiting counters, and journalist data. No persistent database required.

**Configuration Files**: 
- `settings.json`: Bot behavior, rate limits, content filters, formatting rules
- `journalists.json`: Journalist profiles with reliability scores and tier classifications
- `.env`: Twitter posting credentials and mode configuration (simulation vs real posting)

**Logging**: File and console logging with structured error reporting and webhook notifications.

### Processing Pipeline

**Monitoring Flow**: Bot continuously monitors configured journalists → filters content by keywords and engagement → processes through AI for rewriting → applies formatting rules → posts with credibility scores.

**Content Filtering**: Supports football-specific keywords, excludes American football content, filters out retweets and replies, and applies minimum engagement thresholds.

**Async Architecture**: All network operations use async/await patterns with aiohttp for HTTP requests and proper session management.

## External Dependencies

**AI Services**: Groq API for natural language processing and content rewriting using Llama3-8b-8192 model.

**Twitter Data**: twscrape library for Twitter scraping (requires pre-configured Twitter accounts for access).

**Browser Automation**: Playwright for real Twitter posting capabilities through browser automation.

**HTTP Client**: aiohttp for all async HTTP communications with external APIs.

**Webhook Integration**: Configurable webhook endpoints for error reporting and monitoring notifications.

**Environment Configuration**: Supports environment variables for sensitive configuration like API keys and webhook URLs.

## Deployment Information

**Platform**: Render.com - Optimized for 24/7 operation with Docker containerization

**Container**: Custom Docker image with all browser dependencies and system requirements pre-installed

**Deployment Files**:
- `Dockerfile`: Complete containerization with Playwright browser support
- `render.yaml`: Render service configuration with environment variables
- `requirements-render.txt`: Python dependencies for deployment
- `RENDER_DEPLOYMENT.md`: Comprehensive deployment guide

**Required Environment Variables for Deployment**:
- `GROQ_API_KEY`: Groq API key for AI processing
- `TWITTER_POST_USERNAME`: Bot Twitter account username  
- `TWITTER_POST_PASSWORD`: Bot Twitter account password
- `TWITTER_POST_EMAIL`: Bot Twitter account email (optional)
- `WEBHOOK_URL`: Discord/Slack webhook for error notifications (optional)

**Setup Tools**:
- `prepare_for_github.py`: Repository preparation and cleanup
- `render_setup.py`: Pre-deployment configuration checker
- `health_check.py`: Service health monitoring endpoint

**Post-Deployment**: Run `python setup_twitter_accounts.py` in Render console to configure Twitter scraping accounts.