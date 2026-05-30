import random


# =====================================================
# Classe base para todos os eventos da simulação.
#
# Cada evento possui:
# - um instante de ocorrência (time)
# - um método process(), que define sua ação
#
# Os eventos serão armazenados em uma fila de eventos
# futuros ordenada cronologicamente.
# =====================================================
class Event:

    def __init__(self, time):
        self.time = time

    # Permite ordenar os eventos pelo tempo de ocorrência.
    # O heapq utiliza este método para determinar qual
    # evento deve ser processado primeiro.
    def __lt__(self, other):
        return self.time < other.time

    # Método abstrato.
    # Cada tipo de evento implementa sua própria lógica.
    def process(self, simulator):
        raise NotImplementedError


# =====================================================
# Evento de chegada de chamada.
#
# Quando uma chamada chega ao sistema:
# 1) contabiliza a chamada gerada;
# 2) verifica se existe canal livre;
# 3) aceita ou bloqueia a chamada;
# 4) agenda o término da chamada (se aceita);
# 5) agenda a próxima chegada.
#
# Este evento representa o processo de chegada Poisson
# do modelo M/M/k/k.
# =====================================================
class ArrivalEvent(Event):

    def process(self, simulator):

        # Contabiliza uma nova chamada gerada.
        simulator.generated_calls += 1

        # Verifica se existe algum canal disponível.
        if simulator.busy_channels < simulator.k:

            # Aceita a chamada e ocupa um canal.
            simulator.busy_channels += 1
            simulator.accepted_calls += 1

            # Sorteia a duração da chamada utilizando
            # distribuição exponencial com taxa μ.
            #
            # A função expovariate() utiliza internamente
            # o PRNG Mersenne Twister da biblioteca random.
            duration = random.expovariate(
                simulator.mu
            )

            # Calcula o instante de término da chamada.
            end_time = (
                simulator.current_time +
                duration
            )

            # Agenda o evento de saída da chamada.
            simulator.schedule(
                DepartureEvent(end_time)
            )

        else:

            # Todos os canais estão ocupados.
            # Como o sistema M/M/k/k não possui fila,
            # a chamada é bloqueada imediatamente.
            simulator.blocked_calls += 1

        # Sorteia o intervalo até a próxima chegada.
        #
        # Os intervalos entre chegadas seguem uma
        # distribuição exponencial com taxa λ.
        interarrival = random.expovariate(
            simulator.lambda_rate
        )

        # Calcula o instante da próxima chegada.
        next_arrival = (
            simulator.current_time +
            interarrival
        )

        # Agenda a próxima chegada.
        simulator.schedule(
            ArrivalEvent(next_arrival)
        )


# =====================================================
# Evento de término de chamada.
#
# Quando uma chamada termina:
# 1) o canal utilizado é liberado;
# 2) o sistema passa a ter mais capacidade para
#    atender futuras chamadas.
#
# Este evento representa a conclusão do serviço
# no modelo M/M/k/k.
# =====================================================
class DepartureEvent(Event):

    def process(self, simulator):

        # Libera um canal ocupado.
        simulator.busy_channels -= 1