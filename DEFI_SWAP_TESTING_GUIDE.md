# Step-by-Step Guide: Testing DeFi Token Swap Feature

## Prerequisites
- Hardhat node running on localhost (port 8545)
- FastAPI backend server running
- Next.js frontend server running
- MyToken contract already deployed 

---

## Step 1: Deploy MyToken2 Contract

Deploy the second token needed for swapping:

```bash
cd solidity/mytoken
npx hardhat ignition deploy ignition/modules/MyToken2.ts --network localhost
```

**Save the deployed address** from the output. It will look like:
```
MyToken2Module#MyToken2: 0x...
```

---

## Step 2: Deploy TokenSwap Contract

Deploy the swap contract:

```bash
npx hardhat ignition deploy ignition/modules/TokenSwap.ts --network localhost
```

**Save the deployed address** from the output. It will look like:
```
TokenSwapModule#TokenSwap: 0x...
```

---

## Step 3: Set Up the Swap Contract

You need to:
1. Add liquidity to the swap contract
2. Set exchange rates between tokens
3. Approve the swap contract to spend your tokens

### Option A: Using Hardhat Console (Recommended)

Open Hardhat console:
```bash
npx hardhat console --network localhost
```

Then run these commands (replace addresses with your deployed addresses):

```javascript
// Get signers
const [signer] = await ethers.getSigners();
console.log("Signer address:", signer.address);

// Get contract instances
const MyToken = await ethers.getContractAt("MyToken", "0x5FbDB2315678afecb367f032d93F642f64180aa3");
const MyToken2 = await ethers.getContractAt("MyToken2", "YOUR_MYTOKEN2_ADDRESS");
const TokenSwap = await ethers.getContractAt("TokenSwap", "YOUR_TOKENSWAP_ADDRESS");

// Check balances
const myTokenBalance = await MyToken.balanceOf(signer.address);
const myToken2Balance = await MyToken2.balanceOf(signer.address);
console.log("MyToken balance:", ethers.formatEther(myTokenBalance));
console.log("MyToken2 balance:", ethers.formatEther(myToken2Balance));

// Approve swap contract to spend tokens
console.log("Approving tokens...");
await MyToken.approve(TokenSwap.target, ethers.parseEther("100000"));
await MyToken2.approve(TokenSwap.target, ethers.parseEther("100000"));
console.log("Approval complete");

// Add liquidity (e.g., 10000 tokens of each)
console.log("Adding liquidity...");
await TokenSwap.addLiquidity(MyToken.target, ethers.parseEther("10000"));
await TokenSwap.addLiquidity(MyToken2.target, ethers.parseEther("10000"));
console.log("Liquidity added");

// Set exchange rate: 1 MyToken = 2 MyToken2 (rate = 2 * 1e18)
// This means 1 MTK = 2 MTK2
const rate = ethers.parseEther("2"); // 2 * 10^18
await TokenSwap.setExchangeRate(MyToken.target, MyToken2.target, rate);
console.log("Exchange rate set: 1 MTK = 2 MTK2");

// Verify setup
const reserve1 = await TokenSwap.getReserve(MyToken.target);
const reserve2 = await TokenSwap.getReserve(MyToken2.target);
console.log("MyToken reserve:", ethers.formatEther(reserve1));
console.log("MyToken2 reserve:", ethers.formatEther(reserve2));

const quote = await TokenSwap.getQuote(MyToken.target, MyToken2.target, ethers.parseEther("1"));
console.log("Quote for 1 MTK -> MTK2:", ethers.formatEther(quote));
```

### Option B: Create a Setup Script

Create a file `solidity/mytoken/scripts/setup-swap.ts`:

