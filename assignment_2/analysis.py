import assignment_2.constants as c
from collections import deque
import numpy as np
import itertools
import csv
import os

import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("ggplot")  # plotting style


def save_files(results, n):
    """
    Saves results to CSV files

    :param results: SimResults object
    :param n: Number of runs included
    """
    lst_all = [0] * len(c.MU_ARRIVAL_RATE_MIN)
    lst_separate = [0] * len(c.MU_ARRIVAL_RATE_MIN) * c.N_QUEUES

    ind = 0
    # gather all dictionaries into lists
    for lam in range(len(c.MU_ARRIVAL_RATE_MIN)):
        stats = results.get_statistics_all(lam)
        for entry in c.NOT_SAVED_ALL:
            if entry in stats.keys():
                del stats[entry]
        lst_all[lam] = stats

        for q in range(c.N_QUEUES):
            stats = results.get_statistics_separate(lam, q)
            for entry in c.NOT_SAVED_SEP:
                if entry in stats.keys():
                    del stats[entry]
            lst_separate[ind] = stats
            ind += 1

    # save results to CSV files
    # CustomersCanteen_times was messing up lay-out of CSV file
    fieldnames = list(lst_all[0].keys())  # type: ignore
    with open(f"results_all_nrRuns={n}.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lst_all)  # type: ignore

    fieldnames = list(lst_separate[0].keys())  # type: ignore
    with open(
        f"results_separate_nrRuns={n}_nrQueues={c.N_QUEUES}.csv",
        "w",
        newline="",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lst_separate)  # type: ignore


def plot_QL_hist_all(results, lam, path: str, maxq=50, show=False):
    """
    Plots histogram of queue lengths for all queues together

    :param results: SimResults object
    :param lam: index of rate parameter
    :param maxq: maximum queue length to be plotted in histogram
    """
    stats = results.get_statistics_all(lam)
    hist_data = stats["QueueLength_hist"]
    maxx = maxq + 1

    plt.figure()
    plt.bar(range(0, maxx), hist_data[0:maxx])
    plt.title(
        "Histogram of queue lengths with lambda ="
        f" {c.MU_ARRIVAL_RATE_MIN[lam]}\min"
    )
    plt.ylabel("P(Q = k)")
    plt.xlabel("k")
    plt.savefig(os.path.join(path, "hist_queue_length_all.png"), dpi=300)
    if show:
        plt.show()
    plt.close()


def plot_QL_hist_per_queue(results, lam, path: str, maxq=50, show=False):
    """
    Plots histogram of queue lengths for queues in separate subplots

    :param results: SimResults object
    :param lam: index of rate parameter
    :param path: path to save figure
    :param maxq: maximum queue length to be plotted in histogram
    """
    fig, ax = plt.subplots(c.N_QUEUES, 1)
    fig.suptitle(
        "Histogram of queue lengths with lambda ="
        f" {c.MU_ARRIVAL_RATE_MIN[lam]}\min"
    )
    maxx = maxq + 1

    if not isinstance(ax, np.ndarray):
        ax = [ax]

    for q in range(c.N_QUEUES):
        ql = results.get_statistics_separate(lam, q)["QueueLength_hist"]
        ax[q].set_title(f"Queue {q}")
        ax[q].bar(range(0, maxx), ql[0:maxx])
        ax[q].set_ylabel("P(Q = k)")
        ax[q].set_xlabel("k")
    plt.savefig(os.path.join(path, "hist_queue_length_per_queue.png"), dpi=300)
    if show:
        plt.show()
    plt.close()


def plot_hist_wait_t_all(results, lam, path: str, binwidth=10, show=False):
    """
    Plots histogram of waiting times for all queues together

    :param results: SimResults object
    :param lam: index of rate parameter
    :param path: path to save figure
    :param binwidth: width of bins in histogram
    """
    plt.figure()

    sns.histplot(
        results.get_statistics_all(lam)["WaitingTime_all"],
        kde=False,
        bins=int(180 / binwidth),  # type: ignore
        color="red",
    )

    plt.title(f"Waiting times with lambda = {c.MU_ARRIVAL_RATE_MIN[lam]}\min")
    plt.xlabel("Waiting time (s)")
    plt.ylabel("Count")
    plt.savefig(os.path.join(path, "hist_wait_t_all.png"), dpi=300)
    if show:
        plt.show()
    plt.close()


def plot_hist_wait_t_per_queue(results, lam, path: str, binwidth, show=False):
    """
    Plots histogram of waiting times for queues in separate subplots

    :param results: SimResults object
    :param lam: index of rate parameter
    :param path: path to save figure
    :param binwidth: width of bins in histogram
    """
    fig, ax = plt.subplots(c.N_QUEUES, 1)
    fig.suptitle(
        f"Waiting times with lambda = {c.MU_ARRIVAL_RATE_MIN[lam]}\min"
    )

    if not isinstance(ax, np.ndarray):
        ax = [ax]
        
    for q in range(c.N_QUEUES):
        wt = results.get_statistics_separate(lam, q)["WaitingTime_all"]
        ax[q].set_title(f"Queue {q}")
        sns.histplot(wt, ax=ax[q], bins=int(180 / binwidth), color="red")  # type: ignore
        ax[q].set_ylabel("Count")
        ax[q].set_xlabel("Waiting time (s)")

    plt.savefig(os.path.join(path, "hist_cust_wait_t_per_queue.png"), dpi=300)
    if show:
        plt.show()
    plt.close()


def plot_hist_cust_in_cant(results, lam, path: str, binwidth, show=False):
    """
    Plots histogram of number of customers present in canteen

    :param results: SimResults object
    :param lam: index of rate parameter
    :param path: path to save figure
    :param bindwidth: width of bins in histogram
    """

    plt.figure()

    sns.histplot(
        results.get_statistics_all(lam)["CustomersCanteen_all"],
        kde=False,
        bins=int(180 / binwidth),  # type: ignore
        color="red",
    )

    plt.title(
        "Number of customers in canteen with lambda ="
        f" {c.MU_ARRIVAL_RATE_MIN[lam]}\min"
    )
    plt.xlabel("Number of customers")
    plt.ylabel("Count")
    plt.savefig(os.path.join(path, "hist_cust_in_cant.png"), dpi=300)
    if show:
        plt.show()
    plt.close()


def plot_hist_CC_vs_time(results, lam, path: str, time_interval, show=False):
    """
    Plots scatter plot (after applying moving average) of number of customers
    in canteen versus time

    :param results: SimResults object
    :param lam: index of rate parameter
    :param path: path to save figure
    :time_interval: time interval used to calculate average of all values within
        this time interval
    """
    plt.figure()
    stats = results.get_statistics_all(lam)
    plot_time, plot_data = get_average(
        stats["CustomersCanteen_times"],
        stats["CustomersCanteen_values"],
        time_interval,
    )  # type: ignore

    plt.scatter(plot_time, plot_data)  # type: ignore
    plt.xlabel("Time (s)")
    plt.ylabel("Customers in canteen")
    plt.title(
        "Number of customers in canteen over time with lambda ="
        f" {c.MU_ARRIVAL_RATE_MIN[lam]}\min"
    )
    plt.savefig(os.path.join(path, "hist_cc_time.png"), dpi=300)
    if show:
        plt.show()
    plt.close()


def get_average(times, values, time_interval):
    """
    Helper function of plot_hist_CC_vs_time

    :param times, values: contains x (time) and y values for plot
    :time_interval: time interval used to calculate average of all values within
        this time interval

    :returns: x (time) and y values after applying this method similar to a
        moving average
    """

    minT = min(times)
    maxT = max(times)
    steps = (maxT - minT) // time_interval
    stepsize = int(len(times) // steps)

    plot_time = deque()
    plot_data = deque()

    currentT = 0
    for ind1 in range(0, len(times), stepsize):
        ind2 = int(ind1 + stepsize)
        plot_time.append((2 * currentT + time_interval) / 2)

        if ind2 < len(times):
            plot_data.append(np.mean(slice_deque(values, ind1, ind2, 1)))
            currentT = times[ind2]
        else:
            plot_data.append(np.mean(slice_deque(values, ind1, len(times), 1)))
            return plot_time, plot_data


def slice_deque(d, start, stop, step):
    """Helper function to slice deques"""
    d.rotate(-start)
    slice = list(itertools.islice(d, 0, stop - start, step))
    d.rotate(start)
    return slice
