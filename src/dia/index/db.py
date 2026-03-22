"""SQLite persistence for indexed UI/UX patterns."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

import aiosqlite

from dia.config import DB_PATH, ensure_index_dir

_CREATE = """
CREATE TABLE IF NOT EXISTS patterns (
    id              TEXT PRIMARY KEY,
    flow_id         TEXT,
    step_number     INTEGER DEFAULT 0,
    url             TEXT NOT NULL,
    category        TEXT,
    app_name        TEXT,
    flow_name       TEXT,
    description     TEXT,
    screenshot_b64  TEXT,
    markdown        TEXT,
    branding        TEXT,
    metadata        TEXT,
    tags            TEXT,
    indexed_at      TEXT
)
"""


async def init() -> None:
    try:
        ensure_index_dir()
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(_CREATE)
            # Check if columns exist (for migration)
            cursor = await db.execute("PRAGMA table_info(patterns)")
            rows = await cursor.fetchall()
            columns = [row[1] for row in rows]
            if "flow_id" not in columns:
                await db.execute("ALTER TABLE patterns ADD COLUMN flow_id TEXT")
            if "step_number" not in columns:
                await db.execute("ALTER TABLE patterns ADD COLUMN step_number INTEGER DEFAULT 0")
            await db.commit()
    except Exception as e:
        # DO NOT CRASH THE SERVER if indexing is unavailable (e.g. read-only FS)
        print(f"ERROR: Could not initialize database at {DB_PATH}: {e}")


async def save_pattern(data: dict[str, Any]) -> str:
    # Unique ID for each entry (URL + Flow + Step)
    pid_base = f"{data.get('url', '')}:{data.get('flow_name', '')}:{data.get('step_number', 0)}"
    pid = hashlib.md5(pid_base.encode()).hexdigest()

    # Flow ID groups steps together (URL + Flow)
    fid_base = f"{data.get('url', '')}:{data.get('flow_name', '')}"
    fid = hashlib.md5(fid_base.encode()).hexdigest()

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """
                INSERT OR REPLACE INTO patterns
                    (id, flow_id, step_number, url, category, app_name, flow_name, description,
                     screenshot_b64, markdown, branding, metadata, tags, indexed_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    pid,
                    data.get("flow_id", fid),
                    data.get("step_number", 0),
                    data.get("url", ""),
                    data.get("category", ""),
                    data.get("app_name", ""),
                    data.get("flow_name", ""),
                    data.get("description", ""),
                    data.get("screenshot_b64", ""),
                    data.get("markdown", ""),
                    json.dumps(data.get("branding", {})),
                    json.dumps(data.get("metadata", {})),
                    json.dumps(data.get("tags", [])),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            await db.commit()
    except Exception as e:
        print(f"ERROR: Could not save pattern to database: {e}")

    return pid


async def search_patterns(
    *,
    query: str = "",
    category: str = "",
    tags: str = "",
    limit: int = 20,
) -> list[dict[str, Any]]:
    conditions: list[str] = []
    params: list[Any] = []
    if query:
        q = f"%{query}%"
        conditions.append(
            "(description LIKE ? OR app_name LIKE ? OR flow_name LIKE ? OR markdown LIKE ?)"
        )
        params.extend([q, q, q, q])
    if category:
        conditions.append("category = ?")
        params.append(category)
    if tags:
        for t in tags.split(","):
            conditions.append("tags LIKE ?")
            params.append(f"%{t.strip()}%")

    where = " AND ".join(conditions) if conditions else "1=1"
    sql = f"SELECT * FROM patterns WHERE {where} ORDER BY indexed_at DESC LIMIT ?"
    params.append(limit)

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(sql, params)
            rows = await cursor.fetchall()
            return [
                {
                    "id": r["id"],
                    "url": r["url"],
                    "app_name": r["app_name"],
                    "flow_name": r["flow_name"],
                    "category": r["category"],
                    "description": r["description"],
                    "tags": json.loads(r["tags"] or "[]"),
                    "indexed_at": r["indexed_at"],
                    "has_screenshot": bool(r["screenshot_b64"]),
                }
                for r in rows
            ]
    except Exception as e:
        print(f"ERROR: Could not search patterns in database: {e}")
        return []
