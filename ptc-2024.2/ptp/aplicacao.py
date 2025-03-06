from crc import CRC16
from subcamada import Subcamada
import sys  
from quadro import Quadro

class Aplicacao(Subcamada):

    def __init__(self, tout=1000):  # Adicione um valor padrão para o timeout
        Subcamada.__init__(self, sys.stdin, tout)  # Passe o timeout para a classe base
        self.buffer = bytearray()
        self.sequencia = 0

    def recebe(self, quadro: Quadro):
        # Decodifica os dados recebidos e exibe na tela
        if quadro.dados:
            print(f"[Aplicação] Dados recebidos: {quadro.dados.decode()}")
        else:
            print(f"[Aplicação] Quadro recebido sem dados.")
    
    def handle(self):
        dados = sys.stdin.readline().strip()
        dados_bytes = dados.encode('utf-8')
        
        # Monta um Quadro do tipo DATA
        quadro = Quadro(
            tipo='DATA',
            numero_sequencia=self.sequencia,
            tipo_conteudo='text',
            dados=dados_bytes
        )
        self.sequencia = self.sequencia + 1
        print('[Aplicação]:', dados)
        self.lower.envia(quadro)