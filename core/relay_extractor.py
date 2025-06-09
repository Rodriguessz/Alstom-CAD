# src/core/relay_extractor.py
from core.interop import AutoCAD2021 as AutoCAD
from typing import List, cast
from models.relay import Relay


class RelayExtractor:
    def __init__(self):
        pass

    def get_relays(self, blocks: list[AutoCAD.IAcadBlockReference]) -> List[AutoCAD.IAcadBlockReference]:
        relays = [];
        
        for block in blocks:
            if block.Name == "RELE":

                # Cria uma nova instancia da classe Relay afim de representar um objeto de rele.
                relay = Relay();

                #Recupera os atributos que o bloco possui no AUTOCAD.
                relay_attrs = self.get_relay_attributes(block);
                x, y , z = block.InsertionPoint;
                block_name = block.Name;
                block_layer = block.Layer;
                
                # Seta os atributos recuperados do bloco no objeto intanciado.
                for attribute in relay_attrs:
                    relay.__setattr__(str(attribute.TagString).lower(), str(attribute.TextString).lower());
                relay.x = x;
                relay.y = y;
                relay.z = z;
                relay.block_name = block_name;
                relay.layer = block_layer;   

                # Por fim, adiciona a instancia da classe no array;
                relays.append(relay)
                
        return relays
    
    def get_relay_attributes(self, relay: AutoCAD.IAcadBlockReference):
        attr = None;
        if relay.HasAttributes:
            attr = relay.GetAttributes();
        return attr;

    def compare_relays_state(self, relays_state: list, new_relays_state: list):
        """Compara o estado anterior e o novo dos reles, retornando as modificações.

        Args:
            relays_state (list): Lista de instâncias da classe Relay representando o 
                                estado anterior dos reles.
            new_relays_state (list): Lista de instâncias da classe Relay representando o 
                                    novo estado dos reles.

        Returns:
            list: Lista de dicionários representando as modificações.
        """
        modifications = []
        
        #Percore as duas listas de estados, verificando se há diferenças.
        for old_relay, new_relay in zip(relays_state, new_relays_state):
            modification = {}   
            
            # Compara a propriedade r e verifica se há alteração.
            if old_relay.r != new_relay.r:

                #Adiciona a alteração no dicionário, armazenando o valor atual e o anterior.
                modification["r"] = {
                    "previous_state": old_relay.r,
                    "new_state": new_relay.r
                }
            # Compara a propriedade sin e verifica se há alteração.
            if old_relay.sin != new_relay.sin:
                
                #Adiciona a alteração no dicionário, armazenando o valor atual e o anterior.
                modification["sin"] = {
                    "previous_state": old_relay.sin,
                    "new_state": new_relay.sin
                }
            

            # Apenas adiciona modificações se existirem
            if modification:
                modifications.append(modification)

        return modifications

            
            



            
            

        

        