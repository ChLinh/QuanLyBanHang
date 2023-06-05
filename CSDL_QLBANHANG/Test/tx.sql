USE QLDatMon

EXEC usp_XemDanhSachDHTheoKhuVuc

EXEC usp_ChonDonHang 'DH0001'

EXEC usp_XemDanhSachDHDangGiao

EXEC usp_ChuyenThanhDaGiaoHang 'DH0002'

EXEC usp_XemDanhSachDHDaGiao

EXEC dbo.usp_XemTaiKhoanNganHang

declare @return_value int
EXEC @return_value = usp_DaGiaoHang_TX DH0001
select @return_value