import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from transaction_state import TransactionState
from datetime import datetime
# from chain import BlockChain
# from user import User

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int) -> None:
        self.transaction_id = None
        self.timestamp = datetime.now()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.state = TransactionState.STARTED
        self.signature = None

    # let the user sign the transaction
    async def sign(self):
        priv_key = input("Type your private key to sign the transaction: ")
        user = User.get_user(self.sender)
        if user.verify_key(priv_key):
            signature = create_signature(self, priv_key)
            self.signature = signature
            return True
        else:
            return False

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
        self.transaction_id = txn_id
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