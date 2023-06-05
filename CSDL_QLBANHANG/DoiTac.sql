USE QLDatMon

-- Xem hợp đồng của đối tác
GO
IF OBJECT_ID('usp_XemHopDong') IS NOT NULL
	DROP PROC usp_XemHopDong
GO
CREATE PROCEDURE usp_XemHopDong
AS
BEGIN TRANSACTION
	BEGIN TRY
		IF NOT EXISTS(SELECT MADT
					  FROM DOITAC
					  WHERE Madt = CURRENT_USER)
		BEGIN
			PRINT CURRENT_USER + N' không phải là mã đối tác hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		SELECT hd.* 
		FROM HopDong hd JOIN DoiTac dt ON dt.mahd = hd.mahd
		WHERE dt.madt = CURRENT_USER
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Xem thông tin đối tác
GO
IF OBJECT_ID('usp_XemThongTinDoiTac') IS NOT NULL
	DROP PROC usp_XemThongTinDoiTac
GO
CREATE PROCEDURE usp_XemThongTinDoiTac 
as
BEGIN TRANSACTION
	BEGIN TRY
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		select*
		from DOITAC
		where Madt = CURRENT_USER
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Xem cửa hàng chi nhánh của đối tác
use QLDatMon
GO
IF OBJECT_ID('usp_XemCuaHangChiNhanh') IS NOT NULL
	DROP PROC usp_XemCuaHangChiNhanh
GO
CREATE PROCEDURE usp_XemCuaHangChiNhanh @diadiemCN nvarchar(30) null
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem nếu khác null, địa chỉ chi nhánh có tồn tại không
		if @diadiemCN is not null and not exists(SELECT MADT
												 from CHINHANHCH
												 where Madt = CURRENT_USER and DIACHICH = @diadiemCN)
		begin
			print N'Chi nhánh không tồn tại.'
			rollback transaction
			return 0
		end

		if @diadiemCN is Null
		begin 
			select*
			from CHINHANHCH
			where MADT = CURRENT_USER
		end
		else
		begin
			select*
			from CHINHANHCH
			where MADT = CURRENT_USER and DIACHICH = @diadiemCN
		end
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Thêm cửa hàng chi nhánh
use QLDatMon
GO
IF OBJECT_ID('usp_ThemCuaHangChiNhanh') IS NOT NULL
	DROP PROC usp_ThemCuaHangChiNhanh
GO
CREATE PROCEDURE usp_ThemCuaHangChiNhanh
	@DiaChi nvarchar(50),
	@ThoiGianMoCua time,
	@ThoiGianDongCua time,
	@TinhTrang nvarchar(30)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		END
        
		-- Kiểm tra xem địa chỉ này có tồn tại chi nhánh chưa
		IF EXISTS(SELECT MADT
				  FROM dbo.CHINHANHCH
				  WHERE MADT = CURRENT_USER AND DIACHICH = @DiaChi)
		BEGIN
			PRINT N'Địa chỉ đã tồn tại.'
			ROLLBACK TRAN
			RETURN 0
		END

		-- Kiểm tra xem thời gian mở cửa có < hơn thời gian đóng cửa không
		if convert(datetime, @ThoiGianMoCua, 8) >= convert(datetime, @ThoiGianDongCua, 8)
		BEGIN
			print N'Thời gian mở cửa phải < hơn thời gian đóng cửa.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra giá trị tình trạng có nằm trong các giá trị "Mở cửa", "Đóng cửa", "Tạm nghỉ" không 
		if @TinhTrang NOT IN(N'Tạm nghỉ', N'Mở cửa', N'Đóng cửa')
		BEGIN
			print N'Tình trạng cửa hàng không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Lưu tên đối tác
		DECLARE @tendt NVARCHAR(30) = (SELECT TENQUAN FROM dbo.DOITAC WHERE MADT = CURRENT_USER)

		insert into dbo.CHINHANHCH(MADT, DIACHICH, TENDT, THOIGIANMOCUA, THOIGIANDONGCUA, TINHTRANG)
		VALUES(CURRENT_USER, @DiaChi, @tendt, @ThoiGianMoCua, @ThoiGianDongCua, @TinhTrang)
	END TRY
	
	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH

COMMIT TRANSACTION
RETURN 1
GO

-- Sửa địa chỉ chi nhánh cửa hàng 
use QLDatMon
GO
IF OBJECT_ID('usp_SuaDiaChiCuaHangChiNhanh') IS NOT NULL
	DROP PROC usp_SuaDiaChiCuaHangChiNhanh
