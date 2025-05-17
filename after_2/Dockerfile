FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Get curl and ping
RUN apt-get update && apt-get install -y iputils-ping curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

# Copy application code and fix permissions
COPY . .
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1