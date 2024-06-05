
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
from threading import Lock

@dataclass
class Event:
    timestamp: datetime
    data: str




@dataclass 


class Job:
    status:str
    events: List[Event]
    results: str


jobs_lock = Lock()
jobs: Dict[str, "Job"]= {}


def append_event(job_id: str, event_data: str):
    with jobs_lock:
        if job_id not in jobs:
            print(f"start jobs: {job_id}")
            jobs[job_id] = Job(
                status="Started",
                events=[],
                results="",
            )
        else:
            print(f"append event: {job_id}")
        jobs[job_id].events.append(Event(timestamp=datetime.now(), data=event_data))