from pathlib import Path
from services.cad_service import CadService

def main():
    cad_path = Path(r"C:\Users\enzof\Documents\cads\gabinete_reles.dwg")
    service = CadService(cad_path)

    try:
        service.process()
        print("Processamento concluído com sucesso.")
    except Exception as e:
        print(f"Erro durante o processamento: {e}")

if __name__ == "__main__":
    main()