GO
CREATE PROCEDURE usp_SuaDiaChiCuaHangChiNhanh 
	@DiaChiCu nvarchar(30), 
	@DiaChiMoi nvarchar(30)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra cửa hàng chi nhánh có tồn tại không 
		if not exists(SELECT MADT
					  from CHINHANHCH
					  where MADT = CURRENT_USER and DIACHICH = @DiaChiCu)
		BEGIN
			print N'Chi nhánh cửa hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Kiểm tra địa chỉ cửa hàng chi nhánh mới có bị trùng không 
		if exists(SELECT MADT
				  from CHINHANHCH
				  where MADT = CURRENT_USER and DIACHICH = @DiaChiMoi)
		BEGIN
			print N'Địa chỉ chi nhánh cửa hàng mới đã bị trùng.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		update CHINHANHCH
		set DIACHICH = @DiaChiMoi where MADT = CURRENT_USER and DIACHICH = @DiaChiCu
	END TRY
	
	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Sửa tên cửa hàng của đối tác
use QLDatMon
GO
IF OBJECT_ID('usp_SuaTenCuaHang') IS NOT NULL
	DROP PROC usp_SuaTenCuaHang
GO
CREATE PROCEDURE usp_SuaTenCuaHang @TenCuaHang nvarchar(50)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction				
			return 0
		end

		-- Kiểm tra xem đã hết 30 ngày kể từ khi lập hồ sơ chưa
		if exists(SELECT dt.MADT
				  from HOPDONG hd join DOITAC dt on hd.mahd = dt.mahd
				  where dt.madt = CURRENT_USER and datediff(day, hd.thoigianlap, getdate()) > 30)
		begin
			print N'Đã quá 30 ngày kể từ khi lập hợp đồng nên không thể đổi tên.'
			rollback transaction				
			return 0
		end

		update DOITAC
		set tenquan = @TenCuaHang where Madt = CURRENT_USER
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH

COMMIT TRANSACTION
RETURN 1
GO

-- Cập nhật thời gian mở cửa của 1 chi nhánh
use QLDatMon
GO
IF OBJECT_ID('usp_CapNhatThoiGianMoCuaChiNhanhCuaHang') IS NOT NULL
	DROP PROC usp_CapNhatThoiGianMoCuaChiNhanhCuaHang
GO
CREATE PROCEDURE usp_CapNhatThoiGianMoCuaChiNhanhCuaHang
	@DiaChiChiNhanh nvarchar(30),
	@ThoiGianMoCua time
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra cửa hàng chi nhánh có tồn tại không 
		if not exists(SELECT MADT
					  from CHINHANHCH
					  where MADT = CURRENT_USER and DIACHICH = @DiaChiChiNhanh)
		BEGIN
			print N'Chi nhánh cửa hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
								
		-- Kiểm tra xem thời gian mà người dùng nhập có null không
		if @ThoiGianMoCua is null
		begin
			print N'Thời gian nhập vào không thể null.'
			ROLLBACK TRANSACTION
			RETURN 0
		end

		-- Kiểm tra xem thời gian mở cửa cập nhật có < hơn thời gian đóng cửa không
		if exists(SELECT MADT
				  from CHINHANHCH
				  where MADT = CURRENT_USER and DIACHICH = @DiaChiChiNhanh and convert(datetime, @ThoiGianMoCua, 8) > convert(datetime, THOIGIANDONGCUA, 8))
		begin
			print N'Thời gian mở cửa không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		end
		
		update CHINHANHCH 
		set THOIGIANMOCUA = @ThoiGianMoCua 
		where MADT = CURRENT_USER and DIACHICH = @DiaChiChiNhanh
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Cập nhật thời gian đóng cửa của 1 chi nhánh
use QLDatMon
GO
IF OBJECT_ID('usp_CapNhatThoiGianDongCuaChiNhanhCuaHang') IS NOT NULL
	DROP PROC usp_CapNhatThoiGianDongCuaChiNhanhCuaHang
