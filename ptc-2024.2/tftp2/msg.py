import messages_pb2

class Msg:
    def create_rrq(self, filename, mode=messages_pb2.Mode.octet):
        """Cria uma mensagem RRQ."""
        mensagem = messages_pb2.Mensagem()
        mensagem.rrq.fname = filename
        mensagem.rrq.mode = mode
        return mensagem.SerializeToString()

    def create_wrq(self, filename, mode=messages_pb2.Mode.octet):
        """Cria uma mensagem WRQ."""
        mensagem = messages_pb2.Mensagem()
        mensagem.wrq.fname = filename
        mensagem.wrq.mode = mode
        return mensagem.SerializeToString()

    def create_data(self, block_number, data):
        """Cria uma mensagem DATA."""
        mensagem = messages_pb2.Mensagem()
        mensagem.data.block_n = block_number
        mensagem.data.message = data
        return mensagem.SerializeToString()

    def create_ack(self, block_number):
        """Cria uma mensagem ACK."""
        mensagem = messages_pb2.Mensagem()
        mensagem.ack.block_n = block_number
        return mensagem.SerializeToString()

    def create_error(self, error_code, error_msg):
        """Cria uma mensagem Error."""
        mensagem = messages_pb2.Mensagem()
        mensagem.error.errorcode = error_code
        mensagem.error.message = error_msg
        return mensagem.SerializeToString()

    def create_mkdir(self, caminho):
        """Cria uma mensagem MKDIR."""
        mensagem = messages_pb2.Mensagem()
        mensagem.mkdir.path = caminho  
        return mensagem.SerializeToString()
    
    def create_move(self, nome_original, novo_nome):
        mensagem = messages_pb2.Mensagem()
        mensagem.move.nome_orig = nome_original
        if novo_nome not in [None, '']:
            mensagem.move.nome_novo = novo_nome
        return mensagem.SerializeToString()
    def create_list(self, caminho):
        mensagem= messages_pb2.Mensagem()
        mensagem.list.path = caminho
        return mensagem.SerializeToString()        
