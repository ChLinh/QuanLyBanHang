-- Đối tác
-- 1. Ngày hết hạn họp đồng phải lớn hơn ngày lập hợp đồng
use QLDatMon
go
if OBJECT_ID('trg_KTNgayHetHan') is not null
	drop trigger trg_KTNgayHetHan
go
create trigger trg_KTNgayHetHan
on dbo.HOPDONG
for insert, update
as
	IF UPDATE(NGAYLAP) OR UPDATE(NGAYHETHAN)
	begin
		if(exists(SELECT i.MAHD
				  FROM inserted i
				  WHERE i.THOIGIANLAPLAP > i.NGAYHETHAN))
		BEGIN
			RAISERROR('Ngày hết hạn phải lớn hơn ngày lập.', 16, 1)
			ROLLBACK
		END
	END
GO

-- 2. Mã số thuế unique
ALTER TABLE dbo.HOPDONG
ADD UNIQUE (MATHUE)

-- 3. Giới hạn thời gian cập nhật tên cửa hàng trong vòng 30 ngày kể từ ngày lập hợp đồng
use QLDatMon
go
if OBJECT_ID('trg_KTSuaTenQuan') is not null
	drop trigger trg_KTSuaTenQuan
go
create trigger trg_KTSuaTenQuan
on dbo.DOITAC
for update
as
	IF UPDATE(TENQUAN)
	begin
		if(exists(SELECT i.MADT
				  from inserted i JOIN dbo.HOPDONG hd ON i.MAHD = hd.MAHD
				  where datediff(day, hd.THOIGIANLAP, getdate()) > 30))
		begin
			raiserror('Đã quá 30 ngày kể từ khi lập hợp đồng nên không thể đổi tên.', 16, 1)
			rollback
		end
	end
GO

-- 4. Địa chỉ chi nhánh của đối tác phải nằm trong danh sách chi nhánh của hợp đồng
--use QLDatMon
--go
--if OBJECT_ID('trg_KTDiaChiChiNhanh') is not null
--	drop trigger trg_KTDiaChiChiNhanh
--go
--create trigger trg_KTDiaChiChiNhanh
--on dbo.CHINHANHCH
--for insert
--as
--	if(exists(select i.madt
--			  FROM inserted i JOIN dbo.DOITAC dt ON dt.MADT = i.MADT
--			  JOIN dbo.HOPDONG hd on hd.MAHD = dt.MAHD
--			  WHERE i.DIACHICH NOT IN (SELECT CN.DIACHI
--									   FROM dbo.CHINHANH CN
--									   WHERE CN.MAHD = DT.MAHD)))
--	begin
--		raiserror('Địa chỉ chi nhánh không nằm trong hợp đồng.', 16, 1)
--		ROLLBACK
--	end
--GO

-- 5. Tình trạng của cửa hàng phải là 1 “Mở cửa”, 0 “Tạm nghỉ”, -1 “ Đóng cửa”
use QLDatMon
go
if OBJECT_ID('trg_KTTinhTrangChiNhanh') is not null
	drop trigger trg_KTTinhTrangChiNhanh
go
create trigger trg_KTTinhTrangChiNhanh
on dbo.CHINHANHCH
for INSERT, update
AS
	IF UPDATE(TINHTRANG)
	begin
		IF EXISTS(SELECT i.MADT
				  FROM inserted i
				  WHERE i.TINHTRANG NOT IN(1, 0, -1))
		begin
			raiserror('Tình trạng chi nhánh không hợp lệ', 16, 1)
			ROLLBACK
		END
    end
GO

-- 6. Tình trạng món ăn phải là 1 “Có bán”, 0 “Hết hàng”, -1 “Tạm ngưng”
use QLDatMon
go
if OBJECT_ID('trg_KTTinhTrangMonAn') is not null
	drop trigger trg_KTTinhTrangMonAn
go
create trigger trg_KTTinhTrangMonAn
on dbo.MONAN
for INSERT, update
AS
	IF UPDATE(TINHTRANG)
	begin
		IF EXISTS(select*
				  FROM inserted i
				  WHERE i.TINHTRANG NOT IN(1, 0, -1))
		begin
			raiserror('Tình trạng món ăn không hợp lệ', 16, 1)
			ROLLBACK
		END
    end
GO

-- 7. Tình trạng đơn hàng phải là NULL, “Đang chờ tiếp nhận”, “Đang vận chuyển”, “Đã giao hàng”, “Đã hủy”
use QLDatMon
go
if OBJECT_ID('trg_KTTinhTrangDonHang') is not null
	drop trigger trg_KTTinhTrangDonHang
go
create trigger trg_KTTinhTrangDonHang
on dbo.DONHANG
for INSERT, update
AS
	IF UPDATE(TRANGTHAI)
	begin
		IF EXISTS(select*
				  FROM inserted i
				  WHERE i.TRANGTHAI not in (-1, 0, 1, 2, 3))
		begin
			raiserror('Trạng thái đơn hàng không hợp lệ', 16, 1)
			ROLLBACK
		END
    end
GO

-- 8. Số lượng món ăn phải >= 0
use QLDatMon
go
if OBJECT_ID('trg_KTSoLuongMonAn') is not null
	drop trigger trg_KTSoLuongMonAn
go
create trigger trg_KTSoLuongMonAn
on dbo.MONAN
for INSERT, update
AS
	IF UPDATE(SoLuongHienCo)
	begin
		IF EXISTS(SELECT i.MADT
				  FROM inserted i
				  WHERE i.SoLuongHienCo < 0)
		begin
			raiserror('Số lượng hiện có phải >= 0', 16, 1)
			ROLLBACK
		END
    end