```typescript
import { ethers } from "hardhat";

async function main() {
  const [signer] = await ethers.getSigners();
  
  // Replace with your deployed addresses
  const MYTOKEN_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  const MYTOKEN2_ADDRESS = "YOUR_MYTOKEN2_ADDRESS";
  const SWAP_ADDRESS = "YOUR_TOKENSWAP_ADDRESS";
  
  const MyToken = await ethers.getContractAt("MyToken", MYTOKEN_ADDRESS);
  const MyToken2 = await ethers.getContractAt("MyToken2", MYTOKEN2_ADDRESS);
  const TokenSwap = await ethers.getContractAt("TokenSwap", SWAP_ADDRESS);
  
  // Approve
  await MyToken.approve(SWAP_ADDRESS, ethers.parseEther("100000"));
  await MyToken2.approve(SWAP_ADDRESS, ethers.parseEther("100000"));
  
  // Add liquidity
  await TokenSwap.addLiquidity(MYTOKEN_ADDRESS, ethers.parseEther("10000"));
  await TokenSwap.addLiquidity(MYTOKEN2_ADDRESS, ethers.parseEther("10000"));
  
  // Set rate: 1 MTK = 2 MTK2
  await TokenSwap.setExchangeRate(MYTOKEN_ADDRESS, MYTOKEN2_ADDRESS, ethers.parseEther("2"));
  
  console.log("Swap contract setup complete!");
}

main().catch(console.error);
```

Then run:
```bash
npx hardhat run scripts/setup-swap.ts --network localhost
```

---

## Step 4: Update Backend .env File

Update your `backend/.env` file with the new contract addresses:

```env
RPC_URL=http://localhost:8545
PUBLIC_ADDRESS=0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
CHAIN_ID=31337
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
SWAP_CONTRACT_ADDRESS=YOUR_TOKENSWAP_ADDRESS
TOKEN2_ADDRESS=YOUR_MYTOKEN2_ADDRESS
```

**Important:** Replace `YOUR_TOKENSWAP_ADDRESS` and `YOUR_MYTOKEN2_ADDRESS` with the actual addresses from Steps 1 and 2.

---

## Step 5: Restart Backend Server

Restart your FastAPI backend to load the new environment variables:

```bash
cd backend
# If using uvicorn directly:
uvicorn main:app --reload

# Or if using a virtual environment:
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

---

## Step 6: Test Through the Dashboard

1. **Open your browser** and navigate to `http://localhost:3000/dashboard`

2. **Navigate to the Token Swap section**

3. **Test Get Quote:**
   - **Token In Address:** `0x5FbDB2315678afecb367f032d93F642f64180aa3` (MyToken)
   - **Token Out Address:** Your MyToken2 address
   - **Amount In:** `1.0`
   - Click **"Get Quote"**
   - You should see an estimated amount out (should be around 2.0 MTK2 if rate is 1:2)

4. **Test Execute Swap:**
   - Fill in the same addresses and amount
   - Click **"Execute Swap"**
   - You should see a transaction hash and the amount received
   - The swap should execute successfully

5. **Verify the Swap:**
   - Check your balance of both tokens using the Balance page
   - You should see:
     - MyToken balance decreased by ~1.0 (plus fees)
     - MyToken2 balance increased by ~2.0 (minus fees)

---

## Step 7: Test Reverse Swap

Test swapping in the opposite direction:

1. **Token In Address:** Your MyToken2 address
2. **Token Out Address:** `0x5FbDB2315678afecb367f032d93F642f64180aa3` (MyToken)
3. **Amount In:** `2.0`
4. Click **"Execute Swap"**

This should convert 2 MTK2 back to approximately 1 MTK.

---

## Troubleshooting

### Error: "Swap contract not deployed"
- Make sure `SWAP_CONTRACT_ADDRESS` is set in `backend/.env`
- Restart the backend server after updating `.env`

### Error: "Insufficient liquidity"
- Make sure you added liquidity to the swap contract (Step 3)
- Check reserves using Hardhat console: `await TokenSwap.getReserve(tokenAddress)`

### Error: "Exchange rate not set"
- Make sure you set the exchange rate (Step 3)
- Check rate: `await TokenSwap.exchangeRates(tokenA, tokenB)`

### Error: "Failed to approve tokens"
- Make sure you approved the swap contract to spend your tokens
- Check allowance: `await MyToken.allowance(yourAddress, swapAddress)`

### Transaction fails
- Make sure you have enough tokens in your account
- Check your account balance: `await MyToken.balanceOf(yourAddress)`
- Make sure Hardhat node is running and you have ETH for gas

---

## Quick Reference: Contract Addresses

After deployment, your addresses should be:
- **MyToken:** `0x5FbDB2315678afecb367f032d93F642f64180aa3` (already deployed)
- **MyToken2:** `0x...` (from Step 1)
- **TokenSwap:** `0x...` (from Step 2)

Save these addresses for easy reference!

