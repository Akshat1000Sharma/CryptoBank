# CryptoBank

CryptoBank is a decentralized banking prototype that combines **Ethereum smart contracts, a FastAPI backend, and a modern Next.js frontend** to simulate core banking operations on blockchain infrastructure.

The system allows users to interact with blockchain-based banking services such as deposits, withdrawals, and balance tracking while maintaining a user-friendly web interface.

---
## Architecture

The project follows a **three-layer architecture**:


+-------------------------------+
|        Frontend Layer         |
|   Next.js + Liquid Ether UI   |
+---------------+---------------+
                |
                v
+-------------------------------+
|        Backend API Layer      |
|            FastAPI            |
+---------------+---------------+
                |
                v
+-------------------------------+
|      Blockchain Layer         |
|  Solidity Smart Contracts     |
|      (Deployed via Hardhat)   |
+-------------------------------+


### Components

**Frontend**
- Built using **Next.js**
- Interactive blockchain UI using **Liquid Ether components**
- Wallet integration for signing transactions
- Displays balances, transactions, and contract interactions

**Backend**
- Built with **FastAPI**
- Handles API requests between frontend and blockchain
- Manages contract interaction logic
- Provides endpoints for account operations and transaction queries

**Smart Contracts**
- Written in **Solidity**
- Deployed locally using **Hardhat**
- Implements core banking functionality such as:
  - deposit
  - withdraw
  - balance tracking
  - transaction logging

---

## Tech Stack

Frontend
- Next.js
- Liquid Ether UI
- JavaScript / React

Backend
- Python
- FastAPI
- Web3.py

Blockchain
- Solidity
- Hardhat
- Ethereum (local development network)

---

## Features

- Blockchain-based banking prototype
- Smart contract controlled deposits and withdrawals
- FastAPI backend for blockchain interaction
- Interactive Web3 user interface
- Local Ethereum development using Hardhat
- Transaction transparency via blockchain

---

## Project Structure

```
CryptoBank/
│
├── backend/
│ ├── main.py
│ ├── api/
│ └── blockchain/
│
├── frontend/
│ ├── pages/
│ ├── components/
│ └── ui/
│
├── contracts/
│ ├── Bank.sol
│
├── scripts/
│ └── deploy.js
│
└── hardhat.config.js
```

---

## Running the Project

### 1. Clone the repository
```
git clone https://github.com/Akshat1000Sharma/CryptoBank
cd CryptoBank
```


---

### 2. Install dependencies

Backend
```
cd backend
pip install -r requirements.txt
```

Frontend
```
cd frontend
npm install
```


Smart Contracts
```
npm install
```

---

### 3. Start Hardhat local blockchain
```
npx hardhat node
```

---

### 4. Deploy smart contracts
```
npx hardhat run scripts/deploy.js --network localhost
```

---

### 5. Run FastAPI backend
```
uvicorn main:app --reload
```

---

### 6. Run Next.js frontend
```
npm run dev
```

---

## Example Workflow

1. User connects wallet on frontend
2. User submits deposit or withdrawal request
3. FastAPI backend interacts with smart contract
4. Transaction is signed and recorded on blockchain
5. Updated balance is returned to frontend

---

## Learning Goals

This project demonstrates:

- Building **full-stack decentralized applications**
- Integrating **FastAPI with blockchain infrastructure**
- Developing **Solidity smart contracts**
- Creating **interactive Web3 interfaces with Next.js**

---

## Future Improvements

- Smart contract security improvements
- Multi-user account management
- Transaction history dashboard
- Deployment on public Ethereum testnets
