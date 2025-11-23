from web3 import Web3
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional
from settings import w3, PUBLIC_ADDRESS, PRIVATE_KEY, CHAIN_ID
from contract_utils import contract, swap_contract, get_token_contract
from consensus import consensus_manager

def _get_decimals(token_address: str = None) -> int:
    """Get decimals for a token. If None, uses default contract."""
    if token_address:
        token_contract = get_token_contract(token_address)
        return token_contract.functions.decimals().call()
    return contract.functions.decimals().call()

def get_balance(address: str, token_address: str = None) -> dict:
    checksum = Web3.to_checksum_address(address)
    if token_address:
        token_contract = get_token_contract(token_address)
        bal_raw = token_contract.functions.balanceOf(checksum).call()
        decimals = _get_decimals(token_address)
    else:
        bal_raw = contract.functions.balanceOf(checksum).call()
        decimals = _get_decimals()
    return {"address": checksum, "balance": bal_raw / (10 ** decimals)}

def get_total_supply() -> float:
    supply_raw = contract.functions.totalSupply().call()
    decimals = _get_decimals()
    return supply_raw / (10 ** decimals)

def transfer(to: str, amount: float, token_address: str = None) -> str:
    """
    Build, sign and send a transfer transaction.
    `amount` is in token units (e.g., 1.5 tokens). This will convert to token base units.
    Returns the tx hash hex string.
    """
    to_checksum = Web3.to_checksum_address(to)
    
    # Use specified token contract or default
    if token_address:
        token_contract = get_token_contract(token_address)
        decimals = _get_decimals(token_address)
    else:
        token_contract = contract
        decimals = _get_decimals()
    
    amount_int = int(amount * (10 ** decimals))

    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)

    # Try to estimate gas; fall back to a safe default if estimate fails
    try:
        gas_estimate = token_contract.functions.transfer(to_checksum, amount_int).estimateGas({
            "from": PUBLIC_ADDRESS
        })
    except Exception:
        gas_estimate = 100000  # fallback

    gas_price = w3.eth.gas_price

    tx = token_contract.functions.transfer(to_checksum, amount_int).build_transaction({
        "chainId": CHAIN_ID,
        "gas": gas_estimate,
        "gasPrice": gas_price,
        "nonce": nonce,
        "from": PUBLIC_ADDRESS
    })

    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    
    # Add to consensus pool
    consensus_manager.add_transaction_to_pool(
        tx_hash.hex(), PUBLIC_ADDRESS, to_checksum, amount
    )
    
    return tx_hash.hex()

