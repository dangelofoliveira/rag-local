from abc import ABC, abstractmethod
from src.domain.entities.document import Document

class IVectorStore(ABC):

    @abstractmethod
    def add_documents(self, documents: list[Document]) -> None:
        """Indexa uma lista de Documents no banco vetorial."""
        ...

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> list[Document]:
        """Busca os Documents mais similares à query."""
        ...

    @abstractmethod
    def collection_exists(self) -> bool:
        """Verifica se já existe algum documento indexado."""
        ...