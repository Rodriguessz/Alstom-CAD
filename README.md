# AlstomCAD

![Badge de status do projeto](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

AlstomCAD é um projeto que automatiza a manipulação de desenhos CAD, permitindo a modificação de reles em  desenhos AutoCAD especificos, refletindo essas mudanças em uma planilha Excel. O objetivo é simplificar o processo de atualização de informações relacionadas a reles em projetos de engenharia elétrica, proporcionando uma maneira eficiente de manter os dados sincronizados entre os formatos CAD e Excel.

## Features

- **Seleção de arquivos CAD**: Interface para selecionar projetos CAD (.dwg) a partir de um diretório configurado.
- **Integração com Excel**: Seleção de planilhas Excel (.xlsx) para armazenar informações relacionadas aos reles.
- **Monitoramento de mudanças no CAD**: Capacidade de detectar modificações nos desenhos CAD e refletir essas mudanças na planilha Excel correspondente.
- **Interface gráfica (GUI)**: Uso da biblioteca Tkinter para criar uma interface amigável.

## Requisitos

Antes de começar, você precisa ter o seguinte instalado:

- Python 3.x
- Bibliotecas Python necessárias:
    - `tkinter` (normalmente incluído com a instalação do Python)
    - `openpyxl` - para manipulação de arquivos Excel
    - `pywin32` - para automação do AutoCAD ( A biblioteca precisa ser instalada globalmente, fora de um ambiente venv )

Você pode instalar as bibliotecas necessárias utilizando o `pip`:

```bash
pip install -r requirements.txt
```

## Rodando o projeto

Inicie um novo ambiente virtual dentro da pasta alstomcad:

```bash
python -m venv venv
python main.py
```



