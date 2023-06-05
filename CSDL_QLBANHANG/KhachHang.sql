-- Proc tạo mã đơn hàng
USE QLDatMon
GO
IF OBJECT_ID('sp_TaoMaDonHang') IS NOT NULL
	DROP PROCEDURE sp_TaoMaDonHang
GO
CREATE PROCEDURE sp_TaoMaDonHang @madh CHAR(8) OUT
AS
	DECLARE @i INT = 1
	SET @madh = 'DH000001'
	WHILE(EXISTS(SELECT MADON
				 FROM dbo.DONHANG
				 WHERE MADON = @madh))
	BEGIN
		SET @i += 1
		SET @madh = 'DH' + REPLICATE('0', 8 - LEN(@i)) + CAST(@i AS CHAR(8))
	END
GO

-- Tạo đơn hàng
USE QLDatMon
GO
IF OBJECT_ID('usp_TaoDonHang') IS NOT NULL
	DROP PROC usp_TaoDonHang
GO
CREATE PROCEDURE usp_TaoDonHang
	@MaDT CHAR(8),
	@DiaChiCN NVARCHAR(30)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải khách hàng không
		IF NOT EXISTS(SELECT MAKH
					  from dbo.KHACHHANG
					  where MAKH = CURRENT_USER)
		begin
			print current_user + N' không phải là mã khách hàng hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra cửa hàng chi nhánh có tồn tại không 
		if not exists(SELECT MADT
					  from CHINHANHCH
					  where MADT = @MaDT and DIACHICH = @DiaChiCN)
		BEGIN
			print N'Chi nhánh cửa hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
								
		declare @madh char(8)
		EXEC sp_TaoMaDonHang @madh OUT
		
		INSERT DonHang(MADON, MADT, DIACHICH, MAKH) VALUES(@madh, @MaDT, @DiaChiCN, CURRENT_USER)
	END TRY

	BEGIN CATCH
		PRINT N'Bị lỗi'
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Thêm món ăn vào đơn hàng
USE QLDatMon
GO
IF OBJECT_ID('usp_ThemMonAnVaoDonHang') IS NOT NULL
	DROP PROC usp_ThemMonAnVaoDonHang
GO
CREATE PROCEDURE usp_ThemMonAnVaoDonHang
	@MaDT CHAR(8),
	@tenmon NVARCHAR(80),
	@madh CHAR(8), 
	@soluong INT
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải khách hàng không
		IF NOT EXISTS(SELECT MAKH
					  FROM dbo.KHACHHANG
					  WHERE MAKH = CURRENT_USER)
		BEGIN
			PRINT CURRENT_USER + N' không phải là mã khách hàng hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
        
		-- Kiểm tra xem đơn hàng có hợp lệ không
		IF NOT EXISTS(SELECT MADON
					  FROM dbo.DONHANG
					  WHERE MADON = @madh AND MAKH = CURRENT_USER AND TRANGTHAI = 0)
		BEGIN
			PRINT N'Đơn hàng không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra xem món ăn có tồn tại không 
		IF NOT EXISTS(SELECT MADT
					  FROM dbo.MONAN
					  WHERE MADT = @MaDT AND TENMON = @tenmon)
		BEGIN
			PRINT N'Món ăn không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra xem tình trạng món ăn có phải là 'Có bán' không 
		IF NOT EXISTS(SELECT MADT
					  FROM dbo.MONAN
					  WHERE MADT = @MaDT AND TENMON = @tenmon AND TINHTRANG = 1)
		BEGIN
			PRINT N'Món ăn đang trong tình trạng không thể đặt.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra số lượng có hợp lệ không
		IF @soluong <= 0 OR EXISTS(SELECT MADT
								   FROM dbo.MONAN
								   WHERE MADT = @MaDT AND TENMON = @tenmon AND @soluong > SoLuongHienCo)
		BEGIN
			PRINT N'Số lượng không hợp lệ'
			ROLLBACK TRAN
			RETURN 0
		END

		-- Lưu giá của món ăn
		DECLARE @tonggia INT
		SELECT @tonggia = GIA
		FROM dbo.MONAN
		WHERE MADT = @MaDT AND TENMON = @tenmon
		
		INSERT dbo.CHITIETDONHANG
		(
		    MADT,
		    TENMON,
		    MADON,
			TinhTrang,
		    SOLUONG,
		    TONGGIA
		)
		VALUES
		(   @MaDT,   -- MADT - char(8)
		    @tenmon,  -- TENMON - nvarchar(80)
		    @madh,   -- MADON - char(8)
			0,
		    @soluong, -- SOLUONG - int
		    @soluong * @tonggia  -- TONGGIA - int
		    )
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Thay đổi số lượng của 1 món ăn trong đơn hàng 
use QLDatMon
GO
IF OBJECT_ID('usp_ThayDoiSoLuongMonAn_KH') IS NOT NULL
	DROP PROC usp_ThayDoiSoLuongMonAn_KH
