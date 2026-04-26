from src.config.settings import settings
from src.infrastructure.loaders.loader_factory import LoaderFactory
from src.infrastructure.vector_store.chroma_store import ChromaStore
from src.infrastructure.llm.ollama_client import OllamaClient
from src.application.ingest_service import IngestService
from src.application.query_service import QueryService
from src.presentation.gradio_app import GradioApp


def main():
    # Infrastructure
    loader_factory = LoaderFactory()
    vector_store = ChromaStore()
    llm_client = OllamaClient()

    # Application
    ingest_service = IngestService(
        loader_factory=loader_factory,
        vector_store=vector_store
    )
    query_service = QueryService(
        vector_store=vector_store,
        llm_client=llm_client
    )

    # Presentation
    app = GradioApp(
        ingest_service=ingest_service,
        query_service=query_service,
        llm_client=llm_client
    )

    app.launch()


if __name__ == "__main__":
    main()