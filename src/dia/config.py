import os
from pathlib import Path

# NOTE: For remote servers, environment variables should be set by the platform
# (e.g. Docker, Heroku, Vercel, etc.). The local .env file should only be
# used for local development and should NOT be parsed in production code.

TINYFISH_API_KEY: str = os.environ.get("TINYFISH_API_KEY", "")
FIRECRAWL_API_KEY: str = os.environ.get("FIRECRAWL_API_KEY", "")

# Server-side stored credentials to run automated logins
MOBBIN_EMAIL: str = os.environ.get("MOBBIN_EMAIL", "")
MOBBIN_PASSWORD: str = os.environ.get("MOBBIN_PASSWORD", "")

# Allow overriding the index directory via environment variable.
# For remote servers with ephemeral filesystems, this should point to a
# mounted persistent volume (e.g. /mnt/data/uxindex).
INDEX_DIR: Path = Path(os.environ.get("UX_INSPO_INDEX_DIR", "./uxindex")).resolve()


def ensure_index_dir():
    """Lazily create the index directory if it doesn't exist."""
    if not INDEX_DIR.exists():
        try:
            INDEX_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            # On some remote servers, the filesystem might be read-only
            # outside of specific allowed paths.
            print(f"CRITICAL: Could not create index directory at {INDEX_DIR}: {e}")


DB_PATH: Path = INDEX_DIR / "ux_inspo.db"
