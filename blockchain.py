# blockchain.py
from typing import List, Optional
from block import Block
from user import User
from transaction import Transaction
from constant import TransactionState
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

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

    def register_user(self) -> User:
        """Register a new user in the blockchain"""
        user = User()
        self.users.append(user)
        return user

    def get_balance(self, address: str) -> int:
        """Get the balance of a user by their address"""
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
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
        """Verify that the signature is valid for this transaction"""
        if transaction.signature is None or transaction.sender is None:
            return False
        
        try:
            # Reconstruct the message that was signed
            txn_message = f"{transaction.sender}{transaction.receiver}{transaction.amount}{transaction.timestamp}".encode()
            
            # Get the public key from transaction sender (you'll need to maintain a mapping of addresses to public keys)
            # This is simplified - you'll need to implement proper key management
            public_key_hex = self.get_public_key_for_address(transaction.sender)
            if not public_key_hex:
                return False
            
            public_key = serialization.load_pem_public_key(bytes.fromhex(public_key_hex))
            
            # Verify signature
            public_key.verify(
                bytes.fromhex(transaction.signature),
                txn_message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
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

    def get_public_key_for_address(self, address: str) -> Optional[str]:
        """Get the public key for a given address"""
        user = next((user for user in self.users if user.address == address), None)
        return user.get_public_key() if user else None

    