GO
CREATE PROCEDURE usp_CapNhatThoiGianDongCuaChiNhanhCuaHang
	@DiaChiChiNhanh nvarchar(30),
	@ThoiGianDongCua time
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra cửa hàng chi nhánh có tồn tại không 
		if not exists(SELECT MADT
					  from CHINHANHCH
					  where MADT = CURRENT_USER and DIACHICH = @DiaChiChiNhanh)
		BEGIN
			print N'Chi nhánh cửa hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
								
		-- Kiểm tra xem thời gian mà người dùng nhập có null không
		if @ThoiGianDongCua is null
		begin
			print N'Thời gian nhập vào không thể null.'
			ROLLBACK TRANSACTION
			RETURN 0
		end

		-- Kiểm tra xem thời gian đóng cửa cập nhật có > hơn thời gian mở cửa không
		if exists(SELECT MADT
				  from CHINHANHCH
				  where MADT = CURRENT_USER and DIACHICH = @DiaChiChiNhanh and convert(datetime, @ThoiGianDongCua, 8) < convert(datetime, THOIGIANMOCUA, 8))
		begin
			print N'Thời gian đóng cửa không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		end
		
		update CHINHANHCH 
		set THOIGIANDONGCUA = @ThoiGianDongCua 
		where MADT = CURRENT_USER and DIACHICH = @DiaChiChiNhanh
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH

COMMIT TRANSACTION
RETURN 1
GO

-- Cập nhật tình trạng của 1 chi nhánh
use QLDatMon
GO
IF OBJECT_ID('usp_CapNhatTinhTrangChiNhanhCuaHang') IS NOT NULL
	DROP PROC usp_CapNhatTinhTrangChiNhanhCuaHang
GO
CREATE PROCEDURE usp_CapNhatTinhTrangChiNhanhCuaHang
	@DiaChiChiNhanh nvarchar(30),
	@TinhTrang SMALLINT
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra cửa hàng chi nhánh có tồn tại không 
		if not exists(SELECT MADT
					  from CHINHANHCH
					  where MADT = CURRENT_USER and DIACHICH = @DiaChiChiNhanh)
		BEGIN
			print N'Chi nhánh cửa hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
								
		-- Kiểm tra xem tình trạng mà người dùng nhập có null không
		if @TinhTrang is null
		begin
			print N'Tình trạng nhập vào không thể null.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
        
		-- Kiểm tra xem tình trạng mà người dùng nhập có hợp lệ không
		if @TinhTrang NOT IN(1, 0, -1)
		begin
			print N'Tình trạng nhập vào không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
		
		update CHINHANHCH 
		set TINHTRANG = @TinhTrang
		where MADT = CURRENT_USER and DIACHICH = @DiaChiChiNhanh
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH

COMMIT TRANSACTION
RETURN 1
GO

--Xem các món ăn của đối tác 
use QLDatMon
GO
IF OBJECT_ID('usp_XemThucDon') IS NOT NULL
	DROP PROC usp_XemThucDon
GO
CREATE PROCEDURE usp_XemThucDon
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem mã đối tác có tồn tại không
		if not exists(SELECT MADT
					  from DOITAC where MADT = CURRENT_USER)
		begin
			print N'Mã đối tác không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		end

		select*
		from MONAN
		where MADT = CURRENT_USER
	END TRY
	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Thêm món ăn của đối tác 
use QLDatMon
GO
IF OBJECT_ID('usp_ThemMonAn') IS NOT NULL
	DROP PROC usp_ThemMonAn 
GO
CREATE PROCEDURE usp_ThemMonAn 
	@TenMon nvarchar(50),
	@MieuTa nvarchar(100),
	@Gia int,
	@TinhTrang nvarchar(30),
	@SoLuong int
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem món ăn đã tồn tại chưa
		if EXISTS(SELECT MADT FROM MONAN WHERE MADT = CURRENT_USER and TENMON = @TenMon)
		BEGIN
			PRINT N'Món ăn đã tồn tại.'
			ROLLBACK TRAN
			RETURN 0
		END

		-- Kiểm tra xem giá có âm không
		if @Gia < 0
		begin
			PRINT N'Giá món ăn không được < 0.'
			ROLLBACK TRAN
			RETURN 0
		END
        
		-- Kiểm tra xem số lượng có > 0 không
		if @SoLuong <= 0
		begin
			PRINT N'Số lượng phải > 0.'
			ROLLBACK TRAN
			RETURN 0
		end

		-- Kiểm tra xem tình trạng có hợp lệ không
		if @TinhTrang not in (N'Có bán', N'Hết hàng', N'Tạm ngưng')
		BEGIN
			print N'Tình trạng món ăn không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END
		
		INSERT INTO dbo.MONAN
		(
		    MADT,
		    TENMON,
		    MIEUTAMON,
		    GIA,
		    SoLuongHienCo,
		    TINHTRANG
		)
		VALUES
		(   CURRENT_USER,   -- MADT - char(6)
		    @TenMon,  -- TENMON - nvarchar(80)
		    @MieuTa, -- MIEUTAMON - nvarchar(50)
		    @Gia, -- GIA - int
		    @SoLuong, -- SoLuongHienCo - int
		    @TinhTrang  -- TINHTRANG - nvarchar(30)
		    )
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH

