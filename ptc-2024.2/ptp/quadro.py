class Quadro:
    def __init__(self, tipo, numero_sequencia, tipo_conteudo=None, dados=None):
        self.controle = {
            'tipo': tipo,  # 'ACK' ou 'DATA'
            'numero_sequencia': numero_sequencia  # 0 ou 1
        }
        self.reservado = None  # Campo reservado para uso futuro
        self.proto = tipo_conteudo if tipo == 'DATA' else None  # Tipo de conteúdo, apenas para quadros do tipo DATA
        self.dados = dados[:1024] if tipo == 'DATA' and dados else None  # Dados, apenas para quadros do tipo DATA, limitado a 1024 bytes
        self.fcs = None  # Valor do código CRC-16-CCITT

    def __repr__(self):
        return f"Quadro(controle={self.controle}, reservado={self.reservado}, proto={self.proto}, dados={self.dados}, fcs={self.fcs})"