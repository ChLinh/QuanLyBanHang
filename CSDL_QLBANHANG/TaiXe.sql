-- usp_XemThongTinTaiXe
USE QLDatMon
GO
IF OBJECT_ID('usp_XemThongTinTaiXe') IS NOT NULL
	DROP PROC usp_XemThongTinTaiXe
GO
create proc usp_XemThongTinTaiXe
as
begin transaction
	begin try
		if not exists (select CMND from TAIXE where CMND = CURRENT_USER)
		begin
			print N'Không có thông tin tài xế này'
			rollback transaction
			return 0
		end

		select tx.*, tt.DIACHITX, tt.BIENSO, tt.EMAIL
		FROM TAIXE tx JOIN dbo.TTCHITIET_TAIXE tt ON tt.CMND = tx.CMND
		WHERE tx.CMND = CURRENT_USER
	end try

	begin catch
		print N'Lỗi hệ thống'
		rollback transaction
	end catch
commit transaction
return 1

go

-- usp_XemDanhSachDHTheoKhuVuc
IF OBJECT_ID('usp_XemDanhSachDHTheoKhuVuc') IS NOT NULL
	DROP PROC usp_XemDanhSachDHTheoKhuVuc
GO
create proc usp_XemDanhSachDHTheoKhuVuc
as
begin transaction
	begin try
		if not exists (select CMND from TAIXE where CMND = CURRENT_USER)
		begin
			print N'Không có thông tin tài xế này'
			rollback transaction
			return 0
		end

		SELECT dh.MADON, dh.TENKH, dh.TENTX, dh.TENDT, dh.DIACHICH, dh.THOIGIANLAP, dh.DIACHIGIAOHANG, dh.TRANGTHAI, dh.PHISP, dh.PHIVANCHUYEN, dh.TONGTIEN, dh.THANHTOAN, dh.THOIGIANGIAO
		FROM DONHANG dh
		WHERE dh.CMND IS NULL AND dh.TRANGTHAI = 1 AND dh.DIACHICH = (SELECT KHUVUCHD
																	  FROM TAIXE
															          WHERE CMND = CURRENT_USER)
	end try

	begin catch
		print N'Lỗi hệ thống'
		rollback transaction
	end catch
commit transaction
return 1
go

-- usp_XemDanhSachDHDaGiao
IF OBJECT_ID('usp_XemDanhSachDHDaGiao') IS NOT NULL
	DROP PROC usp_XemDanhSachDHDaGiao
GO
create proc usp_XemDanhSachDHDaGiao
as
begin transaction
	begin try
		-- Kiểm tra thông tin tài xế có tồn tại không
		if not exists (select CMND from TAIXE where CMND = CURRENT_USER)
		begin
			print N'Không có thông tin tài xế này'
			rollback transaction
			return 0
		END
    
		SELECT dh.MADON, dh.TENKH, dh.TENTX, dh.TENDT, dh.DIACHICH, dh.THOIGIANLAP, dh.DIACHIGIAOHANG, dh.TRANGTHAI, dh.PHISP, dh.PHIVANCHUYEN, dh.TONGTIEN, dh.THANHTOAN, dh.THOIGIANGIAO
		FROM DONHANG dh
		where dh.CMND = CURRENT_USER and dh.TRANGTHAI = 3
	end try

	begin catch
		print N'Lỗi hệ thống'
		rollback TRANSACTION
        RETURN 0
	end catch

commit transaction
return 1
GO

-- Chọn đơn hàng
IF OBJECT_ID('usp_ChonDonHang') IS NOT NULL
	DROP PROC usp_ChonDonHang
GO
create proc usp_ChonDonHang
	@MaDon char(8)
as
begin transaction
	begin try
		-- Kiểm tra thông tin tài xế có tồn tại không
		if not exists (select CMND from TAIXE where CMND = CURRENT_USER)
		begin
			print N'Không có thông tin tài xế này'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem đơn hàng có tồn tại không
		if not exists(SELECT MADON
					  from DONHANG
					  where MADON = @MaDon)
		begin 
			print N'Đơn hàng không tồn tại'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem đơn hàng có tài xế đặt chưa
		if exists(SELECT MADON
				  from DONHANG
				  where MADON = @MaDon and CMND is not null)
		begin 
			print N'Đơn hàng đã có tài xế'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem đơn hàng có nằm trong khu vực không
		if not exists (select MADON from DONHANG where @MaDon = MADON and DIACHICH = (select KHUVUCHD from TAIXE where CMND = CURRENT_USER))
		begin
			print N'Đơn hàng này không có sẵn ở khu vực này'
			rollback transaction
			return 0
		end
    
		-- Kiểm tra xem trạng thái đơn hàng có hợp lệ không
		if exists(select MADON from DONHANG where @MaDon = MADON AND TRANGTHAI != 1)
		begin
			print N'Trạng thái đơn hàng không hợp lệ'
			rollback transaction
			return 0
		END
        
		update DONHANG
		set CMND = CURRENT_USER, TRANGTHAI = 2
		where MADON = @MaDon
	end try

	begin catch
		print N'Lỗi hệ thống'
		rollback transaction
	end catch
commit transaction
return 1
GO

-- Xem đơn hàng đang giao
IF OBJECT_ID('usp_XemDanhSachDHDangGiao') IS NOT NULL
	DROP PROC usp_XemDanhSachDHDangGiao
