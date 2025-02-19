# create an enum for the state of a transaction
from enum import Enum

class TransactionState(Enum):
    STARTED = 'started'
    SIGNED = 'signed'
    PENDING = 'pending'
    FIRST_CONFIRMED = 'first_confirmed'
    FULLY_CONFIRMED = 'fully_confirmed'
    CANCELED = 'canceled'
    FAILED = 'failed'
