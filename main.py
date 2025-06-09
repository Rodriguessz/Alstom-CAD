import tkinter as tk
from pathlib import Path
from services.cad_service import CadService
from ui.file_cad_selector import FileCadSelector
from ui.file_excel_selector import FileExcelSelector

def main():
    try:        
        # Inicializa a janela de UI da aplicação.
        root = tk.Tk()

        #Inicializa o modulo responsável pela seleção do arquivo DWG.
        file_cad_selector = FileCadSelector(root);
        cad_draw = Path(file_cad_selector.get_selected_file());

        #Inicializa o módulo responsável pela selção do arquivo XLSX.
        file_excel_selector = FileExcelSelector(root)
        excel_sheet = Path(file_excel_selector.get_selected_file());
        
        
        #Inicializa o serviço de Automação do CAD.
        service = CadService(cad_draw);
        service.process();

    except Exception as e:
         print(f"Erro durante o processamento: {e}")

if __name__ == "__main__":
    main()
