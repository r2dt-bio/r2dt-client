from dataclasses import dataclass
from datetime import datetime

from r2dt_client.entities.format import Format


@dataclass
class CacheItem:
    job_id: str
    created_at: datetime
    results: dict[Format, str]
    sequence: str
