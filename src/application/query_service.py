from src.domain.interfaces.i_vector_store import IVectorStore
from src.domain.interfaces.i_llm_client import ILLMClient
from src.domain.entities.query_result import QueryResult


class QueryService:

    _PROMPT_TEMPLATE = """Você é um assistente especializado em responder perguntas com base em documentos fornecidos.
Use apenas as informações dos trechos abaixo para responder. 
Se a resposta não estiver nos trechos, diga que não encontrou a informação nos documentos.

Trechos relevantes:
{context}

Pergunta: {question}

Resposta:"""

    def __init__(self, vector_store: IVectorStore, llm_client: ILLMClient):
        self._vector_store = vector_store
        self._llm_client = llm_client

    def query(self, question: str) -> QueryResult:
        if not question.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        if not self._vector_store.collection_exists():
            raise ValueError("Nenhum documento indexado. Carregue arquivos antes de fazer perguntas.")

        source_documents = self._vector_store.search(question)

        context = "\n\n---\n\n".join([
            f"[Fonte: {doc.source} | Chunk {doc.chunk_index}]\n{doc.content}"
            for doc in source_documents
        ])

        prompt = self._PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )

        answer = self._llm_client.generate(prompt)

        return QueryResult(
            answer=answer,
            source_documents=source_documents,
            query=question
        )