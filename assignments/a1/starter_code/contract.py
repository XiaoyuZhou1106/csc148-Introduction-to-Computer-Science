"""
CSC148, Winter 2019
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This is an abstract class. Only subclasses should be instantiated.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.datetime
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


# TODO: Implement the MTMContract, TermContract, and PrepaidContract
class TermContract(Contract):
    """The sub class of Contract.

    """
    end: datetime.datetime
    time: list

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        Contract.__init__(self, start)
        self.bill = None
        self.end = end
        self.time = []

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        if (month, year) not in self.time:
            self.bill = bill
            if month == self.start.month and year == self.start.year:
                self.bill.add_fixed_cost(TERM_DEPOSIT)
            self.time.append((month, year))
            self.bill.add_fixed_cost(TERM_MONTHLY_FEE)
            self.bill.set_rates('TERM', TERM_MINS_COST)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        new_cal = ceil(call.duration / 60.0)

        if self.bill.free_min < 100:
            if self.bill.free_min + new_cal > 100:
                self.bill.free_min = 100
                self.bill.add_billed_minutes(self.bill.free_min + new_cal - 100)
            else:
                self.bill.add_free_minutes(new_cal)
        else:
            self.bill.add_billed_minutes(new_cal)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        # self.start = None
        # if self.time[-1][1] > self.end.year:
        #     return self.bill.get_cost() - TERM_DEPOSIT
        # elif self.time[-1][1] == self.end.year:
        #     if self.time[-1][0] >= self.end.month:
        #         return self.bill.get_cost() - TERM_DEPOSIT
        #     elif self.time[-1][0] < self.end.month:
        #         return self.bill.get_cost()
        # else:
        #     return self.bill.get_cost()

        self.start = None
        if self.end.month < 12:
            end_time = (self.end.month + 1, self.end.year)
        else:
            end_time = (1, self.end.year + 1)

        if end_time in self.time:
            self.time = []
            return self.bill.get_cost() - TERM_DEPOSIT
        else:
            self.time = []
            return self.bill.get_cost()


class MTMContract(Contract):
    """The sub class of Contract.

    """
    time: list

    def __init__(self, start: datetime.date) -> None:
        Contract.__init__(self, start)
        self.bill = None
        self.time = []

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        if (month, year) not in self.time:
            self.time.append((month, year))
            self.bill = bill
            self.bill.add_fixed_cost(MTM_MONTHLY_FEE)
            self.bill.set_rates('MTM', MTM_MINS_COST)



class PrepaidContract(Contract):
    """The sub class of Contract.

    """
    time: list
    _balance: float

    def __init__(self, start: datetime.date, balance: int) -> None:
        Contract.__init__(self, start)
        self.bill = None
        self.time = []
        self._balance = 0 - balance


    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """

        if len(self.time) != 0:
            self._balance = self.bill.get_cost()
        self.time.append((month, year))
        self.bill = bill
        self.bill.set_rates('PREPAID', PREPAID_MINS_COST)
        if self._balance > -10:
            self._balance = self._balance - 25
        self.bill.add_fixed_cost(self._balance)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))
        self._balance += ceil(call.duration / 60.0) * PREPAID_MINS_COST

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        if self.bill.get_cost() <= 0:
            self.start = None
            return 0.0
        else:
            self.start = None
            return self.bill.get_cost()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
