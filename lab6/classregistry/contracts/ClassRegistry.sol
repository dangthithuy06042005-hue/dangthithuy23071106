// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice Lỗi khi tên truyền vào rỗng
error EmptyName();

/// @notice Lỗi khi địa chỉ này đã đăng ký trước đó
error AlreadyRegistered(address who);

/// @notice Lỗi khi người gọi không phải là owner
error NotOwner();

/// @notice Lỗi khi địa chỉ cần xóa chưa từng đăng ký
error NotRegistered();

contract ClassRegistry {
    // Địa chỉ của chủ sở hữu contract (bất biến sau khi khởi tạo)
    address public immutable owner;

    // Mapping lưu tên của từng địa chỉ ví
    mapping(address => string) public names;

    // Mảng lưu danh sách địa chỉ (để duyệt và đếm)
    address[] public members;

    // Sự kiện bắn ra khi đăng ký thành công
    event Registered(address indexed who, string name);

    // Sự kiện bắn ra khi hủy đăng ký
    event Deregistered(address indexed who);

    modifier onlyOwner() {
        if (msg.sender != owner) {
            revert NotOwner();
        }
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @notice Đăng ký tên cho người gọi (msg.sender)
     */
    function register(string calldata name) external {
        if (bytes(name).length == 0) {
            revert EmptyName();
        }
        if (bytes(names[msg.sender]).length > 0) {
            revert AlreadyRegistered(msg.sender);
        }

        names[msg.sender] = name;
        members.push(msg.sender);

        emit Registered(msg.sender, name);
    }

    /**
     * @notice Hủy đăng ký một địa chỉ (Chỉ Owner có quyền)
     * @dev Áp dụng kỹ thuật swap-and-pop để giữ mảng gọn trong O(1)
     */
    function deregister(address who) external onlyOwner {
        if (bytes(names[who]).length == 0) {
            revert NotRegistered();
        }

        delete names[who];

        uint256 length = members.length;
        for (uint256 i = 0; i < length; i++) {
            if (members[i] == who) {
                members[i] = members[length - 1];
                members.pop();
                break;
            }
        }

        emit Deregistered(who);
    }

    /**
     * @notice Lấy tổng số thành viên hiện tại
     */
    function memberCount() external view returns (uint256) {
        return members.length;
    }

    /**
     * @notice Lấy địa chỉ theo chỉ số index
     */
    function memberAt(uint256 index) external view returns (address) {
        require(index < members.length, "Index out of bounds");
        return members[index];
    }
}
