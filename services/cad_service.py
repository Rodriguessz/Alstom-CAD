from core.cad_reader import CadReader
from pathlib import Path
from models.relay import Relay;
from core.relay_extractor import RelayExtractor;

class CadService:
    def __init__(self, cad_file_path: Path):
        self.reader = CadReader(cad_file_path)
        self.relayExt = RelayExtractor()

    def process(self):
        blocks = self.reader.get_block_entities()
        
        relays = self.relayExt.get_relays(blocks);


            
        return None;