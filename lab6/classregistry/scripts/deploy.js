const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("--------------------------------------------------");
  console.log("Deploying ClassRegistry with account:", deployer.address);

  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "native tokens");

  const ClassRegistry = await hre.ethers.getContractFactory("ClassRegistry");
  const registry = await ClassRegistry.deploy();

  await registry.waitForDeployment();
  const contractAddress = await registry.getAddress();

  console.log(">>> ClassRegistry deployed successfully to:", contractAddress);
  console.log("--------------------------------------------------");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});