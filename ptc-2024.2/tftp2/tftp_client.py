from connection import Connection, ConnectionCallback
from msg import Msg
from poller import Poller
from enums import Estado, Erro
import messages_pb2

import sys

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
        file = messages_pb2.FILE()
        file.nome = caminho
        
        self._file = open(file.nome, 'rb')
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
        
    def move(self, nome_original: str, novo_nome: str):
        mensagem = self._message.create_move(nome_original, novo_nome)
        self._estado = Estado.MOVE
        self._connection.send(mensagem)
        print('Mensagem Move preenchida e enviada.')
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
            elif self._estado == Estado.MKDIR:
                self._handle_mkdir_response(dados)
            elif self._estado == Estado.MOVE:
                self._handle_move_response(dados)
            elif self._estado == Estado.ERRO:
                self._handle_erro()
            elif self._estado == Estado.LIST:
                self._handle_list_response(dados)
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
        print('data_packet:', data_packet)
        received_message = messages_pb2.Mensagem()
        received_message.ParseFromString(data_packet)
        print('received_message:', received_message)
        
        if received_message.HasField('error'):
            self._estado = Estado.ERRO
            return
        elif received_message.HasField('data'): # Primeiro pacote de dados (RRQ)
            self._estado = Estado.RX
            self._mef('DADOS_RECEBIDOS', dados)
        elif received_message.HasField('ack'): # Primeiro ACK (WRQ)
            self._estado = Estado.TX
            self._mef("DADOS_RECEBIDOS", dados)


    def _handle_rx(self, dados):
        """
        Processa o estado RX.

        Args:
            dados (tuple): dados recebidos.
        """
        data_packet, _ = dados
        received_message = messages_pb2.Mensagem()
        received_message.ParseFromString(data_packet)
    
        # Verifica se é um pacote de dados
        if not received_message.HasField('data'):
            print("Erro: Pacote recebido não é um pacote de dados.")
            self._estado = Estado.ERRO
            return

        block_number = received_message.data.block_n
        data = received_message.data.message
        self._file.write(data)
        print(f"Bloco {block_number} recebido e salvo ({len(data)} bytes).")

        # Envia o ACK para o bloco recebido
        ack_message = self._message.create_ack(block_number)
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
        received_message = messages_pb2.Mensagem()
        received_message.ParseFromString(ack_packet)
        print('tx: received_message:', received_message)

        # Verifica se é um ACK
        if not received_message.HasField('ack'):
            print("Erro: pacote recebido não é um ACK.")
            self._estado = Estado.ERRO
            return
        
        ack_block = received_message.ack.block_n
        if ack_block == self._block_number:
            print(f"ACK recebido para o bloco {self._block_number}.")
            data = self._file.read(512)
            if not data:  # Último bloco
                self._last_data = self._message.create_data(self._block_number, b'')
                self._connection.send(self._last_data)
                print("Último bloco enviado.")
                self._estado = Estado.FIM
                self._mef()
                return

            self._block_number += 1
            data_message = self._message.create_data(self._block_number, data)
            self._connection.send(data_message)
            print(f"Bloco {self._block_number} enviado.")

    def _handle_ultima(self, dados):
        """
        Processa o estado ULTIMA.

        Args:
            dados (tuple): último bloco de dados a ser recebidos.
        """
        ack_packet, _ = dados

        received_message = messages_pb2.Mensagem()
        received_message.ParseFromString(ack_packet)

        if not received_message.HasField('ack'):
            print("Erro: Não foi recebido o último ACK.")
            self._estado = Estado.ERRO
            return
        else:        
            print("ACK do último bloco recebido. Transferência concluída.")
            self._estado = Estado.FIM


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



    def mkdir(self, caminho: str):
        """
        Solicita a criação de um diretório no servidor.

        Args:
            caminho (str): nome do diretório a ser criado.
        """
        # Cria a mensagem MKDIR usando o método `create_mkdir` do Msg
        mkdir_message = self._message.create_mkdir(caminho)

        # Envia a mensagem para o servidor
        self._connection.send(mkdir_message)
        print(f"Solicitação MKDIR enviada para criar o diretório '{caminho}'.")

        # Adiciona o callback no poller e aguarda a resposta
        self._estado = Estado.MKDIR
        self._poller.adiciona(self._callback)
        self._poller.despache()

    def _handle_mkdir_response(self, dados: tuple):
        """
        Processa a resposta da solicitação MKDIR.

        Args:
            dados (tuple): Dados recebidos do servidor.
        """
        data_packet, server_address = dados

        # Atualiza o TID do servidor
        self._connection.server_port = server_address[1]

        # Decodifica a mensagem recebida
        received_message = messages_pb2.Mensagem()
        received_message.ParseFromString(data_packet)

        if received_message.HasField('ack'):
            print(f"Diretório '{received_message.ack.block_n}' criado com sucesso no servidor.")
            self._estado = Estado.FIM
        elif received_message.HasField('error'):
            error_code = received_message.error.errorcode
            error_msg = received_message.error.message.decode('utf-8')
            print(f"Erro ao criar o diretório: {error_code} - {error_msg}")
        else:
            print("Resposta inesperada do servidor ao tentar criar o diretório.")
            
    def _handle_move_response(self, dados: tuple):
        """
        Processa a resposta da solicitação MOVE.

        Args:
            dados (tuple): Dados recebidos do servidor.
        """
        data_packet, server_address = dados

        # Atualiza o TID do servidor
        self._connection.server_port = server_address[1]

        # Decodifica a mensagem recebida
        received_message = messages_pb2.Mensagem()
        received_message.ParseFromString(data_packet)

        if received_message.HasField('ack'):
            print(f"Diretório '{received_message.ack.block_n}' criado com sucesso no servidor.")
            self._estado = Estado.FIM
        elif received_message.HasField('error'):
            error_code = received_message.error.errorcode
            error_msg = received_message.error.message.decode('utf-8')
            print(f"Erro ao criar o diretório: {error_code} - {error_msg}")
        else:
            print("Resposta inesperada do servidor ao tentar criar o diretório.")
            
    def _handle_list_response(self, dados: tuple):
        """
        Processa a resposta da solicitação LIST.
        
        Args:
            dados (tuple): dados do servidor.
        """
        data_packet, server_address = dados
               
        # Atualiza o TID do servidor
        self._connection.server_port = server_address[1]
        
        # Decodifica a mensagem recebida
        received_message = messages_pb2.Mensagem()
        received_message.ParseFromString(data_packet)
        
        # Cria uma lista para armazenar a listagem de arquivos e diretórios
        lista = []
        
        if received_message.HasField('error'):
            error_code = received_message.error.errorcode
            error_msg = received_message.error.message.decode('utf-8')
            print(f"Erro ao gerar lista de arquvos: {error_code} - {error_msg}")
            self._estado = Estado.FIM
        # Verifica se a mensagem recebida é uma lista de arquivos e diretórios, armazenando-os na lista, imprime a lista e encerra o programa    
        elif received_message.WhichOneof('msg') == 'list_resp':
            for i in received_message.list_resp.items:
                lista.append(i)
            print(f"Lista: _handle_list_response: {lista}")
            #sys.exit()
            self._estado = Estado.FIM
            print("Fim da listagem de arquivos e diretórios.")
            self._mef()
        else:
            print("Resposta inesperada do servidor ao tentar gerar lista de arquivos e diretórios.")
          
    def list(self, caminho: str):
        """
        Solicita a geração de uma lista de arquivos e diretórios no servidor.
        
        Args:
            caminho (str): caminho do diretório para gerar a lista.
        """
        # Cria a mensagem LIST usando o método `create_list` da classe `msg`
        mensagem = self._message.create_list(caminho)
        # Define o estado atual como LIST
        self._estado = Estado.LIST
        # Envia a mensagem para o servidor e imprime mensagem com o caminho solicitado
        self._connection.send(mensagem)
        print(f"Solicitação LIST enviada para gerar lista de arquivos e diretórios para o caminho '{caminho}'.")
        # Adiciona o callback no poller e aguarda a resposta
        self._poller.adiciona(self._callback)
        self._poller.despache()
        
       

