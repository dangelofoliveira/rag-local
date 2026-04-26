import os
from src.domain.interfaces.i_document_loader import IDocumentLoader
from src.infrastructure.loaders.txt_loader import TxtLoader
from src.infrastructure.loaders.docx_loader import DocxLoader
from src.infrastructure.loaders.csv_loader import CsvLoader


class LoaderFactory:

    _loaders: dict[str, IDocumentLoader] = {
        ".txt": TxtLoader(),
        ".docx": DocxLoader(),
        ".csv": CsvLoader(),
    }

    @staticmethod
    def get_loader(path: str) -> IDocumentLoader:
        ext = os.path.splitext(path)[1].lower()
        loader = LoaderFactory._loaders.get(ext)

        if loader is None:
            raise ValueError(f"Formato não suportado: '{ext}'. Formatos aceitos: {list(LoaderFactory._loaders.keys())}")

        return loader