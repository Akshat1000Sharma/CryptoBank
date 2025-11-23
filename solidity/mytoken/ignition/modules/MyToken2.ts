// ignition/modules/MyToken2.ts
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("MyToken2Module", (m) => {
  const myToken2 = m.contract("MyToken2", [1000000n]);
  
  return { myToken2 };
});

