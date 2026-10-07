# ===========================================
# NetGuard Cognitive AI Demo Container
# ===========================================

FROM python:3.10-slim

# Install system dependencies (curl for container healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy production requirements and install dependencies
COPY requirements-demo.txt ./
RUN pip install --no-cache-dir -r requirements-demo.txt

# Copy required application assets & backend scripts
COPY data/ ./data/
COPY results/models/ ./results/models/
COPY memory/ ./memory/
COPY demo/ ./demo/

EXPOSE 8000

# Run FastAPI backend via Uvicorn
CMD ["python3", "-m", "uvicorn", "demo.server:app", "--host", "0.0.0.0", "--port", "8000"]
