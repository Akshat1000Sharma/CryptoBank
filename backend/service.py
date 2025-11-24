from web3 import Web3
import asyncio
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional
from settings import w3, PUBLIC_ADDRESS, PRIVATE_KEY, CHAIN_ID
from contract_utils import contract, swap_contract, get_token_contract
from consensus import consensus_manager

# Thread-safe nonce manager for concurrent execution
class NonceManager:
    def __init__(self, initial_nonce: int):
        self.nonce = initial_nonce
        self.lock = threading.Lock()
    
    def get_and_increment(self) -> int:
        """Get current nonce and increment atomically"""
        with self.lock:
            current = self.nonce
            self.nonce += 1
            return current

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

def _execute_single_transfer(transfer_req: Dict, nonce_or_manager, delay: float = 0.0) -> str:
    """
    Helper function to execute a single transfer.
    Accepts either a NonceManager (for parallel) or an int (for sequential).
    
    Args:
        transfer_req: Transfer request dictionary
        nonce_or_manager: Either NonceManager instance or int nonce
        delay: Optional delay before sending (for staggering parallel transactions)
    """
    import time
    if delay > 0:
        time.sleep(delay)
    
    to_checksum = Web3.to_checksum_address(transfer_req["to"])
    decimals = _get_decimals()
    amount_int = int(transfer_req["amount"] * (10 ** decimals))

    # Get nonce - handle both NonceManager and int
    if isinstance(nonce_or_manager, NonceManager):
        nonce = nonce_or_manager.get_and_increment()
    else:
        nonce = nonce_or_manager

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

async def batch_transfer_sequential(transactions: List[Dict]) -> Dict:
    """
    Execute multiple transfers sequentially (one after another).
    This is the non-concurrent approach for comparison.
    """
    start_time = time.time()
    
    tx_hashes = []
    # Get current nonce, accounting for any pending transactions
    try:
        current_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS, block_identifier='pending')
    except TypeError:
        try:
            current_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS, 'pending')
        except:
            current_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    except:
        current_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    
    for tx in transactions:
        try:
            # Use current nonce and increment for next transaction
            tx_hash = _execute_single_transfer(tx, current_nonce)
            tx_hashes.append(tx_hash)
            consensus_manager.mark_executed(tx_hash)
            # Increment nonce for next transaction
            current_nonce += 1
        except Exception as e:
            tx_hashes.append(f"ERROR: {str(e)}")
            # Still increment nonce even on error to maintain sequence
            current_nonce += 1
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    successful_count = sum(
        1 for hash_result in tx_hashes 
        if not (isinstance(hash_result, str) and hash_result.startswith("ERROR"))
    )
    
    return {
        "tx_hashes": tx_hashes,
        "status": "completed",
        "verified": successful_count == len(tx_hashes) and successful_count > 0,
        "count": len(tx_hashes),
        "execution_time_seconds": execution_time,
        "successful_count": successful_count,
        "failed_count": len(tx_hashes) - successful_count
    }

