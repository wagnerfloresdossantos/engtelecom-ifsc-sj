import socket
import threading


def send_msg():
    while True:
        MESSAGE = input('Qual mensagem você quer enviar? ')
        sock.sendto(MESSAGE.encode(), (SERVER_IP, SERVER_PORT))
        print(f"Mensagem enviada: {MESSAGE}")

def receive_msg():
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print("Mensagem recebida: %s" % data.decode())
        except Exception as e:
            print(f"Erro ao receber a mensagem: {e}")


SERVER_IP = input('Qual o IP do servidor? ')
SERVER_PORT = int(input('Qual a porta do servidor? '))

# Cria o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8001))

# Cria e inicia as threads
t1 = threading.Thread(target=send_msg)
t2 = threading.Thread(target=receive_msg)

t1.start()
t2.start()

t1.join()
t2.join()
