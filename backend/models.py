from pydantic import BaseModel, Field

class TransferRequest(BaseModel):
    to: str = Field(..., description="Recipient address (0x...)")
    amount: float = Field(..., description="Amount in token units (not wei)")

class BalanceResponse(BaseModel):
    address: str
    balance: float