GO
CREATE PROCEDURE usp_ThayDoiSoLuongMonAn_KH
	@MaDT CHAR(8),
	@tenmon NVARCHAR(80),
	@madh CHAR(8), 
	@soluong INT
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải khách hàng không
		if not exists(SELECT MAKH
					  from dbo.KHACHHANG
					  where MAKH = CURRENT_USER)
		begin
			print current_user + N' không phải là mã khách hàng hợp lệ.'
			rollback transaction
			return 0
		END
        
		-- Kiểm tra xem đơn hàng có hợp lệ không
		if not exists(SELECT MADON
					  from dbo.DONHANG
					  where MADON = @madh AND MAKH = CURRENT_USER AND TRANGTHAI = 0)
		begin
			print N'Đơn hàng không hợp lệ.'
			rollback transaction
			return 0
		END

		-- Kiểm tra xem chi tiết đơn hàng có tồn tại không 
		if not exists(SELECT MADT
					  from dbo.CHITIETDONHANG
					  where MADT = @MaDT AND TENMON = @tenmon AND MADON = @madh)
		BEGIN
			print N'Chi tiết đơn hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra số lượng có hợp lệ không
		IF @soluong <= 0 OR EXISTS(SELECT MADT
								   FROM dbo.MONAN
								   WHERE MADT = @MaDT AND TENMON = @tenmon AND @soluong > SoLuongHienCo)
		BEGIN
			PRINT N'Số lượng không hợp lệ'
			ROLLBACK TRAN
			RETURN 0
		END

		-- Lưu giá của món ăn
		DECLARE @tonggia INT
		SELECT @tonggia = GIA
		FROM dbo.MONAN
		WHERE MADT = @MaDT AND TENMON = @tenmon

		UPDATE dbo.CHITIETDONHANG
		SET SOLUONG = @soluong, TONGGIA = @soluong * @tonggia
		WHERE MADT = @MaDT AND TENMON = @tenmon AND MADON = @madh
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Tăng số lượng của 1 món ăn thêm 1 trong đơn hàng 
use QLDatMon
GO
IF OBJECT_ID('usp_CongSoLuongMonAn_KH') IS NOT NULL
	DROP PROC usp_CongSoLuongMonAn_KH
GO
CREATE PROCEDURE usp_CongSoLuongMonAn_KH
	@MaDT CHAR(8),
	@tenmon NVARCHAR(80),
	@madh CHAR(8)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải khách hàng không
		if not exists(SELECT MAKH
					  from dbo.KHACHHANG
					  where MAKH = CURRENT_USER)
		begin
			print current_user + N' không phải là mã khách hàng hợp lệ.'
			rollback transaction
			return 0
		END
        
		-- Kiểm tra xem đơn hàng có hợp lệ không
		if not exists(SELECT MADON
					  from dbo.DONHANG
					  where MADON = @madh AND MAKH = CURRENT_USER AND TRANGTHAI = 0)
		begin
			print N'Đơn hàng không hợp lệ.'
			rollback transaction
			return 0
		END

		-- Kiểm tra xem chi tiết đơn hàng có tồn tại không 
		if not exists(SELECT MADT
					  from dbo.CHITIETDONHANG
					  where MADT = @MaDT AND TENMON = @tenmon AND MADON = @madh)
		BEGIN
			print N'Chi tiết đơn hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Lưu giá của món ăn
		DECLARE @tonggia INT
		SELECT @tonggia = GIA
		FROM dbo.MONAN
		WHERE MADT = @MaDT AND TENMON = @tenmon

		UPDATE dbo.CHITIETDONHANG
		SET SOLUONG = SOLUONG + 1, TONGGIA = TONGGIA + @tonggia
		WHERE MADT = @MaDT AND TENMON = @tenmon AND MADON = @madh
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Giảm số lượng của 1 món ăn đi 1 trong đơn hàng 
use QLDatMon
GO
IF OBJECT_ID('usp_GiamSoLuongMonAn_KH') IS NOT NULL
	DROP PROC usp_GiamSoLuongMonAn_KH
