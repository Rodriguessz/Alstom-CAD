import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from config.settings import EXCEL_SHEETS_PATH
from pathlib import Path


class FileExcelSelector:
    """A classe FileExcelSelector fornece uma interface gráfica simples utilizando
    Tkinter, permitindo que os usuários selecionem arquivos Excel (.xlsx) de um
    diretório predefinido. Esta classe lida com a criação de um diretório para
    armazenar as planilhas Excel caso ele não exista e apresenta um diálogo para
    a seleção de arquivos, facilitando o processo de escolha de documentos Excel.

    Responsabilidades Principais:
    - Interface Gráfica: Cria elementos da interface, como rótulos e botões,
      para facilitar a interação do usuário na seleção de arquivos Excel.
    - Seleção de Arquivos: Proporciona um método para abrir uma caixa de diálogo
      que permite ao usuário escolher um arquivo Excel específico.
    - Verificação e Criação de Diretórios: Verifica se o diretório para os arquivos
      Excel existe e, caso não exista, tenta criá-lo, assegurando que o caminho
      de seleção sempre esteja disponível.
    """
    
    def __init__(self, masterTk):
        self.master = masterTk
        self.master.title("ALSTOMCAD APPLICATION")
        self.master.geometry("500x300")  # Define a largura da janela para 500 pixels
        self.selected_file = None
        self.sheets_path = EXCEL_SHEETS_PATH
        
        # Criando um Frame para organizar os componentes da interface
        self.main_frame = tk.Frame(self.master, width=500, height=300)
        self.main_frame.pack_propagate(False)  # Impede o redimensionamento
        self.main_frame.pack(padx=10, pady=10)  # Adiciona margens ao redor do Frame
        
        # Criando componentes da UI
        self.label = tk.Label(self.main_frame, text="Selecione um arquivo (.xlsx):")
        self.label.pack(pady=(20, 10))  # Adiciona um espaço acima e abaixo do rótulo

        self.select_button = tk.Button(self.main_frame, text="Selecionar Arquivo", command=self.get_selected_file)
        self.select_button.pack(pady=10)  # Adiciona espaço acima e abaixo do botão

    def get_selected_file(self) -> str:
        """Abre o modal para seleção de arquivos XLSX e retorna o nome do arquivo selecionado."""

        if not Path(self.sheets_path).exists():
            try:
                print(f"O caminho {self.sheets_path} não existe!")
                print("Criando diretório...")
                Path.mkdir(self.sheets_path)
                print("Diretório criado com sucesso!")
            except FileExistsError as e:
                print(f"Erro ao tentar criar diretório {self.sheets_path}: {e}")
        
        self.selected_file = filedialog.askopenfilename(
            title="Selecione um arquivo Excel",
            initialdir=str(self.sheets_path),
            filetypes=(("Arquivos XLSX", "*.xlsx"), ("Todos os arquivos", "*.*"))
        )

        if self.selected_file:  # Verifica se um arquivo foi realmente selecionado
            print(f"Arquivo selecionado: {self.selected_file}")
        else:
            raise Exception("[ERRO] Arquivo não selecionado, impossível prosseguir!");

        
        return self.selected_file

# Exemplo de inicialização da interface
if __name__ == "__main__":
    root = tk.Tk()
    file_selector = FileExcelSelector(root)
    root.mainloop()