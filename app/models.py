from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class ResultStatus(str, Enum):
    PASS = "PASS"
    WEAK = "WEAK"
    MISSING = "MISSING"
    OBSERVED = "OBSERVED"
    NOT_TESTED = "NOT_TESTED"


@dataclass
class OwaspMapping:
    category: str               # e.g., "A02:2025"
    title: str                  # e.g., "Security Misconfiguration"
    rationale: str              # short reason sentence


@dataclass
class CheckResult:
    check_id: str               # e.g., "HDR-01"
    check_name: str             # short display name
    status: ResultStatus        # PASS / WEAK / MISSING / OBSERVED / NOT_TESTED
    owasp: List[OwaspMapping] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    note: Optional[str] = None  # short explanation for humans

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d