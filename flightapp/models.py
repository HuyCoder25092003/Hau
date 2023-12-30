from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from flightapp import db, app
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class BaoCao(BaseModel):
    __tablename__ = 'bao_cao'
    danh_sach_bao_cao_theo_thang = relationship('BaoCaoTheoThang', backref='bao_cao', lazy=False)
    tuyen_bay = relationship('TuyenBay', secondary='chi_tiet_bao_cao',
                                 lazy='subquery', backref=backref('tuyen_bay', lazy=True))


class BaoCaoTheoThang(BaseModel):
    __tablename__ = 'bao_cao_theo_thang'
    ten_bao_cao = Column(String(30), nullable=False)
    bao_cao_id = Column(Integer, ForeignKey(BaoCao.id), nullable=False)


class NguoiDung(BaseModel):
    __abstract__ = True
    ten = Column(String(30), nullable=False)
    dien_thoai = Column(String(10), nullable=False)
    cccd = Column(String(12), nullable=False)


class KhachHang(NguoiDung):
    __tablename__ = 'khach_hang'
    chuyen_bay_id = relationship('ChuyenBay', secondary='ve',
                                 lazy='subquery', backref=backref('khach_hang', lazy=True))

    def __str__(self):
        return self.ten


class NhanVien(NguoiDung):
    __tablename__ = 'nhan_vien'
    ve = relationship('Ve', backref='nhan_vien', lazy=False)
    lich_chuyen_bay = relationship('LichChuyenBay', backref='nhan_vien', lazy=False)

    def __str__(self):
        return self.ten


class Admin(NguoiDung):
    __tablename__ = 'admin'
    quy_dinh_id = relationship('QuyDinh', backref='admin')

    def __str__(self):
        return self.ten


class Ve(BaseModel):
    __tablename__ = 've'
    khach_hang_id = Column(Integer, ForeignKey(KhachHang.id), primary_key=True)
    chuyen_bay_id = Column(Integer, ForeignKey('chuyen_bay.id'), primary_key=True)
    ten_ve = Column(String(30), nullable=False)
    gia_ve = Column(Float, default=0)
    ngay_xuat_ve = Column(DateTime, default=datetime.now())
    kich_hoat = Column(Boolean, default=True)
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    hang_ve_id = Column(Integer, ForeignKey('hang_ve.id'), nullable=False)
    ghe_id = Column(Integer, ForeignKey('ghe.id'), unique=True)

    def __str__(self):
        return self.ten_ve


class HangVe(BaseModel):
    __tablename__ = 'hang_ve'
    hang_ve = Column(Integer, nullable=False)
    ve = relationship('Ve', backref='hang_ve', lazy=False)
    ghe = relationship('Ghe', backref='hang_ve', lazy=False)

    def __str__(self):
        return self.hang_ve


class Ghe(BaseModel):
    __tablename__ = 'ghe'
    trang_thai = Column(String(10), nullable=False)
    hang_ve_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    may_bay_id = Column(Integer, ForeignKey('may_bay.id'), nullable=False)
    ve = relationship('Ve', backref='ghe', uselist=False)

    def __str__(self):
        return self.trang_thai


class MayBay(BaseModel):
    __tablename__ = 'may_bay'
    ten_may_bay = Column(String(30), nullable=False)
    ghe = relationship('Ghe', backref='may_bay', lazy=False)
    chuyen_bay = relationship('ChuyenBay', backref='may_bay', lazy=False)

    def __str__(self):
        return self.ten_may_bay


class ChuyenBay(BaseModel):
    __tablename__ = 'chuyen_bay'
    khoi_hanh = Column(DateTime, nullable=False)
    may_bay_id = Column(Integer, ForeignKey('may_bay.id'), nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey('tuyen_bay.id'), nullable=False)
    chuyen_bay_mot_chang = relationship('ChuyenbayMotChang', backref='chuyen_bay', lazy=False)
    chuyen_bay_nhieu_chang = relationship('ChuyenBayNhieuChang', backref='chuyen_bay', lazy=False)


