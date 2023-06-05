USE QLDatMon

-- Tạo index trên bảng DangKyThongTin
CREATE NONCLUSTERED INDEX IX_DangKyThongTin_MaNV ON dbo.DANGKYTHONGTIN(MANV)

-- Tạo index trên bảng HopDong
CREATE NONCLUSTERED INDEX IX_HopDong_MaNV ON dbo.HOPDONG(MANV)