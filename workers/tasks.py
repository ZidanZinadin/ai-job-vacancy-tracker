import asyncio
import os

from celery import Celery

from scrapers.job_scraper import is_semantic_match, scrape_jobs_with_playwright

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("signaljobs", broker=REDIS_URL, backend=REDIS_URL)


@celery_app.task(name="scan_tracker")
def scan_tracker(tracker: dict) -> dict:
    jobs = asyncio.run(scrape_jobs_with_playwright(tracker["website_url"]))
    matches = [
        {
            "title": job.title,
            "link": job.link,
            "company": job.company,
            "location": job.location,
            "salary": job.salary,
            "hash": job.content_hash,
        }
        for job in jobs
        if is_semantic_match(job, tracker.get("keywords", []), tracker.get("location"))
    ]

    return {
        "tracker_id": tracker["id"],
        "found": len(jobs),
        "matched": len(matches),
        "matches": matches,
    }
