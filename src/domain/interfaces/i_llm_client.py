from abc import ABC, abstractmethod

class ILLMClient(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Envia um prompt ao LLM e retorna a resposta gerada."""
        ...