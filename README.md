# N8N SEO Automation

A Django web app that powers SEO workflows with [n8n](https://n8n.io): keyword research, SERP metadata, blog publishing, and backlink ingestion. The app exposes webhooks for n8n and provides a staff UI for managing keywords, metadata, and blogs.

---

## Features

- **Keywords** — Seed keyword research, bulk import, approve/analyze flow, and optional n8n-triggered analysis
- **SERP metadata** — Store and approve metadata (title, intent, outline, must-cover, secondary keywords) per keyword
- **Blogs** — Create blogs from metadata, upload featured images via webhook, manage drafts
- **Backlinks** — Ingest backlink data via webhook; list and search in the UI
- **n8n integration** — Webhooks for keyword research, keyword analysis, blog creation, image upload, and backlinks

---

## Tech stack

- **Backend:** Django 6.x, Python 3.12
- **Database:** PostgreSQL 17
- **Orchestration:** Docker Compose (Django app, n8n, Postgres, Adminer)
- **Automation:** n8n (optional; webhooks work with any HTTP client)

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- For local (non-Docker) runs: Python 3.12+, PostgreSQL 17, and a running n8n instance if using workflows

---

## Quick start (Docker)

1. **Clone and enter the repo**
   ```bash
   git clone <repo-url> n8n-seo-automation && cd n8n-seo-automation
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env: set DB_*, WEBHOOK_TOKEN, and optional N8N_* / API keys
   ```

3. **Start services**
   ```bash
   docker compose up -d
   ```

4. **Run migrations and create a staff user**
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```

5. **Import n8n workflows**
   - Open n8n: http://localhost:5678 (log in with `N8N_BASIC_AUTH_USER` / `N8N_BASIC_AUTH_PASSWORD` from `.env`).
   - For each workflow: **Workflows** → **Import from File** (or **Add workflow** → **Import from File**), then select a JSON file from the `n8n-workflows/` folder:
     - `keyword_research_workflow.json`
     - `keyword_analyze_workflow.json`
     - `blog_automation_workflow.json`
     - `backlinks_workflow.json`
     - `tavily_tool_workflow.json`
   - After importing, set each workflow’s webhook/HTTP nodes to use `http://web:8000` (or your web service URL) and ensure `.env` credentials (e.g. DataForSEO, OpenAI, Tavily, `WEBHOOK_TOKEN`) are configured in n8n if the workflows use them.

6. **Open the app**
   - Web UI: http://localhost:8000  
   - n8n: http://localhost:5678  
   - Adminer (DB): http://localhost:8080  

Staff-only pages (keywords, metadata, blogs, backlinks) require logging in with a user that has `is_staff=True`.

---

## Environment variables

| Variable | Description | Default |
|----------|-------------|--------|
| `DB_NAME` | PostgreSQL database name | `web` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `postgres` |
| `DB_HOST` | PostgreSQL host (use `db` in Docker) | — |
| `DB_PORT` | PostgreSQL port | `5432` |
| `WEBHOOK_TOKEN` | Shared secret for webhook auth (optional) | — |
| `N8N_BASE_URL` | n8n base URL (e.g. `http://n8n:5678`) | — |
| `N8N_KEYWORD_RESEARCH_WEBHOOK_URL` | Path to keyword-research webhook | — |
| `N8N_KEYWORD_ANALYZE_WEBHOOK_URL` | Path to keyword-analyze webhook | — |
| `N8N_BLOG_POST_WEBHOOK_URL` | Path to blog-post webhook | — |
| `DATA_FOR_SEO_USERNAME` / `DATA_FOR_SEO_PASSWORD` | DataForSEO (used by n8n) | — |
| `OPEN_AI_API_KEY` | OpenAI (used by n8n) | — |
| `TAVILY_API_KEY` | Tavily (used by n8n) | — |

Copy `.env.example` to `.env` and set values for your environment.

---

## Project structure

```
n8n-seo-automation/
├── docker-compose.yml    # web, n8n, db, adminer
├── .env.example
├── web/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── api/              # Webhook endpoints (n8n → app)
│   ├── backlink/         # Backlinks app (models, views, admin)
│   ├── kw/               # Keywords app (list, edit, approve, analyze)
│   ├── post/             # Metadata + Blogs apps
│   ├── static/
│   ├── templates/        # Base layout, home
│   └── web/              # Django project (settings, urls)
```

---

## Web UI routes

| Path | Description |
|------|-------------|
| `/` | Dashboard (counts + quick actions) |
| `/kw/keywords/` | Keyword list (search, approve, edit, analyze, delete) |
| `/posts/metadata/` | Metadata list (approve, create blog) |
| `/posts/blogs/` | Blog list (create from metadata, delete) |
| `/backlinks/` | Backlink list (search) |
| `/admin/` | Django admin |

All of the above (except `/` and `/admin/`) are staff-only.

---

## API webhooks (n8n → app)

Base URL: `http://<web-host>/api/v1/` (e.g. `http://web:8000/api/v1/` from another container).

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `keyword-research-webhook/` | POST | Bulk-create keywords from research payload (`seedKeyword`, `keywords[]`) |
| `keyword-analyze-webhook/` | POST | Receive analysis results; create Metadata, set keyword `is_analyzed` |
| `keyword-analyze-cron-job-webhook/` | GET | Return approved, not-yet-analyzed keywords (for n8n cron) |
| `blog-post-webhook/` | POST | Create a blog (title, slug, content, alt_text); returns `blog_id` |
| `image-upload-webhook/` | POST | Upload featured image for a blog (`blog_id`, `file`, `extension`) |
| `backlinks-webhook/` | POST | Bulk-create backlinks (`backlinks[]` with camelCase fields) |

Request bodies are JSON unless noted (e.g. image upload is multipart). Use `WEBHOOK_TOKEN` in headers if you add token checks in the app.

---

## Development (without Docker)

1. Create a virtualenv and install dependencies:
   ```bash
   cd web && python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Set `DB_*` in `.env` to point to your local Postgres (or override in `web/web/settings.py`).

3. Run migrations and server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. Optional: run n8n separately and set `N8N_BASE_URL` to that instance.

---

## Production checklist

- [ ] Set `DEBUG=False` and configure `ALLOWED_HOSTS`.
- [ ] Use a strong `SECRET_KEY` and keep it out of version control.
- [ ] Set `DB_*` and `WEBHOOK_TOKEN` (and any API keys) in the environment.
- [ ] Serve the app with a proper ASGI/WSGI server (e.g. Gunicorn) and reverse proxy (e.g. Nginx).
- [ ] Run `collectstatic` and serve static/media via the reverse proxy or CDN.
- [ ] Restrict webhook endpoints (e.g. by IP or token) if they are public.
