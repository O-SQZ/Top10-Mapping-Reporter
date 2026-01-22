from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    timeout_sec: int = 10
    user_agent: str = "Top10-Mapping-Reporter/0.1"
    verify_tls: bool = True