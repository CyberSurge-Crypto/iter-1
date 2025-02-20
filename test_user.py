import pytest
from user import User
from transaction import Transaction
from cryptography.hazmat.primitives import serialization

@pytest.fixture
def user():
    return User("test_user")

@pytest.fixture
def second_user():
    return User("test_user_2")

class TestUser:
    def test_user_creation(self, user):
        """Test if user is created with correct initial values"""
        assert user.user_id == "test_user"
        assert user.balance == 0
        assert user.public_key is not None
        assert len(user.public_key) > 0

    def test_get_public_key(self, user):
        """Test if public key is returned correctly"""
        public_key = user.get_public_key()
        assert isinstance(public_key, str)
        assert public_key == user.public_key

    def test_verify_keys(self, user):
        """Test key verification"""
        # Get private key in PEM format
        private_key_pem = user._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Verify with correct private key
        assert user.verify_keys(private_key_pem) == True
        
        # Verify with incorrect private key (create new user for different key pair)
        other_user = User("other")
        other_private_key = other_user._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        assert user.verify_keys(other_private_key) == False

    @pytest.mark.asyncio
    async def test_start_transaction_insufficient_balance(self, user, second_user):
        """Test transaction creation with insufficient balance"""
        transaction = await user.start_transaction(second_user.public_key, 100)
        assert transaction is None

    @pytest.mark.asyncio
    async def test_start_transaction_sufficient_balance(self, user, second_user):
        """Test transaction creation with sufficient balance"""
        # Manually set balance for testing
        user.balance = 1000
        
        transaction = await user.start_transaction(second_user.public_key, 100)
        assert transaction is not None
        assert isinstance(transaction, Transaction)
        assert transaction.sender == user.public_key
        assert transaction.receiver == second_user.public_key
        assert transaction.amount == 100 