def swap_tokens(token_in: str, token_out: str, amount_in: float) -> Dict:
    """
    Swap tokens using the TokenSwap contract.
    Returns dict with tx_hash and amount_out.
    """
    if swap_contract is None:
        raise Exception("Swap contract not deployed. Please set SWAP_CONTRACT_ADDRESS in .env")
    
    token_in_checksum = Web3.to_checksum_address(token_in)
    token_out_checksum = Web3.to_checksum_address(token_out)
    
    # Get decimals for input token
    decimals_in = _get_decimals(token_in)
    amount_in_int = int(amount_in * (10 ** decimals_in))
    
    # Get quote first
    try:
        quote_raw = swap_contract.functions.getQuote(
            token_in_checksum, token_out_checksum, amount_in_int
        ).call()
        decimals_out = _get_decimals(token_out)
        amount_out = quote_raw / (10 ** decimals_out)
    except Exception as e:
        raise Exception(f"Failed to get quote: {str(e)}")
    
    # Approve swap contract to spend tokens (if needed)
    token_in_contract = get_token_contract(token_in)
    try:
        allowance = token_in_contract.functions.allowance(
            PUBLIC_ADDRESS, swap_contract.address
        ).call()
        if allowance < amount_in_int:
            # Approve
            nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
            approve_tx = token_in_contract.functions.approve(
                swap_contract.address, amount_in_int
            ).build_transaction({
                "chainId": CHAIN_ID,
                "gas": 100000,
                "gasPrice": w3.eth.gas_price,
                "nonce": nonce,
                "from": PUBLIC_ADDRESS
            })
            signed_approve = w3.eth.account.sign_transaction(approve_tx, PRIVATE_KEY)
            w3.eth.send_raw_transaction(signed_approve.raw_transaction)
    except Exception as e:
        raise Exception(f"Failed to approve tokens: {str(e)}")
    
    # Execute swap
    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    try:
        gas_estimate = swap_contract.functions.swap(
            token_in_checksum, token_out_checksum, amount_in_int
        ).estimateGas({"from": PUBLIC_ADDRESS})
    except Exception:
        gas_estimate = 200000
    
    swap_tx = swap_contract.functions.swap(
        token_in_checksum, token_out_checksum, amount_in_int
    ).build_transaction({
        "chainId": CHAIN_ID,
        "gas": gas_estimate,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "from": PUBLIC_ADDRESS
    })
    
    signed = w3.eth.account.sign_transaction(swap_tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    
    return {
        "tx_hash": tx_hash.hex(),
        "amount_out": amount_out
    }

def get_swap_quote(token_in: str, token_out: str, amount_in: float) -> float:
    """Get a quote for swapping tokens without executing."""
    if swap_contract is None:
        raise Exception("Swap contract not deployed. Please set SWAP_CONTRACT_ADDRESS in .env")
    
    token_in_checksum = Web3.to_checksum_address(token_in)
    token_out_checksum = Web3.to_checksum_address(token_out)
    
    decimals_in = _get_decimals(token_in)
    amount_in_int = int(amount_in * (10 ** decimals_in))
    
    quote_raw = swap_contract.functions.getQuote(
        token_in_checksum, token_out_checksum, amount_in_int
    ).call()
    
    decimals_out = _get_decimals(token_out)
    return quote_raw / (10 ** decimals_out)

def _execute_single_transfer(transfer_req: Dict, nonce: int) -> str:
    """Helper function to execute a single transfer (for parallel execution)"""
    to_checksum = Web3.to_checksum_address(transfer_req["to"])
    decimals = _get_decimals()
    amount_int = int(transfer_req["amount"] * (10 ** decimals))

    # Use provided nonce
    try:
        gas_estimate = contract.functions.transfer(to_checksum, amount_int).estimateGas({
            "from": PUBLIC_ADDRESS
        })
    except Exception:
        gas_estimate = 100000

    gas_price = w3.eth.gas_price

    tx = contract.functions.transfer(to_checksum, amount_int).build_transaction({
        "chainId": CHAIN_ID,
        "gas": gas_estimate,
        "gasPrice": gas_price,
        "nonce": nonce,
        "from": PUBLIC_ADDRESS
    })

    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    
    # Add to consensus pool
    consensus_manager.add_transaction_to_pool(
        tx_hash.hex(), PUBLIC_ADDRESS, to_checksum, transfer_req["amount"]
    )
    
    return tx_hash.hex()

async def batch_transfer_parallel(transactions: List[Dict]) -> Dict:
    """
    Execute multiple transfers in parallel.
    Uses ThreadPoolExecutor to run transactions concurrently.
    Acts as a super node that processes multiple transactions simultaneously.
    Properly handles nonces to avoid conflicts.
    """
    # Get starting nonce
    base_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    
    # Execute transactions in parallel using ThreadPoolExecutor
    # Each transaction gets a unique nonce
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=min(len(transactions), 10)) as executor:
        # Create tasks with unique nonces
        tasks = [
            loop.run_in_executor(executor, _execute_single_transfer, tx, base_nonce + i)
            for i, tx in enumerate(transactions)
        ]
        # Wait for all to complete
        tx_hashes = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions and convert to strings
    successful_hashes = []
    for hash_result in tx_hashes:
        if isinstance(hash_result, Exception):
            successful_hashes.append(f"ERROR: {str(hash_result)}")
        else:
            successful_hashes.append(hash_result)
            # Mark as executed in consensus manager
            consensus_manager.mark_executed(hash_result)
    
    # Check if all transactions reached consensus (simplified check)
    # In a real system, we'd wait for verifications
    verified_count = sum(
        1 for hash_result in successful_hashes 
        if not (isinstance(hash_result, str) and hash_result.startswith("ERROR"))
    )
    all_verified = verified_count == len(successful_hashes) and verified_count > 0
    
    return {
        "tx_hashes": successful_hashes,
        "status": "completed",
        "verified": all_verified,
        "count": len(successful_hashes)
    }
