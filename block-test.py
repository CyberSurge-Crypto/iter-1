import time
from block import Block  # Ensure your Block class is in a file named 'block.py'

# Dummy transaction class for testing
class DummyTransaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

def test_compute_hash():
    # Test with one transaction.
    transactions = [DummyTransaction("Alice", "Bob", 10)]
    block = Block(index=1, transactions=transactions, timestamp=time.time(), previous_hash="0")
    
    computed_hash = block.compute_hash()
    print("Computed hash:", computed_hash)
    
    # Verify that the computed hash is a 64-character hexadecimal string.
    assert isinstance(computed_hash, str), "Hash should be a string."
    assert len(computed_hash) == 64, "Hash should be 64 characters long."

def test_mine_block():
    # Test mining a block with one transaction.
    transactions = [DummyTransaction("Alice", "Bob", 10)]
    block = Block(index=1, transactions=transactions, timestamp=time.time(), previous_hash="0")
    
    difficulty = 2
    print("Mining block with difficulty:", difficulty)
    block.mine(difficulty)
    print("Mined block hash:", block.hash)
    
    # Verify that the block's hash starts with the required number of zeros.
    assert block.hash.startswith("0" * difficulty), (
        f"Block hash {block.hash} does not meet the difficulty requirement."
    )

def test_zero_transactions_validation():
    # Test that creating a block with zero transactions raises a ValueError.
    transactions = []  # Empty list of transactions.
    try:
        block = Block(index=2, transactions=transactions, timestamp=time.time(), previous_hash="0")
        # If block creation succeeds, that is an error.
        assert False, "Expected ValueError when creating a block with zero transactions."
    except ValueError as e:
        print("Caught expected ValueError:", e)

def test_multiple_transactions():
    # Test a block with multiple transactions.
    transactions = [
        DummyTransaction("Alice", "Bob", 10),
        DummyTransaction("Bob", "Charlie", 5),
        DummyTransaction("Charlie", "Dave", 2)
    ]
    block = Block(index=3, transactions=transactions, timestamp=time.time(), previous_hash="0")
    
    print("Block with multiple transactions computed hash:", block.hash)
    assert isinstance(block.hash, str), "Hash should be a string with multiple transactions."
    
    # Test mining with multiple transactions.
    difficulty = 2
    block.mine(difficulty)
    print("Mined block with multiple transactions hash:", block.hash)
    assert block.hash.startswith("0" * difficulty), (
        "Block hash does not meet the difficulty requirement for multiple transactions."
    )

def main():
    print("Starting block tests...\n")
    
    print("Testing compute_hash()")
    test_compute_hash()
    print("compute_hash() test passed!\n")
    
    print("Testing mine()")
    test_mine_block()
    print("mine() test passed!\n")
    
    print("Testing block with zero transactions validation")
    test_zero_transactions_validation()
    print("Zero transactions validation test passed!\n")
    
    print("Testing block with multiple transactions")
    test_multiple_transactions()
    print("Multiple transactions test passed!\n")
    
    print("All tests passed!")

if __name__ == "__main__":
    main()
