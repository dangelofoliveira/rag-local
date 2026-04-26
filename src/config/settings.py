from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # LLM
    llm_model: str
    llm_base_url: str

    # Embeddings
    embedding_model: str

    # ChromaDB
    chroma_db_path: str
    chroma_collection_name: str

    # Chunking
    chunk_size: int
    chunk_overlap: int

    # Busca
    top_k_results: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()