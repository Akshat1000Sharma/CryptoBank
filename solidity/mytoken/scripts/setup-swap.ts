import hre from "hardhat";

/**
 * Setup script for TokenSwap contract
 * 
 * This script:
 * 1. Approves the swap contract to spend tokens
 * 2. Adds liquidity to both token pools
 * 3. Sets exchange rate between tokens
 * 
 * Usage:
 * npx hardhat run scripts/setup-swap.ts --network localhost
 * 
 * Make sure to update the addresses below with your deployed contract addresses!
 */

async function main() {
  // For Hardhat 3, get ethers from the network
  // When using --network localhost, it connects to the default hardhat network
  const network = await hre.network.connect({
    chainType: "l1",
  });
  const { ethers } = network;
  
  const [signer] = await ethers.getSigners();
  console.log("Setting up swap contract with signer:", signer.address);
  
  // ============================================
  // UPDATE THESE ADDRESSES WITH YOUR DEPLOYED CONTRACTS
  // ============================================
  const MYTOKEN_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; // MyToken
  const MYTOKEN2_ADDRESS = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0"; // MyToken2
  const SWAP_ADDRESS = "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9"; // TokenSwap
  
  // ============================================
  // CONFIGURATION
  // ============================================
  const LIQUIDITY_AMOUNT = ethers.parseEther("10000"); // 10,000 tokens
  const EXCHANGE_RATE = ethers.parseEther("2"); // 1 MTK = 2 MTK2
  
  console.log("\n=== Loading Contracts ===");
  const MyToken = await ethers.getContractAt("MyToken", MYTOKEN_ADDRESS);
  const MyToken2 = await ethers.getContractAt("MyToken2", MYTOKEN2_ADDRESS);
  const TokenSwap = await ethers.getContractAt("TokenSwap", SWAP_ADDRESS);
  
  console.log("MyToken address:", MYTOKEN_ADDRESS);
  console.log("MyToken2 address:", MYTOKEN2_ADDRESS);
  console.log("TokenSwap address:", SWAP_ADDRESS);
  
  // Check balances
  console.log("\n=== Checking Balances ===");
  const myTokenBalance = await MyToken.balanceOf(signer.address);
  const myToken2Balance = await MyToken2.balanceOf(signer.address);
  console.log("MyToken balance:", ethers.formatEther(myTokenBalance), "MTK");
  console.log("MyToken2 balance:", ethers.formatEther(myToken2Balance), "MTK2");
  
  if (myTokenBalance < LIQUIDITY_AMOUNT || myToken2Balance < LIQUIDITY_AMOUNT) {
    console.error("\n❌ ERROR: Insufficient balance for liquidity!");
    console.error("Need at least", ethers.formatEther(LIQUIDITY_AMOUNT), "of each token");
    process.exit(1);
  }
  
  // Approve swap contract
  console.log("\n=== Approving Tokens ===");
  const approveAmount = ethers.parseEther("100000"); // Approve 100k tokens
  console.log("Approving MyToken...");
  const approve1Tx = await MyToken.approve(SWAP_ADDRESS, approveAmount);
  await approve1Tx.wait();
  console.log("✅ MyToken approved");
  
  console.log("Approving MyToken2...");
  const approve2Tx = await MyToken2.approve(SWAP_ADDRESS, approveAmount);
  await approve2Tx.wait();
  console.log("✅ MyToken2 approved");
  
  // Add liquidity
  console.log("\n=== Adding Liquidity ===");
  console.log("Adding", ethers.formatEther(LIQUIDITY_AMOUNT), "MyToken...");
  const liquidity1Tx = await TokenSwap.addLiquidity(MYTOKEN_ADDRESS, LIQUIDITY_AMOUNT);
  await liquidity1Tx.wait();
  console.log("✅ MyToken liquidity added");
  
  console.log("Adding", ethers.formatEther(LIQUIDITY_AMOUNT), "MyToken2...");
  const liquidity2Tx = await TokenSwap.addLiquidity(MYTOKEN2_ADDRESS, LIQUIDITY_AMOUNT);
  await liquidity2Tx.wait();
  console.log("✅ MyToken2 liquidity added");
  
  // Set exchange rate
  console.log("\n=== Setting Exchange Rate ===");
  console.log("Setting rate: 1 MTK =", ethers.formatEther(EXCHANGE_RATE), "MTK2");
  const rateTx = await TokenSwap.setExchangeRate(MYTOKEN_ADDRESS, MYTOKEN2_ADDRESS, EXCHANGE_RATE);
  await rateTx.wait();
  console.log("✅ Exchange rate set");
  
  // Verify setup
  console.log("\n=== Verifying Setup ===");
  const reserve1 = await TokenSwap.getReserve(MYTOKEN_ADDRESS);
  const reserve2 = await TokenSwap.getReserve(MYTOKEN2_ADDRESS);
  const rate = await TokenSwap.exchangeRates(MYTOKEN_ADDRESS, MYTOKEN2_ADDRESS);
  
  console.log("MyToken reserve:", ethers.formatEther(reserve1), "MTK");
  console.log("MyToken2 reserve:", ethers.formatEther(reserve2), "MTK2");
  console.log("Exchange rate:", ethers.formatEther(rate), "MTK2 per MTK");
  
  // Test quote
  const testAmount = ethers.parseEther("1");
  const quote = await TokenSwap.getQuote(MYTOKEN_ADDRESS, MYTOKEN2_ADDRESS, testAmount);
  console.log("\n=== Test Quote ===");
  console.log("1 MTK ->", ethers.formatEther(quote), "MTK2");
  
  console.log("\n✅ Swap contract setup complete!");
  console.log("\nNext steps:");
  console.log("1. Update backend/.env with SWAP_CONTRACT_ADDRESS and TOKEN2_ADDRESS");
  console.log("2. Restart your FastAPI backend server");
  console.log("3. Test the swap feature in the dashboard at http://localhost:3000/dashboard");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

