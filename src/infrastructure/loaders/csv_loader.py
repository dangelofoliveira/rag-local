import pandas as pd
from src.infrastructure.loaders.base_loader import BaseLoader
from src.domain.entities.document import Document
from src.config.settings import settings


class CsvLoader(BaseLoader):

    def load(self, path: str) -> list[Document]:
        df = pd.read_csv(path)
        documents = []

        for row_index, row in df.iterrows():
            content = " | ".join([f"{col}: {val}" for col, val in row.items()])
            chunks = self._make_chunks(content, settings.chunk_size, settings.chunk_overlap)

            for chunk_index, chunk in enumerate(chunks):
                documents.append(Document(
                    id=self._generate_id(path, row_index * 1000 + chunk_index, chunk),
                    content=chunk,
                    source=path,
                    chunk_index=row_index,
                    metadata={"type": "csv", "row": row_index}
                ))

        return documents