GO
CREATE PROCEDURE usp_GiamSoLuongMonAn_KH
	@MaDT CHAR(8),
	@tenmon NVARCHAR(80),
	@madh CHAR(8)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải khách hàng không
		if not exists(SELECT MAKH
					  from dbo.KHACHHANG
					  where MAKH = CURRENT_USER)
		begin
			print current_user + N' không phải là mã khách hàng hợp lệ.'
			rollback transaction
			return 0
		END
        
		-- Kiểm tra xem đơn hàng có hợp lệ không
		if not exists(SELECT MADON
					  from dbo.DONHANG
					  where MADON = @madh AND MAKH = CURRENT_USER AND TRANGTHAI = 0)
		begin
			print N'Đơn hàng không hợp lệ.'
			rollback transaction
			return 0
		END

		-- Kiểm tra xem chi tiết đơn hàng có tồn tại không 
		if not exists(SELECT MADT
					  from dbo.CHITIETDONHANG
					  where MADT = @MaDT AND TENMON = @tenmon AND MADON = @madh)
		BEGIN
			print N'Chi tiết đơn hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Lưu giá của món ăn
		DECLARE @tonggia INT
		SELECT @tonggia = GIA
		FROM dbo.MONAN
		WHERE MADT = @MaDT AND TENMON = @tenmon

		DECLARE @soluong INT
		SELECT @soluong = SOLUONG
		FROM dbo.CHITIETDONHANG
		WHERE MADON = @madh and MADT = @MaDT AND TENMON = @tenmon

		IF @soluong <= 1
		BEGIN 
			print N'Không thể trừ thêm nữa.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
        else
		begin
			UPDATE dbo.CHITIETDONHANG
			SET SOLUONG = SOLUONG - 1, TONGGIA = TONGGIA - @tonggia
			WHERE MADT = @MaDT AND TENMON = @tenmon AND MADON = @madh
		end
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Xóa 1 món ăn khỏi đơn hàng 
use QLDatMon
GO
IF OBJECT_ID('usp_XoaMonAnKhoiDonHang_KH') IS NOT NULL
	DROP PROC usp_XoaMonAnKhoiDonHang_KH
GO
CREATE PROCEDURE usp_XoaMonAnKhoiDonHang_KH
	@MaDT CHAR(8),
	@tenmon NVARCHAR(80),
	@madh CHAR(8)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải khách hàng không
		if not exists(SELECT MAKH
					  from dbo.KHACHHANG
					  where MAKH = CURRENT_USER)
		begin
			print current_user + N' không phải là mã khách hàng hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem đơn hàng có hợp lệ không
		if not exists(SELECT MADON
					  from dbo.DONHANG
					  where MADON = @madh AND MAKH = CURRENT_USER AND TRANGTHAI = 0)
		begin
			print N'Đơn hàng không hợp lệ.'
			rollback transaction
			return 0
		END

		-- Kiểm tra xem chi tiết đơn hàng có tồn tại không 
		if not exists(SELECT MADT
					  from dbo.CHITIETDONHANG
					  where MADT = @MaDT AND TENMON = @tenmon AND MADON = @madh)
		BEGIN
			print N'Chi tiết đơn hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		DELETE dbo.CHITIETDONHANG
		WHERE MADT = @MaDT AND TENMON = @tenmon AND MADON = @madh
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Xóa 1 đơn hàng 
use QLDatMon
GO
IF OBJECT_ID('usp_Xoa1DonHang_KH') IS NOT NULL
	DROP PROC usp_Xoa1DonHang_KH
GO
CREATE PROCEDURE usp_Xoa1DonHang_KH @madh CHAR(8)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải khách hàng không
		if not exists(SELECT MAKH 
					  from dbo.KHACHHANG
					  where MAKH = CURRENT_USER)
		begin
			print current_user + N' không phải là mã khách hàng hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem đơn hàng có hợp lệ không
		if not exists(SELECT MADON
					  from dbo.DONHANG
					  where MADON = @madh AND MAKH = CURRENT_USER AND TRANGTHAI = 0)
		begin
			print N'Đơn hàng không hợp lệ.'
			rollback transaction
			return 0
		END

		DELETE dbo.CHITIETDONHANG WHERE MADON = @madh
		DELETE dbo.DONHANG WHERE MADON = @madh
	
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Hủy đơn hàng 
use QLDatMon
GO
IF OBJECT_ID('usp_HuyDonHang_KH') IS NOT NULL
	DROP PROC usp_HuyDonHang_KH
GO
CREATE PROCEDURE usp_HuyDonHang_KH
	@madh CHAR(8)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải khách hàng không
		IF NOT EXISTS(SELECT MAKH 
					  FROM dbo.KHACHHANG
					  WHERE MAKH = CURRENT_USER)
		BEGIN
			PRINT CURRENT_USER + N' không phải là mã khách hàng hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra xem đơn hàng có hợp lệ không 
		IF NOT EXISTS(SELECT MADON 
					  FROM dbo.DONHANG
					  WHERE MADON = @madh AND MAKH = CURRENT_USER)
		BEGIN
			PRINT N'Đơn hàng không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra xem đơn hàng có đang trong trạng thái "Đang chờ tiếp nhận" không 
		IF NOT EXISTS(SELECT MADON
					  FROM dbo.DONHANG
					  WHERE MADON = @madh AND TRANGTHAI = 1)
		BEGIN
			PRINT N'Đơn hàng chỉ được hủy khi ở trạng thái Đang chờ tiếp nhận.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Lưu mã đối tác
		DECLARE @madt CHAR(8) = (SELECT MADT
								 FROM dbo.DONHANG
								 WHERE MADON = @madh)
		WHILE(EXISTS(SELECT MADON
					 FROM dbo.CHITIETDONHANG
					 WHERE MADON = @madh AND TinhTrang = 1))
		BEGIN
			DECLARE @tenmon NVARCHAR(80) 
			DECLARE @soluong INT

			SELECT @tenmon = TENMON, @soluong = SOLUONG
            FROM dbo.CHITIETDONHANG
			WHERE MADON = @madh AND TinhTrang = 1

			UPDATE dbo.MONAN SET SoLuongHienCo = SoLuongHienCo + @soluong WHERE MADT = @madt AND TENMON = @tenmon
			UPDATE dbo.CHITIETDONHANG SET TinhTrang = -1 WHERE MADON = @madh AND MADT = @madt AND TENMON = @tenmon
		END

		UPDATE dbo.DONHANG
		SET TRANGTHAI = -1
		WHERE MADON = @madh
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Khách hàng có thể xem thông tin của chính mình 
USE QLDatMon
GO
DROP PROCEDURE IF EXISTS USP_XEMKHACHHANG
GO

CREATE PROCEDURE USP_XEMKHACHHANG
AS
	BEGIN TRY
		SELECT * FROM KHACHHANG WHERE MAKH = CURRENT_USER
	END TRY

	BEGIN CATCH
		ROLLBACK TRAN
		RETURN 0
	END CATCH

COMMIT TRANSACTION
RETURN 1
GO

--Khách hàng có thể đặt đơn hàng 
DROP PROCEDURE IF EXISTS USP_DATDONHANG
GO

CREATE PROCEDURE USP_DATDONHANG
	@madon CHAR(8),
	@thanhtoan NVARCHAR(15),
	@diachigh NVARCHAR(40)
