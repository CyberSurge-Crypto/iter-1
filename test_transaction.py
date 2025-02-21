import unittest
from transaction import Transaction
from constant import TransactionState

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.sender = "sender_address"
        self.receiver = "receiver_address"
        self.amount = 100
        self.transaction = Transaction(self.sender, self.receiver, self.amount)

    def test_initialization(self):
        self.assertEqual(self.transaction.sender, self.sender)
        self.assertEqual(self.transaction.receiver, self.receiver)
        self.assertEqual(self.transaction.amount, self.amount)
        self.assertEqual(self.transaction.state, TransactionState.STARTED)
        self.assertIsNotNone(self.transaction.transaction_id)
        self.assertIsNotNone(self.transaction.timestamp)
        self.assertIsNone(self.transaction.signature)

    def test_str(self):
        expected_str = f"{self.transaction.transaction_id} {self.transaction.timestamp} {self.sender} {self.receiver} {self.amount} {self.transaction.state}"
        self.assertEqual(str(self.transaction), expected_str)

    def test_to_dict(self):
        transaction_dict = self.transaction.to_dict()
        self.assertEqual(transaction_dict["transaction_id"], self.transaction.transaction_id)
        self.assertEqual(transaction_dict["timestamp"], self.transaction.timestamp.isoformat())
        self.assertEqual(transaction_dict["sender"], self.sender)
        self.assertEqual(transaction_dict["receiver"], self.receiver)
        self.assertEqual(transaction_dict["amount"], self.amount)
        self.assertEqual(transaction_dict["state"], self.transaction.state.value)
        self.assertIsNone(transaction_dict["signature"])

if __name__ == '__main__':
    unittest.main()