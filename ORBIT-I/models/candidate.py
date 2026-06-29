from dataclasses import dataclass


@dataclass
class Candidate:
    name: str = ""
    email: str = ""
    skills: list[str] | None = None
    experience_years: int = 0
