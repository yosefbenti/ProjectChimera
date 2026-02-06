FROM python:3.11-slim

WORKDIR /app

# Install build deps for common packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# Install Python deps if requirements file exists; allow build to continue
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt || true

CMD ["pytest", "-q"]
