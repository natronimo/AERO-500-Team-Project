import numpy as np

class SkiLiftSimulation:
    def __init__(self, T, lift_capacity=4, lift_interval=20.0):


        # System states
        self.N = 0 
        self.clock = 0.0
        self.T = T
        self.lift_capacity = lift_capacity
        self.lift_interval = lift_interval      

        # Event List
        self.t_arrival = self.generate_arrival()
        self.t_lift_depart = lift_interval  # First lift departs at t = lift_interval

        # Statistical Counters
        self.N_arrivals = 0
        self.N_served = 0
        self.total_wait = 0.0

    def generate_arrival(self):
        return self.clock + np.random.exponential(1. / (10 / 60))

    def advance_time(self):

        t_event = min(self.t_arrival, self.t_lift_depart)

        time_delta = t_event - self.clock
        self.total_wait += self.N * time_delta

        self.clock = t_event
        
        if t_event == self.t_arrival:
            self.handle_arrival()
        else:
            self.handle_lift_departure()

    def handle_arrival(self):
        self.N += 1
        self.N_arrivals += 1

        # Schedule next arrival
        if self.clock < self.T:
            self.t_arrival = self.generate_arrival()
        else:
            self.t_arrival = float('inf')

    def handle_lift_departure(self):
        num_boarding = min(self.N, self.lift_capacity)
        self.N -= num_boarding
        self.N_served += num_boarding


        if self.clock + self.lift_interval <= self.T:
            self.t_lift_depart = self.clock + self.lift_interval
        else:
            self.t_lift_depart = float('inf')


np.random.seed(0)
sim = SkiLiftSimulation(T=300.0)  # seconds

while sim.clock < sim.T:
    sim.advance_time()


print(f"Total arrivals: {sim.N_arrivals}")
print(f"Total served: {sim.N_served}")
print(f"People left in line: {sim.N}")
print(f"Total wait time: {sim.total_wait:.2f} sec")
print(f"Average number in system: {sim.total_wait / sim.clock:.2f}")
print(f"Average wait per person served: {sim.total_wait / sim.N_served:.2f} sec")

print("testing version control")