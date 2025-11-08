"""Simple conversation graph recorder.

Records exchanges between agents and can save a JSON file suitable for
visualisation (nodes/edges or flat exchanges list).
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import List, Dict, Any, Optional


class ConversationGraph:
    def __init__(self) -> None:
        # store a list of exchanges; each exchange is a dict
        self.exchanges: List[Dict[str, Any]] = []

    def add_exchange(
        self,
        from_agent: str,
        to_agent: Optional[str],
        message: str,
        response: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Add an exchange and return its index as id."""
        idx = len(self.exchanges)
        entry = {
            "id": idx,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "response": response,
            "meta": meta or {},
        }
        self.exchanges.append(entry)
        return idx

    def as_dict(self) -> Dict[str, Any]:
        return {"exchanges": self.exchanges}

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.as_dict(), f, indent=2, ensure_ascii=False)