GO
create proc usp_XemDanhSachDHDangGiao
as
begin transaction
	begin try
		-- Kiểm tra thông tin tài xế có tồn tại không
		if not exists (select CMND from TAIXE where CMND = CURRENT_USER)
		begin
			print N'Không có thông tin tài xế này'
			rollback transaction
			return 0
		END
    
		SELECT dh.MADON, dh.TENKH, dh.TENTX, dh.TENDT, dh.DIACHICH, dh.THOIGIANLAP, dh.DIACHIGIAOHANG, dh.TRANGTHAI, dh.PHISP, dh.PHIVANCHUYEN, dh.TONGTIEN, dh.THANHTOAN, dh.THOIGIANGIAO
		FROM DONHANG dh
		where dh.CMND = CURRENT_USER and dh.TRANGTHAI = 2
	end try

	begin catch
		print N'Lỗi hệ thống'
		rollback transaction
	end catch

commit transaction
return 1
GO

-- usp_TheoDoiThuNhap
IF OBJECT_ID('usp_TheoDoiThuNhap') IS NOT NULL
	DROP PROC usp_TheoDoiThuNhap
GO
create proc usp_TheoDoiThuNhap
as
begin transaction
	begin try
		-- Kiểm tra thông tin tài xế có tồn tại không
		if not exists (select CMND from TAIXE where CMND = CURRENT_USER)
		begin
			print N'Không có thông tin tài xế này'
			rollback transaction
			return 0
		END
        
		select sum(PHIVANCHUYEN)
		from DONHANG
		where CMND = CURRENT_USER and TRANGTHAI = 3
		group by CMND
	end try

	begin catch
		print N'Lỗi hệ thống'
		rollback transaction
	end catch
commit transaction
return 1
GO

-- Chỉnh tình trạng đơn hàng thành 'Đã giao hàng'
USE QLDatMon
IF OBJECT_ID('usp_ChuyenThanhDaGiaoHang') IS NOT NULL
	DROP PROC usp_ChuyenThanhDaGiaoHang
GO
create proc usp_ChuyenThanhDaGiaoHang
	@MaDon char(8)
as
begin transaction
	begin TRY
		if not exists (select CMND from TAIXE where CMND = CURRENT_USER)
		begin
			print N'Không có thông tin tài xế này'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem tài xế có đang giao đơn hàng này không
		if NOT EXISTS(SELECT CMND
				      FROM DONHANG
				      WHERE MADON = @MaDon and CMND = CURRENT_USER)
		begin 
			print N'Đơn hàng không do tài xế này đảm nhiệm'
			rollback transaction
			return 0
		END
        
		-- Kiểm tra xem tình trạng đơn hàng có hợp lệ không
		if exists(select MADON 
				  FROM DONHANG 
				  WHERE @MaDon = MADON AND TRANGTHAI != 2)
		begin
			print N'Trạng thái đơn hàng không hợp lệ'
			rollback transaction
			return 0
		END

		update DONHANG
		set TRANGTHAI = 3, THOIGIANGIAO = GETDATE()
		where MADON = @MaDon
		
		---- Tạo các biến lưu giá trị
		DECLARE @madt CHAR(8)
		DECLARE @makh CHAR(8)
		DECLARE @matk_dt CHAR(8)
		DECLARE @matk_tx CHAR(8) = (SELECT MATK_NH FROM dbo.TAIXE WHERE CMND = CURRENT_USER)
		DECLARE @thanhtoan NVARCHAR(15)
		DECLARE @phisp INT
		DECLARE @phivanchuyen INT

		SELECT @madt = MADT, @makh = MAKH, @thanhtoan = THANHTOAN, @phisp = PHISP, @phivanchuyen = PHIVANCHUYEN
        FROM dbo.DONHANG
		WHERE MADON = @MaDon

		SELECT @matk_dt = dt.MATK_NH
        FROM dbo.DOITAC dt 
		WHERE MADT = @madt

		UPDATE dbo.TAIKHOANNH
		SET SODU = SODU + 0.8 * @phisp
		WHERE MATK_NH = @matk_dt

		IF @thanhtoan = N'Chuyển khoản'
		BEGIN
			DECLARE @matk_kh CHAR(8) = (SELECT MATK_NH FROM dbo.KHACHHANG WHERE MAKH = @makh)
			UPDATE dbo.TAIKHOANNH
			SET SODU = SODU - (@phisp + @phivanchuyen)
			WHERE MATK_NH = @matk_kh
		END

		UPDATE dbo.TAIKHOANNH
		SET SODU = SODU + @phivanchuyen
		WHERE MATK_NH = @matk_tx
	end try

	begin catch
		print N'Lỗi hệ thống'
		rollback TRANSACTION
        RETURN 0
	end catch

commit transaction
return 1
GO

-- usp_XemTaiKhoanNganHang
IF OBJECT_ID('usp_XemTaiKhoanNganHang') IS NOT NULL
	DROP PROC usp_XemTaiKhoanNganHang
GO
create proc usp_XemTaiKhoanNganHang
as
begin transaction
	begin try
	-- Kiểm tra thông tin tài xế có tồn tại không
		IF not exists (select CMND from TAIXE where CMND = CURRENT_USER)
		begin
			print N'Không có thông tin tài xế này'
			rollback transaction
			return 0
		end
	-- Kiểm tra tài xế có tài khoản ngân hàng không
		if exists(select tx.CMND
				  FROM TAIXE tx
				  WHERE tx.CMND = CURRENT_USER AND tx.MATK_NH IS NULL)
		begin
			print N'Tài xế không có tài khoản ngân hàng'
			rollback transaction
			return 0
		end

		select tk.*
		from TAIXE tx join TAIKHOANNH tk on tk.MATK_NH = tx.MATK_NH
		where tx.CMND = CURRENT_USER
	end try

	begin catch
		print N'Lỗi hệ thống'
		rollback transaction
	end catch
commit transaction
return 1
go
