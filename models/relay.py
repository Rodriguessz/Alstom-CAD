from dataclasses import dataclass
from typing import Optional, cast
from core.interop import AutoCAD2021 as AutoCAD
from pywintypes import com_error


@dataclass
class Relay:
    r: str                              # Nome ou identificação do relé
    sin: str                            # Sinal do Rele
    x: float                            # Posição X no CAD
    y: float                            # Posição Y no CAD
    layer: str                          # Camada (Layer) do relé
    block_name: str                     # Nome do bloco CAD
    description: Optional[str] = None   # Descrição opcional

    def __init__(self, r , sin, x , y , layer , block_name):
        self.r = r;
        self.sin = sin;
        self.x = x;
        self.y = y;
        self.layer = layer;
        self.block_name = block_name;



        
    