AS
BEGIN TRAN
	BEGIN TRY
		-- Kiểm tra xem người dùng proc này có phải khách hàng không
		IF NOT EXISTS (SELECT MAKH FROM KHACHHANG WHERE MAKH = CURRENT_USER)
		BEGIN
			ROLLBACK TRAN
			RETURN 0
		END

		-- Kiểm tra xem đơn hàng có hợp lệ không
		if not exists(SELECT MADON 
					  from dbo.DONHANG
					  where MADON = @madon AND MAKH = CURRENT_USER AND TRANGTHAI = 0)
		begin
			print N'Đơn hàng không hợp lệ.'
			rollback transaction
			return 0
		END
		
		-- Lưu mã đối tác và địa chỉ chi nhánh
		DECLARE @madt CHAR(8)
		DECLARE @diachiCN NVARCHAR(30)

		-- Lưu tổng tiền các món ăn
		DECLARE @tongtien INT = 0
		
		SELECT @madt = MADT, @diachiCN = DIACHICH
		FROM dbo.DONHANG
		WHERE MADON = @madon

		IF @diachigh IS NULL
		BEGIN
			SELECT @diachigh = DIACHIKH
            FROM dbo.KHACHHANG
			WHERE MAKH = CURRENT_USER
		END
		
		WHILE(exists(SELECT MADON
					 from dbo.CHITIETDONHANG
					 where MADON = @madon AND TinhTrang = 0))
		BEGIN
			DECLARE @tenmon NVARCHAR(80) 
			DECLARE @soluong INT
			DECLARE @gia int

			SELECT @tenmon = TENMON, @soluong = SOLUONG, @gia = TONGGIA
            FROM dbo.CHITIETDONHANG
			WHERE MADON = @madon AND TinhTrang = 0

			SET @tongtien += @gia

			-- Kiểm tra lại xem có thể đặt món được không
			IF EXISTS(SELECT MADT
					  FROM dbo.MONAN
					  WHERE MADT = @madt AND TENMON = @tenmon AND ((@soluong > SoLuongHienCo) OR (TINHTRANG != 1)))
			BEGIN
				EXEC dbo.usp_Xoa1DonHang_KH @madh = @madon -- char(8)
				--EXEC dbo.usp_TaoDonHang @MaDT = @madt,     -- char(8)
				--                        @DiaChiCN = @diachiCN -- nvarchar(30)
				
				COMMIT TRAN
				RETURN 2
			END

			UPDATE dbo.MONAN SET SoLuongHienCo = SoLuongHienCo - @soluong WHERE MADT = @madt AND TENMON = @tenmon
			UPDATE dbo.CHITIETDONHANG SET TinhTrang = 1 WHERE MADON = @madon AND MADT = @madt AND TENMON = @tenmon
		END

		UPDATE dbo.DONHANG
		SET TRANGTHAI = 1, THANHTOAN = @thanhtoan, DIACHIGiaoHang = @diachiGH, ThoigianLAP = GETDATE(), PHISP = @tongtien, PHIVANCHUYEN = 0.05 * @tongtien, TONGTIEN = @tongtien * 1.05
		WHERE MADON = @madon

		UPDATE dbo.DONHANG
		SET THOIGIANGIAO = DATEADD(hh, 1, thoigianLAP)
		WHERE MADON = @madon
	END TRY

	BEGIN CATCH
		ROLLBACK TRAN
		RETURN 0
	END CATCH
COMMIT TRAN
RETURN 1
GO

--Khách hàng có thể xem danh sách các cửa hàng 
DROP PROCEDURE IF EXISTS USP_XEMDANHSACHCUAHANG
GO

--CREATE PROCEDURE USP_XEMDANHSACHCUAHANG @MADT CHAR(8)
--AS
--	BEGIN TRY

--	IF NOT EXISTS (SELECT * FROM CHINHANHCH WHERE MADT = @MADT)
--	BEGIN
--		RETURN 0
--	END

--	SELECT * FROM CHINHANHCH WHERE MADT = @MADT
--	RETURN 1
--	END TRY

--	BEGIN CATCH
--		RETURN 0
--	END CATCH
--GO

CREATE PROCEDURE USP_XEMDANHSACHCUAHANG
AS
	BEGIN TRY

		SELECT * FROM CHINHANHCH
		RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
	END CATCH
GO

--Xem danh sách đơn hàng đã đặt 
USE QLDatMon
DROP PROCEDURE IF EXISTS USP_XEMDANHSACHDONHANG
GO

CREATE PROCEDURE USP_XEMDANHSACHDONHANG @trangthai SMALLINT
AS
	BEGIN TRY
		if @TrangThai not in (-1, 0, 1, 2, 3)
		BEGIN
			print N'Tình trạng đơn hàng không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		SELECT dh.MADON, dh.TENKH, dh.TENTX, dh.TENDT, dh.DIACHICH, dh.THOIGIANLAP, dh.DIACHIGIAOHANG, dh.TRANGTHAI, dh.PHISP, dh.PHIVANCHUYEN, dh.TONGTIEN, dh.THANHTOAN, dh.THOIGIANGIAO
		FROM DONHANG dh
		WHERE dh.MAKH = CURRENT_USER and dh.TRANGTHAI = @TrangThai

		RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
	END CATCH
GO

--Khách hàng có thể xem đơn hàng hiện tại của mình
USE QLDatMon
DROP PROCEDURE IF EXISTS USP_XEMDONHANG
GO

