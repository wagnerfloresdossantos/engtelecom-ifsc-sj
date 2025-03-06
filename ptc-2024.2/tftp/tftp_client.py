from connection import Connection, ConnectionCallback
from msg import Msg
from poller import Poller
from enums import Estado, Erro

class TftpClient:
    def __init__(self, server: str, port: int):
        """
        Inicializa o cliente TFTP.

        Args:
            server (str): endereço do servidor.
            port (int): porta do servidor.
        """
        self._connection = Connection(server, port)
        self._message = Msg()
        self._estado = None 
        self._file = None  
        self._block_number = 0  
        self._last_data = None  
        self._poller = Poller()
        self._callback = ConnectionCallback(self._connection, self)  

    def envia_arquivo(self, caminho: str):
        """
        Inicia o processo de envio de arquivo.

        Args:
            caminho (str): caminho do arquivo para envio.
        """
        self._file = open(caminho, 'rb')
        self._block_number = 0
        self._estado = Estado.INIT
        _wrq_message = self._message.create_wrq(caminho)
        self._connection.send(_wrq_message)
        print(f"WRQ enviado para enviar o arquivo '{caminho}'.")
        self._poller.adiciona(self._callback)
        self._poller.despache()  

    def recebe_arquivo(self, caminho: str):
        """
        Inicia o processo de recebimento de arquivo.

        Args:
            caminho (str): caminho para salvar o arquivo recebido.
        """
        self._file = open(caminho, 'wb')
        self._block_number = 0
        self._estado = Estado.INIT
        _rrq_message = self._message.create_rrq(caminho)
        self._connection.send(_rrq_message)
        print(f"RRQ enviado para receber o arquivo '{caminho}'.")
        self._poller.adiciona(self._callback) 
        self._poller.despache()  

    def _mef(self, evento: str = None, dados: tuple = None):
        """
        Máquina de estados acionada por eventos.

        Args:
            evento (str): tipo do evento recebido.
            dados (tuple): dados associados ao evento.
        """
        if self._estado == Estado.FIM:
            self._callback.handle_finish()
        
        if evento == "DADOS_RECEBIDOS":
            if self._estado == Estado.INIT:
                self._handle_init(dados)
            elif self._estado == Estado.RX:
                self._handle_rx(dados)
            elif self._estado == Estado.TX:
                self._handle_tx(dados)
            elif self._estado == Estado.ULTIMA:
                self._handle_ultima(dados)
            elif self._estado == Estado.ERRO:
                self._handle_erro()
        elif evento == "TIMEOUT":
            print("Timeout ocorrido. Estado alterado para ERRO.")
            self._estado = Estado.ERRO
        elif evento == "ERROR":
            print("Erro durante o processamento. Estado alterado para ERRO.")
            self._estado = Estado.ERRO

    def _handle_init(self, dados: tuple):
        """
        Processa o estado INIT.

        Args:
            dados (tuple): primeiros dados recebidos.
        """
        if not dados:
            return

        data_packet, server_address = dados

        # Atualiza o TID do servidor
        self._connection.server_port = server_address[1]
        print(f"TID do servidor atualizado para {self._connection.server_port}")

        # Verifica se é um pacote de erro
        if data_packet[:2] == b'\x00\x05':
            error_code = data_packet[2:4]
            error_msg = data_packet[4:-1].decode()
            print(f"Erro do servidor: código {int.from_bytes(error_code, 'big')}, mensagem: {error_msg}")
            self._estado = Estado.ERRO
            return

        # Diferencia RX/TX
        if data_packet[:2] == b'\x00\x03':  # Primeiro pacote de dados (RRQ)
            print("Primeiro bloco de dados recebido.")
            self._estado = Estado.RX
            self._mef("DADOS_RECEBIDOS", dados)
        elif data_packet[:2] == b'\x00\x04':  # Primeiro ACK (WRQ)
            print("ACK inicial recebido.")
            self._estado = Estado.TX
            self._mef("DADOS_RECEBIDOS", dados)


    def _handle_rx(self, dados):
        """
        Processa o estado RX.

        Args:
            dados (tuple): dados recebidos.
        """
        data_packet, _ = dados

        # Verifica se é um pacote de dados
        if data_packet[:2] != b'\x00\x03':
            print("Erro: pacote recebido não é um pacote de dados.")
            self._estado = Estado.ERRO
            return

        block_number = int.from_bytes(data_packet[2:4], 'big')
        data = data_packet[4:]
        self._file.write(data)
        print(f"Bloco {block_number} recebido e salvo ({len(data)} bytes).")

        # Envia o ACK para o bloco recebido
        ack_message = self._message.create_ack(data_packet[2:4])
        self._connection.send(ack_message)
        print(f"ACK enviado para o bloco {block_number}.")

        # Verifica se é o último bloco
        if len(data) < 512:
            print("Último bloco recebido. Fim da transferência.")
            self._estado = Estado.FIM
            self._mef()

    def _handle_tx(self, dados):
        """
        Processa o estado TX.

        Args:
            dados (tuple): deve ser um ack recebido do rx do servidor.
        """
        ack_packet, _ = dados

        # Verifica se é um ACK
        if ack_packet[:2] != b'\x00\x04':
            print("Erro: pacote recebido não é um ACK.")
            self._estado = Estado.ERRO
            return

        ack_block = int.from_bytes(ack_packet[2:4], 'big')
        if ack_block == self._block_number:
            print(f"ACK recebido para o bloco {self._block_number}.")
            data = self._file.read(512)
            if not data:  # Último bloco
                self._last_data = self._message.create_data(self._block_number.to_bytes(2, 'big'), b'')
                self._connection.send(self._last_data)
                print("Último bloco enviado.")
                self._estado = Estado.FIM
                self._mef()
                return

            self._block_number += 1
            data_message = self._message.create_data(self._block_number.to_bytes(2, 'big'), data)
            self._connection.send(data_message)
            print(f"Bloco {self._block_number} enviado.")

    def _handle_ultima(self, dados):
        """
        Processa o estado ULTIMA.

        Args:
            dados (tuple): último bloco de dados a ser recebidos.
        """
        ack_packet, _ = dados

        if ack_packet[:2] == b'\x00\x04':
            ack_block = int.from_bytes(ack_packet[2:4], 'big')
            if ack_block == self._block_number:
                print("ACK do último bloco recebido. Transferência concluída.")
                self._estado = Estado.FIM
        else:
            print("Erro: não foi recebido ACK do último bloco.")
            self._estado = Estado.ERRO

    def _handle_erro(self):
        """Estado ERRO"""
        self._callback.handle_erro()
        
    def _handle_erro(self, error_code):
        """
        Processa o estado ERRO.

        Args:
            error_code (int): código de erro recebido do servidor.
        """
        match error_code:
            case Erro.ARQUIVO_NAO_ENCONTRADO:
                error_message = self._message.create_error(error_code, b'Arquivo nao encontrado.')
            case Erro.VIOLACAO_ACESSO:
                error_message = self._message.create_error(error_code, b'Violacao de acesso.')
            case Erro.DISCO_CHEIO:
                error_message = self._message.create_error(error_code, b'Disco cheio.')
            case Erro.OPERACAO_ILEGAL:
                error_message = self._message.create_error(error_code, b'Operacao ilegal.')
            case Erro.ID_DESCONHECIDO:
                error_message = self._message.create_error(error_code, b'ID desconhecido.')
            case Erro.ARQUIVO_EXISTENTE:
                error_message = self._message.create_error(error_code, b'Arquivo existente.')
            case Erro.USUARIO_INEXISTENTE:
                error_message = self._message.create_error(error_code, b'Usuario inexistente.')
            
        self._connection.send(error_message)
        
        self._callback.handle_erro()
