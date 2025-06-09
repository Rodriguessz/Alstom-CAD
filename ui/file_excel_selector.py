import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from config.settings import EXCEL_SHEETS_PATH
from pathlib import Path


class FileExcelSelector:
    """Módulo responsável pela manipulação/seleção de arquivos"""
    def __init__(self, masterTk):
        self.master = masterTk
        self.selected_file = None;
        self.sheets_path = EXCEL_SHEETS_PATH;
    
        # Criando componentes da UI
        self.label = tk.Label(self.master, text="Selecione um arquivo (.xlsx):")
        self.label.pack()

        self.select_button = tk.Button(self.master, text="Selecionar Arquivo", command=self.get_selected_file)
        self.select_button.pack()


    def get_selected_file(self) -> str:
        """Abre o modal para seleção de arquivos XLSX e retona o nome do arquivo selecionado"""

        if not Path(self.sheets_path).exists():
            try:
                print(f"O caminho {self.sheets_path} não existe!")
                print("Criando diretório...")
                print("Diretório criado com sucesso!")

                Path.mkdir(self.sheets_path)
            except FileExistsError as e:
                print(f"Erro ao tentar criar diretório cadDraws {e}")
            
        self.selected_file = filedialog.askopenfilename(title="Selecione um arquivo CAD",
                                                        initialdir=str(self.sheets_path),
                                                         filetypes=(("Arquivos XLSX", "*.xlsx"), ("Todos os arquivos", "*.*")))

        return self.selected_file;
        
