# SignalJobs

AI job vacancy tracker platform for monitoring job websites, deduplicating listings, scoring matches, and notifying users.

## What is included

- `index.html` - dependency-free interactive MVP dashboard you can open immediately.
- `backend/app` - FastAPI skeleton for trackers, jobs, and scan dispatch.
- `workers` - Celery task entrypoint for scheduled scans.
- `scrapers` - Playwright-oriented scraper contract with hashing-based duplicate detection.
- `docs/architecture.md` - production architecture and deployment notes.

## Local preview

Open:

```text
/Users/zinadinzidan/Documents/Project/ai-job-vacancy-tracker/index.html
```

The prototype stores trackers and UI state in `localStorage`.

## Production stack target

- Frontend: Next.js, Tailwind CSS, shadcn/ui, Zustand
- Backend: FastAPI, SQLAlchemy, Pydantic
- Queue: Redis + Celery
- Scraping: Playwright
- Database: PostgreSQL
- Email: Resend
- Push: Firebase Cloud Messaging
- Alerts: Telegram Bot API
- Monitoring: Sentry

## MVP milestones

1. Replace the static UI with a Next.js app using the same information architecture.
2. Add auth and user-scoped trackers.
3. Persist trackers and jobs in PostgreSQL.
4. Run scheduled scans via Celery and Redis.
5. Send email and Telegram alerts for new job hashes.
6. Add embeddings for semantic matching once keyword matching is stable.
