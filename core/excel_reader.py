from pathlib import Path
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing import Optional

class ExcelReader:
    """Classe representativa do EXCEL"""

    def __init__(self, file_path: Path ):
        self.file_path = file_path;
        self.workbook = None
        self.sheet: Optional[Worksheet] = None

    def exists(self) -> bool:
        """Verifica se o arquivo Excel existe"""
        return self.file_path.exists()
    
    def open_excel_sheet(self, sheet_name: str = None):
        """Abre a planilha e carrega a aba especificada (ou a primeira, por padrão)"""

        if not self.exists():
            raise FileNotFoundError(f"Arquivo Excel não encontrado: {self.file_path}")

        self.workbook = load_workbook(self.file_path)

        if sheet_name:
            if sheet_name in self.workbook.sheetnames:
                self.sheet = self.workbook[sheet_name]
            else:
                raise ValueError(f"Aba '{sheet_name}' não encontrada no arquivo.")
        else:
            # Se nenhum nome for passado, seleciona a primeira aba
            self.sheet = self.workbook.active

    def find_cell_by_value(self, value: str):
        """Procura por um valor na planilha inteira e retorna a célula (se existir)"""
        if not self.sheet:
            raise ValueError("Aba Excel não carregada.")

        #Percore as linhas da planilha
        for row in self.sheet.iter_rows():
            #Percorre as celulas presentes na linha atual e compara com o valor passado;
            for cell in row:
                #Padroniza os valores removendo espaçoes e deixando em lowecase para comparação
                if str(cell.value).strip().lower() == value.strip().lower():
                    return cell
        return None

    def update_cell_by_value(self, target_value: str, new_value):
        """Procura uma célula pelo valor e atualiza com novo valor"""
        cell = self.find_cell_by_value(target_value)
        if cell:
            cell.value = new_value
            return True
        return False
    
    def save_changes(self, new_path: Optional[Path] = None):
        """Salva as alterações feitas na planilha"""
        if not self.workbook:
            raise ValueError("Workbook não carregado.")

        #Salva em um novo local ou no local padrão;
        path_to_save = new_path or self.file_path
        self.workbook.save(path_to_save)
