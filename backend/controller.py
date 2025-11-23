# controller.py
from fastapi import APIRouter, HTTPException
from models import (
    TransferRequest, BalanceResponse, SwapRequest, SwapResponse,
    BatchTransferRequest, BatchTransferResponse, TransactionVerification, VerifyRequest
)
import service
from consensus import consensus_manager

router = APIRouter(prefix="/api", tags=["token"])

@router.get("/balance/{address}", response_model=BalanceResponse)
def balance(address: str, token_address: str = None):
    try:
        return service.get_balance(address, token_address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/total-supply")
def total_supply():
    try:
        return {"total_supply": service.get_total_supply()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/transfer/")
def transfer(req: TransferRequest):
    try:
        tx_hash = service.transfer(req.to, req.amount)
        return {"tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/swap", response_model=SwapResponse)
async def swap(req: SwapRequest):
    try:
        result = service.swap_tokens(req.token_in, req.token_out, req.amount_in)
        return SwapResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/swap/quote")
def get_swap_quote(token_in: str, token_out: str, amount_in: float):
    try:
        amount_out = service.get_swap_quote(token_in, token_out, amount_in)
        return {"amount_out": amount_out, "token_in": token_in, "token_out": token_out}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/batch-transfer", response_model=BatchTransferResponse)
async def batch_transfer(req: BatchTransferRequest):
    try:
        transactions = [{"to": tx.to, "amount": tx.amount} for tx in req.transactions]
        result = await service.batch_transfer_parallel(transactions)
        return BatchTransferResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify/{tx_hash}")
def verify_transaction(tx_hash: str, req: VerifyRequest):
    try:
        result = consensus_manager.verify_transaction(tx_hash, req.verifier_address)
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Verification failed"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/verify/{tx_hash}", response_model=TransactionVerification)
def get_transaction_status(tx_hash: str):
    try:
        status = consensus_manager.get_transaction_status(tx_hash)
        if not status:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return TransactionVerification(
            tx_hash=status["tx_hash"],
            verified=status["consensus_reached"],
            verifiers=status["verifiers"],
            consensus_reached=status["consensus_reached"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/consensus/add-verifier")
def add_verifier(address: str):
    try:
        consensus_manager.add_verifier(address)
        return {"success": True, "message": f"Verifier {address} added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/consensus/verifiers")
def get_verifiers():
    try:
        return {"verifiers": list(consensus_manager.verifiers)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
