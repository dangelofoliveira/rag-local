import gradio as gr
from src.application.ingest_service import IngestService
from src.application.query_service import QueryService
from src.infrastructure.llm.ollama_client import OllamaClient


class GradioApp:

    def __init__(self, ingest_service: IngestService, query_service: QueryService, llm_client: OllamaClient):
        self._ingest_service = ingest_service
        self._query_service = query_service
        self._llm_client = llm_client
        self._app = self._build()

    def _build(self) -> gr.Blocks:
        with gr.Blocks(title="RAG Local", theme=gr.themes.Soft()) as app:

            gr.Markdown("# 📚 RAG Local")
            gr.Markdown("Carregue seus documentos e faça perguntas em linguagem natural.")

            with gr.Tab("📂 Carregar Documentos"):
                self._build_ingest_tab()

            with gr.Tab("💬 Perguntar"):
                self._build_query_tab()

        return app

    def _build_ingest_tab(self) -> None:
        gr.Markdown("### Envie seus arquivos (TXT, DOCX, CSV)")

        file_input = gr.File(
            label="Selecione os arquivos",
            file_count="multiple",
            file_types=[".txt", ".docx", ".csv"]
        )

        ingest_button = gr.Button("📥 Indexar Documentos", variant="primary")
        ingest_output = gr.Textbox(label="Resultado", lines=10, interactive=False)

        ingest_button.click(
            fn=self._handle_ingest,
            inputs=[file_input],
            outputs=[ingest_output]
        )

    def _build_query_tab(self) -> None:
        gr.Markdown("### Faça uma pergunta sobre seus documentos")

        status = self._get_ollama_status()
        gr.Markdown(status)

        question_input = gr.Textbox(
            label="Sua pergunta",
            placeholder="Ex: Quais são as regras de combate?",
            lines=2
        )

        query_button = gr.Button("🔍 Perguntar", variant="primary")

        answer_output = gr.Textbox(label="Resposta", lines=10, interactive=False)
        sources_output = gr.Textbox(label="Fontes utilizadas", lines=5, interactive=False)

        query_button.click(
            fn=self._handle_query,
            inputs=[question_input],
            outputs=[answer_output, sources_output]
        )

    def _handle_ingest(self, files: list) -> str:
        if not files:
            return "⚠️ Nenhum arquivo selecionado."

        lines = []
        for file in files:
            try:
                count = self._ingest_service.ingest(file.name)
                lines.append(f"✅ {file.name} — {count} chunks indexados")
            except ValueError as e:
                lines.append(f"❌ {file.name} — {str(e)}")
            except Exception as e:
                lines.append(f"❌ {file.name} — Erro inesperado: {str(e)}")

        return "\n".join(lines)

    def _handle_query(self, question: str) -> tuple[str, str]:
        if not question.strip():
            return "⚠️ Digite uma pergunta.", ""

        if not self._llm_client.is_available():
            return "❌ Ollama não está rodando. Inicie o Ollama e tente novamente.", ""

        if not self._llm_client.is_model_available():
            return f"❌ Modelo não encontrado. Rode: ollama pull {self._llm_client._model}", ""

        try:
            result = self._query_service.query(question)

            sources = "\n\n".join([
                f"📄 {doc.source} — chunk {doc.chunk_index}"
                for doc in result.source_documents
            ])

            return result.answer, sources

        except ValueError as e:
            return f"⚠️ {str(e)}", ""
        except Exception as e:
            return f"❌ Erro inesperado: {str(e)}", ""

    def _get_ollama_status(self) -> str:
        if not self._llm_client.is_available():
            return "⚠️ **Ollama offline.** Inicie o Ollama para usar o chat."
        if not self._llm_client.is_model_available():
            return f"⚠️ **Modelo não encontrado.** Rode: `ollama pull {self._llm_client._model}`"
        return f"✅ **Ollama online** — modelo `{self._llm_client._model}` pronto."

    def launch(self) -> None:
        self._app.launch()