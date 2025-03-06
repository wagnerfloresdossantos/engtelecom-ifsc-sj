import socket
import sys
from poller import Callback

class Connection:
    """ Classe que gerencia a comunicação com um servidor utilizando um socket UDP"""
    
    def __init__(self, server_ip: str, server_port: int):
        """
        Args:
            server (str): ip do servidor
            port (int): porta do servidor
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def send(self, data: bytes):
        """Envia dados para o servidor"""
        self.socket.sendto(data, (self.server_ip, self.server_port))
    
    def receive(self, buffer_size: int = 516):
        """Recebe dados do servidor 
        
        Args:
            buffer_size (int):  2 opcode + 2 block + 512 data  
        """
        return self.socket.recvfrom(buffer_size)
    
    def close(self):
        """Fecha o socket"""
        self.socket.close()


class ConnectionCallback(Callback):
    """Callback para gerenciar eventos de conexão com o Poller"""
    
    def __init__(self, connection, client):
        super().__init__(fileobj=connection.socket, timeout=5)
        self.connection = connection
        self.client = client 

    def handle(self):
        """Recebe pacotes e encaminha para o cliente"""
        try:            
            # Processa os pacotes
            data_packet, server_address = self.connection.receive()
            self.client._mef(evento="DADOS_RECEBIDOS", dados=(data_packet, server_address))
        except Exception as e:
            print(f"Erro ao processar pacote: {e}")
            self.client._mef(evento="ERROR")

    def handle_timeout(self):
        """Notifica o cliente sobre timeouts."""
        print("Timeout ocorrido.")
        self.client._mef(evento="TIMEOUT")

    def handle_finish(self):
        print("Transferência concluída, encerrando a conexão.")
        self.disable()
        sys.exit() 
    
    def handle_erro(self):
        print("Transferência falhou. Encerrando.")
        self.disable()
        sys.exit()
        
        