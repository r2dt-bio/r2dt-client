from typing import Optional

import httpx
from yarl import URL

from r2dt_client.cache.cache import JobCache
from r2dt_client.entities.exceptions import R2dtError
from r2dt_client.entities.format import Format
from r2dt_client.entities.job import R2dtJob
from r2dt_client.entities.job_status import JobStatus


BASE_URL = URL("https://www.ebi.ac.uk/Tools/services/rest/r2dt")

_email: Optional[str] = None
_cache = JobCache()


def setup(email: str) -> None:
    global _email
    _email = email


def clear_job_cache() -> None:
    _cache.clear()


def submit(
    sequence: str, email: Optional[str] = None, skip_cache: bool = False
) -> R2dtJob:
    if not skip_cache:
        cached_result = _cache.get(sequence)
        if cached_result:
            return R2dtJob(
                cached_result.job_id,
                sequence,
                JobStatus.FINISHED,
                cached_result.results,
            )

    email = email or _email
    if not email:
        raise R2dtError(
            "Email is not set. Please run r2dt_client.configure('YOUR_EMAIL') "
            "before submitting jobs"
        )

    url = BASE_URL / "run"
    data = {"email": _email, "sequence": sequence}
    response = httpx.post(str(url), data=data)
    if response.is_success:
        job_id = response.text
        return R2dtJob(job_id, sequence, JobStatus.QUEUED)
    else:
        raise Exception(
            f"Error submitting job: {response.status_code}\n{response.text}"
        )


def update_status_for(job: R2dtJob) -> None:
    url = BASE_URL / "status" / job.job_id
    response = httpx.get(str(url))
    if response.is_success:
        status = JobStatus(response.text)
        job.status = status
    else:
        raise R2dtError(
            f"Error fetching status: {response.status_code}, {response.text}"
        )


def _fetch_result(job: R2dtJob, fmt: Format) -> str:
    cached_data = _cache.get(job.sequence)
    if cached_data and fmt in cached_data.results:
        return cached_data.results[fmt]

    url = BASE_URL / "result" / job.job_id / fmt.value
    response = httpx.get(str(url))
    response_text = response.text
    if not response.is_success:
        raise R2dtError(
            f"Error fetching {fmt} result : " f"{response.status_code}, {response_text}"
        )
    return response_text


def fetch_results_for(job: R2dtJob, cache: bool = True) -> None:
    if not job.done:
        raise R2dtError(
            f"Cannot fetch results for unfinished job with id {job.job_id},"
            f" status: {job.status}"
        )

    for fmt in Format:
        if fmt not in job.results:
            job.results[fmt] = _fetch_result(job, fmt)

    if cache:
        _cache.put(job.sequence, job.job_id, job.results)
