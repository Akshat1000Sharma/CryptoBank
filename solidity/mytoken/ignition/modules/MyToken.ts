// ignition/modules/MyToken.ts
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

/**
 * Deploy MyToken with an initial supply of 1_000_000 tokens.
 * The contract constructor is: constructor(uint256 initialSupply)
 */
export default buildModule("MyTokenModule", (m) => {
  // Pass constructor args as the second parameter: [1000000n]
  // Using BigInt literal because Ignition expects bigint for integer constructor args.
  const myToken = m.contract("MyToken", [1000000n]);

  // Return the Future(s) so other modules / the deploy logs can reference them
  return { myToken };
});
