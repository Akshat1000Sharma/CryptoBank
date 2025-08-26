// scripts/deploy.js
import hre from "hardhat";   // import the Hardhat runtime as the default
const { ethers } = hre;     // grab ethers from the HRE

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  const initialSupply = 1_000_000;

  const MyToken = await ethers.getContractFactory("MyToken");
  const token = await MyToken.deploy(initialSupply);

  await token.deployed();
  console.log("MyToken deployed to:", token.address);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
