USE QLDatMon

--DoiTac
EXEC sp_addrole 'DoiTac'
GRANT EXECUTE ON usp_XemHopDong TO DoiTac
GRANT EXECUTE ON usp_XemThongTinDoiTac TO DoiTac
GRANT EXECUTE ON usp_XemCuaHangChiNhanh TO DoiTac
GRANT EXECUTE ON usp_ThemCuaHangChiNhanh TO DoiTac
GRANT EXECUTE ON usp_SuaDiaChiCuaHangChiNhanh TO DoiTac
GRANT EXECUTE ON usp_SuaTenCuaHang TO DoiTac
GRANT EXECUTE ON usp_CapNhatThoiGianMoCuaChiNhanhCuaHang TO DoiTac
GRANT EXECUTE ON usp_CapNhatThoiGianDongCuaChiNhanhCuaHang TO DoiTac
GRANT EXECUTE ON usp_CapNhatTinhTrangChiNhanhCuaHang TO DoiTac
GRANT EXECUTE ON usp_XemThucDon TO DoiTac
GRANT EXECUTE ON usp_ThemMonAn TO DoiTac
GRANT EXECUTE ON usp_SuaGiaMonAn TO DoiTac
GRANT EXECUTE ON usp_SuaMieuTaMonAn TO DoiTac
GRANT EXECUTE ON usp_SuaTinhTrangMonAn TO DoiTac
GRANT EXECUTE ON usp_Xem_DS_DonHang TO DoiTac
GRANT EXECUTE ON usp_Xem_DS_DonHang_CN TO DoiTac
GRANT EXECUTE ON usp_XemDanhGiaCuaHang TO DoiTac
GRANT EXECUTE ON usp_XemDanhGiaMonAn TO DoiTac
GRANT EXECUTE ON usp_XemTongDoanhThu TO DoiTac
GRANT EXECUTE ON usp_XemMonAnBanChayNhat TO DoiTac
GRANT EXECUTE ON usp_XoaCuaHangChiNhanh TO DoiTac
GRANT EXECUTE ON usp_XoaMonAn TO DoiTac
GRANT EXECUTE ON usp_SuaSoLuong1MonAn_DT TO DoiTac
GRANT EXECUTE ON USP_XEMCHITIETDONHANG TO DoiTac

--KhachHang
EXEC SP_ADDROLE 'KhachHang'
GO
GRANT EXECUTE ON USP_XEMKHACHHANG TO KhachHang
GRANT EXECUTE ON USP_DATDONHANG TO KhachHang
GRANT EXECUTE ON USP_XEMDANHSACHCUAHANG TO KhachHang
GRANT EXECUTE ON USP_XEMDANHSACHDONHANG TO KhachHang
GRANT EXECUTE ON USP_XEMCHITIETDONHANG TO KhachHang
GRANT EXECUTE ON USP_THUCDON TO KhachHang
GRANT EXECUTE ON USP_DANHGIAMONAN TO KhachHang
GRANT EXECUTE ON USP_CAPNHATDANHGIAMONAN TO KhachHang
GRANT EXECUTE ON USP_DANHGIASHOP TO KhachHang
GRANT EXECUTE ON USP_CAPNHATDANHGIASHOP TO KhachHang
GRANT EXECUTE ON USP_DANHGIATAIXE TO KhachHang
GRANT EXECUTE ON USP_CAPNHATDANHGIATAIXE TO KhachHang
GRANT EXEC ON usp_TaoDonHang TO KhachHang
GRANT EXEC ON usp_ThemMonAnVaoDonHang TO KhachHang
GRANT EXEC ON usp_ThayDoiSoLuongMonAn_KH TO KhachHang
GRANT EXEC ON usp_XoaMonAnKhoiDonHang_KH TO KhachHang
GRANT EXEC ON usp_Xoa1DonHang_KH TO KhachHang
GRANT EXEC ON usp_HuyDonHang_KH TO KhachHang
GRANT EXEC ON usp_GiamSoLuongMonAn_KH TO KhachHang
GRANT EXEC ON usp_CongSoLuongMonAn_KH TO KhachHang

--TaiXe
EXEC sp_addrole 'TAIXE'
GRANT EXECUTE ON usp_XemThongTinTaiXe TO TAIXE
GRANT EXECUTE ON usp_XemDanhSachDHTheoKhuVuc TO TAIXE
GRANT EXECUTE ON usp_XemDanhSachDHDaGiao TO TAIXE
GRANT EXECUTE ON usp_ChonDonHang TO TAIXE
GRANT EXECUTE ON usp_TheoDoiThuNhap TO TAIXE
GRANT EXECUTE ON usp_ChuyenThanhDaGiaoHang TO TAIXE
GRANT EXECUTE ON usp_XemTaiKhoanNganHang TO TAIXE 
GRANT EXEC ON usp_XemDanhSachDHDangGiao TO TAIXE

--NhanVien
EXEC sp_addrole 'NhanVien'
GRANT EXECUTE ON usp_XemThongTin TO NhanVien
GRANT EXECUTE ON usp_XemDanhSachDangKi TO NhanVien
GRANT EXECUTE ON usp_XemHopDongDaLap TO NhanVien
GRANT EXECUTE ON usp_DuyetHopDong TO NhanVien
GRANT EXECUTE ON usp_DanhSachHopDongSapHetHan TO NhanVien
GRANT EXECUTE ON usp_KiemTraHopDongSapHetHan TO NhanVien
GRANT EXECUTE ON usp_GiaHanHopDong TO NhanVien

--QuanTri
EXEC sp_addrole 'QuanTri', 'db_accessadmin'

GRANT SELECT, UPDATE, INSERT, DELETE
ON NHANVIEN
TO QuanTri
WITH GRANT OPTION

GRANT SELECT, UPDATE
ON DOITAC
TO QuanTri
WITH GRANT OPTION

GRANT SELECT, UPDATE
ON KHACHHANG
TO QuanTri
WITH GRANT OPTION

GRANT SELECT, UPDATE
ON TAIXE
TO QuanTri
WITH GRANT OPTION

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------ Account 
--Khach Hang
CREATE LOGIN [KH000001] WITH PASSWORD = '123', DEFAULT_DATABASE = QLDatMon
CREATE USER [KH000001] FROM LOGIN [KH000001]
EXEC sp_addrolemember 'KhachHang', 'KH000001'

CREATE LOGIN [KH000002] WITH PASSWORD = '123', DEFAULT_DATABASE = QLDatMon
CREATE USER [KH000002] FROM LOGIN [KH000002]
EXEC sp_addrolemember 'KhachHang', 'KH000002'

--Doi Tac
CREATE LOGIN [DT000001] WITH PASSWORD = '123'
CREATE USER [DT000001] FROM LOGIN [DT000001]
EXEC sp_addrolemember 'DoiTac', 'DT000001'

--Nhân viên
CREATE LOGIN [NV000001] WITH PASSWORD = '123'
CREATE USER [NV000001] FROM LOGIN [NV000001]
EXEC sp_addrolemember 'NhanVien', 'NV000001'

-- Tài xế
CREATE LOGIN [TX000001] WITH PASSWORD = '123'
CREATE USER [TX000001] from login [TX000001]
exec sp_addrolemember 'TAIXE', 'TX000001'
