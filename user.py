from typing import Dict, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from transaction import Transaction
import hashlib

class User:
    _users: Dict[str, 'User'] = {}  # Class variable to store all users

    def __init__(self):
        # Get private and public key
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self._public_key = self._private_key.public_key()
        
        # Generate address from public key
        public_key_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.address = self._generate_address(public_key_bytes)
        self.balance = 0

        # Add user to class variable
        User._users[self.address] = self

    def _generate_address(self, public_key_bytes: bytes) -> str:
        """Generate an address from public key"""
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        # Return last 40 chars of hex string (similar to ETH address format)
        return '0x' + ripemd160_hash.hex()[:40]

    def get_address(self) -> str:
        """Return the user's address"""
        return self.address

    def get_public_key(self) -> str:
        """Return the user's public key as hex string"""
        return self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()

    def start_transaction(self, receiver_address: str, amount: int) -> Optional[Transaction]:
        """
        Start a new transaction if user has sufficient balance
        Args:
            receiver_address: Receiver's blockchain address
            amount: Amount to transfer
        Returns:
            Transaction object if successful, None otherwise
        """
        if self.balance >= amount:
            transaction = Transaction(self.address, receiver_address, amount)
            self.sign_transaction(transaction)
            return transaction
        return None

    def sign_transaction(self, transaction: Transaction) -> None:
        """Sign a transaction with the user's private key"""
        txn_message = f"{transaction.sender}{transaction.receiver}{transaction.amount}{transaction.timestamp}"
        signature = self._private_key.sign(
            txn_message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        transaction.signature = signature.hex()
    
    def broadcast_transaction(self, transaction: Transaction) -> None:
        """Broadcast a transaction to the network"""
        # TODO: Implement broadcasting
        pass