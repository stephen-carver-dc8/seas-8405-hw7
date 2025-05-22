FROM python:slim

# Set working directory
WORKDIR /app

# Get ping
RUN apt update && apt install -y curl iputils-ping && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

# Copy application code and fix permissions
COPY . .
RUN chown -R appuser:appuser /app
RUN chmod +x healthcheck.sh

# Switch to the non-root user
USER appuser

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD healthcheck.sh