COMMIT TRANSACTION
RETURN 1
GO

--Sửa giá món ăn 
use QLDatMon
GO
IF OBJECT_ID('usp_SuaGiaMonAn') IS NOT NULL
	DROP PROC usp_SuaGiaMonAn 
GO
CREATE PROCEDURE usp_SuaGiaMonAn 
	@TenMon nvarchar(50),
	@Gia int
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem món ăn có tồn tại không
		if not EXISTS(SELECT MADT FROM MONAN WHERE MADT = CURRENT_USER and TENMON = @TenMon)
		BEGIN
			PRINT N'Món ăn không tồn tại.'
			ROLLBACK TRAN
			RETURN 0
		END

		-- Kiểm tra xem giá món ăn có âm không
		if @Gia < 0
		begin
			PRINT N'Giá món ăn không được < 0.'
			ROLLBACK TRAN
			RETURN 0
		end

		update MONAN
		set GIA = @Gia 
		where MADT = CURRENT_USER and TENMON = @TenMon
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Sửa số lượng của 1 món ăn
use QLDatMon
GO
IF OBJECT_ID('usp_SuaSoLuong1MonAn_DT') IS NOT NULL
	DROP PROC usp_SuaSoLuong1MonAn_DT
GO
CREATE PROCEDURE usp_SuaSoLuong1MonAn_DT
	@TenMon nvarchar(50),
	@soluong int
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem món ăn có tồn tại không
		if not EXISTS(SELECT MADT FROM MONAN WHERE MADT = CURRENT_USER and TENMON = @TenMon)
		BEGIN
			PRINT N'Món ăn không tồn tại.'
			ROLLBACK TRAN
			RETURN 0
		END

		-- Kiểm tra xem giá món ăn có âm không
		if @soluong <= 0
		begin
			PRINT N'Số lượng không được <= 0.'
			ROLLBACK TRAN
			RETURN 0
		end

		update MONAN
		set SoLuongHienCo = @soluong 
		where MADT = CURRENT_USER and TENMON = @TenMon
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Sửa miêu tả của món ăn 
use QLDatMon
GO
IF OBJECT_ID('usp_SuaMieuTaMonAn') IS NOT NULL
	DROP PROC usp_SuaMieuTaMonAn
GO
CREATE PROCEDURE usp_SuaMieuTaMonAn
	@TenMon nvarchar(50),
	@MieuTaMon nvarchar(80)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem món ăn có tồn tại không
		if not EXISTS(SELECT MADT FROM MONAN WHERE MADT = CURRENT_USER and TENMON = @TenMon)
		BEGIN
			PRINT N'Món ăn không tồn tại.'
			ROLLBACK TRAN
			RETURN 0
		END

		update MONAN
		set MIEUTAMON = @MieuTaMon
		where MADT = CURRENT_USER and TENMON = @TenMon
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Sửa tình trạng của món ăn 
use QLDatMon
GO
IF OBJECT_ID('usp_SuaTinhTrangMonAn') IS NOT NULL
	DROP PROC usp_SuaTinhTrangMonAn
GO
CREATE PROCEDURE usp_SuaTinhTrangMonAn
	@TenMon nvarchar(50),
	@TinhTrang SMALLINT
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem món ăn có tồn tại không
		if not EXISTS(SELECT MADT FROM MONAN WHERE MADT = CURRENT_USER and TENMON = @TenMon)
		BEGIN
			PRINT N'Món ăn không tồn tại.'
			ROLLBACK TRAN
			RETURN 0
		END

		-- Kiểm tra xem tình trạng có hợp lệ không
		if @TinhTrang NOT IN(1, 0, -1)
		BEGIN
			print N'Tình trạng món ăn không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		update MONAN
		set TINHTRANG = @TinhTrang
		where MADT = CURRENT_USER and TENMON = @TenMon
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Xem danh tất cả sách đơn hàng của đối tác 
use QLDatMon
GO
IF OBJECT_ID('usp_Xem_DS_DonHang') IS NOT NULL
	DROP PROC usp_Xem_DS_DonHang 
