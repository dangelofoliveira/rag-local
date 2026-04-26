from src.infrastructure.loaders.base_loader import BaseLoader
from src.domain.entities.document import Document
from src.config.settings import settings


class TxtLoader(BaseLoader):

    def load(self, path: str) -> list[Document]:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = self._make_chunks(text, settings.chunk_size, settings.chunk_overlap)

        return [
            Document(
                id=self._generate_id(path, i, chunk),
                content=chunk,
                source=path,
                chunk_index=i,
                metadata={"type": "txt"}
            )
            for i, chunk in enumerate(chunks)
        ]