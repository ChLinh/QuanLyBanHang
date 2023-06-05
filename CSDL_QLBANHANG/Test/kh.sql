USE QLDatMon

exec USP_XEMDANHSACHCUAHANG

EXEC dbo.usp_TaoDonHang @MaDT = 'DT000001',     -- char(6)
                        @DiaChiCN = N'Lê Lai' -- nvarchar(30)

EXEC dbo.USP_XEMDANHSACHDONHANG @trangthai = 0 -- nvarchar(30)


EXEC dbo.usp_ThemMonAnVaoDonHang @MaDT = 'DT000001',    -- char(6)
                                    @tenmon = N'Mỳ bò', -- nvarchar(80)
                                    @madh = 'DH000001',    -- char(6)
                                    @soluong = 3   -- int


EXEC dbo.USP_XEMCHITIETDONHANG @MADH = 'DH000001' -- char(6)

EXEC dbo.usp_CongSoLuongMonAn_KH @MaDT = 'DT000001',    -- char(6)
                                    @tenmon = N'Mỳ bò', -- nvarchar(80)
                                    @madh = 'DH000001'    -- char(6)

EXEC dbo.USP_XEMCHITIETDONHANG @MADH = 'DH000001' -- char(6)

EXEC dbo.usp_GiamSoLuongMonAn_KH @MaDT = 'DT000001',    -- char(6)
                                    @tenmon = N'Mỳ bò', -- nvarchar(80)
                                    @madh = 'DH000001'    -- char(6)

EXEC dbo.USP_XEMCHITIETDONHANG @MADH = 'DH000001' -- char(6)

EXEC dbo.usp_XoaMonAnKhoiDonHang_KH @MaDT = 'DT000001',    -- char(6)
                                    @tenmon = N'Mỳ bò', -- nvarchar(80)
                                    @madh = 'DH000001'     -- char(6)


EXEC dbo.USP_DATDONHANG @madon = 'DH000001', @thanhtoan = N'Chuyển khoản', @diachigh = 'Lê Lai' -- char(6)

EXEC dbo.USP_XEMDANHSACHDONHANG @trangthai = 1 -- nvarchar(30)

EXEC dbo.usp_Xoa1DonHang_KH @madh = 'DH000001' -- char(6)

DECLARE @i int
EXEC @i = dbo.USP_THUCDON @MADT = 'DT000001' -- char(6)
PRINT @i
