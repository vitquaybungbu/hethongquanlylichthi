from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quan_ly_thi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# THÊM DÒNG NÀY (Bắt buộc để dùng tính năng thông báo lỗi của Flask)
app.secret_key = 'mot_chuoi_ky_tu_bi_mat_bat_ky' 

db = SQLAlchemy(app)

# http://127.0.0.1:5000/ để chạy ứng dụng

# =======================================
# Phần 1: Định nghĩa các lớp (OOP MODELS)
# =======================================

class CanBo(db.Model):
    __tablename__ = 'can_bo'
    id = db.Column(db.Integer, primary_key=True)
    ma_cb = db.Column(db.String(20), unique=True, nullable=False)
    ten_cb = db.Column(db.String(100), nullable=False)
    vai_tro = db.Column(db.String(50)) # Giá trị có thể là "Giảng dạy", "Coi thi", "Khác"

    # Liên kết với bảng phân công 
    phan_cong = db.relationship('PhanCong', backref='can_bo', lazy=True)

class LichThi(db.Model):
    __tablename__ = 'lich_thi'
    id = db.Column(db.Integer, primary_key=True)
    ma_lop = db.Column(db.String(50), nullable=False)
    ma_hp = db.Column(db.String(20), nullable=False)
    ten_hp = db.Column(db.String(100), nullable=False)
    ngay_thi = db.Column(db.String(20), nullable=False) # Dạng YYYY-MM-DD
    gio_thi = db.Column(db.String(20))
    kip_thi = db.Column(db.Integer, nullable=False)
    si_so = db.Column(db.Integer, nullable=False)
    phong_thi = db.Column(db.String(50))

    # Ba cột mới thêm cho kinh phí
    thu = db.Column(db.Integer, default=0)
    chi = db.Column(db.Integer, default=0)
    ghi_chu_kinh_phi = db.Column(db.String(200), default="")

    # Liên kết với bảng phân công
    phan_cong = db.relationship('PhanCong', backref='lich_thi', lazy=True)

    # Một phương thức OOP cơ bản để xác định số cán bộ cần thiết
    def so_luong_can_bo_yeu_cau(self):
        if self.si_so >= 60:
            return 2
        return 1

class PhanCong(db.Model):
    __tablename__ = 'phan_cong'
    id = db.Column(db.Integer, primary_key=True)
    lich_thi_id = db.Column(db.Integer, db.ForeignKey('lich_thi.id'), nullable=False)
    can_bo_id = db.Column(db.Integer, db.ForeignKey('can_bo.id'), nullable=False)
    nhiem_vu = db.Column(db.String(50)) # Ví dụ: "Cán bộ 1", "Cán bộ 2"

# =======================================
# PHẦN 2: ROUTES (XỬ LÝ GIAO DIỆN WEB)
# =======================================

@app.route('/', methods=['GET', 'POST'])
def trang_chu():
    # 1. Nếu người dùng bấm nút "Thêm vào danh sách" (Hành động POST)
    if request.method == 'POST':
        # Lấy dữ liệu từ các ô input trên web
        ma = request.form['ma_cb']
        ten = request.form['ten_cb']
        vai_tro = request.form['vai_tro']

        # Áp dụng OOP: Tạo một "Đối tượng" (Object) Cán bộ mới
        can_bo_moi = CanBo(ma_cb=ma, ten_cb=ten, vai_tro=vai_tro)
        
        # Đưa vào Database và lưu lại
        db.session.add(can_bo_moi)
        db.session.commit()
        
        # Lưu xong thì tự động load lại trang chủ
        return redirect(url_for('trang_chu'))

        pass

    # 2. Nếu người dùng chỉ vào xem web bình thường (Hành động GET)
    # Lấy toàn bộ danh sách cán bộ đang có trong Database
    danh_sach = CanBo.query.all()
    danh_sach_lt = LichThi.query.all()
    
    # Render ra file HTML và truyền danh sách sang cho HTML hiển thị
    return render_template('index.html', danh_sach_cb=danh_sach, danh_sach_lt=danh_sach_lt)

# TẠO THÊM ROUTE MỚI ĐỂ XỬ LÝ IMPORT EXCEL
@app.route('/import_excel', methods=['POST'])
def import_excel():
    # Lấy file người dùng upload
    file = request.files['file_excel']
    
    if file:
        # Đọc trực tiếp file Excel vào bộ nhớ bằng pandas
        df = pd.read_excel(file)

        # Xóa toàn bộ khoảng trắng thừa ở đầu/cuối của tên cột
        df.columns = df.columns.str.strip()
        
        # Vòng lặp đọc từng dòng trong Excel và biến thành Object LichThi
        for index, row in df.iterrows():
            ngay_thi_raw = str(row['Ngày thi'])
            ngay_thi_chuan = ngay_thi_raw.split(' ')[0]
            
            gio_thi_raw = str(row.get('Giờ thi', ''))
            # Nếu chuỗi có chứa dấu ':', ta cắt nó ra và chỉ ghép lại 2 phần đầu (Giờ và Phút)
            if ':' in gio_thi_raw:
                gio_thi_chuan = ':'.join(gio_thi_raw.split(':')[:2])
            else:
                gio_thi_chuan = gio_thi_raw

            lt = LichThi(
                ma_lop=str(row['Mã lớp']),
                ma_hp=str(row['Mã HP']),
                ten_hp=str(row['Tên HP']),
                ngay_thi=str(ngay_thi_chuan),
                gio_thi=str(gio_thi_chuan),
                kip_thi=int(row['Kíp']),
                si_so=int(row['Sĩ số']),
                phong_thi=str(row['Phòng'])
            )
            db.session.add(lt)
        
        # Lưu toàn bộ vào Database
        db.session.commit()
        
    return redirect(url_for('trang_chu'))

