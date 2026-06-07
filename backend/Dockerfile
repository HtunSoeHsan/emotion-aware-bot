# Use an official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0

# Set working directory
WORKDIR /app

# Install system dependencies needed for building packages (pyaudio, opencv, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    portaudio19-dev \
    libgl1 \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NLTK datasets
RUN python -c "import nltk; nltk.download('vader_lexicon', quiet=True); nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# Copy the rest of the application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["python", "main.py"]
