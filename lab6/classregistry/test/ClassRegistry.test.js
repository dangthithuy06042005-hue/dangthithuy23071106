const { loadFixture } = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ClassRegistry", function () {
  async function deployClassRegistryFixture() {
    const [owner, alice, bob, ...others] = await ethers.getSigners();
    const ClassRegistry = await ethers.getContractFactory("ClassRegistry");
    const registry = await ClassRegistry.deploy();
    return { registry, owner, alice, bob, others };
  }

  describe("Deployment", function () {
    it("Khởi tạo đúng chủ sở hữu (owner)", async function () {
      const { registry, owner } = await loadFixture(deployClassRegistryFixture);
      expect(await registry.owner()).to.equal(owner.address);
    });

    it("Số lượng ban đầu là 0", async function () {
      const { registry } = await loadFixture(deployClassRegistryFixture);
      expect(await registry.memberCount()).to.equal(0);
    });
  });

  describe("Register", function () {
    it("Đăng ký thành công: lưu tên đúng và phát ra event Registered", async function () {
      const { registry, alice } = await loadFixture(deployClassRegistryFixture);

      await expect(registry.connect(alice).register("Alice"))
        .to.emit(registry, "Registered")
        .withArgs(alice.address, "Alice");

      expect(await registry.names(alice.address)).to.equal("Alice");
      expect(await registry.memberCount()).to.equal(1);
      expect(await registry.memberAt(0)).to.equal(alice.address);
    });

    it("Revert EmptyName nếu tên rỗng", async function () {
      const { registry, alice } = await loadFixture(deployClassRegistryFixture);

      await expect(registry.connect(alice).register(""))
        .to.be.revertedWithCustomError(registry, "EmptyName");
    });

    it("Revert AlreadyRegistered nếu cùng một ví đăng ký 2 lần", async function () {
      const { registry, alice } = await loadFixture(deployClassRegistryFixture);

      await registry.connect(alice).register("Alice First");

      await expect(registry.connect(alice).register("Alice Second"))
        .to.be.revertedWithCustomError(registry, "AlreadyRegistered")
        .withArgs(alice.address);
    });
  });

  describe("Deregister", function () {
    it("Revert NotOwner nếu người không phải owner gọi deregister", async function () {
      const { registry, alice, bob } = await loadFixture(deployClassRegistryFixture);

      await registry.connect(alice).register("Alice");

      await expect(registry.connect(bob).deregister(alice.address))
        .to.be.revertedWithCustomError(registry, "NotOwner");
    });

    it("Revert NotRegistered nếu deregister địa chỉ chưa đăng ký", async function () {
      const { registry, owner, bob } = await loadFixture(deployClassRegistryFixture);

      await expect(registry.connect(owner).deregister(bob.address))
        .to.be.revertedWithCustomError(registry, "NotRegistered");
    });

    it("Owner deregister thành công và mảng được thu gọn bằng swap-and-pop", async function () {
      const { registry, owner, alice, bob } = await loadFixture(deployClassRegistryFixture);

      await registry.connect(alice).register("Alice");
      await registry.connect(bob).register("Bob");
      expect(await registry.memberCount()).to.equal(2);

      await registry.connect(owner).deregister(alice.address);

      expect(await registry.names(alice.address)).to.equal("");
      expect(await registry.memberCount()).to.equal(1);
      expect(await registry.memberAt(0)).to.equal(bob.address);
    });
  });

  describe("Multi-user Loop Test", function () {
    it("Vòng lặp đăng ký nhiều tài khoản với các tên khác nhau", async function () {
      const { registry, others } = await loadFixture(deployClassRegistryFixture);
      const signersToTest = others.slice(0, 5);

      for (let i = 0; i < signersToTest.length; i++) {
        const name = `Student_${i + 1}`;
        await registry.connect(signersToTest[i]).register(name);
      }

      expect(await registry.memberCount()).to.equal(signersToTest.length);

      for (let i = 0; i < signersToTest.length; i++) {
        const expectedName = `Student_${i + 1}`;
        expect(await registry.names(signersToTest[i].address)).to.equal(expectedName);
      }
    });
  });
});
