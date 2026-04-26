from dataclasses import dataclass
from src.domain.entities.document import Document

@dataclass
class QueryResult:
    answer: str
    source_documents: list[Document]
    query: str