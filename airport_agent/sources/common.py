"""Shared download helper: retries, a timeout, and a temporary file that is swapped in only after it passes its check."""
import os
import time
import zipfile
from pathlib import Path

import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"


def is_zip(path: Path) -> bool:
    return zipfile.is_zipfile(path)


def save_checked(dest: Path, get_bytes, check=None, attempts: int = 3) -> Path:
    """Call get_bytes() (with retries), write to dest.tmp, run check(tmp_path), then swap into place.

    A failed download or a failed check leaves any existing file at `dest` untouched.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    last = None
    for attempt in range(1, attempts + 1):
        try:
            tmp.write_bytes(get_bytes())
            if check is not None and not check(tmp):
                raise ValueError(f"downloaded file for {dest.name} failed its format check")
            os.replace(tmp, dest)
            return dest
        except Exception as err:  # network errors, bad payloads - retry, then give up and keep the old file
            last = err
            if tmp.exists():
                tmp.unlink()
            if attempt < attempts:
                time.sleep(3 * attempt)
    raise RuntimeError(f"could not fetch {dest.name} after {attempts} attempts: {last}")


def get(url: str, timeout: int = 300, **kwargs) -> bytes:
    r = requests.get(url, timeout=timeout, headers={"User-Agent": UA}, **kwargs)
    r.raise_for_status()
    return r.content
