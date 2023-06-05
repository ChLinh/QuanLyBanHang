USE QLDatMon

EXEC dbo.usp_XemThucDon

EXEC dbo.usp_SuaTinhTrangMonAn @TenMon = N'Mỳ bò',   -- nvarchar(50)
                               @TinhTrang = -1 -- nvarchar(20)

EXEC dbo.usp_SuaTinhTrangMonAn @TenMon = N'Mỳ bò',   -- nvarchar(50)
                               @TinhTrang = 1 -- nvarchar(20)

DECLARE @od DATETIME = '2022-2-10 23:5:10'
DECLARE @nd DATETIME = DATEADD(hh, 1, @od)

PRINT @nd

EXEC dbo.usp_XemThongTinDoiTac
EXEC dbo.usp_XemHopDong
EXEC usp_XemCuaHangChiNhanh NULL
EXEC dbo.usp_XemThucDon

EXEC dbo.usp_ThemMonAn @TenMon = N'Cơm gà',    -- nvarchar(50)
                       @MieuTa = N'Cơm kèm gà nướng',    -- nvarchar(100)
                       @Gia = 100000,         -- int
                       @TinhTrang = 1, -- nvarchar(30)
                       @SoLuong = 100      -- int

exec usp_Xem_DS_DonHang 0
