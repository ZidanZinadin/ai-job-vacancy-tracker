from datetime import datetime
from typing import Literal

from pydantic import BaseModel, HttpUrl


NotificationMethod = Literal["email", "telegram", "push"]
TrackerFrequency = Literal["1h", "4h", "12h"]


class TrackerCreate(BaseModel):
    website_url: HttpUrl
    keywords: list[str]
    location: str | None = None
    salary_min: int | None = None
    job_type: str | None = None
    frequency: TrackerFrequency = "4h"
    notification_methods: list[NotificationMethod] = ["email"]


class TrackerRead(TrackerCreate):
    id: str
    user_id: str
    active: bool
    created_at: datetime


class JobRead(BaseModel):
    id: str
    tracker_id: str
    title: str
    company: str | None = None
    location: str | None = None
    salary: str | None = None
    link: HttpUrl
    hash: str
    match_score: int
    created_at: datetime


class ScanRequest(BaseModel):
    tracker_id: str
