# SignalJobs Architecture

## Runtime Shape

```text
Next.js frontend
  -> FastAPI backend
  -> Redis queue
  -> Celery workers
  -> Playwright scrapers
  -> PostgreSQL
  -> Resend / Telegram / Firebase notifications
```

## Core Data Model

- `users`: account identity and billing owner.
- `trackers`: one monitoring rule per site, keyword set, location, frequency, and channel set.
- `jobs`: normalized job listings found by scrapers.
- `notifications`: one sent alert per user and job.
- `scrape_logs`: scan outcomes, timings, and error payloads.

## Duplicate Detection

Use three identifiers in order:

1. Native job ID when available.
2. Canonical URL hash.
3. Normalized content hash from title, company, location, salary, and link.

Only notify when no previous job exists for that tracker and hash.

## Scraper Policy

- Prefer direct HTML parsing for simple pages.
- Use Playwright for JS-heavy pages.
- Add randomized wait times and viewport/user-agent variation.
- Do not aggressively poll protected sites.
- For LinkedIn and Indeed, start with user-provided URLs and conservative schedules.

## MVP Scope

- Email auth.
- Create, pause, delete, and scan trackers.
- Keyword matching with location and salary filters.
- Email and Telegram alerts.
- Dashboard with unread jobs and scan logs.

## Later AI Scope

- Embeddings for semantic keyword expansion.
- CV to vacancy scoring.
- Job summary extraction.
- Cover letter draft generation.

## Deployment

- Frontend: Vercel.
- API and worker: Render or Railway.
- Database: Supabase or Neon Postgres.
- Redis: Upstash, Railway Redis, or Render Redis.
- Error tracking: Sentry.
- Product analytics: PostHog.