async def performance_comparison_test(num_transactions: int = 5) -> Dict:
    """
    Compare concurrent vs sequential batch transfer execution.
    Returns detailed performance metrics for both approaches.
    
    Args:
        num_transactions: Number of test transactions to execute (default: 5)
    
    Returns:
        Dictionary with performance comparison data
    """
    # Generate test transactions (sending to different addresses with small amounts)
    # Using the default account's address variations for testing
    test_addresses = [
        "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
        "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
        "0x90F79bf6EB2c4f870365E785982E1f101E93b906",
        "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65",
        "0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc",
        "0x976EA74026E726554dB657fA54763abd0C3a0aa9",
        "0x14dC79964da2C08b23698B3D3cc7Ca32193d995a",
        "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8F",
        "0xa0Ee7A142d267C1f36714E4a8F75612F20a797E8",
        "0xBcd4042DE499D14e55001CcbB24a551F3b954096"
    ]
    
    # Create test transactions
    test_transactions = [
        {"to": test_addresses[i % len(test_addresses)], "amount": 0.1}
        for i in range(num_transactions)
    ]
    
    print(f"\n=== Performance Test: {num_transactions} transactions ===")
    print("Running concurrent execution...")
    
    # Test concurrent execution
    concurrent_start = time.time()
    concurrent_result = await batch_transfer_parallel(test_transactions)
    concurrent_end = time.time()
    
    # Wait a bit to ensure transactions are processed and nonces are updated
    await asyncio.sleep(3)
    
    print("Running sequential execution...")
    
    # Test sequential execution
    sequential_start = time.time()
    sequential_result = await batch_transfer_sequential(test_transactions)
    sequential_end = time.time()
    
    # Calculate metrics
    concurrent_time = concurrent_result["execution_time_seconds"]
    sequential_time = sequential_result["execution_time_seconds"]
    
    concurrent_success_rate = (
        concurrent_result["successful_count"] / concurrent_result["count"] * 100
        if concurrent_result["count"] > 0 else 0
    )
    sequential_success_rate = (
        sequential_result["successful_count"] / sequential_result["count"] * 100
        if sequential_result["count"] > 0 else 0
    )
    
    speedup_factor = sequential_time / concurrent_time if concurrent_time > 0 else 0
    improvement_percentage = ((sequential_time - concurrent_time) / sequential_time * 100) if sequential_time > 0 else 0
    
    return {
        "concurrent_execution": {
            "execution_time_seconds": concurrent_time,
            "successful_count": concurrent_result["successful_count"],
            "failed_count": concurrent_result["failed_count"],
            "total_count": concurrent_result["count"],
            "success_rate": concurrent_success_rate,
            "average_time_per_tx": concurrent_time / concurrent_result["count"] if concurrent_result["count"] > 0 else 0,
            "tx_hashes": concurrent_result["tx_hashes"][:5]  # Limit to first 5 for response size
        },
        "sequential_execution": {
            "execution_time_seconds": sequential_time,
            "successful_count": sequential_result["successful_count"],
            "failed_count": sequential_result["failed_count"],
            "total_count": sequential_result["count"],
            "success_rate": sequential_success_rate,
            "average_time_per_tx": sequential_time / sequential_result["count"] if sequential_result["count"] > 0 else 0,
            "tx_hashes": sequential_result["tx_hashes"][:5]  # Limit to first 5 for response size
        },
        "improvement_percentage": improvement_percentage,
        "speedup_factor": speedup_factor,
        "test_configuration": {
            "num_transactions": num_transactions,
            "amount_per_transaction": 0.1,
            "test_type": "batch_transfer_comparison"
        }
    }

def _prepare_transaction(transfer_req: Dict, nonce: int) -> tuple:
    """
    Prepare a transaction (build and sign) without sending it.
    This is the expensive part that benefits from parallel processing.
    Returns (signed_raw_tx, to_address, amount) tuple.
    """
    to_checksum = Web3.to_checksum_address(transfer_req["to"])
    decimals = _get_decimals()
    amount_int = int(transfer_req["amount"] * (10 ** decimals))

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
    return (signed.raw_transaction, to_checksum, transfer_req["amount"])

async def batch_transfer_parallel(transactions: List[Dict]) -> Dict:
    """
    Execute multiple transfers with parallel preparation.
    Prepares transactions in parallel (gas estimation, signing) but sends them sequentially.
    This demonstrates the performance benefit of parallel processing while ensuring correct nonce ordering.
    """
    start_time = time.time()
    
    # Get starting nonce, accounting for pending transactions
    try:
        base_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS, block_identifier='pending')
    except TypeError:
        try:
            base_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS, 'pending')
        except:
            base_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    except:
        base_nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    
    # Prepare all transactions in parallel (this is the expensive part)
    # Gas estimation and signing happen concurrently
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=min(len(transactions), 10)) as executor:
        prepare_tasks = [
            loop.run_in_executor(executor, _prepare_transaction, tx, base_nonce + i)
            for i, tx in enumerate(transactions)
        ]
        prepared_txs = await asyncio.gather(*prepare_tasks, return_exceptions=True)
    
    # Send transactions sequentially to ensure proper nonce ordering
    # But they're already prepared, so this is much faster than sequential preparation
    tx_hashes = []
    for prepared in prepared_txs:
        if isinstance(prepared, Exception):
            tx_hashes.append(f"ERROR: {str(prepared)}")
        else:
            try:
                signed_tx, to_address, amount = prepared
                tx_hash = w3.eth.send_raw_transaction(signed_tx)
                tx_hash_hex = tx_hash.hex()
                tx_hashes.append(tx_hash_hex)
                consensus_manager.add_transaction_to_pool(
                    tx_hash_hex, PUBLIC_ADDRESS, to_address, amount
                )
                consensus_manager.mark_executed(tx_hash_hex)
            except Exception as e:
                tx_hashes.append(f"ERROR: {str(e)}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
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
    successful_count = sum(
        1 for hash_result in successful_hashes 
        if not (isinstance(hash_result, str) and hash_result.startswith("ERROR"))
    )
    all_verified = successful_count == len(successful_hashes) and successful_count > 0
    
    return {
        "tx_hashes": successful_hashes,
        "status": "completed",
        "verified": all_verified,
        "count": len(successful_hashes),
        "execution_time_seconds": execution_time,
        "successful_count": successful_count,
        "failed_count": len(successful_hashes) - successful_count
    }
