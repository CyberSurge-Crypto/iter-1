# create an enum for the state of a transaction
from enum import Enum

DIFFICULTY = 2

class TransactionState(Enum):
    STARTED = 'started'
    SIGNED = 'signed'
    PENDING = 'pending'
    FIRST_CONFIRMED = 'first_confirmed'
    FULLY_CONFIRMED = 'fully_confirmed'
    CANCELED = 'canceled'
    FAILED = 'failed'