# user.py
from typing import Dict, Optional
import hashlib
import secrets

class User:
    _users: Dict[str, 'User'] = {}  # Class variable to store all users

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.public_key = self._generate_public_key()
        self.private_key = self._generate_private_key()
        self.balance = 0
        User._users[self.public_key] = self

    def _generate_public_key(self) -> str:
        """Generate a public key based on user_id"""
        random_seed = secrets.token_hex(16)
        return hashlib.sha256(f"{self.user_id}{random_seed}".encode()).hexdigest()

    def _generate_private_key(self) -> str:
        """Generate a private key paired with the public key"""
        return hashlib.sha256(f"{self.public_key}secret".encode()).hexdigest()

    def get_public_key(self) -> str:
        return self.public_key

    def verify_keys(self, private_key: str) -> bool:
        """Verify if the provided private key matches the user's private key"""
        return private_key == self.private_key

    async def start_transaction(self, receiver: str, amount: int) -> Optional['Transaction']:
        """Start a new transaction"""
        from transaction import Transaction
        if self.balance >= amount:
            transaction = Transaction(self.public_key, receiver, amount)
            return transaction
        return None

    @classmethod
    def get_user(cls, public_key: str) -> Optional['User']:
        """Get a user by their public key"""
        return cls._users.get(public_key)