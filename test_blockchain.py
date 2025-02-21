import unittest
import time
from blockchain import Blockchain
from user import User
from transaction import Transaction
from block import Block

class TestBlockchainFramework(unittest.TestCase):
    def setUp(self):
        """Setup the blockchain and users before each test"""
        self.blockchain = Blockchain()
        self.user1 = User()
        self.user2 = User()

        self.blockchain.register_user(self.user1)
        self.blockchain.register_user(self.user2)

        # Give some initial balance
        self.user1.balance = 100

    def test_create_users(self):
        """Test if users are created and registered properly"""
        self.assertIn(self.user1.get_address(), self.blockchain.user_registry)
        self.assertIn(self.user2.get_address(), self.blockchain.user_registry)

    def test_transaction_creation(self):
        """Test if a transaction is created properly"""
        tx = self.user1.start_transaction(self.user2.get_address(), 50)
        self.assertIsNotNone(tx)
        self.assertEqual(tx.sender, self.user1.get_address())
        self.assertEqual(tx.receiver, self.user2.get_address())
        self.assertEqual(tx.amount, 50)

    def test_transaction_signature(self):
        """Test if a transaction is properly signed and verified"""
        tx = self.user1.start_transaction(self.user2.get_address(), 20)
        self.assertTrue(self.user1.verify_transaction(tx))

    def test_add_transaction_to_mempool(self):
        """Test adding a valid transaction to the pending transactions"""
        tx = self.user1.start_transaction(self.user2.get_address(), 30)
        self.blockchain.pending_transactions.append(tx)
        self.assertIn(tx, self.blockchain.pending_transactions)

    def test_mining_block(self):
        """Test mining a block and adding it to the chain"""
        tx = self.user1.start_transaction(self.user2.get_address(), 25)
        self.blockchain.pending_transactions.append(tx)
        
        # Mine block
        new_block = Block(
            index=len(self.blockchain.chain),
            transactions=self.blockchain.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.blockchain.get_last_block().hash
        )
        new_block.mine(difficulty=2)  # Assuming difficulty is 2
        self.blockchain.add_block(new_block)

        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(new_block.previous_hash, self.blockchain.chain[-2].hash)
        print("pass test_mining_block")

    def test_balance_update_after_transaction(self):
        """Test if the balance updates correctly after transactions"""
        tx = self.user1.start_transaction(self.user2.get_address(), 40)
        self.blockchain.pending_transactions.append(tx)

        # Mine the transaction into a block
        new_block = Block(
            index=len(self.blockchain.chain),
            transactions=self.blockchain.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.blockchain.get_last_block().hash
        )
        new_block.mine(difficulty=2)
        self.blockchain.add_block(new_block)
        # Check balances after the transaction
        self.assertEqual(self.blockchain.get_balance(self.user1.get_address()), 60)
        self.assertEqual(self.blockchain.get_balance(self.user2.get_address()), 40)

    def test_block_validation(self):
        """Test if block validation works correctly"""
        tx = self.user1.start_transaction(self.user2.get_address(), 15)
        self.blockchain.pending_transactions.append(tx)

        new_block = Block(
            index=len(self.blockchain.chain),
            transactions=self.blockchain.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.blockchain.get_last_block().hash
        )
        new_block.mine(difficulty=2)
        self.assertTrue(self.blockchain.validate_block(new_block))

if __name__ == '__main__':
    unittest.main()
