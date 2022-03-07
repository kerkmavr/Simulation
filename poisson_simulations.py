def arrival_process(rate):
    """
    Computes arrival times for iid exponentially distributed Poisson arrivals. Prerequisites: simpy, random, bisect
    """
    time = 0.
    while True:
        interarrival = random.expovariate(rate)  # generate interarrival
        time += interarrival
        yield time  # generator produces the next arrival time


def poisson_process(rate):
    """
    Returns a Poisson Process, N(t), which instantiates a new process every time it is called
    pp memoizes the arrival times to reduce computational cost
    """

    # Store arrivals
    a_process = arrival_process(rate)
    arrivals = [0.]

    def pp(time):
        """
        Returns the Kernel given the time which is the count till that time.
        """
        # If we haven't simulated that far yet...
        while arrivals[-1] < time:
            arrival_time = next(a_process)
            arrivals.append(arrival_time)
        count = bisect.bisect_right(arrivals, time) - 1
        return count

    return pp


def simpy_arrival_process(env, rate):  # env is simpy.Environment
    """
    Arrival process, implemented with Simpy
    """
    count = 0  # Counting the number of arrivals
    while True:
        interarrival = random.expovariate(rate)
        # Yield a Timeout Event
        yield env.timeout(interarrival)
        count += 1
        print(f'arrival {count:4d} at time {env.now:5.2f}')


# Actual Implementation

# The necessary imports
import simpy
import random
import bisect

# creates a SimPy Environment
env = simpy.Environment()

# Initialization of a new arrival process connected to the Environment at a predefined rate
arrivals = simpy_arrival_process(env, 3)

# Feed the Environment to process the first arrival event
env.process(arrivals)

# Run the simulated Environment (stopping after t=50)
env.run(until=50)
