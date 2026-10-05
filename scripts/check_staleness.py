"""Exit 1 if the catalogue or regulatory notes were last reviewed more than MAX_DAYS ago (default 180)."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bridge.catalogue import DATA_LAST_REVIEWED, MODELS  # noqa: E402
from bridge.regions import LAST_REVIEWED as REGIONS_REVIEWED  # noqa: E402


def stale_items(today: date, max_days: int) -> list[str]:
    items = [("catalogue", DATA_LAST_REVIEWED), ("regional notes", REGIONS_REVIEWED)]
    items += [(f"model {m['key']}", m["review"]["last_reviewed"]) for m in MODELS]
    return [f"{name}: reviewed {d} ({(today - date.fromisoformat(d)).days} days ago)"
            for name, d in items if (today - date.fromisoformat(d)).days > max_days]


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 180
    old = stale_items(date.today(), limit)
    print("\n".join(old) if old else f"All reviews are within {limit} days.")
    sys.exit(1 if old else 0)
