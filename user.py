from typing import Dict, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from transaction import Transaction

class User:
    _users: Dict[str, 'User'] = {}  # Class variable to store all users

    def __init__(self, user_id: str):
        self.user_id = user_id
        # Generate RSA key pair
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self._private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()
        self.balance = 0
        User._users[self.public_key] = self

    def get_public_key(self) -> str:
        """Return the user's public key"""
        return self.public_key

    def verify_keys(self, test_private_key: bytes) -> bool:
        """
        Verify if a private key matches this user's public key pair
        Args:
            test_private_key: The private key to test in bytes format
        Returns:
            bool: True if the keys form a valid pair, False otherwise
        """
        try:
            # Create a test message
            test_message = b"Verification test message"
            
            # Sign with test private key
            test_key = serialization.load_pem_private_key(test_private_key, password=None)
            signature = test_key.sign(
                test_message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            # Verify with stored public key
            public_key = serialization.load_pem_public_key(
                bytes.fromhex(self.public_key)
            )
            
            # Attempt verification
            try:
                public_key.verify(
                    signature,
                    test_message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                return True
            except:
                return False
                
        except Exception:
            return False

    async def start_transaction(self, receiver: str, amount: int) -> Optional['Transaction']:
        """
        Start a new transaction if user has sufficient balance
        Args:
            receiver: Receiver's public key
            amount: Amount to transfer
        Returns:
            Transaction object if successful, None otherwise
        """
        if self.balance >= amount:
            transaction = Transaction(self.public_key, receiver, amount)
            return transaction
        return None