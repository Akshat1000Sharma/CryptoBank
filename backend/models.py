from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class TransferRequest(BaseModel):
    to: str = Field(..., description="Recipient address (0x...)")
    amount: float = Field(..., description="Amount in token units (not wei)")

class BalanceResponse(BaseModel):
    address: str
    balance: float

class SwapRequest(BaseModel):
    token_in: str = Field(..., description="Token address to swap from")
    token_out: str = Field(..., description="Token address to swap to")
    amount_in: float = Field(..., description="Amount of token_in to swap")

class SwapResponse(BaseModel):
    tx_hash: str
    amount_out: float

class BatchTransferRequest(BaseModel):
    transactions: List[TransferRequest] = Field(..., description="List of transfer transactions")

class BatchTransferResponse(BaseModel):
    tx_hashes: List[str]
    status: str
    verified: bool

class TransactionVerification(BaseModel):
    tx_hash: str
    verified: bool
    verifiers: List[str]
    consensus_reached: bool

class VerifyRequest(BaseModel):
    verifier_address: str = Field(..., description="Address of the verifier")

class PerformanceMetrics(BaseModel):
    execution_time_seconds: float
    successful_count: int
    failed_count: int
    total_count: int
    success_rate: float
    average_time_per_tx: float
    tx_hashes: List[str]

class PerformanceComparisonResponse(BaseModel):
    concurrent_execution: PerformanceMetrics
    sequential_execution: PerformanceMetrics
    improvement_percentage: float
    speedup_factor: float
    test_configuration: Dict
