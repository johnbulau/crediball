FROM python:3.11-slim

# Install system dependencies required for browser automation
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    xvfb \
    libxss1 \
    libgconf-2-4 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements-render.txt .
RUN pip install --no-cache-dir -r requirements-render.txt

# Install Playwright browsers and dependencies
RUN playwright install --with-deps

# Copy application code
COPY . .

# Create necessary directories and files
RUN mkdir -p /app/logs
RUN touch /app/bot.log

# Set environment variables
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# Start Xvfb (virtual display) and run the bot
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & python main.py"]