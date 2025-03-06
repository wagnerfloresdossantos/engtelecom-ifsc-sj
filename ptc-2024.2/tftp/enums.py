import enum


class Estado(enum.Enum):
    """
    Enumeração dos estados possíveis do cliente TFTP.

    Attributes:
        INIT (int): estado inicial.
        RX (int): recebendo dados.
        TX (int): enviando dados.
        ULTIMA (int): último bloco.
        ERRO (int): erro.
        FIM (int): fim da transferência.
    """
    INIT = 0
    RX = 1
    TX = 2
    ULTIMA = 3
    ERRO = 4
    FIM = 5

class Erro(enum.Enum):
    """
    Enumeração dos possíveis erros do cliente TFTP.

    Attributes:
        ERRO_NAO_DEFINIDO (int): erro indefinido.
        ARQUIVO_NAO_ENCONTRADO (int): arquivo não encontrado.
        VIOLACAO_ACESSO (int): violação de acesso.
        DISCO_CHEIO (int): disco cheio.
        OPERACAO_ILEGAL (int): operação ilegal.
        ID_DESCONHECIDO (int): id desconhecido.
        ARQUIVO_EXISTENTE (int): arquivo já existe.
        USUARIO_INEXISTENTE (int): usuário inexistente.
    """
    ERRO_NAO_DEFINIDO = 0
    ARQUIVO_NAO_ENCONTRADO = 1
    VIOLACAO_ACESSO = 2
    DISCO_CHEIO = 3
    OPERACAO_ILEGAL = 4
    ID_DESCONHECIDO = 5
    ARQUIVO_EXISTENTE = 6
    USUARIO_INEXISTENTE = 7