@app.route('/them_lich_thi', methods=['POST'])
def them_lich_thi():
    # Lấy dữ liệu từ form HTML
    ma_lop = request.form.get('ma_lop')
    ma_hp = request.form.get('ma_hp')
    ten_hp = request.form.get('ten_hp')
    ngay_thi = request.form.get('ngay_thi')
    gio_thi = request.form.get('gio_thi') # Lấy thêm giờ thi
    kip_thi = request.form.get('kip_thi')
    si_so = request.form.get('si_so')
    phong_thi = request.form.get('phong_thi')

    # Tạo đối tượng LichThi mới
    lich_moi = LichThi(
        ma_lop=str(ma_lop),
        ma_hp=str(ma_hp),
        ten_hp=str(ten_hp),
        ngay_thi=str(ngay_thi),
        gio_thi=str(gio_thi),
        kip_thi=int(kip_thi),
        si_so=int(si_so),
        phong_thi=str(phong_thi)
    )
    
    # Lưu vào Database
    db.session.add(lich_moi)
    db.session.commit()
    
    flash("Đã thêm lịch thi thủ công thành công!", "success")
    return redirect(url_for('trang_chu'))

@app.route('/phan_cong/<int:id>', methods=['GET', 'POST'])
def phan_cong(id):
    lich = LichThi.query.get_or_404(id)

    # Bước 1: Tìm ID của những cán bộ ĐÃ CÓ LỊCH gác thi vào đúng ngày và kíp này
    can_bo_ban = db.session.query(PhanCong.can_bo_id).join(LichThi).filter(
        LichThi.ngay_thi == lich.ngay_thi,
        LichThi.kip_thi == lich.kip_thi
    ).all()
    
    # Dữ liệu trả về là một danh sách các tuple [(1,), (3,)], ta bóc nó ra thành list ID bình thường [1, 3]
    danh_sach_id_ban = [cb[0] for cb in can_bo_ban]
    
    # Bước 2: Lấy danh sách cán bộ thỏa mãn điều kiện KHÔNG NẰM TRONG danh sách ID bận ở trên
    if danh_sach_id_ban:
        # Nếu có người bận, thì dùng dấu ~ (NOT) để loại trừ họ ra
        danh_sach_cb_ranh = CanBo.query.filter(~CanBo.id.in_(danh_sach_id_ban)).all()
    else:
        # Nếu chưa ai bận ca này thì lấy toàn bộ danh sách
        danh_sach_cb_ranh = CanBo.query.all()
    
    # 1. Đếm số lượng cán bộ đã được phân công vào ca này
    danh_sach_da_phan_cong = PhanCong.query.filter_by(lich_thi_id=lich.id).all()
    so_luong_da_phan_cong = len(danh_sach_da_phan_cong)
    so_luong_yeu_cau = lich.so_luong_can_bo_yeu_cau()

    if request.method == 'POST':
        can_bo_id = request.form.get('can_bo_id')
        
        # 2. Chặn lỗi: Cố tình thêm khi đã đủ người
        if so_luong_da_phan_cong >= so_luong_yeu_cau:
            flash("Ca thi này đã đủ cán bộ coi thi!", "warning")
            return redirect(url_for('phan_cong', id=lich.id))

        # 3. Chặn lỗi: Chọn 1 người 2 lần cho cùng 1 ca thi
        da_co_trong_ca_nay = PhanCong.query.filter_by(lich_thi_id=lich.id, can_bo_id=can_bo_id).first()
        if da_co_trong_ca_nay:
            flash("Cán bộ này đã được phân công vào ca này rồi!", "danger")
            return redirect(url_for('phan_cong', id=lich.id))

        # 4. Chặn lỗi: Trùng lịch với ca thi khác (giữ nguyên logic cũ)
        trung_lich = db.session.query(PhanCong).join(LichThi).filter(
            PhanCong.can_bo_id == can_bo_id,
            LichThi.ngay_thi == lich.ngay_thi,
            LichThi.kip_thi == lich.kip_thi
        ).first()

        if trung_lich:
            flash("Cán bộ này đã bị trùng lịch! Vui lòng chọn người khác.", "danger")
            return redirect(url_for('phan_cong', id=lich.id))

        da_co_trong_ca_nay = PhanCong.query.filter_by(lich_thi_id=lich.id, can_bo_id=can_bo_id).first()
        if da_co_trong_ca_nay:
            flash("Cán bộ này đã được phân công vào ca này rồi!", "danger")
            return redirect(url_for('phan_cong', id=lich.id))

        # 5. Nếu qua hết các vòng kiểm tra -> Lưu phân công mới
        pc_moi = PhanCong(lich_thi_id=lich.id, can_bo_id=can_bo_id, nhiem_vu="Coi thi")
        db.session.add(pc_moi)
        db.session.commit()
        
        flash("Phân công thành công!", "success")
        # Load lại trang này để người dùng xem đã đủ người chưa (thay vì về thẳng trang chủ)
        return redirect(url_for('phan_cong', id=lich.id)) 

    # Truyền thêm các biến đếm số lượng ra HTML
    return render_template('phan_cong.html', 
                           lich=lich, 
                           danh_sach_cb=danh_sach_cb_ranh,
                           danh_sach_da_phan_cong=danh_sach_da_phan_cong,
                           so_luong_yeu_cau=so_luong_yeu_cau,
                           so_luong_da_phan_cong=so_luong_da_phan_cong)