class ChuyenbayMotChang(BaseModel):
    __tablename__ = 'chuyen_bay_1_chang'
    ten_chang_bay = Column(String(30), nullable=False)
    chang_bay = relationship('ChangBay', backref='chang_bay', uselist=False)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)

    def __str__(self):
        return self.ten_chang_bay


class ChuyenBayNhieuChang(BaseModel):
    __tablename__ = 'chuyen_bay_nhieu_chang'
    lich_chuyen_bay = relationship('LichChuyenBay', backref='chuyen_bay_nhieu_chang', lazy=False)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)


class LichChuyenBay(BaseModel):
    __tablename__ = 'lich_chuyen_bay'
    thoi_gian_bay = Column(Integer, default=0)
    chuyen_bay_nhieu_chang_id = Column(Integer, ForeignKey(ChuyenBayNhieuChang.id), nullable=False)
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)


class ChangBay(BaseModel):
    __tablename__ = 'chang_bay'
    chuyen_bay_1_chang = Column(Integer, ForeignKey(ChuyenbayMotChang.id), unique=True)
    san_bay_id = relationship('SanBay', backref='chang_bay')
    chuyen_bay_nhieu_chang = relationship('ChuyenBayNhieuChang', secondary='ghi_chu', lazy='subquery',
                                          backref=backref('chang_bay', lazy=True))


ghi_chu = db.Table('ghi_chu',
                   Column('chuyen_bay_nhieu_chang_id', Integer, ForeignKey(ChuyenBayNhieuChang.id),
                          primary_key=True),
                   Column('chang_bay_id', Integer, ForeignKey(ChangBay.id), primary_key=True)
                   )


class TuyenBay(BaseModel):
    __tablename__ = 'tuyen_bay'
    doanh_thu = Column(Float, default=0)
    so_luot_bay = Column(Integer, default=0)
    ty_le = Column(Float, default=0)
    chuyen_bay = relationship('ChuyenBay', backref='tuyen_bay', lazy=False)


class ChiTietBaoCao(BaseModel):
    __tablename__ = 'chi_tiet_bao_cao'
    bao_cao_theo_thang_id = Column(Integer, ForeignKey(BaoCao.id), primary_key=True)
    tuyen_bay_id = Column(Integer, ForeignKey(TuyenBay.id), primary_key=True)


class SanBay(BaseModel):
    __tablename__ = 'san_bay'
    ten_san_bay = Column(String(30), nullable=False)
    diaChi = Column(String(30), nullable=False)
    san_bay_di = Column(String(30), nullable=False)
    san_bay_den = Column(String(30), nullable=False)
    chang_bay_id = Column(Integer, ForeignKey(ChangBay.id), nullable=False)


class QuyDinh(BaseModel):
    __tablename__ = 'quy_dinh'
    admin_id = Column(Integer, ForeignKey(Admin.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        #  db.create_all()
        tuyen_bay_id = 1
        existing_tuyen_bay = db.session.query(TuyenBay).get(tuyen_bay_id)

        if not existing_tuyen_bay:
            tuyen_bay = TuyenBay(id=tuyen_bay_id, doanh_thu=0, so_luot_bay=0, ty_le=0)
            db.session.add(tuyen_bay)
            db.session.commit()
        else:
            tuyen_bay = existing_tuyen_bay

        # Tạo một đối tượng ChuyenBay
        khoi_hanh = datetime.now()
        khoi_hanh_str = khoi_hanh.strftime("%Y-%m-%d %H:%M:%S")

        chuyen_bay = ChuyenBay(khoi_hanh=khoi_hanh_str, may_bay_id=1, tuyen_bay_id=tuyen_bay_id)
        db.session.add(chuyen_bay)
        db.session.commit()

        # Tạo các đối tượng ChuyenbayMotChang và liên kết với ChuyenBay
        chuyen_bay_mot_chang_mot = ChuyenbayMotChang(ten_chang_bay='Tân Sơn Nhất', chuyen_bay_id=chuyen_bay.id)
        chuyen_bay_mot_chang_hai = ChuyenbayMotChang(ten_chang_bay='Noi Bai', chuyen_bay_id=chuyen_bay.id)
        db.session.add_all([chuyen_bay_mot_chang_mot, chuyen_bay_mot_chang_hai])
        db.session.commit()
