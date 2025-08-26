from web3 import Web3
from settings import w3, PUBLIC_ADDRESS, PRIVATE_KEY, CHAIN_ID
from contract_utils import contract

def _get_decimals() -> int:
    return contract.functions.decimals().call()

def get_balance(address: str) -> dict:
    checksum = Web3.to_checksum_address(address)
    bal_raw = contract.functions.balanceOf(checksum).call()
    decimals = _get_decimals()
    return {"address": checksum, "balance": bal_raw / (10 ** decimals)}

def get_total_supply() -> float:
    supply_raw = contract.functions.totalSupply().call()
    decimals = _get_decimals()
    return supply_raw / (10 ** decimals)

def transfer(to: str, amount: float) -> str:
    """
    Build, sign and send a transfer transaction.
    `amount` is in token units (e.g., 1.5 tokens). This will convert to token base units.
    Returns the tx hash hex string.
    """
    to_checksum = Web3.to_checksum_address(to)
    decimals = _get_decimals()
    amount_int = int(amount * (10 ** decimals))

    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)

    # Try to estimate gas; fall back to a safe default if estimate fails
    try:
        gas_estimate = contract.functions.transfer(to_checksum, amount_int).estimateGas({
            "from": PUBLIC_ADDRESS
        })
    except Exception:
        gas_estimate = 100000  # fallback

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
    return tx_hash.hex()
