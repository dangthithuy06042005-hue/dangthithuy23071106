const hre = require("hardhat");

async function main() {
  const registryAddress = process.env.REGISTRY;
  const nameToRegister = process.env.NAME;

  if (!registryAddress || !nameToRegister) {
    throw new Error("Vui lòng cung cấp cả biến môi trường REGISTRY và NAME!");
  }

  const [caller] = await hre.ethers.getSigners();
  console.log("Registering from account:", caller.address);
  console.log("Target Registry Address:", registryAddress);
  console.log("Name to register:", nameToRegister);

  const registry = await hre.ethers.getContractAt("ClassRegistry", registryAddress);
  const tx = await registry.register(nameToRegister);

  console.log("Transaction sent! Hash:", tx.hash);
  console.log("Waiting for confirmation...");
  const receipt = await tx.wait();

  console.log(">>> Registered successfully in block:", receipt.blockNumber);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});