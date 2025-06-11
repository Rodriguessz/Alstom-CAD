from core.cad_reader import CadReader;
from core.excel_reader import ExcelReader;

from pathlib import Path;
from models.relay import Relay;
from core.relay_extractor import RelayExtractor;
import time;

class CadService:
    """A classe CadService é responsável por integrar a leitura de desenhos do AutoCAD
    e a atualização de dados em planilhas do Excel, facilitando a automação no
    gerenciamento de reles em projetos de CAD. Através da interação com os módulos
    CadReader e ExcelReader, esta classe permite monitorar alterações em documentos
    do AutoCAD e aplicar as modificações relevantes em uma planilha especificada.

    Responsabilidades Principais:
    - Abertura de Documentos: Abre desenhos do AutoCAD e planilhas do Excel conforme
      o caminho de arquivo fornecido.
    - Verificação de Modificações: Monitora constantemente as modificações no
      desenho CAD, comparando o estado atual dos reles com um estado anterior.
    - Extração de Dados: Utiliza a classe RelayExtractor para identificar e extrair
      informações sobre reles a partir do desenho CAD.
    - Aplicação de Alterações: Atualiza a planilha do Excel com as modificações
      detectadas, garantindo que as informações permaneçam sincronizadas entre os
      documentos CAD e Excel.
    - Tratamento de Erros: Captura e trata exceções durante todo o processo de leitura
      e atualização, garantindo a robustez do serviço.

    Exemplo de Uso:
        cad_service = CadService(Path('caminho/para/desenho.dwg'), Path('caminho/para/planilha.xlsx'))
        cad_service.process()

    Essa classe combina funcionalidades de leitura de CAD e Excel para permitir automações
    eficientes em ambientes que exigem atualizações regulares e monitoramento de
    configurações de reles em projetos de engenharia elétrica ou similares.
    """
    
    def __init__(self, cad_file_path: Path, excel_file_path : Path):
        print(cad_file_path)
        self.cad_reader = CadReader(cad_file_path);
        self.excel_reader = ExcelReader(excel_file_path);
        self.sheet_reader = None;
        self.relayExtractor = RelayExtractor();

    def process(self):
        try:
            #Abre o desenho selecionado pelo usuário
            self.cad_reader.open_model_space();

            #Carrega a planilha do excel selecionada pelo usuário;
            self.excel_reader.open_excel_sheet("MAPEAMENTO RELÉS");

            #Recupera a data de última modificação do documento.
            last_modification_date = self.cad_reader.get_last_modification();

            #Recupera o estado atual dos reles no desenho.
            relays_state = self.cad_reader.map_rele_entities(self.relayExtractor);

            while True:
                # Aguarda X tempo para verificar novamente se houve alteração no documento.
                time.sleep(10)
                    
                new_modification_date = self.cad_reader.get_last_modification();

                if last_modification_date != new_modification_date:

                    # Mapeia o documento em busca do novo estado dos reles;
                    new_relays_state = self.cad_reader.map_rele_entities(self.relayExtractor);

                    # Retorna todas as modificações 
                    modifications = self.relayExtractor.compare_relays_state(relays_state, new_relays_state);
                    print(modifications)

                    #Aplica as modificações na planilha do excel.
                    if modifications:
                        self.excel_reader.aplly_relays_modifications(modifications)
                            
                    self.excel_reader.save_changes();
                    print("Planilha atualizada com sucesso!")

                    self.cad_reader.close_model_space()
                    return None;
                else:
                    print("Nenhuma modificação detectada no documento")
 
        except Exception as e:
            print(f"Erro ao processar serviço: {e}")
            self.cad_reader.close_model_space();
    
        
     