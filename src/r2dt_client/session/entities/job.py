from typing import TYPE_CHECKING
from typing import Optional

from r2dt_client.session.entities.exceptions import R2dtError
from r2dt_client.session.entities.format import Format
from r2dt_client.session.entities.job_status import JobStatus


if TYPE_CHECKING:
    from r2dt_client.session import R2dtClient  # This import is only for type checking


class R2dtJob:
    job_id: str
    _status: JobStatus
    r2dt_client: "R2dtClient"
    sequence: str
    results: dict[Format, str]

    def __init__(
        self,
        client: "R2dtClient",
        job_id: str,
        sequence: str,
        status: JobStatus = JobStatus.UNKNOWN,
        results: Optional[dict[Format, str]] = None,
    ):
        self.r2dt_client = client
        self.job_id = job_id
        self.sequence = sequence
        self._status = status or JobStatus.UNKNOWN
        self.results = results or {}

    @property
    async def done(self) -> bool:
        return (await self.status).final

    @property
    async def status(self) -> JobStatus:
        if not self._status.final:
            self._status = await self.r2dt_client.status(self.job_id)
        return self._status

    @status.setter
    def status(self, status: JobStatus) -> None:
        if self._status.final:
            raise R2dtError(
                f"Cannot update status for finished job with "
                f"id: {self.job_id}, status: {self.status}"
            )
        self._status = status

    async def result(self, format: Format) -> str:
        if not self._status.final:
            raise R2dtError(
                f"Cannot fetch result for unfinished job with id {self.job_id},"
                f" status: {self.status}"
            )

        if format not in self.results:
            self.results[format] = await self.r2dt_client.result(
                self.job_id, self.sequence, format
            )

        return self.results[format]

    def __str__(self) -> str:
        return f"R2dtJob(job_id={self.job_id}, status={self.status})"
