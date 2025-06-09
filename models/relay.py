from dataclasses import dataclass
from typing import Optional, cast
from core.interop import AutoCAD2021 as AutoCAD
from pywintypes import com_error


@dataclass
class Relay:
    r: str;                              # Nome ou identificação do relé
    sin: str;                            # Sinal do Rele
    x: float;                            # Posição X no CAD
    y: float;                            # Posição Y no CAD
    z: float;                            # Posição Z no CAD
    layer: str;                          # Camada (Layer) do relé
    block_name: str;                     # Nome do bloco CAD
    description: Optional[str];          # Descrição opcional

    def __init__(self):
        self.r = None;
        self.sin = None;
        self.x = None;
        self.y = None;
        self.z = None;
        self.layer = None;
        self.block_name = "RELE";
        self.description = f"Referencia de Bloco: {self.block_name}"

    


        
    