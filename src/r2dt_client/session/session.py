import aiohttp
from yarl import URL

from r2dt_client.session.entities.exceptions import R2dtError
from r2dt_client.session.entities.format import Format
from r2dt_client.session.entities.job import R2dtJob
from r2dt_client.session.entities.job_status import JobStatus
from r2dt_client.session.services.cache import JobCacheService


BASE_URL = URL("https://www.ebi.ac.uk/Tools/services/rest/r2dt")


class R2dtClient:
    def __init__(self, email: str):
        self.session = None
        self.email = email
        self.cache = JobCacheService()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
        self.cache.close()

    async def run(self, sequence: str) -> R2dtJob:
        cached_result = self.cache.get(sequence)
        if cached_result:
            return R2dtJob(
                self, cached_result.job_id, JobStatus.FINISHED, cached_result.results
            )

        url = BASE_URL / "run"
        data = {"email": self.email, "sequence": sequence}
        async with self.session.post(url, data=data) as response:
            if response.status == 200:
                job_id = await response.text()
                return R2dtJob(self, job_id)
            else:
                raise Exception(f"Error submitting job: {response.status}")

    async def status(self, job_id: str) -> JobStatus:
        url = BASE_URL / "status" / job_id
        async with self.session.get(url) as response:
            if not response.ok:
                raise R2dtError(
                    f"Error fetching status: {response.status}, {await response.text()}"
                )

            status = JobStatus(await response.text())
            if status == JobStatus.FINISHED:
                self.cache.put(job_id, await self.result(job_id, Format.svg))
            return status

    async def result(self, job_id: str, sequence: str, format: Format) -> str:
        url = BASE_URL / "result" / job_id / format.value
        cached_data = self.cache.get(sequence)
        if cached_data and format.value in cached_data.results:
            return cached_data.results[format.value]

        async with self.session.get(url) as response:
            response_text = await response.text()
            if not response.ok:
                raise R2dtError(
                    f"Error fetching result ({format}): "
                    f"{response.status}, {response_text}"
                )
            self.cache.put(sequence, job_id, {format.value: response_text})
            return response_text
