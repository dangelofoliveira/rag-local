from abc import ABC
from src.domain.interfaces.i_document_loader import IDocumentLoader
import hashlib


class BaseLoader(IDocumentLoader, ABC):

    def _generate_id(self, source: str, chunk_index: int, content: str) -> str:
        raw = f"{source}_{chunk_index}_{content}"
        return hashlib.md5(raw.encode()).hexdigest()

    def _make_chunks(self, text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - chunk_overlap

        return chunks