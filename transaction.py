import hashlib
from constant import TransactionState
from datetime import datetime
# from chain import BlockChain
# from user import User

# 新区块：验证没有以前发过的交易
# txn-ID: sender + receiver + time（交易本身产生）

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int) -> None:
        time = datetime.now()
        self.transaction_id = sender + receiver + str(time) + amount
        self.timestamp = time
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.state = TransactionState.STARTED
        self.signature = None

## methods moved to the BlockChain class

    # let the user sign the transaction
    def sign(self, priv_key: str):
        signature = create_signature(self, priv_key)
        self.signature = signature
        return

    # verify the signature is from the sender
    def verify(self):
        if (self.signature is None or self.sender is None):
            return False
        elif (self.signature == verify_signature(self, self.sender)):
            return True
        return False

    # validate that the sender has enough balance
    def validate(self):
        if (self.sender is None):
            return False
        return BlockChain.get_balance(self.sender) >= self.amount
    
    # called by validator nodes
    def double_authenticate(self):
        if self.verify() and self.validate():
            self.state = TransactionState.SIGNED
            return
        else:
            self.state = TransactionState.FAILED
            return
    
    # called by the miner
    def first_confirm(self, txn_id):
        self.state = TransactionState.FIRST_CONFIRMED
        self.transaction_id = txn_id # delete
        return

    # called by the miner that mined the 6th block since the txn
    def fully_confirm(self):
        self.state = TransactionState.FULLY_CONFIRMED
        return

    # called by the miner of the txn block (after finding this block rollbacked)
    def cancel(self):
        self.state = TransactionState.CANCELED
        return

    def __str__(self):
        return str(str(self.transaction_id)) + " " + str(self.timestamp) + " " + str(self.sender) + " " + str(self.receiver) + " " + str(self.amount) + " " + str(self.state)
    
    def __dict__(self):
        return {
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "state": self.state
        }
    
## from Copilot-GPT4o
def create_signature(txn, private_key):
    message = f"{txn.sender}{txn.receiver}{txn.amount}{txn.timestamp}"
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    signature = private_key.sign(message_hash)
    return signature

## from Copilot-GPT4o
def verify_signature(txn, public_key):
    message = f"{txn.sender}{txn.receiver}{txn.amount}{txn.timestamp}"
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    return public_key.verify(txn.signature, message_hash)