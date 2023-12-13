from typing import Optional

from r2dt_client.session.entities.exceptions import R2dtError
from r2dt_client.session.entities.format import Format
from r2dt_client.session.entities.job_status import JobStatus


__all__ = ["R2dtJob"]


class R2dtJob:
    job_id: str
    _status: JobStatus
    email: str
    sequence: str
    results: dict[Format, str]

    def __init__(
        self,
        email: str,
        job_id: str,
        sequence: str,
        status: JobStatus = JobStatus.UNKNOWN,
        results: Optional[dict[Format, str]] = None,
    ):
        self.email = email
        self.job_id = job_id
        self.sequence = sequence
        self._status = status or JobStatus.UNKNOWN
        self.results = results or {}

    @property
    def done(self) -> bool:
        return self.status.final

    @property
    def status(self) -> JobStatus:
        if not self._status.final:
            from r2dt_client.session import R2dtClient

            self._status = R2dtClient(self.email).status(self.job_id)
        return self._status

    @status.setter
    def status(self, status: JobStatus) -> None:
        if self._status.final:
            raise R2dtError(
                f"Cannot update status for finished job with "
                f"id: {self.job_id}, status: {self.status}"
            )
        self._status = status

    def result(self, format: Format) -> str:
        if not self._status.final:
            raise R2dtError(
                f"Cannot fetch result for unfinished job with id {self.job_id},"
                f" status: {self.status}"
            )

        if format not in self.results:
            from r2dt_client.session import R2dtClient

            self.results[format] = R2dtClient(self.email).result(
                self.job_id, self.sequence, format
            )

        return self.results[format]

    def __str__(self) -> str:
        return f"R2dtJob(job_id={self.job_id}, status={self.status})"

    __repr__ = __str__
