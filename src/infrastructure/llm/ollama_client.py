import ollama
from src.domain.interfaces.i_llm_client import ILLMClient
from src.config.settings import settings


class OllamaClient(ILLMClient):

    def __init__(self):
        self._client = ollama.Client(host=settings.llm_base_url)
        self._model = settings.llm_model

    def generate(self, prompt: str) -> str:
        response = self._client.generate(
            model=self._model,
            prompt=prompt
        )
        return response.response

    def is_available(self) -> bool:
        try:
            self._client.list()
            return True
        except Exception:
            return False

    def is_model_available(self) -> bool:
        try:
            models = self._client.list()
            return any(
                self._model in model.model
                for model in models.models
            )
        except Exception:
            return False