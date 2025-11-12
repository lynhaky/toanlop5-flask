import random
from fractions import Fraction

def tao_cau_hoi():
    ds = [
        ("Tính 25 + 47 =", 72),
        ("3/5 + 2/5 =", "1"),
        ("Hình chữ nhật có chiều dài 8m, rộng 6m. Chu vi là:", 28),
        ("Giá trị của 0.25 x 100 là:", 25),
        ("Thể tích hình hộp 3x4x5 dm là:", 60),
        ("40% của 200 là:", 80),
        ("Trung bình cộng của 5, 10, 15 là:", 10),
        ("Một cửa hàng bán 20kg gạo, mỗi kg 18.000đ. Tổng là:", 360000),
        ("Tính 1/2 × 3/4 =", "3/8"),
        ("Hình vuông cạnh 5cm có diện tích:", 25),
    ]
    return random.sample(ds, 10)

def main():
    print("=== ỨNG DỤNG HỌC TOÁN LỚP 5 ===\n")
    cau_hoi = tao_cau_hoi()
    dung = 0
    for i, (q, dap_an) in enumerate(cau_hoi, start=1):
        tl = input(f"{i}. {q} ").strip()
        if str(tl) == str(dap_an):
            print("✅ Đúng!\n")
            dung += 1
        else:
            print(f"❌ Sai! Đáp án đúng là {dap_an}\n")
    print(f"🎯 Kết quả: {dung}/10 câu đúng ({dung*10} điểm)\n")

if __name__ == "__main__":
    main()
