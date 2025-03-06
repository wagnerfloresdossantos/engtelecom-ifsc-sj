

from arq import ARQ
import poller
import sys
from subcamada import Subcamada
from enquadramento import Enquadramento
from aplicacao import Aplicacao
from serial import Serial


Timeout = 15 # 15 segundos

# nome da porta serial informada como primeiro argumento
# de linha de comando
porta = Serial(sys.argv[1])

# cria objeto Enquadramento
enq = Enquadramento(porta, Timeout)

# cria objeto ARQ
arq = ARQ(Timeout)

# Cria objeto Aplicacao
app = Aplicacao()

# Conecta as subcamadas
# Deve ser feito a partir da subcamada inferior
enq.conecta(arq)  # Enquadramento → ARQ
arq.conecta(app)  # ARQ → Aplicacao

# cria o Poller e registra os callbacks
sched = poller.Poller()
sched.adiciona(enq)
#sched.adiciona(arq)  
sched.adiciona(app)

# entrega o controle ao Poller
sched.despache()