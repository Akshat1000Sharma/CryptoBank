# settings.py
from pathlib import Path
from dotenv import load_dotenv
import os
from web3 import Web3

# Assume settings.py sits in project root. Adjust if placed elsewhere.
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

RPC_URL = os.getenv("RPC_URL")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CHAIN_ID = int(os.getenv("CHAIN_ID", "1"))
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

if not RPC_URL:
    raise RuntimeError("RPC_URL not set in .env")

if not PUBLIC_ADDRESS or not PRIVATE_KEY or not CONTRACT_ADDRESS:
    raise RuntimeError("PUBLIC_ADDRESS, PRIVATE_KEY and CONTRACT_ADDRESS must be set in .env")

# Ensure hex prefixes
if not PUBLIC_ADDRESS.startswith("0x"):
    PUBLIC_ADDRESS = "0x" + PUBLIC_ADDRESS
if not PRIVATE_KEY.startswith("0x"):
    PRIVATE_KEY = "0x" + PRIVATE_KEY
if not CONTRACT_ADDRESS.startswith("0x"):
    CONTRACT_ADDRESS = "0x" + CONTRACT_ADDRESS

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise RuntimeError(f"Failed to connect to RPC node at {RPC_URL}")

# Convert to checksum addresses
PUBLIC_ADDRESS = Web3.to_checksum_address(PUBLIC_ADDRESS)
CONTRACT_ADDRESS = Web3.to_checksum_address(CONTRACT_ADDRESS)
