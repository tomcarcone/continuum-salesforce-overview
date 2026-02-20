FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# MCP server listens on this port
EXPOSE 8000

# Health check — the MCP endpoint is at /mcp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import httpx, sys; r=httpx.get('http://localhost:${PORT:-8000}/mcp/health', timeout=4); sys.exit(0 if r.status_code < 500 else 1)" || exit 1

CMD ["python", "server.py"]