CREATE PROCEDURE USP_XEMDONHANG @MADH CHAR(8)
AS
	BEGIN TRY

		IF NOT EXISTS (SELECT MADON FROM DONHANG WHERE MADON = @MADH)
		BEGIN
			RETURN 0
		END

		SELECT dh.MADON, dh.TENKH, dh.TENTX, dh.TENDT, dh.DIACHICH, dh.THOIGIANLAP, dh.DIACHIGIAOHANG, dh.TRANGTHAI, dh.PHISP, dh.PHIVANCHUYEN, dh.TONGTIEN, dh.THANHTOAN, dh.THOIGIANGIAO
		FROM DONHANG dh
		WHERE dh.MAKH = CURRENT_USER and dh.MADON = @MADH

		RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
	END CATCH
GO

--Khách hàng có thể xem chi tiết đơn hàng của mình 
DROP PROCEDURE IF EXISTS USP_XEMCHITIETDONHANG
GO

CREATE PROCEDURE USP_XEMCHITIETDONHANG @MADH CHAR(8)
AS
	BEGIN TRY

	IF NOT EXISTS (SELECT MADON FROM DONHANG WHERE MADON = @MADH)
	BEGIN
		RETURN 0
	END

	SELECT * FROM CHITIETDONHANG WHERE MADON = @MADH
	RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
	END CATCH
GO

--Xem thực đơn của 1 cửa hàng cụ thể
DROP PROCEDURE IF EXISTS USP_THUCDON
GO

CREATE PROCEDURE USP_THUCDON @MADT CHAR(8)
AS
	BEGIN TRY

	IF NOT EXISTS (SELECT MADT FROM MONAN WHERE MADT = @MADT)
	BEGIN
		RETURN 0
	END

	SELECT * FROM MONAN WHERE MADT = @MADT
	RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
	END CATCH
GO

--Khách hàng có thể thêm đánh giá món ăn
DROP PROCEDURE IF EXISTS USP_DANHGIAMONAN
GO

CREATE PROCEDURE USP_DANHGIAMONAN  @MADT CHAR(8), @MONAN VARCHAR(80), @RATING FLOAT, @COMMENT VARCHAR(50)
AS
	BEGIN TRY

	IF NOT EXISTS (SELECT MADT FROM MONAN WHERE MADT = @MADT AND TENMON = @MONAN)
	BEGIN
		RETURN 0
	END

	IF @RATING IS NULL
	BEGIN
		RETURN 0
	END

	ELSE IF @RATING < 0 OR @RATING > 5
	BEGIN
		RETURN 0
	END

	INSERT INTO DANHGIATHUCAN
	VALUES (@MADT, @MONAN, CURRENT_USER, @RATING, @COMMENT)
	RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
		ROLLBACK TRANSACTION
	END CATCH
GO

--Khách hàng có thể cập nhật lại đánh giá của mình
DROP PROCEDURE IF EXISTS USP_CAPNHATDANHGIAMONAN
GO

CREATE PROCEDURE USP_CAPNHATDANHGIAMONAN  @MADT CHAR(8), @MONAN VARCHAR(80), @RATING FLOAT, @COMMENT VARCHAR(50)
AS
	BEGIN TRY

	IF NOT EXISTS(SELECT MADT FROM DANHGIATHUCAN WHERE MADT = @MADT AND TENMON = @MONAN AND MAKH = CURRENT_USER)
	BEGIN
		RETURN 0
	END

	IF @RATING IS NULL
	BEGIN
		RETURN 0
	END

	ELSE IF @RATING < 0 OR @RATING > 5
	BEGIN
		RETURN 0
	END

	UPDATE DANHGIATHUCAN
	SET RATING = @RATING, COMMENT = @COMMENT
	WHERE MADT = @MADT AND TENMON = @MONAN AND MAKH = CURRENT_USER
	RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
		ROLLBACK TRANSACTION
	END CATCH
GO

--Khách hàng có thể thêm đánh giá cửa hàng
DROP PROCEDURE IF EXISTS USP_DANHGIASHOP
GO

CREATE PROCEDURE USP_DANHGIASHOP  @MADT CHAR(8), @DCHI VARCHAR(20), @RATING FLOAT, @COMMENT VARCHAR(50)
AS
	BEGIN TRY

	IF NOT EXISTS (SELECT MADT FROM CHINHANHCH WHERE MADT = @MADT AND DIACHICH = @DCHI)
	BEGIN
		RETURN 0
	END

	IF @RATING IS NULL
	BEGIN
		RETURN 0
	END

	ELSE IF @RATING < 0 OR @RATING > 5
	BEGIN
		RETURN 0
	END

	INSERT INTO DANHGIASHOP
	VALUES (CURRENT_USER, @MADT, @DCHI, @RATING, @COMMENT)
	RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
		ROLLBACK TRANSACTION
	END CATCH
