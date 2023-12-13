import hashlib
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Optional
from typing import cast

import diskcache  # type: ignore

from r2dt_client.session.entities.cache_item import CacheItem
from r2dt_client.session.entities.format import Format


CACHE_DIR = Path("~/.r2dt_cache").absolute()
CACHE_PATH = CACHE_DIR.as_posix()


class JobCacheService:
    def __init__(self, cache_dir: str = CACHE_PATH):
        self.disk_cache = diskcache.Cache(cache_dir)

    def get(self, sequence: str) -> Optional[CacheItem]:
        key = self._create_cache_key(sequence)

        if key in self.disk_cache:
            return cast(CacheItem, self.disk_cache[key])

        return None

    def put(self, sequence: str, job_id: str, results: dict[Format, str]) -> None:
        key = self._create_cache_key(sequence)
        if item := self.disk_cache.get(key):
            item.job_id = job_id
            item.results = item.results | results
            self.disk_cache[key] = item
        else:
            self.disk_cache[key] = CacheItem(
                job_id=job_id,
                sequence=sequence,
                results=results,
                created_at=datetime.now(tz=timezone.utc),
            )

    @staticmethod
    def _create_cache_key(sequence: str) -> str:
        return hashlib.sha256(sequence.encode("utf-8")).hexdigest()

    def close(self) -> None:
        self.disk_cache.close()
