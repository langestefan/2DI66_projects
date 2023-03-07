from collections import deque
from numpy.ma.core import zeros
import matplotlib.pyplot as plt
import numpy as np


class SimResults:
    MAX_ENTRIES = 10000  # maximum number of time steps to be recorded

    def __init__(self, nr_queues):
        self.nrQueues = nr_queues

        self.sumQL = np.zeros((self.nrQueues, 1))  # total sum of queue lengths
        self.sumQL2 = np.zeros(
            (self.nrQueues, 1)
        )  # total sum of queue lengths squared
        self.sumW = np.zeros((self.nrQueues, 1))  # total sum of waiting times
        self.sumW2 = np.zeros(
            (self.nrQueues, 1)
        )  # total sum of waiting times squared

        # columns correspond with one queue
        # values in columns are queue lengths
        self.hist_ql = np.ones((self.MAX_ENTRIES, self.nrQueues)) * -1
        self.hist_w = (
            np.ones((self.MAX_ENTRIES, self.nrQueues)) * -1
        )  # number of registered waiting times

        self.oldTime = 0
        self.times = deque([self.oldTime])

        self.nQL = 0
        self.nW = 0

        self.canteen = deque()
        self.customers = deque()
        self.group = deque()

        self.sojournC = deque()
        self.sojournG = deque()

    def register_queue_length(self, time, ql):
        # queue length registered at each change, even if change only
        # occurred in one queue only

        # ql = queue length array
        self.sumQL += ql * (time - self.oldTime)
        self.sumQL2 += ql * ql * (time - self.oldTime)
        self.hist_ql[self.nrEntries_ql, :] = ql
        self.times.append(time)
        self.oldTime = time

        self.nQL += 1

        if self.nQL >= self.MAX_ENTRIES:
            raise ValueError(
                "Amount of entries exceeded expected maximum of"
                f" {self.MAX_ENTRIES}"
            )

    def register_waiting_time(self, w, q):
        self.hist_w[self.nrEntries_w, q] = w
        self.sumW[q] += w
        self.sumW2[q] += w * w

        self.nW += 1

        if self.nW >= self.MAX_ENTRIES:
            raise ValueError(
                "Amount of entries exceeded expected maximum of"
                f" {self.MAX_ENTRIES}"
            )

    def register_canteen(self, n):
        self.canteen.append(n)

    def register_group(self, g):
        self.group.append(g)
        # get_customers returns deque
        self.customers += g.get_customers()

    def register_sojourn_t(self, c):
        # TODO: Check variable names of customer
        # NOTE: c.arrivalTime is without grabTime!
        self.sojournC.append(c.depTime - c.arrivalTime)

        # TODO: Add all_left Boolean to check whether member of group left
        if c.get_group.all_left:
            # TODO: Add departure & arrival time of group to class Group
            self.sojournG.append(c.get_group.depTime - c.get_group.arrivalTime)

    def get_mean_ql(self):
        return self.sumQL / self.oldTime

    def get_var_ql(self):
        return self.sumQL2 / self.oldTime - self.getMeanQueueLength() ** 2

    def get_mean_wait_t(self):
        return self.sumW / self.nW

    def get_var_wait_t(self):
        return self.sumW2 / self.nW - self.getMeanWaitingTime() ** 2

    def get_mean_cust_canteen(self):
        return np.mean(self.canteen)

    def get_mean_sojourn_cust(self):
        return np.mean(self.sojournC)

    def get_mean_sojourn_group(self):
        return np.mean(self.sojournG)

    def get_ql_hist(self):
        return self.hist_ql

    def get_wait_t_hist(self):
        return self.hist_w

    def get_times(self):
        return self.times

    def __str__(self):
        s = f""
        for q in range(self.nrQueues):
            s += (
                f"Mean queue {q+1} length: {str(self.getMeanQueueLength())} \n"
            )
            s += (
                f"Std queue {q+1} length:"
                f" {str(np.sqrt(self.getVarianceQueueLength()))} \n"
            )
            s += (
                f"Mean waiting time of queue {q+1}:"
                f" {str(self.getMeanWaitingTime())} \n"
            )
            s += (
                f"Std waiting time of queue {q+1}:"
                f" {str(np.sqrt(self.getVarianceWaitingTime()))} \n"
            )

        return s

    def hist_ql(self, maxq=50):
        # TODO: Implement histogram plotting
        pass

    def hist_wait_t(self, nrBins=100):
        # TODO: Implement histogram plotting
        pass
