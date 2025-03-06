class Msg:

    def create_rrq(self, filename):
        # Cria a cabeçalho rrq
        self.filename = filename
        mensage_rrq = b'\x00\x01' # opcode para RRQ 2 bytes
        mensage_rrq += filename.encode() 
        mensage_rrq += b'\x00'
        mensage_rrq += 'octet'.encode() 
        mensage_rrq += b'\x00'
        return mensage_rrq

        print(f'Solicitando a transferência do arquivo {filename}...')

    def create_wrq(self, filename):
        # Cria o cabeçalho wrq
        self.filename = filename
        mensage_wrq = b'\x00\x02' # opcode para WRQ 2 bytes
        mensage_wrq += filename.encode() 
        mensage_wrq += b'\x00'
        mensage_wrq += 'octet'.encode() 
        mensage_wrq += b'\x00'
        return mensage_wrq
        print(f'Solicitando a transferência do arquivo {filename}...')

    def create_data(self, block, data):
        # Cria o cabeçalho data
        mensage_data = b'\x00\x03'
        mensage_data += block
        mensage_data += data
        return mensage_data

    def create_ack(self, block):
        # cria o cabeçalho ack
        mensage_ack =  b'\x00\x04'
        mensage_ack += block
        return mensage_ack
    
    def create_error(self, erro_code, erro_msg):
        # cria cabeçalho erro
        mensage_error =  b'\x00\x05'
        mensage_error += erro_code
        mensage_error += erro_msg
        mensage_error += b'\x00'
        return mensage_error

    def send_data(self):
        # Lógica para enviar dados

        print('Enviando dados...')

    def receive_data(self):
        # Lógica para receber dados
        print('Recebendo dados...')
    