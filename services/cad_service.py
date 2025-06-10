from core.cad_reader import CadReader;
from core.excel_reader import ExcelReader;

from pathlib import Path;
from models.relay import Relay;
from core.relay_extractor import RelayExtractor;
import time;

class CadService:
    """Módulo que representa a lógica para automação do desenho no CAD"""
    
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
            self.excel_reader.open_excel_sheet("MAPA_RELES");

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

                    for mod in modifications:
                        self.excel_reader.update_cell_by_value(mod["r"]["previous_state"], mod["r"]["new_state"]);
                        
                    
                    self.excel_reader.save_changes();

                    self.cad_reader.close_model_space()
                    return None;
                else:
                    print("Nenhuma modificação detectada no documento")
 
        except Exception as e:
            print(f"Erro ao processar serviço: {e}")
    
        
     