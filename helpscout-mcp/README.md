# HelpScout MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that connects Claude to your HelpScout knowledge base. Once deployed, you can add it as a connector in Claude's **Ask your org** feature so your team can ask Claude questions and get answers sourced directly from your help articles.

## What it does

The server exposes four tools to Claude:

| Tool | Description |
|------|-------------|
| `search_articles` | Full-text search across published articles |
| `get_article` | Fetch the complete content of an article by ID |
| `list_collections` | Browse all top-level collections in your knowledge base |
| `list_articles` | List all articles within a specific collection |

---

## Prerequisites

- Python 3.11+
- A HelpScout account with Docs enabled
- Your HelpScout **Docs API key** (see below)

### Getting your HelpScout API key

1. Log in to Help Scout
2. Click your avatar → **Your Profile**
3. Select **Authentication** → **API Keys** tab
4. Click **Generate an API Key** and copy the value

---

## Local development

```bash
# 1. Clone and enter the directory
cd helpscout-mcp

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set HELPSCOUT_API_KEY=your_key_here

# 5. Run the server
python server.py
# Server starts at http://localhost:8000/mcp
```

### Test with the MCP Inspector

```bash
# Run in stdio mode for the MCP Inspector
MCP_TRANSPORT=stdio HELPSCOUT_API_KEY=your_key python server.py

# Or use the CLI shorthand
mcp dev server.py
```

---

## Deployment

The server must be publicly accessible over HTTPS for Claude's "Ask your org" connector to reach it. Choose any of the options below.

### Option A — Railway (recommended, simplest)

1. Push this directory to a GitHub repo
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Select your repo
4. Add the environment variable `HELPSCOUT_API_KEY` in the Railway dashboard
5. Railway auto-detects the `Dockerfile` and deploys. Note the public URL it assigns (e.g. `https://your-app.railway.app`)

### Option B — Render

1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repo
3. Set **Environment** → add `HELPSCOUT_API_KEY`
4. Set **Start Command** to `python server.py`
5. Deploy and note the URL

### Option C — Docker (any cloud VM)

```bash
# Build
docker build -t helpscout-mcp .

# Run (replace with your key)
docker run -d \
  -e HELPSCOUT_API_KEY=your_key_here \
  -p 8000:8000 \
  helpscout-mcp
```

Ensure port 8000 is open and put a TLS-terminating reverse proxy (nginx, Caddy, etc.) in front for HTTPS.

---

## Connecting to Claude's "Ask your org"

1. Open [claude.ai](https://claude.ai) → your organisation's settings
2. Navigate to **Integrations** → **Ask your org** → **Add connector**
3. Choose **Custom (MCP)**
4. Enter your server URL:
   ```
   https://your-deployed-server.example.com/mcp
   ```
5. Save. Claude will now be able to call the server's tools when answering questions from your team.

---

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HELPSCOUT_API_KEY` | Yes | — | HelpScout Docs API key |
| `PORT` | No | `8000` | Port to bind to |
| `HOST` | No | `0.0.0.0` | Host to bind to |
| `MCP_TRANSPORT` | No | `streamable-http` | Set to `stdio` for local Inspector testing |

---

## Security notes

- The server communicates with HelpScout over HTTPS only.
- Your API key is never exposed in responses — keep it in environment variables, never in source code.
- The server only requests **published, public** articles by default.
- Add an authentication layer (bearer token header check) if you need to restrict which MCP clients can connect.
