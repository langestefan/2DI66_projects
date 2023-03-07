from assignment_2.customer import Customer


class Event:
    ARRIVAL = 0
    DEPARTURE = 1

    def __init__(self, typ: int, time: float, cust: Customer):
        """_summary_

        :param: typ: Event type (arrival or departure)
        :param: time: Time of event
        :param: cust: Customer number
        """
        self.logstr = {"className": self.__class__.__name__}
        self.type = typ
        self.time = time
        self.customer = cust  # especially needed if there are multiple servers

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        s = ("Arrival", "Departure")
        return (
            s[self.type]
            + " of customer "  # noqa: W503
            + str(self.customer)  # noqa: W503
            + " at t = "  # noqa: W503
            + str(round(self.time, 3))  # noqa: W503
        )

    def get_customer(self):
        """
        Returns the customer associated with this event.
        """
        return self.customer
