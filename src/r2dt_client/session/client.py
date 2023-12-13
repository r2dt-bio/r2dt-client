import httpx
from yarl import URL

from r2dt_client.session.entities.exceptions import R2dtError
from r2dt_client.session.entities.format import Format
from r2dt_client.session.entities.job import R2dtJob
from r2dt_client.session.entities.job_status import JobStatus
from r2dt_client.session.services.cache import JobCacheService


BASE_URL = URL("https://www.ebi.ac.uk/Tools/services/rest/r2dt")


class R2dtClient:
    def __init__(self, email: str):
        self.email = email
        self.cache = JobCacheService()

    def run(self, sequence: str) -> R2dtJob:
        cached_result = self.cache.get(sequence)
        if cached_result:
            return R2dtJob(
                self.email,
                cached_result.job_id,
                sequence,
                JobStatus.FINISHED,
                cached_result.results,
            )

        url = BASE_URL / "run"
        data = {"email": self.email, "sequence": sequence}
        response = httpx.post(str(url), data=data)
        if response.is_success:
            job_id = response.text
            return R2dtJob(self.email, job_id, sequence)
        else:
            raise Exception(
                f"Error submitting job: {response.status_code}\n{response.text}"
            )

    def status(self, job_id: str) -> JobStatus:
        url = BASE_URL / "status" / job_id
        response = httpx.get(str(url))
        if response.is_success:
            return JobStatus(response.text)
        else:
            raise R2dtError(
                f"Error fetching status: {response.status_code}, {response.text}"
            )

    def result(self, job_id: str, sequence: str, format: Format) -> str:
        url = BASE_URL / "result" / job_id / format.value
        cached_data = self.cache.get(sequence)
        if cached_data and format in cached_data.results:
            return cached_data.results[format]

        response = httpx.get(str(url))
        response_text = response.text
        if not response.is_success:
            raise R2dtError(
                f"Error fetching result ({format}): "
                f"{response.status_code}, {response_text}"
            )
        self.cache.put(sequence, job_id, {format: response_text})
        return response_text
