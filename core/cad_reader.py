import time
import os
from pathlib import Path
from win32com.client import gencache, Dispatch
from typing import cast
from core.interop import AutoCAD2021 as AutoCAD
from pywintypes import com_error

class CadReader:
    """A classe CadReader atua como uma interface para interagir com desenhos do AutoCAD,
    aproveitando a automação COM (Component Object Model) para ler e manipular informações
    contidas em arquivos de desenho CAD. Sua implementação permite abrir, fechar, e acessar
    o espaço do modelo de documentos CAD, além de extrair entidades específicas e fornecer
    informações sobre a última modificação do arquivo.

    Responsabilidades Principais:
    - Gerenciamento do AutoCAD: Controla a instância do AutoCAD, garantindo visibilidade e
      disponibilidade para interações.
    - Verificação e Acesso a Arquivos: Valida a existência de arquivos CAD e permite a
      abertura segura de documentos.
    - Carregamento do Modelo: Aguarda até que o AutoCAD e o espaço do modelo estejam prontos
      para interação.
    - Extração de Entidades de Bloco: Coleta entidades de bloco, facilitando a identificação
      de objetos específicos, como reles.
    - Informações sobre Modificações: Capta informações sobre a última data de modificação
      do arquivo CAD.

    A classe utiliza a biblioteca pywin32 para se comunicar com a API do AutoCAD, proporcionando
    um controle direto sobre a aplicação a partir do Python. O tratamento de exceções é robusto
    para garantir a estabilidade nas interações com a aplicação.
    """
    def __init__(self, file_path: Path):
        self.file_path = file_path;
        self.acad_app: AutoCAD.IAcadApplication = gencache.EnsureDispatch("AutoCAD.Application");
        self.document: AutoCAD.IAcadDocument | None = None;
        self.model_space: AutoCAD.IAcadModelSpace | None = None;

        try:
            self.acad_app.Visible = True
        except Exception as e:
            print(f"[Erro] AutoCAD não pôde ser tornado visível: {e}")

    def exists(self) -> bool:
        """Verifica se  o caminho do arquivo selecionado pelo usuário realmente existe"""
        return self.file_path.exists()

    def open_model_space(self) -> AutoCAD.IAcadModelSpace:
        """Recupera o desenho CAD selecionado pelo usuário"""
        try:
            # Verifica se o documento já foi aberto anteriormente
            if self.document is not None:
                return cast(AutoCAD.IAcadModelSpace, self.document.ModelSpace)

            # Valida se o arquivo selecionado pelo usuário é válido.
            if not self.exists():
                raise FileNotFoundError(f"Arquivo CAD não encontrado: {self.file_path}")
            
            # Carrega o documento selecionado
            self.document = self.acad_app.Documents.Open(str(self.file_path))

            # Espera o autoCAD carregar por completo para atender chamados COM
            self.wait_until_ready() 

            # Espera o ducmento ser completamente carregado.
            self.wait_model_space_load(self.document.ModelSpace) 

            #Retorna o documento completamente carregado.
            self.model_space = cast(AutoCAD.IAcadModelSpace, self.document.ModelSpace)
            return self.model_space;
        
        except Exception as e:
            raise RuntimeError(f"[Aviso] Erro ao abrir documento CAD: {e}")
        
    def close_model_space(self) -> bool:
        """Fecha o desenho ativo no AutoCAD"""
        if self.document:
            try:
                self.document.Close(True)
                return True
            except com_error as e:
                print(f"[Aviso] Erro ao fechar o documento: {e}")
          
    def wait_until_ready(self, timeout: int = 30):
        """Espera até o AutoCAD estar pronto para interações COM"""
        waited = 0
        
        while not self.acad_app.GetAcadState().IsQuiescent:
            if waited >= timeout:
                raise TimeoutError("AutoCAD não ficou pronto a tempo.")
            print("Aguardando AutoCAD carregar o documento...")
            time.sleep(10)
            waited += 1

    def wait_model_space_load(self, model_space):
        """Aguarda até que todos os objetos do desenho sejam completamente carregados."""
        # Aguarda até que ModelSpace esteja acessível
        attempts = 0
        while True:
            try:
                _ = model_space.Count  # força o autocad a responder quantas entidades o desenho possui, caso consiga, o desenho está totalmente carregado.
                break
            except com_error:
                if attempts >= 30:
                    raise TimeoutError("ModelSpace não ficou acessível a tempo.")
                print("Aguardando acesso ao ModelSpace...")
                time.sleep(1)
                attempts += 1

    def get_last_modification(self) -> str:
        """Recupera a data da última modificação do arquivo"""
        
        #Recupera a data de modificação.
        modification_time  = os.path.getmtime(self.file_path);
    
        # Transforma o valor retornado pelo getmtime em um valor legível usando ctime();
        modification_time = time.ctime(modification_time);
    
        return modification_time;

    def get_block_entities(self) -> list[AutoCAD.IAcadBlockReference]:
        """Retorna todas as entidades de bloco existentes no desenho atual"""
        block_entities = []
        try:
            if self.model_space is not None:
                for entity in self.model_space:
                    if entity.EntityName == "AcDbBlockReference":
                        block_ref = cast(AutoCAD.IAcadBlockReference, Dispatch(entity))
                        block_entities.append(block_ref)
            else:
                raise Exception("Model space não carregada!")
        except com_error as e:
            raise RuntimeError(f"Erro ao ler entidades do ModelSpace: {e}")

        return block_entities

    def map_rele_entities(self, relayExtractorUtil) -> list:
        """Mapeia o documento e extrai o estado atual das instâncias da classe Relay.
        
        Esta função retorna uma lista de objetos Relay, cada um representando o estado
        atual dos reles no documento. É útil para comparar o estado dos reles em um 
        determinado momento com outro, permitindo identificar mudanças e modificações.
        """

        # Recupera as entidades de bloco do desenho;
        blocks = self.get_block_entities();
        
        #Verifica se existe algum objeto de bloco no desenho;
        if not blocks:
            raise Exception("Nenhum objeto de bloco encontrado no desenho selecionado!")

        # Extrai todos os reles do documento atual;
        relays = relayExtractorUtil.get_relays(blocks);

        return relays;