import os
from src.domain.interfaces.i_vector_store import IVectorStore
from src.infrastructure.loaders.loader_factory import LoaderFactory


class IngestService:

    def __init__(self, loader_factory: LoaderFactory, vector_store: IVectorStore):
        self._loader_factory = loader_factory
        self._vector_store = vector_store

    def ingest(self, path: str) -> int:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo não encontrado: '{path}'")

        loader = self._loader_factory.get_loader(path)
        documents = loader.load(path)
        self._vector_store.add_documents(documents)

        return len(documents)

    def ingest_directory(self, directory: str) -> dict[str, int]:
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"Diretório não encontrado: '{directory}'")

        results = {}
        supported = {".txt", ".docx", ".csv"}

        for filename in os.listdir(directory):
            ext = os.path.splitext(filename)[1].lower()
            if ext not in supported:
                continue

            path = os.path.join(directory, filename)
            try:
                count = self.ingest(path)
                results[filename] = count
            except Exception as e:
                results[filename] = f"Erro: {str(e)}"

        return results