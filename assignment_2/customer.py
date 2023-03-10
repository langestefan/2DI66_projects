import logging
import scipy.stats as stats
from dist.distribution import Distribution

import assignment_2.constants as c


logger = logging.getLogger(__name__)


class Customer:
    def __init__(
        self, t_arr: float, t_grab_food: float, cash: bool, uniq_group_id: int
    ):
        """
        Creates a new customer.

        :param t_arr: The time the customer arrived.
        :param t_grab_food: The time the customer needs to grab their food.
        :param cash: Whether the customer uses cash to pay. If False, the
                     customer uses a bank card.
        :param uniq_group_id: Unique group ID of the customer.
        """
        self.logstr = {"className": self.__class__.__name__}
        self.use_cash = cash
        self.t_arrival_group = t_arr
        self.t_grab_food = t_grab_food
        self.t_left = -1 # time customer left canteen 
        self.queue_id = -1 
        self.uniq_group_id = uniq_group_id

        # make sure t_grab_food > t_arrival_group
        if t_grab_food <= t_arr:
            raise ValueError("t_grab_food <= t_arr")

    def __str__(self):
        return (
            f"Customer: t_arr: {round(self.t_arrival_group, 3)}, t_grab_food:"
            f" {round(self.t_grab_food, 3)}, cash: {bool(self.use_cash)}"
            f", queue_id: {self.queue_id}, uniq_group_id: {self.uniq_group_id}"
        )

    def get_t_done_grab(self):
        """
        Returns the time the customer is done grabbing their food.

        :return: Time stamp of done grabbing food.
        """
        return self.t_grab_food
    
    def get_t_arrival(self):
        """
        Returns the time customer entered canteen 

        :return: Time stamp of customer entering canteen.
        """
        return self.t_arrival_group

    def get_uses_cash(self):
        """
        Returns whether the customer uses cash to pay.

        :return: True if the customer uses cash, False otherwise.
        """
        return self.use_cash
    
    def get_t_left(self):
        """
        Returns time customer left canteen (t = -1 if customer is still in canteen)

        :return: Time customer left canteen 
        """
        return self.t_left
    
    def set_t_left(self, t):
        """
        Sets time stamp of when customer left canteen 
        
        :param t: Time at which customer left canteen 
        """
        if t < self.get_t_done_grab():
            raise ValueError("Departure time is earalier than arrival time")
        self.t_left = t
        
    def set_queue_id(self, queue_id: int):
        """
        Sets the queue id of the customer.

        :param queue_id: Assigned queue id.
        """
        if queue_id < 0:
            raise ValueError("queue_id must be >= 0")
        self.queue_id = queue_id

    def get_queue_id(self):
        """
        Returns the queue id of the customer.

        :return: Queue id customer is assigned to.
        """
        if self.queue_id < 0:
            raise ValueError("queue_id was never set!")
        return self.queue_id
