from typing import Optional

from r2dt_client.entities.exceptions import R2dtError
from r2dt_client.entities.format import Format
from r2dt_client.entities.job_status import JobStatus


__all__ = ["R2dtJob"]


class R2dtJob:
    _job_id: str
    _status: JobStatus
    _sequence: str
    _results: dict[Format, str]

    def __init__(
        self,
        job_id: str,
        sequence: str,
        status: JobStatus = JobStatus.UNKNOWN,
        results: Optional[dict[Format, str]] = None,
    ):
        self._job_id = job_id
        self._sequence = sequence
        self._status = status or JobStatus.UNKNOWN
        self._results = results or {}

    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def sequence(self) -> str:
        return self._sequence

    @property
    def results(self) -> dict[Format, str]:
        return self._results

    @property
    def done(self) -> bool:
        return self.status.final

    @property
    def status(self) -> JobStatus:
        return self._status

    @status.setter
    def status(self, status: JobStatus) -> None:
        if status != self._status and self._status.final:
            raise R2dtError(
                f"Cannot update status for finished job with "
                f"id: {self._job_id}, current status: {self._status}"
            )
        self._status = status

    def __str__(self) -> str:
        return f"R2dtJob(job_id={self._job_id}, status={self.status})"

    __repr__ = __str__