GO
CREATE PROCEDURE usp_Xem_DS_DonHang
	@TrangThai SMALLINT
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		if @TrangThai not in (-1, 0, 1, 2, 3)
		BEGIN
			print N'Tình trạng đơn hàng không hợp lệ.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		SELECT dh.MADON, dh.TENKH, dh.TENTX, dh.TENDT, dh.DIACHICH, dh.THOIGIANLAP, dh.DIACHIGIAOHANG, dh.TRANGTHAI, dh.PHISP, dh.PHIVANCHUYEN, dh.TONGTIEN, dh.THANHTOAN, dh.THOIGIANGIAO
		FROM DONHANG dh
		WHERE dh.MADT = CURRENT_USER and dh.TRANGTHAI = @TrangThai
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Xem danh sách đơn hàng theo chi nhánh của đối tác 
use QLDatMon
GO
IF OBJECT_ID('usp_Xem_DS_DonHang_CN') IS NOT NULL
	DROP PROC usp_Xem_DS_DonHang_CN
GO
CREATE PROCEDURE usp_Xem_DS_DonHang_CN
	@DiaChiCN nvarchar(30),
	@TrangThai nvarchar(20)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra cửa hàng chi nhánh có tồn tại không 
		if not exists(SELECT MADT
					  from CHINHANHCH
					  where MADT = CURRENT_USER and DIACHICH = @DiaChiCN)
		BEGIN
			print N'Chi nhánh cửa hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		SELECT dh.MADON, dh.TENKH, dh.TENTX, dh.TENDT, dh.DIACHICH, dh.THOIGIANLAP, dh.DIACHIGIAOHANG, dh.TRANGTHAI, dh.PHISP, dh.PHIVANCHUYEN, dh.TONGTIEN, dh.THANHTOAN, dh.THOIGIANGIAO
		FROM DONHANG dh
		WHERE dh.MADT = CURRENT_USER AND dh.DIACHICH = @DiaChiCN and dh.TRANGTHAI = @TrangThai
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Xem đánh giá chi nhánh cửa hàng
use QLDatMon
GO
IF OBJECT_ID('usp_XemDanhGiaCuaHang') IS NOT NULL
	DROP PROC usp_XemDanhGiaCuaHang
GO
CREATE PROCEDURE usp_XemDanhGiaCuaHang
	@DiaChiCN nvarchar(30)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra cửa hàng chi nhánh có tồn tại không 
		if @DiaChiCN is not null and not exists(SELECT MADT
												from CHINHANHCH
											    where MADT = CURRENT_USER and DIACHICH = @DiaChiCN)
		BEGIN
			print N'Chi nhánh cửa hàng không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Nếu địa chỉ chi nhánh null sẽ hiện ra tất cả đánh giá
		if @DiaChiCN is null
		begin
			select*
			from DANHGIASHOP
			where MADT = CURRENT_USER
		end
		else
		begin
			select*
			from DANHGIASHOP
			where MADT = CURRENT_USER and DIACHICH = @DiaChiCN
		end
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Xem đánh giá món ăn cửa hàng
use QLDatMon
GO
IF OBJECT_ID('usp_XemDanhGiaMonAn') IS NOT NULL
	DROP PROC usp_XemDanhGiaMonAn
GO
CREATE PROCEDURE usp_XemDanhGiaMonAn
	@TenMon nvarchar(30)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra tên món có tồn tại không 
		if @TenMon is not null and not exists(SELECT MADT
											  from MONAN
											  where MADT = CURRENT_USER and TENMON = @TenMon)
		BEGIN
			print N'Tên món ăn không tồn tại.'
			ROLLBACK TRANSACTION
			RETURN 0
		END

		-- Nếu tên món ăn null sẽ hiện ra tất cả đánh giá
		if @TenMon is null
		begin
			select*
			from DANHGIATHUCAN
			where MADT = CURRENT_USER
		end
		else
		begin
			select*
			from DANHGIATHUCAN
			where MADT = CURRENT_USER and TENMON = @TenMon
		end
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Xem tổng doanh thu theo thời gian
go
if OBJECT_ID('usp_XemTongDoanhThu') is not null
	drop proc usp_XemTongDoanhThu
