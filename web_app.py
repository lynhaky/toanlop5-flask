# ==========================================================
# 🧮 HỌC TOÁN LỚP 5 – SGK KẾT NỐI TRI THỨC (Hà Huy Khoái, Lê Anh Vinh)
# Phiên bản WebApp hoàn chỉnh – có hình minh họa, chấm điểm
# ==========================================================

from flask import Flask, render_template, request, url_for
import random, json, os

app = Flask(__name__)

# === Nạp dữ liệu SGK ===
DATA_PATH = os.path.join("data", "questions_ketnoitrituc.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    SGK_QUESTIONS = json.load(f)

# === Danh mục bài học theo SGK ===
Bai_MAP = {
    "1": {
        (1, 1): "1. Ôn tập và bổ sung",
        (2, 2): "2. Số thập phân",
        (3, 3): "3. Đơn vị đo diện tích",
        (4, 4): "4. Phép tính với số thập phân",
        (5, 5): "5. Hình phẳng",
        (6, 6): "6. Ôn tập học kì I"
    },
    "2": {
        (7, 7): "7. Tỉ số và tỉ lệ phần trăm",
        (8, 8): "8. Thể tích và đơn vị đo thể tích",
        (9, 9): "9. Diện tích và thể tích một số hình khối",
        (10, 10): "10. Thời gian - Vận tốc - Quãng đường",
        (11, 11): "11. Thống kê và xác suất",
        (12, 12): "12. Ôn tập cuối năm"
    }
}


# === Hàm hỗ trợ lấy chủ đề theo bài ===
def get_topics_for_range(part, bai_from, bai_to):
    topics = []
    pmap = Bai_MAP.get(part, {})
    for (start, end), topic in pmap.items():
        if start >= bai_from and end <= bai_to:
            topics.append(topic)
    return topics


# === Hàm tạo bộ câu hỏi ngẫu nhiên ===
def make_quiz(part="1", bai_from=1, bai_to=1, n=10):
    phan_key = "phan1" if part == "1" else "phan2"
    if phan_key not in SGK_QUESTIONS:
        return []

    topics = get_topics_for_range(part, bai_from, bai_to)
    pool = []

    if not topics:
        # Nếu không chọn bài cụ thể thì lấy toàn phần
        for items in SGK_QUESTIONS[phan_key].values():
            pool.extend(items)
    else:
        # Lấy đúng chủ đề theo bài
        for topic in topics:
            if topic in SGK_QUESTIONS[phan_key]:
                pool.extend(SGK_QUESTIONS[phan_key][topic])

    # Lấy ngẫu nhiên n câu
    selected = random.sample(pool, min(n, len(pool)))

    quiz = []
    for q in selected:
        quiz.append({
            "q": q["q"],
            "a": q["a"],
            "type": "text",
            "img": q.get("img", None)
        })
    return quiz


# === Trang chủ: chọn bài học ===
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        part = request.form.get("part", "1")
        bai_from = int(request.form.get("bai_from") or 1)
        bai_to = int(request.form.get("bai_to") or bai_from)
        n = int(request.form.get("n") or 10)

        quiz = make_quiz(part, bai_from, bai_to, n)
        return render_template(
            "quiz.html",
            quiz=quiz,
            part=part,
            bai_from=bai_from,
            bai_to=bai_to,
            graded=False
        )
    return render_template("index.html")


# === Trang chấm điểm ===
@app.route("/grade", methods=["POST"])
def grade():
    quiz = []
    i = 0
    while True:
        q = request.form.get(f"q{i}")
        if not q:
            break
        correct = request.form.get(f"correct{i}")
        user = request.form.get(f"user{i}", "").strip()
        quiz.append({"q": q, "correct": correct, "user": user})
        i += 1

    score = 0
    details = []
    for item in quiz:
        ok = item["user"].replace(",", ".") == item["correct"].replace(",", ".")
        if ok:
            score += 1
        details.append({
            "q": item["q"],
            "user": item["user"],
            "correct": item["correct"],
            "ok": ok
        })

    n = len(quiz)
    percent = round(score / n * 100, 1) if n > 0 else 0

    return render_template(
        "quiz.html",
        quiz=details,
        graded=True,
        score=score,
        n=n,
        percent=percent
    )


# === Chạy ứng dụng ===
if __name__ == "__main__":
    print("🚀 Học Toán Lớp 5 - SGK Kết nối tri thức (Hà Huy Khoái, Lê Anh Vinh)")
    print("📘 Truy cập: http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