GO

--Khách hàng có thể cập nhật lại đánh giá cửa hàng
DROP PROCEDURE IF EXISTS USP_CAPNHATDANHGIASHOP
GO

CREATE PROCEDURE USP_CAPNHATDANHGIASHOP  @MADT CHAR(8), @DCHI VARCHAR(20), @RATING FLOAT, @COMMENT VARCHAR(50)
AS
	BEGIN TRY

	IF NOT EXISTS (SELECT MADT FROM DANHGIASHOP WHERE MADT = @MADT AND DIACHICH = @DCHI AND MAKH = CURRENT_USER)
	BEGIN
		RETURN 0
	END

	IF @RATING IS NULL
	BEGIN
		RETURN 0
	END

	ELSE IF @RATING < 0 OR @RATING > 5
	BEGIN
		RETURN 0
	END

	UPDATE DANHGIASHOP
	SET RATING = @RATING, COMMENT = @COMMENT
	WHERE MADT = @MADT AND DIACHICH = @DCHI AND MAKH = CURRENT_USER
	RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
		ROLLBACK TRANSACTION
	END CATCH
GO

--Khách hàng có thể thêm đánh giá tài xế
DROP PROCEDURE IF EXISTS USP_DANHGIATAIXE
GO

CREATE PROCEDURE USP_DANHGIATAIXE @CMND VARCHAR(80), @RATING FLOAT, @COMMENT VARCHAR(50)
AS
	BEGIN TRY

	IF NOT EXISTS (SELECT CMND FROM TAIXE WHERE CMND = @CMND)
	BEGIN
		RETURN 0
	END

	IF @RATING IS NULL
	BEGIN
		RETURN 0
	END

	ELSE IF @RATING < 0 OR @RATING > 5
	BEGIN
		RETURN 0
	END

	INSERT INTO dbo.DANHGIATAIXE
	(
	    MAKH,
	    CMND,
	    RATING,
	    COMMENT
	)
	VALUES
	(   CURRENT_USER,   -- MAKH - char(8)
	    @CMND,   -- CMND - char(8)
	    @RATING, -- RATING - float
	    @COMMENT  -- COMMENT - nvarchar(50)
	)
	RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
		ROLLBACK TRANSACTION
	END CATCH
GO

--Khách hàng có thể cập nhật lại đánh giá tài xế 
DROP PROCEDURE IF EXISTS USP_CAPNHATDANHGIATAIXE
GO

CREATE PROCEDURE USP_CAPNHATDANHGIATAIXE @CMND VARCHAR(80), @RATING FLOAT, @COMMENT VARCHAR(50)
AS
	BEGIN TRY

	IF NOT EXISTS (SELECT CMND FROM DANHGIATAIXE WHERE CMND = @CMND AND MAKH = CURRENT_USER)
	BEGIN
		RETURN 0
	END

	IF @RATING IS NULL
	BEGIN
		RETURN 0
	END

	ELSE IF @RATING < 0 OR @RATING > 5
	BEGIN
		RETURN 0
	END

	UPDATE DANHGIATAIXE
	SET RATING = @RATING, COMMENT = @COMMENT
	WHERE CMND = @CMND AND MAKH = CURRENT_USER
	RETURN 1
	END TRY

	BEGIN CATCH
		RETURN 0
	END CATCH
GO

--Khách hàng có thể xem tài khoản ngân hàng của mình
DROP PROCEDURE IF EXISTS USP_XEMTAIKHOANNGANHANG
GO

CREATE PROCEDURE USP_XEMTAIKHOANNGANHANG
AS
	BEGIN TRY

	IF NOT EXISTS (SELECT KH.MATK_NH FROM TAIKHOANNH TK JOIN KHACHHANG KH ON KH.MATK_NH = TK.MATK_NH WHERE KH.MAKH = CURRENT_USER)
	BEGIN
		RETURN 0
	END

	SELECT * FROM TAIKHOANNH TK JOIN KHACHHANG KH ON KH.MATK_NH = TK.MATK_NH WHERE KH.MAKH = CURRENT_USER
	RETURN 1
	END TRY

	BEGIN CATCH
	RETURN 0
	END CATCH

GO
