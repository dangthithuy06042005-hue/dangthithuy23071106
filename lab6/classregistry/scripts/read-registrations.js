const hre = require("hardhat");

async function main() {
  const registryAddress = process.env.REGISTRY;
  if (!registryAddress) {
    throw new Error("Thieu bien REGISTRY!");
  }

  console.log("--------------------------------------------------");
  console.log("Reading data from ClassRegistry at:", registryAddress);
  const registry = await hre.ethers.getContractAt("ClassRegistry", registryAddress);

  // Đọc số lượng thành viên
  const count = await registry.memberCount();
  console.log(`>>> Total registered members: ${count}`);

  // Đọc danh sách từ Event Log
  console.log("\n--- Danh sach thanh vien tu Event Log ---");
  const filter = registry.filters.Registered();
  const events = await registry.queryFilter(filter);

  if (events.length === 0) {
    console.log("Chua co ai dang ky.");
  } else {
    events.forEach((event, idx) => {
      console.log(`[${idx + 1}] Address: ${event.args.who} | Name: "${event.args.name}"`);
    });
  }
  console.log("--------------------------------------------------");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
