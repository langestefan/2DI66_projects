from collections import deque
import matplotlib.pyplot as plt
import numpy as np
plt.style.use("ggplot")  # plotting style

class SimResults:
    """SimResults class"""
    MAX_ENTRIES = 10000  # maximum number of time steps to be recorded

    def __init__(self, nr_queues):
        """
        :param nr_queues: number of queues present in simulation
        """
        self.nrQueues = nr_queues

<<<<<<< HEAD
        # storing values related to queue length 
=======
>>>>>>> 394ca6d2955bb9d391c4a44738d16f3cf3939e3c
        self.sumQL = np.zeros((1, self.nrQueues))  # total sum of queue lengths
        self.sumQL2 = np.zeros(
            (1, self.nrQueues)
        )  # total sum of queue lengths squared
        self.histQL = np.zeros((self.MAX_ENTRIES+1, self.nrQueues)) # plot data
        self.allQL = deque() # list of all queue length values 
        self.nQL = 0 # number of entries 
        
        # storing values related to waiting time 
        self.sumW = np.zeros((self.nrQueues, 1))  # total sum of waiting times
        self.sumW2 = np.zeros(
            (self.nrQueues, 1)
        )  # total sum of waiting times squared
        self.allW = deque() # list of all waiting times, also plot data
        self.nW = 0 # number of entries 

        # storing values related to time 
        self.oldTime = 0
        self.times = deque([self.oldTime])

        # variables to keep track of number of customers in canteen and 
        # at which time stamps changes occured 
        self.canteen_times = deque() 
        self.canteen = deque() 
        
        # variables to store customer and group objects
        self.groups = deque() # to store group with index corresponding to group nr
        self.visitors = {} # to store customer with corresponding group nr

        # lists to gather sojourn times of customers and groups
        self.sojournC = deque()
        self.sojournG = deque()

    def register_queue_length(self, time, ql):
<<<<<<< HEAD
        """
        Registers queue length 
        
        :param time: time stamp at which length of one of the queues changed
        :param ql: queue lengths of each queue 
        """
        # update parameters 
        self.allQL.append(ql)
        self.sumQL += np.array(ql * (time - self.oldTime))
        self.sumQL2 += np.array(ql * ql * (time - self.oldTime))
        self.nQL += 1
        
        for q in range(len(ql)):
            self.histQL[min(ql[q], self.MAX_ENTRIES), q] += (time - self.oldTime)
            
=======
        # queue length registered at each change, even if change only
        # occurred in one queue only

        # ql = queue length array
        self.sumQL += np.array(ql * (time - self.oldTime))
        self.sumQL2 += np.array(ql * ql * (time - self.oldTime))
        #self.hist_ql[self.nrEntries_ql, :] = ql
>>>>>>> 394ca6d2955bb9d391c4a44738d16f3cf3939e3c
        self.times.append(time)
        self.oldTime = time

        if self.nQL >= self.MAX_ENTRIES:
            raise ValueError(
                "Amount of entries exceeded expected maximum of"
                f" {self.MAX_ENTRIES}"
            )

    def register_waiting_time(self, w, q):
<<<<<<< HEAD
        """
        Registers waiting time
        
        :param w: waiting time
        :param q: queue id 
        """
        # update parameters 
        self.allW.append(w)
=======
        # w = waiting time 
        # q = queue id 
        
        #self.hist_w[self.nrEntries_w, q] = w
>>>>>>> 394ca6d2955bb9d391c4a44738d16f3cf3939e3c
        self.sumW[q] += w
        self.sumW2[q] += w * w
        self.nW += 1

        if self.nW >= self.MAX_ENTRIES:
            raise ValueError(
                "Amount of entries exceeded expected maximum of"
                f" {self.MAX_ENTRIES}"
            )

    def register_canteen(self, t, n):
        """
        Registers number of customers in canteen each time it changed
        
        :param t: time stamp of change
        :param n: number of customers in canteen 
        """
        # update parameters 
        self.canteen_times.append(t)
        self.canteen.append(n)

    def register_group(self, g):
<<<<<<< HEAD
        """
        Registers group and corresponding customer objects
        
        :param g: Group object
        """
        # update parameters 
        self.groups.append(g)
        
        for c in g.get_customers():
            self.visitors[c] = len(self.groups)-1
        
    def register_sojourn_t(self, c):
        """
        Registers customer and group sojourn times 
        
        :param c: Customer object 
        """
        # update parameters
        self.sojournC.append(c.get_t_left() - c.get_t_arrival())
        
        group_nr = self.visitors[c]
        g = self.groups[group_nr]

        # check if all customers of a group have left the canteen 
        if not g.group_in_canteen():
            g.set_t_departure(c.get_t_left())
            self.sojournG.append(c.get_t_left()-g.get_t_arrival())
=======
        self.group.append(g)
        # get_customers returns deque
        self.customers += [c for c in g.get_customers()]

    def register_sojourn_t(self, c):
        # TODO: Check variable names of customer
        # NOTE: c.arrivalTime is without grabTime!
        self.sojournC.append(c.get_t_left() - c.get_t_arrival())

        # TODO: Add all_left Boolean to check whether member of group left
        #if c.get_group.all_left:
            # TODO: Add departure & arrival time of group to class Group
        #    self.sojournG.append(c.get_group.depTime - c.get_group.arrivalTime)
>>>>>>> 394ca6d2955bb9d391c4a44738d16f3cf3939e3c

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

    def get_ql_hist(self, q):
        return [x[q]/self.oldTime for x in self.histQL]

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
    
    def histQueueLength(self, maxq=50):
        """
        Plots histogram of queue lengths per queue 
        
        :param maxq: maximum queue length to be plotted in histogram
        """
        fig, ax = plt.subplots(self.nrQueues//3, 3)
        fig.suptitle("Histogram of queue lengths")
        
        for q in range(self.nrQueues):
            ql = self.get_ql_hist(q)
            maxx = maxq + 1
            ax[q].set_title(f"Queue {q}")
            ax[q].bar(range(0, maxx), ql[0:maxx])
            ax[q].set_ylabel('P(Q = k)')
            ax[q].set_xlabel('k')
        plt.show()
