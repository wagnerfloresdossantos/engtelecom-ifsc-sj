import tftp_client

# Usuário entra com o endereço do servidor tftp
server = input("Qual o endereço do servidor?\n")

# Usuário entra com a porta do servidor tftp
port = int(input("Qual a porta?\n"))

# Cliente Tftp é instanciado
cliente = tftp_client.TftpClient(server, port)

# Menu de opções 
operacao = int(input("1 - Enviar arquivo \n2 - Baixar arquivo\n"))

# se for baixar o arquivo, então qual o caminho (no servidor) que está esse arquivo?
# se for enviar o arquivo, então qual o caminho (relativo a partir desse menu.py) que está esse arquivo?
caminho = input("Qual o caminho do arquivo?\n")


if operacao == 1:
    cliente.envia_arquivo(caminho)
elif operacao == 2:
    cliente.recebe_arquivo(caminho)