import random


class Event:

    def __init__(self, time):
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

    def process(self, simulator):
        raise NotImplementedError


class ArrivalEvent(Event):

    def process(self, simulator):

        simulator.generated_calls += 1

        # verifica canal livre
        if simulator.busy_channels < simulator.k:

            simulator.busy_channels += 1
            simulator.accepted_calls += 1

            # gera duração da chamada
            duration = random.expovariate(simulator.mu)

            end_time = simulator.current_time + duration

            simulator.schedule(
                DepartureEvent(end_time)
            )

        else:
            simulator.blocked_calls += 1

        # agenda próxima chegada
        interarrival = random.expovariate(
            simulator.lambda_rate
        )

        next_arrival = simulator.current_time + interarrival

        simulator.schedule(
            ArrivalEvent(next_arrival)
        )


class DepartureEvent(Event):

    def process(self, simulator):

        simulator.busy_channels -= 1