from enum import Enum
from quadro import Quadro
from subcamada import Subcamada
from collections import deque  # Usaremos deque para a fila de saída

class EstadoARQ(Enum):
    OCIOSO = 0
    ESPERA = 1

class ARQ(Subcamada):
    def __init__(self, tout: float):
        super().__init__(0, tout)  # Inicializa a subcamada
        tout = 1000
        #self.disable()
        #self.disable_timeout()
        self._estado = EstadoARQ.OCIOSO
        self._N = 0  # Bit de sequência para transmissão
        self._M = 0  # Bit de sequência para recepção
        self._ultimo_quadro = None
        self.timeout_callback = tout
        self._fila_saida = deque()  # Fila de saída para quadros

    def _enviar_quadro(self, quadro):
        """Envia um quadro e atualiza o último quadro enviado."""
        self._ultimo_quadro = quadro
        self.lower.envia(quadro)

    def _reenviar_quadro(self):
        """Reenvia o último quadro enviado."""
        if self._ultimo_quadro:
            self.lower.envia(self._ultimo_quadro)

    def _enviar_ack(self, seq):
        """Envia um quadro ACK com o número de sequência especificado."""
        ack = Quadro(tipo='ACK', numero_sequencia=seq)
        self.lower.envia(ack)

    def _mef(self, evento: str = None, quadro: Quadro = None):
        """
        Máquina de estados acionada por eventos para ARQ Pare-e-espere.

        Args:
            evento (str): tipo do evento recebido.
            quadro (Quadro): quadro associado ao evento (quando aplicável).
        """
        if evento == "APP_TX":  # Aplicação deseja enviar dados
            print(f"[ARQ] Enfileirando quadro: {quadro}")
            self._fila_saida.append(quadro)  # Enfileira o quadro

            if self._estado == EstadoARQ.OCIOSO:
                self._enviar_quadro(self._fila_saida.popleft())  # Envia o próximo quadro da fila
                self._estado = EstadoARQ.ESPERA

        elif evento == "RX_ACK":  # Recebimento de ACK
            print(f"[ARQ] Recebido ACK: {quadro}")
            if self._estado == EstadoARQ.ESPERA:
                if quadro.controle['numero_sequencia'] == self._N:
                    self._N = 1 - self._N  # Alterna entre 0 e 1

                    if self._fila_saida:  # Se houver quadros na fila
                        self._enviar_quadro(self._fila_saida.popleft())  # Envia o próximo quadro
                    else:
                        self._estado = EstadoARQ.OCIOSO  # Volta ao estado Ocioso

        elif evento == "RX_DATA":  # Recebimento de quadro DATA
            print(f"[ARQ] Recebido quadro DATA: {quadro}")
            print("DATA Recebida:", quadro.dados.decode())
            if quadro.controle['numero_sequencia'] == self._M:
                self._enviar_ack(self._M)  # Envia ACK correspondente
                self._M = 1 - self._M  # Alterna entre 0 e 1

        elif evento == "TIMEOUT":  # Timeout ocorrido
            if self._estado == EstadoARQ.ESPERA:
                self._reenviar_quadro()

    def recebe(self, quadro):
        """Recebe um quadro da subcamada inferior."""
        # print("Quadro recebido!")
        # print(quadro.controle['tipo'])
        if quadro.controle['tipo'] == 'ACK':
            self._mef("RX_ACK", quadro)
        elif quadro.controle['tipo'] == 'DATA':
            self._mef("RX_DATA", quadro)

    def envia(self, quadro):
        """Envia um quadro para a subcamada inferior."""
        self._mef("APP_TX", quadro)

    def timeout(self):
        """Trata o evento de timeout."""
        self._mef("TIMEOUT")