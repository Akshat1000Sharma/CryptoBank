# Complete Guide: Testing Token Swap from Frontend UI

## ✅ What You've Already Done
- ✅ Deployed MyToken contract
- ✅ Deployed MyToken2 contract  
- ✅ Deployed TokenSwap contract
- ✅ Set up liquidity and exchange rates

## 🚀 Now Let's Test from the Frontend!

---

## Step 1: Update Backend Environment Variables

**Location:** `backend/.env` file

Add these two lines to your existing `.env` file:

```env
SWAP_CONTRACT_ADDRESS=0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9
TOKEN2_ADDRESS=0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
```

**Your complete `.env` should look like:**
```env
RPC_URL=http://localhost:8545
PUBLIC_ADDRESS=0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
CHAIN_ID=31337
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
SWAP_CONTRACT_ADDRESS=0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9
TOKEN2_ADDRESS=0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
```

---

## Step 2: Restart Your Backend Server

**Why?** The backend needs to reload the new environment variables.

**How to restart:**

1. **Stop the current backend server** (if running):
   - Press `Ctrl+C` in the terminal where it's running

2. **Start it again:**
   ```bash
   cd backend
   
   # If using virtual environment:
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   
   # Start the server:
   uvicorn main:app --reload
   ```

3. **Verify it's running:**
   - You should see: `Application startup complete`
   - Server should be at: `http://localhost:8000`

---

## Step 3: Make Sure Frontend is Running

**In a separate terminal:**

```bash
cd frontend
npm run dev
```

**Verify:**
- Frontend should be at: `http://localhost:3000`
- You should see the homepage

---

## Step 4: Open the Dashboard

1. **Open your browser** and go to:
   ```
   http://localhost:3000/dashboard
   ```

2. **You should see** the DeFi Dashboard with 4 sections:
   - 🔄 Token Swap (DeFi)
   - ⚡ Parallel Batch Transfer
   - 🔐 Consensus & Verification
   - 👥 Verifier Management

---

## Step 5: Test the Swap Feature

### Test 1: Get a Quote (Preview the Swap)

1. **Scroll to the "🔄 Token Swap (DeFi)" section**

2. **Fill in the form:**
   - **Token In Address:** 
     ```
     0x5FbDB2315678afecb367f032d93F642f64180aa3
     ```
     (This is your MyToken address)
   
   - **Token Out Address:**
     ```
     0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
     ```
     (This is your MyToken2 address)
   
   - **Amount In:**
     ```
     1.0
     ```
     (You want to swap 1 MyToken)

3. **Click "Get Quote" button**

4. **Expected Result:**
   - You should see a blue box appear below
   - It should show: **"Estimated Amount Out: ~1.994"** (or similar)
   - This means 1 MTK will give you approximately 1.994 MTK2 (after fees)

### Test 2: Execute the Swap

1. **With the same values still in the form**, click **"Execute Swap"**

2. **What happens:**
   - The transaction is sent to the blockchain
   - You'll see a green success message
   - It will show:
     - Transaction hash (like: `0x1234...`)
     - Amount out received

3. **Expected Result:**
   - Success message appears
   - Transaction hash is displayed
   - Amount out shows ~1.994 MTK2

### Test 3: Verify the Swap Worked

1. **Go to the Balance page:**
   - Click "Balance" in the navigation bar
   - Or go to: `http://localhost:3000/balance`

2. **Check your balances:**
   - Enter your address: `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266`
   - Click to check balance
   - You should see your MyToken balance decreased by ~1.0
   - (To check MyToken2 balance, you'd need to modify the balance page or use a different method)

### Test 4: Reverse Swap (Swap Back)

1. **Go back to Dashboard:** `http://localhost:3000/dashboard`

2. **Fill in the form in REVERSE:**
   - **Token In Address:** 
     ```
     0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
     ```
     (MyToken2 - the one you just received)
   
   - **Token Out Address:**
     ```
     0x5FbDB2315678afecb367f032d93F642f64180aa3
     ```
     (MyToken - swap back to original)
   
   - **Amount In:**
     ```
     2.0
     ```
     (Swap 2 MTK2 back to MTK)

3. **Click "Get Quote"** - should show ~0.997 MTK (after fees)

4. **Click "Execute Swap"** - should execute successfully

---

## 🎯 Quick Reference: Contract Addresses

Keep these handy while testing:

| Contract | Address |
|----------|---------|
| **MyToken (MTK)** | `0x5FbDB2315678afecb367f032d93F642f64180aa3` |
| **MyToken2 (MTK2)** | `0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0` |
| **TokenSwap** | `0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9` |
| **Your Account** | `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266` |

---

## 🐛 Troubleshooting

### Error: "Swap contract not deployed"
- **Fix:** Make sure `SWAP_CONTRACT_ADDRESS` is in `backend/.env`
- **Fix:** Restart the backend server after updating `.env`

### Error: "Failed to get quote" or "Failed to process swap"
- **Check:** Is your Hardhat node running? (`npx hardhat node`)
- **Check:** Is your backend server running? (`http://localhost:8000`)
- **Check:** Are the contract addresses correct in `.env`?

### Error: "Insufficient liquidity"
- **Fix:** Run the setup script again:
  ```bash
  cd solidity/mytoken
  npx hardhat run scripts/setup-swap.ts --network localhost
  ```

### No response from frontend
- **Check:** Is frontend server running? (`http://localhost:3000`)
- **Check:** Open browser console (F12) for errors
- **Check:** Check backend logs for errors

### Transaction fails
- **Check:** Do you have enough tokens?
- **Check:** Is Hardhat node still running?
- **Check:** Check Hardhat node logs for transaction errors

---

## 📸 What You Should See

### Successful Quote:
```
🔄 Token Swap (DeFi)
[Form with addresses and amount]
[Get Quote] [Execute Swap]

Estimated Amount Out: 1.994
```

### Successful Swap:
```
Swap successful! TX: 0x1234..., Amount out: 1.994
```

---

## ✅ Success Checklist

- [ ] Backend `.env` updated with swap addresses
- [ ] Backend server restarted
- [ ] Frontend server running
- [ ] Dashboard page loads
- [ ] Get Quote works and shows estimated amount
- [ ] Execute Swap works and shows transaction hash
- [ ] Can swap in both directions

---

## 🎉 You're Done!

Once you can successfully:
1. Get quotes
2. Execute swaps
3. See transaction hashes

Your DeFi swap feature is working! 🚀

