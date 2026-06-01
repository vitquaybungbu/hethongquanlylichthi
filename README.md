# 🦆 Hệ thống Quản lý Lịch thi & Phân công Coi thi (Exam Proctoring Management System)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

Dự án môn học **Lập trình Hướng đối tượng (OOP)**. Đây là một hệ thống nền tảng Web được xây dựng nhằm giải quyết triệt để bài toán sắp xếp lịch gác thi, loại bỏ lỗi trùng lịch, và tự động hóa quy trình quản lý tài chính cho công tác khảo thí tại các trường Đại học.

## ✨ Tính năng nổi bật

* **📊 Import/Export dữ liệu thông minh:** Đọc trực tiếp dữ liệu lịch thi từ file Excel (.xlsx) thông qua thư viện `pandas` với khả năng tự động chuẩn hóa dữ liệu.
* **🛡️ Thuật toán chống trùng lịch:** Áp dụng giải thuật lọc dữ liệu thời gian thực (Real-time Exclusion). Tự động loại bỏ các cán bộ đang bận hoặc đã được phân công khỏi danh sách lựa chọn, chặn đứng 100% lỗi trùng ngày/kíp thi.
* **👥 Phân bổ nhân sự tự động:** Đóng gói logic OOP để tự động tính toán số lượng cán bộ cần thiết dựa trên sĩ số sinh viên (≥60 SV yêu cầu 2 cán bộ).
* **💰 Quản lý Tài chính:** Theo dõi dòng tiền thu/chi, lệ phí thi và thù lao coi thi theo từng ca thi cụ thể, tự động tính toán tổng lũy kế toàn hệ thống.
* **📈 Báo cáo Thống kê:** Theo dõi năng suất và đếm tổng số ca gác thi của từng giảng viên để phục vụ nghiệm thu minh bạch.

## 🛠️ Công nghệ sử dụng (Tech Stack)

* **Backend:** Python, Flask 
* **Database:** SQLite, SQLAlchemy (ORM)
* **Data Processing:** Pandas, Openpyxl
* **Frontend:** HTML5, CSS3, Bootstrap 5, Jinja2

## 🚀 Hướng dẫn Cài đặt & Khởi chạy

Làm theo các bước sau để chạy dự án trên máy tính cục bộ của bạn:

**1. Clone kho lưu trữ này về máy:**
```bash
git clone [https://github.com/vitquaybungbu/hethongquanlylichthi.git](https://github.com/vitquaybungbu/hethongquanlylichthi.git)
cd hethongquanlylichthi
```
**2. Cài đặt các thư viện cần thiết:**
Mở Terminal tại thư mục dự án và chạy lệnh sau:

```bash
pip install flask flask-sqlalchemy pandas openpyxl
```
**3. Khởi động Server:**

```bash
python app.py
```
**4. Truy cập hệ thống:**
Mở trình duyệt web và truy cập vào địa chỉ:
```bash
http://127.0.0.1:5000/
```
📁 Cấu trúc Thư mục (Project Structure)
```bash
📦 HeThongLichThi
 ┣ 📂 templates/           # Chứa giao diện Web (Frontend)
 ┃ ┣ 📜 index.html         # Trang chủ (Quản lý Cán bộ & Lịch thi)
 ┃ ┣ 📜 phan_cong.html     # Giao diện thuật toán phân công
 ┃ ┣ 📜 thong_ke.html      # Giao diện báo cáo hiệu suất
 ┃ ┗ 📜 kinh_phi.html      # Giao diện quản lý thu/chi
 ┣ 📜 app.py               # Chứa logic Backend, thuật toán OOP & Database Models
 ┣ 📜 quan_ly_thi.db       # Cơ sở dữ liệu SQLite (Tự động tạo)
 ┗ 📜 README.md            # Tài liệu dự án
 ```

👨‍💻 Đội ngũ phát triển (Nhóm Mr. Beast)
Đỗ Nguyễn Việt Anh (Leader) - Phân tích hệ thống & Fullstack

Nguyễn Thế Dương - Backend & Database

Đỗ Minh Đức - UI/UX & Frontend

Hòa Thị Mai Anh - Tester & Documentation

Dự án được phát triển phục vụ mục đích học thuật tại Trường Đại học Việt Nhật (VJU) - ĐHQGHN.
