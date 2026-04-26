from dataclasses import dataclass, field

@dataclass
class Document:
    id: str
    content: str
    source: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)