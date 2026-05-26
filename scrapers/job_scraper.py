from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class ScrapedJob:
    title: str
    link: str
    company: str | None = None
    location: str | None = None
    salary: str | None = None
    description: str | None = None

    @property
    def content_hash(self) -> str:
        source = "|".join(
            [
                self.title.strip().lower(),
                self.link.strip().lower(),
                (self.company or "").strip().lower(),
                (self.location or "").strip().lower(),
                (self.salary or "").strip().lower(),
            ]
        )
        return sha256(source.encode("utf-8")).hexdigest()


async def scrape_jobs_with_playwright(url: str) -> list[ScrapedJob]:
    """Playwright implementation placeholder.

    Production implementation should:
    - launch chromium headless
    - use randomized user agent and viewport
    - wait for network idle or known listing selectors
    - extract title, link, company, location, salary, and description
    - return normalized ScrapedJob instances
    """
    return [
        ScrapedJob(
            title="Example vacancy",
            company="Example employer",
            location="London",
            salary="£30,000",
            link=url,
            description="Placeholder result for wiring the worker pipeline.",
        )
    ]


def is_semantic_match(job: ScrapedJob, keywords: list[str], location: str | None) -> bool:
    haystack = " ".join(
        [
            job.title,
            job.company or "",
            job.location or "",
            job.salary or "",
            job.description or "",
        ]
    ).lower()
    keyword_match = any(keyword.lower() in haystack for keyword in keywords)
    location_match = not location or location.lower() in haystack
    return keyword_match and location_match
