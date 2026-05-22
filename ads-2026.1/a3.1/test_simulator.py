from events import Event
from simulator import Simulator


class TestEvent(Event):

    def __init__(self, time, name):
        super().__init__(time)
        self.name = name

    def process(self, simulator):
        print(
            f"Tempo {simulator.current_time:.2f} -> "
            f"Evento: {self.name}"
        )


sim = Simulator(end_time=10)

sim.schedule(TestEvent(5, "Evento A"))
sim.schedule(TestEvent(2, "Evento B"))
sim.schedule(TestEvent(7, "Evento C"))
sim.schedule(TestEvent(1, "Evento D"))

sim.run()