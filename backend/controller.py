# controller.py
from fastapi import APIRouter, HTTPException
from models import TransferRequest, BalanceResponse
import service

router = APIRouter(prefix="/api", tags=["token"])

@router.get("/balance/{address}", response_model=BalanceResponse)
def balance(address: str):
    try:
        return service.get_balance(address)
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
        # For security, you might not want to return raw exception messages in production
        raise HTTPException(status_code=400, detail=str(e))
