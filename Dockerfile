FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update &amp;&amp; apt-get install -y --no-install-recommends \
    gcc \
    &amp;&amp; rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd --create-home appuser &amp;&amp; chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "api.api_call:app", "--host", "0.0.0.0", "--port", "8000"]