go
CREATE PROCEDURE usp_XemTongDoanhThu
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end
		
		select sum(PHISP) * 0.8
		from DONHANG
		where MADT = CURRENT_USER and TRANGTHAI = N'Đã giao hàng'
		group by MADT
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Xem món ăn bán chạy nhất
go
if OBJECT_ID('usp_XemMonAnBanChayNhat') is not null
	drop proc usp_XemMonAnBanChayNhat
go
CREATE PROCEDURE usp_XemMonAnBanChayNhat
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end
		
		SELECT TENMON
		from MONAN
		where MADT = CURRENT_USER and TENMON = (select distinct ct.TENMON
												from CHITIETDONHANG ct join DONHANG dh on dh.MADON = ct.MADON
												where ct.MADT = CURRENT_USER and dh.TRANGTHAI = N'Đã giao hàng'
												group by ct.TENMON
												having sum(SOLUONG) >= (select sum(SOLUONG)
																		from CHITIETDONHANG ct join DONHANG dh on dh.MADON = ct.MADON
																		where ct.MADT = CURRENT_USER and dh.TRANGTHAI = N'Đã giao hàng'
																		group by ct.TENMON))
		
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

-- Xóa cửa hàng chi nhánh
use QLDatMon
GO
IF OBJECT_ID('usp_XoaCuaHangChiNhanh') IS NOT NULL
	DROP PROC usp_XoaCuaHangChiNhanh
GO
CREATE PROCEDURE usp_XoaCuaHangChiNhanh @diachiCN nvarchar(30)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra cửa hàng chi nhánh có tồn tại không 
		if not exists(SELECT MADT
					  from CHINHANHCH
					  where MADT = CURRENT_USER and DIACHICH = @diachiCN)
		BEGIN
			print N'Chi nhánh cửa hàng không tồn tại.'
			ROLLBACK TRANSACTION
			--RETURN 11
		END

		-- Kiểm tra xem chi nhánh này đã được xuất hiện ở các bảng khác chưa
		if exists(SELECT MADT
				  from DONHANG
				  where MADT = CURRENT_USER and DIACHICH = @diachiCN)
		or exists(SELECT MADT
				  from DANHGIASHOP
				  where MADT = CURRENT_USER and DIACHICH = @diachiCN)
		BEGIN
			update CHINHANHCH 
			set TINHTRANG = N'Đóng cửa'
			where MADT = CURRENT_USER and DIACHICH = @diachiCN
		END
		else
		begin
			delete from CHINHANHCH where MADT = CURRENT_USER and DIACHICH = @diachiCN
		end
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
		--RETURN 011
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO

--Xóa món ăn của đối tác
use QLDatMon
GO
IF OBJECT_ID('usp_XoaMonAn') IS NOT NULL
	DROP PROC usp_XoaMonAn
GO
CREATE PROCEDURE usp_XoaMonAn 
	@TenMon nvarchar(50)
AS
BEGIN TRANSACTION
	BEGIN TRY
		-- Kiểm tra xem người chạy proc này có phải đối tác không
		if not exists(SELECT MADT 
					  from DOITAC
					  where Madt = CURRENT_USER)
		begin
			print current_user + N' không phải là mã đối tác hợp lệ.'
			rollback transaction
			return 0
		end

		-- Kiểm tra xem món ăn có tồn tại không
		if not EXISTS(SELECT MADT FROM MONAN WHERE MADT = CURRENT_USER and TENMON = @TenMon)
		BEGIN
			PRINT N'Món ăn không tồn tại.'
			ROLLBACK TRAN
			RETURN 0
		END
		
		-- Kiểm tra xem món ăn này đã được xuất hiện ở các bảng khác chưa
		if exists(SELECT MADT
				  from CHITIETDONHANG
				  where MADT = CURRENT_USER and TENMON = @TenMon)
		or exists(SELECT MADT
				  from DANHGIATHUCAN
				  where MADT = CURRENT_USER and TENMON = @TenMon)
		BEGIN
			update MONAN
			set TINHTRANG = N'Tạm ngưng'
			where MADT = CURRENT_USER and TENMON = @TenMon
		END
		else
		begin
			delete from MONAN where MADT = CURRENT_USER and TENMON = @TenMon
		end
	END TRY
	
	BEGIN CATCH
		ROLLBACK TRANSACTION 
		RETURN 0
	
	END CATCH
COMMIT TRANSACTION
RETURN 1
GO