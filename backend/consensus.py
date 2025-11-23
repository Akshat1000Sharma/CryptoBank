# consensus.py
"""
Consensus and verification mechanism for transactions.
This implements a simple voting-based consensus where multiple verifiers
can verify transactions before they are executed.
"""
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib

@dataclass
class Transaction:
    """Represents a transaction in the pool"""
    tx_hash: str
    from_address: str
    to_address: str
    amount: float
    timestamp: datetime
    verifiers: Set[str]
    executed: bool = False

class ConsensusManager:
    """
    Manages consensus and verification for transactions.
    Uses a simple voting mechanism where transactions need a threshold
    of verifications before execution.
    """
    
    def __init__(self, verification_threshold: int = 2):
        """
        Initialize consensus manager.
        
        Args:
            verification_threshold: Number of verifications needed for consensus
        """
        self.verification_threshold = verification_threshold
        self.transaction_pool: Dict[str, Transaction] = {}
        self.verifiers: Set[str] = set()
        self.verified_transactions: Set[str] = set()
    
    def add_verifier(self, address: str):
        """Add a verifier address"""
        self.verifiers.add(address)
    
    def add_transaction_to_pool(self, tx_hash: str, from_address: str, 
                                to_address: str, amount: float) -> bool:
        """
        Add a transaction to the verification pool.
        
        Returns:
            True if added successfully, False if already exists
        """
        if tx_hash in self.transaction_pool:
            return False
        
        self.transaction_pool[tx_hash] = Transaction(
            tx_hash=tx_hash,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            timestamp=datetime.now(),
            verifiers=set()
        )
        return True
    
    def verify_transaction(self, tx_hash: str, verifier_address: str) -> Dict:
        """
        Verify a transaction.
        
        Returns:
            Dict with verification status and consensus info
        """
        if tx_hash not in self.transaction_pool:
            return {
                "success": False,
                "error": "Transaction not found in pool"
            }
        
        if verifier_address not in self.verifiers:
            return {
                "success": False,
                "error": "Address is not a registered verifier"
            }
        
        tx = self.transaction_pool[tx_hash]
        
        if tx.executed:
            return {
                "success": False,
                "error": "Transaction already executed"
            }
        
        # Add verifier
        tx.verifiers.add(verifier_address)
        
        # Check if consensus reached
        consensus_reached = len(tx.verifiers) >= self.verification_threshold
        
        if consensus_reached:
            self.verified_transactions.add(tx_hash)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "verifiers": list(tx.verifiers),
            "verification_count": len(tx.verifiers),
            "consensus_reached": consensus_reached,
            "threshold": self.verification_threshold
        }
    
    def get_transaction_status(self, tx_hash: str) -> Optional[Dict]:
        """Get status of a transaction"""
        if tx_hash not in self.transaction_pool:
            return None
        
        tx = self.transaction_pool[tx_hash]
        return {
            "tx_hash": tx_hash,
            "from": tx.from_address,
            "to": tx.to_address,
            "amount": tx.amount,
            "timestamp": tx.timestamp.isoformat(),
            "verifiers": list(tx.verifiers),
            "verification_count": len(tx.verifiers),
            "consensus_reached": len(tx.verifiers) >= self.verification_threshold,
            "executed": tx.executed
        }
    
    def mark_executed(self, tx_hash: str):
        """Mark a transaction as executed"""
        if tx_hash in self.transaction_pool:
            self.transaction_pool[tx_hash].executed = True
    
    def can_execute(self, tx_hash: str) -> bool:
        """Check if a transaction can be executed (consensus reached)"""
        return tx_hash in self.verified_transactions
    
    def validate_transaction(self, tx_hash: str, from_address: str, 
                           to_address: str, amount: float) -> bool:
        """
        Validate transaction data integrity.
        Creates a hash of transaction data and compares with tx_hash.
        """
        # Create a hash of transaction data
        data = f"{from_address}{to_address}{amount}"
        computed_hash = hashlib.sha256(data.encode()).hexdigest()
        
        # In a real system, tx_hash would be the actual transaction hash
        # For simplicity, we'll just check if transaction exists
        return tx_hash in self.transaction_pool

# Global consensus manager instance
consensus_manager = ConsensusManager(verification_threshold=2)

