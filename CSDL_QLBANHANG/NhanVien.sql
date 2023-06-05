﻿--NHANVIEN
-- Xem thông tin
USE QLDatMon
IF OBJECT_ID('usp_XemThongTin') IS NOT NULL
	DROP PROC usp_XemThongTin
go
CREATE PROC usp_XemThongTin
AS
BEGIN TRANSACTION
	BEGIN TRY
		IF NOT EXISTS (SELECT MANV 
					   FROM NHANVIEN
					   WHERE MANV=CURRENT_USER)
		BEGIN
			PRINT N'Mã nhân viên không hợp lệ'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		SELECT* 
		FROM NHANVIEN
		WHERE MANV=CURRENT_USER
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
go

-- Xem danh sách đăng ký thông tin
USE QLDatMon
IF OBJECT_ID('usp_XemDanhSachDangKi') IS NOT NULL
	DROP PROC usp_XemDanhSachDangKi
go
CREATE PROC usp_XemDanhSachDangKi
AS
BEGIN TRANSACTION
	BEGIN TRY
		IF NOT EXISTS (SELECT MANV 
					   FROM NHANVIEN
					   WHERE MANV=CURRENT_USER)
		BEGIN
			PRINT N'Mã nhân viên không hợp lệ'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		SELECT* 
		FROM DANGKYTHONGTIN 
		WHERE MANV IS NULL
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
go

-- Xem danh sách hợp đồng đã lập
USE QLDatMon
IF OBJECT_ID('usp_XemHopDongDaLap') IS NOT NULL
	DROP PROC usp_XemHopDongDaLap
go
CREATE PROC usp_XemHopDongDaLap
AS
BEGIN TRANSACTION
	BEGIN TRY
		IF NOT EXISTS (SELECT MANV 
					   FROM NHANVIEN
					   WHERE MANV=CURRENT_USER)
		BEGIN
			PRINT N'Mã nhân viên không hợp lệ'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		SELECT* FROM HOPDONG where MANV = CURRENT_USER
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
go

-- Duyệt hợp đồng
USE QLDatMon
IF OBJECT_ID('usp_DuyetHopDong') IS NOT NULL
	DROP PROC usp_DuyetHopDong
go
CREATE PROC usp_DuyetHopDong
	@MAHD CHAR(8)
AS
BEGIN TRANSACTION
	BEGIN TRY
		IF NOT EXISTS (SELECT MANV 
					   FROM NHANVIEN
					   WHERE MANV=CURRENT_USER)
		BEGIN
			PRINT N'Mã nhân viên không hợp lệ'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		IF EXISTS(SELECT MAHD from HOPDONG where MAHD = @MAHD and MANV is not null)
		BEGIN
			PRINT N'Hợp đồng đã được duyệt'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		update HOPDONG
		set MANV = CURRENT_USER
		where MAHD = @MAHD
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
go

-- Danh sách sắp hết hạn hợp đồng
USE QLDatMon
IF OBJECT_ID('usp_DanhSachHopDongSapHetHan') IS NOT NULL
	DROP PROC usp_DanhSachHopDongSapHetHan
go
CREATE PROC usp_DanhSachHopDongSapHetHan
AS
BEGIN TRANSACTION
	BEGIN TRY
		IF NOT EXISTS (SELECT MANV 
					   FROM NHANVIEN
					   WHERE MANV=CURRENT_USER)
		BEGIN
			PRINT N'Mã nhân viên không hợp lệ'
			ROLLBACK TRANSACTION
			RETURN 0
		END
		
		SELECT* 
		FROM HOPDONG
		WHERE datediff(day, getdate(), NGAYHETHAN) >= 0 and datediff(day, getdate(), NGAYHETHAN) <= 30
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Kiểm tra hợp đồng sắp hết hạng
USE QLDatMon
IF OBJECT_ID('usp_KiemTraHopDongSapHetHan') IS NOT NULL
	DROP PROC usp_KiemTraHopDongSapHetHan
go
CREATE PROC usp_KiemTraHopDongSapHetHan
	@MAHD CHAR(8)
AS
BEGIN TRANSACTION
	BEGIN TRY
		IF NOT EXISTS (SELECT MANV 
					   FROM NHANVIEN
					   WHERE MANV=CURRENT_USER)
		BEGIN
			PRINT N'Mã nhân viên không hợp lệ'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra mã hợp đồng có tồn tại không
		IF NOT EXISTS(SELECT MAHD
					  FROM dbo.HOPDONG
					  WHERE MAHD = @MAHD)
		BEGIN
			PRINT N'Mã hợp đồng không tồn tại'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		SELECT* 
		FROM HOPDONG
		WHERE MAHD=@MAHD AND datediff(day, getdate(), NGAYHETHAN) >= 0 and DATEDIFF(day, getdate(), NGAYHETHAN) <= 30 
	END TRY
	BEGIN CATCH
		ROLLBACK TRANSACTION
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Gia hạn hợp đồng
USE QLDatMon
IF OBJECT_ID('usp_GiaHanHopDong') IS NOT NULL
	DROP PROC usp_GiaHanHopDong
GO
CREATE  PROC usp_GiaHanHopDong
	@MAHD CHAR(8),
	@THOIGIANGIAHAN INT
AS
BEGIN TRANSACTION
	BEGIN TRY
		IF NOT EXISTS (SELECT MANV 
					   FROM NHANVIEN
					   WHERE MANV=CURRENT_USER)
		BEGIN
			PRINT N'Mã nhân viên không hợp lệ'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra mã hợp đồng có tồn tại không
		IF NOT EXISTS(SELECT MAHD
					  FROM dbo.HOPDONG
					  WHERE MAHD = @MAHD)
		BEGIN
			PRINT N'Mã hợp đồng không tồn tại'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		UPDATE HOPDONG 
		SET NGAYHETHAN=DATEADD(mm, @THOIGIANGIAHAN, NGAYHETHAN), MANV = CURRENT_USER
		WHERE MAHD=@MAHD
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO
