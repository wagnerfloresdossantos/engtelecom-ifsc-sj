from serial import Serial
from subcamada import Subcamada
from crc import CRC16
from quadro import Quadro
from enum import Enum

# Estados da MEF de enquadramento
class State(Enum):
    OCIOSO = 1
    START = 2
    RX = 3
    ESCAPE = 4

class Enquadramento(Subcamada):
    def __init__(self, porta_serial: Serial, tout: float):
        Subcamada.__init__(self, porta_serial, tout)
        self.dev = porta_serial
        self._buffer = bytearray()
        self._state = State.OCIOSO

    def handle(self):
        # Lê os bytes disponíveis na serial
        dados = self.dev.read()
        for byte in dados:
            #print(f"[Enquadramento] Byte recebido: {byte:02x}")
            self._handle_mef(byte)

    def _handle_mef(self, byte: int):
        if self._state == State.OCIOSO:
            if byte == 0x7e:
                self._clean_buffer()
                self._state = State.START
        elif self._state == State.START:
            if byte == 0x7d:
                self._state = State.ESCAPE
            elif len(self._buffer) > 1024:
                self._clean_buffer()
                self._state = State.OCIOSO
            else:
                self._store(byte)
                self._state = State.RX
        elif self._state == State.RX:
            if len(self._buffer) > 1024:
                self._clean_buffer()
                self._state = State.OCIOSO
            elif byte == 0x7d:
                self._state = State.ESCAPE
            elif byte == 0x7e:
                # Delimitador de fim de quadro encontrado: processa o frame
                self._process_frame()
                self._clean_buffer()
                self._state = State.OCIOSO
            else:
                self._store(byte)
        elif self._state == State.ESCAPE:
            # Byte escapado: desfaz o escape e volta para RX
            self._store(byte ^ 0x20)
            self._state = State.RX

    def _store(self, byte: int):
        self._buffer.append(byte)

    def _clean_buffer(self):
        self._buffer.clear()

    def _process_frame(self):
        # Se o buffer tem tamanho mínimo (pelo menos 2 bytes para FCS)
        if len(self._buffer) >= 2:
            # Verifica o CRC do quadro recebido (buffer sem os delimitadores)
            if CRC16(self._buffer).check_crc():
                print("\n[Enquadramento] CRC válido! Dados enviados para Aplicacao.")
                # Separa os bytes do quadro e do FCS
                quadro_bytes = self._buffer[:-2]
                fcs_bytes = self._buffer[-2:]
                
                # Extrai o byte de controle (bit 7)
                control_byte = quadro_bytes[0] 
                is_ack = (control_byte & 0x80) != 0  # Check bit 7
                tipo = 'ACK' if is_ack else 'DATA'
                
                # Extrai o bit de sequência (bits 3-6)
                numero_sequencia = (control_byte >> 3) & 0x0F
                dados = quadro_bytes[2:] if len(quadro_bytes) > 2 else None
                
                quadro = Quadro(tipo, numero_sequencia, dados=dados)
                quadro.fcs = fcs_bytes  # Atribui o FCS recebido
                self.upper.recebe(quadro)
            
    def envia(self, quadro: Quadro):
        # Mapeamento para converter o campo tipo para o bit 7 do controle
        tipo_mapping = {'DATA': 0x00, 'ACK': 0x80}  # Bit 7: 0 = DATA, 1 = ACK
        tipo_bit = tipo_mapping.get(quadro.controle['tipo'], 0x00)

        # Monta o campo Controle: tipo (bit 7) e número de sequência (bit 3)
        controle_byte = tipo_bit | (quadro.controle['numero_sequencia'] << 3)

        # Constrói o payload do quadro: Controle, Reservado, Proto (se DATA), Dados
        frame = bytearray()
        frame.append(controle_byte)  # Campo Controle
        frame.append(0x00)  # Campo Reservado (0x00 por padrão)

        # Adiciona o campo Proto apenas se o quadro for do tipo DATA
        if quadro.controle['tipo'] == 'DATA' and quadro.proto:
            frame.append(ord(quadro.proto[0]))  # Converte o primeiro caractere do proto para byte

        # Adiciona os dados, se houver
        if quadro.dados:
            frame.extend(quadro.dados)

        # Gera o FCS a partir do payload e anexa ao frame
        crc_obj = CRC16(frame)
        fcs_bytes = crc_obj.gen_crc()[-2:]  # Últimos 2 bytes (FCS)
        quadro.fcs = fcs_bytes
        frame += fcs_bytes

        # Realiza o escaping dos bytes especiais (0x7e e 0x7d)
        frame_escapado = self._escape(frame)

        # Monta o quadro completo com delimitadores de início e fim
        quadro_completo = bytearray()
        quadro_completo.append(0x7e)  # Delimitador de início
        quadro_completo += frame_escapado
        quadro_completo.append(0x7e)  # Delimitador de fim

        print(f"[Enquadramento] Enviando quadro {quadro.controle['tipo']}: {quadro_completo.hex()}")
        self.dev.write(bytes(quadro_completo))

    def _escape(self, data: bytearray) -> bytearray:
        resultado = bytearray()
        for byte in data:
            if byte in (0x7e, 0x7d):
                resultado.append(0x7d)
                resultado.append(byte ^ 0x20)
            else:
                resultado.append(byte)
        return resultado

    def recebe(self, quadro: Quadro):
        # Encaminha o quadro para a camada superior
        self.upper.recebe(quadro)

    def handle_timeout(self):
        # Em caso de timeout, se estivermos em meio a um frame, limpa o buffer e retorna ao estado OCIOSO
        if self._state in (State.START, State.RX, State.ESCAPE):
            print("[Enquadramento] Timeout: quadro incompleto descartado.")
            self._clean_buffer()
            self._state = State.OCIOSO