@app.route('/xoa_phan_cong/<int:id>', methods=['POST'])
def xoa_phan_cong(id):
    # Tìm bản ghi phân công trong Database dựa vào ID
    pc_can_xoa = PhanCong.query.get_or_404(id)
    
    # Lưu lại ID của lịch thi trước khi xóa để biết đường quay về đúng trang
    lich_id = pc_can_xoa.lich_thi_id
    
    # Xóa khỏi Database
    db.session.delete(pc_can_xoa)
    db.session.commit()
    
    # Hiện thông báo và quay lại trang phân công của ca thi đó
    flash("Đã hủy phân công cán bộ thành công!", "success")
    return redirect(url_for('phan_cong', id=lich_id))

@app.route('/thong_ke')
def thong_ke():
    # Lấy toàn bộ danh sách cán bộ
    danh_sach_cb = CanBo.query.all()
    
    # Sắp xếp tùy chọn: Nếu bạn muốn người gác thi nhiều nhất hiện lên đầu, 
    # có thể dùng hàm sort của Python. Ở đây ta truyền thẳng ra giao diện.
    return render_template('thong_ke.html', danh_sach_cb=danh_sach_cb)

@app.route('/kinh_phi')
def quan_ly_kinh_phi():
    danh_sach_lt = LichThi.query.all()
    # Tính tổng thu và tổng chi của toàn bộ hệ thống
    tong_thu = sum((lt.thu or 0) for lt in danh_sach_lt)
    tong_chi = sum((lt.chi or 0) for lt in danh_sach_lt)
    
    return render_template('kinh_phi.html', danh_sach_lt=danh_sach_lt, tong_thu=tong_thu, tong_chi=tong_chi)

@app.route('/cap_nhat_kinh_phi/<int:id>', methods=['POST'])
def cap_nhat_kinh_phi(id):
    lich = LichThi.query.get_or_404(id)
    
    # Lấy dữ liệu từ form, nếu bỏ trống thì mặc định là 0
    thu_moi = request.form.get('thu', type=int)
    chi_moi = request.form.get('chi', type=int)
    
    lich.thu = thu_moi if thu_moi is not None else 0
    lich.chi = chi_moi if chi_moi is not None else 0
    lich.ghi_chu_kinh_phi = request.form.get('ghi_chu_kinh_phi', '')
    
    db.session.commit()
    flash(f"Đã cập nhật kinh phí cho lớp {lich.ma_lop} thành công 🦆!", "success")
    return redirect(url_for('quan_ly_kinh_phi'))

@app.route('/xoa_can_bo/<int:id>', methods=['POST'])
def xoa_can_bo(id):
    cb_can_xoa = CanBo.query.get_or_404(id)
    
    # 1. Xóa toàn bộ các phân công gác thi liên quan đến cán bộ này trước
    PhanCong.query.filter_by(can_bo_id=cb_can_xoa.id).delete()
    
    # 2. Xóa cán bộ khỏi hệ thống
    db.session.delete(cb_can_xoa)
    db.session.commit()
    
    flash(f"Đã xóa cán bộ {cb_can_xoa.ten_cb} và các lịch gác liên quan!", "success")
    return redirect(url_for('trang_chu'))

@app.route('/xoa_lich_thi/<int:id>', methods=['POST'])
def xoa_lich_thi(id):
    lt_can_xoa = LichThi.query.get_or_404(id)
    
    # 1. Xóa toàn bộ các phân công gác thi liên quan đến ca thi này
    PhanCong.query.filter_by(lich_thi_id=lt_can_xoa.id).delete()
    
    # 2. Xóa lịch thi
    db.session.delete(lt_can_xoa)
    db.session.commit()
    
    flash(f"Đã xóa lịch thi lớp {lt_can_xoa.ma_lop} thành công!", "success")
    return redirect(url_for('trang_chu'))

# =======================================
# PHẦN 3: CHẠY ỨNG DỤNG
# =======================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)