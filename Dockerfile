FROM python:3.12-slim

# Install system dependencies for Discord voice
RUN apt-get update && apt-get install -y \
    libopus0 \
    libopus-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Start the bot
CMD ["python", "bot.py"]