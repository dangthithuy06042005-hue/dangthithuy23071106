from eth_account import Account
from eth_account.messages import encode_defunct

# Dùng khóa cố định để chứng minh Task 1 (chạy nhiều lần chữ ký không đổi)
acct = Account.from_key("0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318")

print("Địa chỉ ví (Address):", acct.address)

# Task 1: Ký thông điệp và kiểm tra
print("\n--- TASK 1: Ký thông điệp (Kiểm tra chữ ký) ---")
msg = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 3")
sig = Account.sign_message(msg, acct.key)
print("Chữ ký (r, s, v):")
print("r:", hex(sig.r))
print("s:", hex(sig.s))
print("v:", sig.v)
print(" Khi chạy lệnh này nhiều lần, chúng ta sẽ thấy chuỗi r, s, v này luôn CỐ ĐỊNH giống hệt nhau.")

# Khôi phục địa chỉ hợp lệ
print("\n--- Khôi phục địa chỉ từ chữ ký hợp lệ ---")
who = Account.recover_message(msg, signature=sig.signature)
print("Địa chỉ khôi phục được :", who)
print("Khớp với ví ban đầu?   :", who == acct.address)

# Task 2: Chỉnh sửa thông điệp (Tampered)
print("\n--- TASK 2: Thông điệp bị sửa 1 ký tự (Tính toàn vẹn) ---")
bad = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 4")
bad_who = Account.recover_message(bad, signature=sig.signature)
print("Thông điệp sai khôi phục ra địa chỉ:", bad_who)
print("Khớp với ví ban đầu?                 :", bad_who == acct.address)
print("-> Kết luận Task 2: Vì địa chỉ khôi phục sai hoàn toàn so với gốc, nên phát hiện được dữ liệu bị sửa đổi!")
