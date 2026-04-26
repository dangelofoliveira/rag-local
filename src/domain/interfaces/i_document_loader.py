from abc import ABC, abstractmethod
from src.domain.entities.document import Document

class IDocumentLoader(ABC):

    @abstractmethod
    def load(self, path: str) -> list[Document]:
        """Lê um arquivo e retorna uma lista de Documents (chunks)."""
        ...