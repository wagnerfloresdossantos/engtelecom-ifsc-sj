import tftp_client

# Usuário entra com o endereço do servidor tftp
server = input("Qual o endereço do servidor?\n")

# Usuário entra com a porta do servidor tftp
port = int(input("Qual a porta?\n"))

# Cliente Tftp é instanciado
cliente = tftp_client.TftpClient(server, port)

# Menu de opções 
operacao = int(input("1 - Enviar arquivo \n2 - Baixar arquivo\n3 - Criar diretórioloc(mkdir)\n4 - Renomear ou remover arquivo(move)\n5 - listar arquivos (list)\n"))

# se for baixar o arquivo, então qual o caminho (no servidor) que está esse arquivo?
# se for enviar o arquivo, então qual o caminho (relativo a partir desse menu.py) que está esse arquivo?
# se for criar uma pasta o caminho é o nome relativo do diretorio a ser criado a partir do indicado no tftp_server

if operacao != 4 and operacao != 5:
    caminho = input("Qual o nome do arquivo/diretório?\n")

if operacao == 1:
    cliente.envia_arquivo(caminho)
elif operacao == 2:
    cliente.recebe_arquivo(caminho)
elif operacao == 3:
    cliente.mkdir(caminho)
elif operacao == 4:
    nome_original = input("Qual o nome original do arquivo que você deseja renomear?\n")
    novo_nome = input("Qual o novo nome que você deseja colocar? (Não digite nada caso queira remover)\n")
    cliente.move(nome_original, novo_nome)
elif operacao == 5:
    caminho = input("Qual o caminho do diretório que deseja listar?\n")
    cliente.list(caminho)
    