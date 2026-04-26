import chromadb
from chromadb.utils import embedding_functions
from src.domain.interfaces.i_vector_store import IVectorStore
from src.domain.entities.document import Document
from src.config.settings import settings


class ChromaStore(IVectorStore):

    def __init__(self):
        self._client = chromadb.PersistentClient(path=settings.chroma_db_path)

        self._embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )

        self._collection = self._client.get_or_create_collection(
            name=settings.chroma_collection_name,
            embedding_function=self._embedding_fn
        )

    def add_documents(self, documents: list[Document]) -> None:
        ids = [doc.id for doc in documents]
        contents = [doc.content for doc in documents]
        metadatas = [
            {**doc.metadata, "source": doc.source, "chunk_index": doc.chunk_index}
            for doc in documents
        ]

        self._collection.upsert(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )

    def search(self, query: str, top_k: int = 5) -> list[Document]:
        results = self._collection.query(
            query_texts=[query],
            n_results=top_k
        )

        documents = []
        for i in range(len(results["ids"][0])):
            metadata = results["metadatas"][0][i]
            documents.append(Document(
                id=results["ids"][0][i],
                content=results["documents"][0][i],
                source=metadata.pop("source"),
                chunk_index=metadata.pop("chunk_index"),
                metadata=metadata
            ))

        return documents

    def collection_exists(self) -> bool:
        return self._collection.count() > 0