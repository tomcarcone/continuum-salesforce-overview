FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# MCP server listens on this port
EXPOSE 8000

# No HTTP health check needed — Render monitors the process directly.

CMD ["python", "server.py"]
