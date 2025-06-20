from dataclasses import dataclass


@dataclass
class Equipment:
    name: str
    description: str
    type: str
    location: str
    criticality: str
    status: str
