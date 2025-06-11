import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from config.settings import CAD_DRAWS_PATH
from pathlib import Path


class FileCadSelector:
    """Módulo responsável pela manipulação e seleção de arquivos CAD.

    A classe FileCadSelector fornece uma interface gráfica simples utilizando
    Tkinter para permitir ao usuário selecionar arquivos CAD (.dwg) a partir
    de um diretório pré-configurado. Esta classe lida com a criação de um
    diretório para armazenar os desenhos CAD caso ele não exista, além de
    apresentar um diálogo para a seleção de arquivos, facilitando o processo
    de escolha de documentos CAD.

    Responsabilidades Principais:
    - Interface Gráfica: Cria elementos da interface, incluindo rótulos e botões,
      para facilitar a interação do usuário na seleção de arquivos.
    - Seleção de Arquivos: Fornece um método para abrir uma caixa de diálogo que
      permite ao usuário escolher um arquivo CAD específico.
    - Verificação e Criação de Diretórios: Verifica se o diretório para os
      arquivos CAD existe e, caso não exista, tenta criá-lo, garantindo que o
      caminho de seleção sempre estará disponível.
    """
    
    def __init__(self, masterTk):
        self.master = masterTk
        self.master.title("ALSTOM CAD Application")  # Título da janela
        self.selected_file = None
        self.draws_path = CAD_DRAWS_PATH

        # Criando um Frame para organizar os componentes da interface
        self.main_frame = tk.Frame(self.master, width=500, height=300)  # Size can be adjusted
        self.main_frame.pack_propagate(False)  # Impede o redimensionamento
        self.main_frame.pack(padx=10, pady=10)  # Adiciona margens ao redor do Frame

        # Criando componentes da UI
        self.label = tk.Label(self.main_frame, text="Selecione um arquivo CAD (.dwg):")
        self.label.pack(pady=(20, 10))  # Adiciona espaço acima e abaixo do rótulo

        self.select_button = tk.Button(self.main_frame, text="Selecionar Arquivo", command=self.get_selected_file)
        self.select_button.pack(pady=10)  # Adiciona espaço acima e abaixo do botão

    def get_selected_file(self) -> str:
        """Abre o modal para seleção de arquivos CAD e retorna o nome do arquivo selecionado."""

        # Verifica se o diretório existe, se não, tenta criá-lo
        if not Path(self.draws_path).exists():
            try:
                print(f"O caminho {self.draws_path} não existe! Criando diretório...")
                Path.mkdir(self.draws_path, parents=True, exist_ok=True)  # Cria diretórios pai se não existirem
                print("Diretório criado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao tentar criar diretório: {e}")
                return None  # Retorna None se ocorrer um erro na criação do diretório
            
        self.selected_file = filedialog.askopenfilename(
            title="Selecione um arquivo CAD",
            initialdir=str(self.draws_path),
            filetypes=(("Arquivos DWG", "*.dwg"), ("Todos os arquivos", "*.*"))
        )

        # Verifica se um arquivo foi realmente selecionado
        if self.selected_file:
            print(f"Arquivo selecionado: {self.selected_file}")
        else:
            raise Exception("[ERRO] Arquivo não selecionado, impossível prosseguir!");

        return self.selected_file
        

# Exemplo de inicialização da interface
if __name__ == "__main__":
    root = tk.Tk()
    file_selector = FileCadSelector(root)
    root.mainloop()