import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from config.settings import CAD_DRAWS_PATH
from pathlib import Path


class FileCadSelector:
    """Módulo responsável pela manipulação/seleção de arquivos"""
    def __init__(self, masterTk):
        self.master = masterTk
        self.selected_file = None;
        self.draws_path = CAD_DRAWS_PATH;
    
        # Criando componentes da UI
        self.label = tk.Label(self.master, text="Selecione um arquivo CAD:")
        self.label.pack()

        self.select_button = tk.Button(self.master, text="Selecionar Arquivo", command=self.get_selected_file)
        self.select_button.pack()


    def get_selected_file(self) -> str:
        """Abre o modal para seleção de arquivos CAD e retona o nome do arquivo selecionado"""

        if not Path(self.draws_path).exists():
            try:
                print(f"O caminho {self.draws_path} não existe!")
                print("Criando diretório...")
                print("Diretório criado com sucesso!")

                Path.mkdir(self.draws_path)
            except FileExistsError as e:
                print(f"Erro ao tentar criar diretório cadDraws {e}")
            
        self.selected_file = filedialog.askopenfilename(title="Selecione um arquivo CAD",
                                                        initialdir=str(self.draws_path),
                                                         filetypes=(("Arquivos DWG", "*.dwg"), ("Todos os arquivos", "*.*")))

        return self.selected_file;
        
