import time
from pathlib import Path
from win32com.client import gencache, Dispatch
from typing import cast
from core.interop import AutoCAD2021 as AutoCAD
from pywintypes import com_error

class CadReader:
    """Classe representativa do AUTOCAD"""
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.acad_app: AutoCAD.IAcadApplication = gencache.EnsureDispatch("AutoCAD.Application")
        self.document: AutoCAD.IAcadDocument | None = None

        try:
            self.acad_app.Visible = True
        except Exception as e:
            print(f"[Erro] AutoCAD não pôde ser tornado visível: {e}")

    def exists(self) -> bool:
        """Verifica o caminho do arquivo selecionado pelo usuário"""
        return self.file_path.exists()

    def wait_until_ready(self, timeout: int = 30):
        """Espera até o AutoCAD estar pronto para interações COM"""
        waited = 0

        while not self.acad_app.GetAcadState().IsQuiescent:
            if waited >= timeout:
                raise TimeoutError("AutoCAD não ficou pronto a tempo.")
            print("Aguardando AutoCAD carregar o documento...")
            time.sleep(10)
            waited += 1

    def open_model_space(self) -> AutoCAD.IAcadModelSpace:
        """Recupera o desenho CAD selecionado pelo usuário"""

        # Verifica se o documento já foi aberto anteriormente
        if self.document is not None:
            return cast(AutoCAD.IAcadModelSpace, self.document.ModelSpace)

        # Valida se o arquivo selecionado pelo usuário é válido.
        if not self.exists():
            raise FileNotFoundError(f"Arquivo CAD não encontrado: {self.file_path}")

        try:
            self.document = self.acad_app.Documents.Open(str(self.file_path))
            self.wait_until_ready()  # Aguarda AutoCAD iniciar os processor por completo para atender chamados COM.

            # Aguarda até que ModelSpace esteja acessível
            attempts = 0
            while True:
                try:
                    model_space = self.document.ModelSpace
                    _ = model_space.Count  # força o autocad a responder quantas entidades o desenho possui, caso consiga, o desenho está totalmente carregado.
                    break
                except com_error:
                    if attempts >= 30:
                        raise TimeoutError("ModelSpace não ficou acessível a tempo.")
                    print("Aguardando acesso ao ModelSpace...")
                    time.sleep(1)
                    attempts += 1

        except com_error as e:
            raise RuntimeError(f"Erro ao abrir documento CAD: {e}")

        return cast(AutoCAD.IAcadModelSpace, self.document.ModelSpace)

    def close_model_space(self):
        if self.document:
            try:
                self.document.Close(True)
            except com_error as e:
                print(f"[Aviso] Erro ao fechar o documento: {e}")

    def get_block_entities(self) -> list[AutoCAD.IAcadBlockReference]:
        model_space = self.open_model_space()
        block_entities = []

        try:
            for entity in model_space:
                if entity.EntityName == "AcDbBlockReference":
                     block_ref = cast(AutoCAD.IAcadBlockReference, Dispatch(entity))
                     block_entities.append(block_ref)
        except com_error as e:
            raise RuntimeError(f"Erro ao ler entidades do ModelSpace: {e}")

        return block_entities
