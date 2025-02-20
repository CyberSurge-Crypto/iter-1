# blockchain.py
from typing import List
from block import Block
from user import User
from transaction import Transaction
from consensus import verify_signature
from constant import TransactionState
import time

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.users: List[User] = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Create the genesis block of the blockchain"""
        genesis_transaction = Transaction("genesis", "genesis", 0)
        genesis_block = Block(0, [genesis_transaction], time.time(), "0")
        self.chain.append(genesis_block)

    def register_user(self, user_id: str) -> User:
        """Register a new user in the blockchain"""
        user = User(user_id)
        self.users.append(user)
        return user

    def get_balance(self, public_key: str) -> int:
        """Get the balance of a user by their public key"""
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == public_key:
                    balance -= transaction.amount
                if transaction.receiver == public_key:
                    balance += transaction.amount
        return balance

    def get_last_block(self) -> Block:
        """Get the last block in the chain"""
        return self.chain[-1]

    def add_block(self, block: Block) -> bool:
        """Add a new block to the chain"""
        if self.is_chain_valid() and block.previous_hash == self.get_last_block().hash:
            self.chain.append(block)
            return True
        return False

    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verify hash
            if current_block.hash != current_block.compute_hash():
                return False

            # Verify chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False

            # Verify transactions
            for transaction in current_block.transactions:
                if not transaction.verify() or not transaction.validate():
                    return False

        return True
    
    """
    Below is the methods that interacts with transactions
    """
    def verify_transaction(self, transaction: Transaction) -> bool:
        """ Verify that the signature is from the sender in this transaction """
        if (transaction.signature is None or transaction.sender is None):
            return False
        elif (transaction.signature == verify_signature(transaction, transaction.sender)):
            return True
        return False

    def validate_transaction(self, transaction: Transaction) -> bool:
        """ Validate that the sender has enough balance for this transaction """
        if (transaction.sender is None):
            return False
        return self.get_balance(transaction, transaction.sender) >= transaction.amount
    
    def prove_transaction(self, transaction: Transaction) -> None:
        """Allow full-node users to prove the transaction (and notify the miners)"""
        if self.verify(transaction) and self.validate(transaction):
            transaction.state = TransactionState.SIGNED
        else:
            transaction.state = TransactionState.FAILED
        return

    