GO

-- 9. Tổng giá = (Tổng giá chi tiết đơn hàng) + Phí vận chuyển
use QLDatMon
go
if OBJECT_ID('trg_TinhTongGia') is not null
	drop trigger trg_TinhTongGia
go
create trigger trg_TinhTongGia
on dbo.DONHANG
for update
AS
	IF UPDATE(PHISP) OR UPDATE(PHIVANCHUYEN)
	begin
		DECLARE @madon CHAR(8)

		SELECT @madon = i.MADON
        FROM Inserted i

		UPDATE dbo.DONHANG SET TONGTIEN = PHIVANCHUYEN + PHISP WHERE MADON = @madon
    end
GO

-- 10. Số lượng chi nhánh trong hợp đồng bằng số lượng chi nhánh khai báo
use QLDatMon
go
if OBJECT_ID('trg_TinhSLChiNhanh') is not null
	drop trigger trg_TinhSLChiNhanh
go
create trigger trg_TinhSLChiNhanh
on dbo.CHINHANH
for INSERT
AS
	DECLARE @mahd CHAR(8)
	DECLARE @soCN int
	
	SELECT @mahd = i.MAHD, @soCN = COUNT(*)
    FROM Inserted i JOIN dbo.CHINHANH cn on cn.MAHD = i.MAHD
	GROUP BY i.MAHD

    UPDATE dbo.HOPDONG SET SOCHINHANH = @soCN WHERE MAHD = @mahd
GO

-- 11. Thời gian đóng cửa phải lớn hơn thời gian mở cửa trong chi nhánh
use QLDatMon
go
if OBJECT_ID('trg_KTThoiGian') is not null
	drop trigger trg_KTThoiGian
go
create trigger trg_KTThoiGian
on dbo.CHINHANHCH
for insert, UPDATE
as
	IF UPDATE(THOIGIANDONGCUA) OR UPDATE(THOIGIANMOCUA)
	begin
		if(exists(select*
				  FROM inserted i
				  WHERE convert(datetime, i.THOIGIANMOCUA, 8) > convert(datetime, i.THOIGIANDONGCUA, 8)))
		BEGIN
			RAISERROR('Thời gian đóng cửa phải lớn hơn thời gian mở cửa.', 16, 1)
			ROLLBACK
		END
	END
GO

-- 12. Mã đối tác trong chi tiết đơn hàng phải giống mã đối tác trong đơn hàng
use QLDatMon
go
if OBJECT_ID('trg_KTMaDT') is not null
	drop trigger trg_KTMaDT
go
create trigger trg_KTMaDT
on dbo.CHITIETDONHANG
for insert, UPDATE
as
	IF UPDATE(MADT)
	begin
		IF EXISTS(SELECT i.MADON
				  FROM inserted i JOIN dbo.DONHANG dh ON i.MADON = dh.MADON
				  WHERE dh.MADT != i.MADT)
		BEGIN
			RAISERROR('Mã đối tác trong chi tiết đơn hàng phải giống mã đối tác trong đơn hàng.', 16, 1)
			ROLLBACK
		END
	END
GO

-- 14. Giá trị của thanh toán trong đơn hàng phải là "Chuyển khoản" hoặc "Tiền mặt"
use QLDatMon
go
if OBJECT_ID('trg_KTThanhToan') is not null
	drop trigger trg_KTThanhToan
go
create trigger trg_KTThanhToan
on dbo.DONHANG
for insert, UPDATE
as
	IF UPDATE(THANHTOAN)
	begin
		IF EXISTS(SELECT i.MADON
				  FROM inserted i
				  WHERE i.THANHTOAN NOT IN (N'Chuyển khoản', N'Tiền mặt'))
		BEGIN
			RAISERROR('Giá trị của thanh toán không hợp lệ.', 16, 1)
			ROLLBACK
		END
	END
GO

-- Khách hàng
-- 1. Email unique
ALTER TABLE dbo.KHACHHANG
ADD UNIQUE (EMAIL)

-- Tài xế
-- 1. Biển số xe là duy nhất
ALTER TABLE dbo.TAIXE
ADD UNIQUE (BIENSO)

-- Nhân viên
-- 1. Loại nhân viên phải là “Nhân viên” hoặc “Quản trị”
use QLDatMon
go
if OBJECT_ID('trg_KTTinhTrangNhanVien') is not null
	drop trigger trg_KTTinhTrangNhanVien
go
create trigger trg_KTTinhTrangNhanVien
on dbo.NHANVIEN
for INSERT, update
AS
	IF UPDATE(LOAINV)
	begin
		IF EXISTS(select*
				  FROM inserted i
				  WHERE i.LOAINV not in (N'Nhân viên', N'Quản trị'))
		begin
			raiserror('Loại nhân viên không hợp lệ', 16, 1)
			ROLLBACK
		END
    end
GO

-- Tài khoản ngân hàng
-- 1. Số dư tài khoản phải >= 0
use QLDatMon
go
if OBJECT_ID('trg_KTSoDuTK') is not null
	drop trigger trg_KTSoDuTK
go
create trigger trg_KTSoDuTK
on dbo.TAIKHOANNH
for INSERT, update
AS
	IF UPDATE(SODU)
	begin
		IF EXISTS(select*
				  FROM inserted i
				  WHERE i.SODU < 0)
		begin
			raiserror('Số dư phải >= 0', 16, 1)
			ROLLBACK
		END
    end
GO