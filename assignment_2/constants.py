"""Constants for assignment 2."""
import logging

# bernoulli probability of cash payment
P_CASH = 0.4

# p value for geometric distribution of group size
P_GROUP_SIZE = 1 / 3

# mean value for exponential distribution of service time (sec.)
MU_SERVICE_CASH = 20
MU_SERVICE_BANK = 12

# mean value for customer to grab their food (sec.)
MU_CUSTOM_GRAB_FOOD = 80

# customers arrive in groups according to a Poisson process
# with mean arrival rate of 1, 2, 3, 4 groups per minute
MU_ARRIVAL_RATE_MIN = [1, 2, 3, 4]
MU_ARRIVAL_RATE_SEC = [x / 60 for x in MU_ARRIVAL_RATE_MIN]

# simulation duration 12:00 - 13:00 in seconds
SIM_T = 100 #3600

# number of servers / queues
N_SERVERS = 3
N_QUEUES = 3

# debugging
LOG_FES = False
TIME_SLEEP = 0.5
DEBUG_THROTTLE = False
LOG_LEVEL = logging.DEBUG
