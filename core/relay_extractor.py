# src/core/relay_extractor.py
from core.interop import AutoCAD2021 as AutoCAD
from typing import List, cast
from models.relay import Relay


class RelayExtractor:
    """Classe responsável por extrair informações sobre reles a partir de blocos 
    do AutoCAD.

    A classe RelayExtractor fornece métodos para a identificação e extração de
    entidades de reles em um desenho do AutoCAD, representadas como instâncias
    da classe Relay.

    Responsabilidades Principais:
    - Extração de Rele: Identifica blocos de reles baseados no nome ("RELE") e 
      recupera suas propriedades, como atributos e coordenadas.
    - Recuperação de Atributos: Obtém atributos associados a blocos de relé do AutoCAD
      para armazenar as informações relevantes.
    - Comparação de Estados: Compara os estados anteriores e novos dos reles em um desenho especificando, retornando
      as modificações detectadas em forma de dicionário, permitindo o rastreamento de
      mudanças ao longo do tempo.

    A classe é integrada com a API do AutoCAD para facilitar a automação 
    na manipulação de desenhos, especialmente em aplicações que requerem 
    monitoramento de modificações em sistemas que utilizam representações 
    gráficas de reles e sua configuração.
    """

    def __init__(self):
        pass

    def get_relays(self, blocks: list[AutoCAD.IAcadBlockReference]) -> List[AutoCAD.IAcadBlockReference]:
        """Extrai todas as entidades de bloco que representam um RELE, retornando um lista contendo instâncias da classe Relay."""
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
        """Recupera os atributos associados ao RELE."""
        attr = None;
        if relay.HasAttributes:
            attr = relay.GetAttributes();
        return attr;

    def compare_relays_state(self, relays_state: list, new_relays_state: list):
        """Compara o estado anterior e o novo dos reles, retornando as modificações ao longo do tempo.

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

            # Compara as propriedades ( R, SIN) verifica se há alteração. Caso haja, adidcio-nas em um dicionário com o valor antigo e o novo.
            if old_relay.r != new_relay.r:
                modification["r"] = {
                    "previous_state": old_relay.r,
                    "new_state": new_relay.r
                }

            if old_relay.sin != new_relay.sin:
                modification["sin"] = {
                    "r": old_relay.r,
                    "previous_state": old_relay.sin,
                    "new_state": new_relay.sin
                }
            

            # Apenas adiciona modificações se existirem
            if modification:
                modifications.append(modification)

        return modifications

            
            



            
            

        

        