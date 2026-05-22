import heapq

from events import ArrivalEvent


class Simulator:

    def __init__(
        self,
        end_time,
        lambda_rate,
        mu,
        k
    ):

        self.current_time = 0.0
        self.end_time = end_time

        self.lambda_rate = lambda_rate
        self.mu = mu
        self.k = k

        self.event_queue = []

        # estado do sistema
        self.busy_channels = 0

        # métricas
        self.generated_calls = 0
        self.accepted_calls = 0
        self.blocked_calls = 0

        # estatísticas de utilização
        self.area_busy_channels = 0
        self.last_event_time = 0

    def schedule(self, event):

        heapq.heappush(
            self.event_queue,
            event
        )

    def update_statistics(self):

        time_diff = (
            self.current_time
            - self.last_event_time
        )

        self.area_busy_channels += (
            self.busy_channels * time_diff
        )

        self.last_event_time = self.current_time

    def run(self):

        # primeira chegada
        self.schedule(ArrivalEvent(0))

        while (
            self.event_queue
            and self.current_time < self.end_time
        ):

            event = heapq.heappop(
                self.event_queue
            )

            self.current_time = event.time

            self.update_statistics()

            event.process(self)

    def results(self):

        blocking_probability = (
            self.blocked_calls
            / self.generated_calls
        )

        utilization = (
            self.area_busy_channels
            / (self.k * self.current_time)
        )

        throughput = (
            self.accepted_calls
            / self.current_time
        )

        return {
            "generated": self.generated_calls,
            "accepted": self.accepted_calls,
            "blocked": self.blocked_calls,
            "blocking_probability":
                blocking_probability,
            "utilization":
                utilization,
            "throughput":
                throughput
        }