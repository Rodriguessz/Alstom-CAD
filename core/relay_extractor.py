# src/core/relay_extractor.py
from core.interop import AutoCAD2021 as AutoCAD
from typing import List, cast
from models.relay import Relay


class RelayExtractor:
    def __init__(self):
        pass

    def get_relays(self, blocks: list[AutoCAD.IAcadBlockReference]) -> List[AutoCAD.IAcadBlockReference]:
        relays = []
        
        for block in blocks:
            if block.Name == "RELE":
                relay = Relay(None, None, None, None, None,None)
                relay_attrs = self.get_relay_attributes(block)

                for attribute in relay_attrs:
                     relay[attribute.TagString] = attribute.TextString;
                relays.append(block)

                print(relay.r)
                print(relay.sin)

        return relays
    
    def get_relay_attributes(self, relay: AutoCAD.IAcadBlockReference):
        attr = None;
        if relay.HasAttributes:
            attr = relay.GetAttributes();
        return attr;
