from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from .schemas import JobRead, ScanRequest, TrackerCreate, TrackerRead

app = FastAPI(title="SignalJobs API", version="0.1.0")

TRACKERS: dict[str, TrackerRead] = {}
JOBS: dict[str, JobRead] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/trackers", response_model=TrackerRead)
def create_tracker(payload: TrackerCreate) -> TrackerRead:
    tracker_id = str(uuid4())
    tracker = TrackerRead(
        id=tracker_id,
        user_id="dev-user",
        active=True,
        created_at=datetime.now(UTC),
        **payload.model_dump(),
    )
    TRACKERS[tracker_id] = tracker
    return tracker


@app.get("/trackers", response_model=list[TrackerRead])
def list_trackers() -> list[TrackerRead]:
    return list(TRACKERS.values())


@app.patch("/trackers/{tracker_id}/pause", response_model=TrackerRead)
def pause_tracker(tracker_id: str) -> TrackerRead:
    tracker = TRACKERS.get(tracker_id)
    if tracker is None:
        raise HTTPException(status_code=404, detail="Tracker not found")
    updated = tracker.model_copy(update={"active": False})
    TRACKERS[tracker_id] = updated
    return updated


@app.post("/scans")
def enqueue_scan(payload: ScanRequest) -> dict[str, str]:
    if payload.tracker_id not in TRACKERS:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return {"status": "queued", "tracker_id": payload.tracker_id}


@app.get("/jobs", response_model=list[JobRead])
def list_jobs() -> list[JobRead]:
    return sorted(JOBS.values(), key=lambda job: job.created_at, reverse=True)
