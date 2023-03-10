import logging
import numpy as np

import assignment_2.customer as Customer

logger = logging.getLogger(__name__)


class Group:
    def __init__(
        self,
        n_customers: int,
        use_cash: np.ndarray,
        t_arr: float,
        t_grab_food: np.ndarray,
    ):
        """
        Creates a new group of customers.

        :param n_customers: The number of customers in the group.
        :param use_cash: A list of booleans indicating whether the customer uses cash or not.
        :param t_arr: The time the group arrived.
        :param t_grab_food: A list of times the customers need to grab their food. (counting up from t_arr)
        """
        self.logstr = {"className": self.__class__.__name__}
        self.t_arrival = t_arr
        self.n_customers = n_customers
        self.t_departure = -1
        self.cust_in_canteen = {x: True for x in range(n_customers)}

        if t_grab_food.size != n_customers or use_cash.size != n_customers:
            raise ValueError(
                f"Nr of customers: {n_customers} does not match the size of"
                f" t_grab_food: {t_grab_food.size} or use_cash:"
                f" {use_cash.size}"
            )

        # list of customers
        self.customers = np.empty(n_customers, dtype=Customer.Customer)

        # if it is a single customer we need to make it an array
        if not isinstance(use_cash, np.ndarray):
            use_cash = np.array([use_cash])
            t_grab_food = np.array([t_grab_food])

        for idx, use_cash_cust in enumerate(use_cash):
            # check if t_grab_food is larger than t_arr
            if t_grab_food[idx] <= t_arr:
                raise ValueError("t_grab_food <= t_arr")

            # create customer
            self.customers[idx] = Customer.Customer(
                t_arr=t_arr,
                t_grab_food=t_grab_food[idx],
                cash=bool(use_cash_cust),
                uniq_group_id=idx,
            )

    def __str__(self):
        return (
            "Group at: "
            + str(self.t_arrival)  # noqa: W503
            + " with N: "  # noqa: W503
        )
    
    def group_in_canteen(self):
        """
        Checks whether every customer in this group has left canteen 
        
        :returns: Boolean if group is still in canteen 
        """
        uniq_group_id = 0
        while uniq_group_id < self.n_customers:
            customer = self.cust_in_canteen[uniq_group_id]
            
            # check if customer is still in canteen (t_left = -1)
            if customer and self.customers[uniq_group_id].get_t_left() != -1:
                self.cust_in_canteen[uniq_group_id] = False 
                
            if np.sum(np.array(list(self.cust_in_canteen.values()))) == 0:
                return False 
            
            uniq_group_id += 1
            
        return True 
    
    def set_t_departure(self, t):
        self.t_departure= t

    def get_customers(self):
        return self.customers

    def get_nr_customers(self):
        return self.n_customers
    
    def get_t_arrival(self):
        return self.t_arrival

    def get_t_departure(self):
        return self.t_departure