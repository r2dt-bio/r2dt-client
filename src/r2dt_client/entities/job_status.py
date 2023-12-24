from enum import Enum


class JobStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"

    @property
    def final(self) -> bool:
        return self == JobStatus.FINISHED
