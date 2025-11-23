# contract_utils.py
from web3 import Web3
from settings import w3, CONTRACT_ADDRESS
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Minimal ERC-20 ABI: only the methods we need
ERC20_MINIMAL_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    }
]

# TokenSwap contract ABI
TOKEN_SWAP_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "tokenIn", "type": "address"},
            {"name": "tokenOut", "type": "address"},
            {"name": "amountIn", "type": "uint256"}
        ],
        "name": "swap",
        "outputs": [{"name": "amountOut", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "tokenIn", "type": "address"},
            {"name": "tokenOut", "type": "address"},
            {"name": "amountIn", "type": "uint256"}
        ],
        "name": "getQuote",
        "outputs": [{"name": "amountOut", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "token", "type": "address"}],
        "name": "getReserve",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "token", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "addLiquidity",
        "outputs": [],
        "type": "function",
    }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ERC20_MINIMAL_ABI)

# Get swap contract address from env or use a default
SWAP_CONTRACT_ADDRESS = os.getenv("SWAP_CONTRACT_ADDRESS")
if SWAP_CONTRACT_ADDRESS:
    if not SWAP_CONTRACT_ADDRESS.startswith("0x"):
        SWAP_CONTRACT_ADDRESS = "0x" + SWAP_CONTRACT_ADDRESS
    SWAP_CONTRACT_ADDRESS = Web3.to_checksum_address(SWAP_CONTRACT_ADDRESS)
    swap_contract = w3.eth.contract(address=SWAP_CONTRACT_ADDRESS, abi=TOKEN_SWAP_ABI)
else:
    # Create a dummy contract if not deployed yet
    swap_contract = None

# Get token2 address from env
TOKEN2_ADDRESS = os.getenv("TOKEN2_ADDRESS")
if TOKEN2_ADDRESS:
    if not TOKEN2_ADDRESS.startswith("0x"):
        TOKEN2_ADDRESS = "0x" + TOKEN2_ADDRESS
    TOKEN2_ADDRESS = Web3.to_checksum_address(TOKEN2_ADDRESS)

def get_token_contract(token_address: str):
    """Get a contract instance for a specific token address"""
    token_checksum = Web3.to_checksum_address(token_address)
    return w3.eth.contract(address=token_checksum, abi=ERC20_MINIMAL_ABI)
