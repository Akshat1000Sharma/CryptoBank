// ignition/modules/TokenSwap.ts
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("TokenSwapModule", (m) => {
  const tokenSwap = m.contract("TokenSwap", []);
  
  return { tokenSwap };
});

