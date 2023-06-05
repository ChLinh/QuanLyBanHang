-- Code tạo partition
-- -1: Đã hủy 
-- 0: NULL
-- 1: Đang chờ xác nhận
-- 2: Đang giao hàng
-- 3: Giao hàng thành công
USE QLDatMon
GO
ALTER DATABASE QLDatMon
ADD FILEGROUP FG2

ALTER DATABASE QLDatMon
ADD FILEGROUP FG3

ALTER DATABASE QLDatMon
ADD FILEGROUP FG4

ALTER DATABASE QLDatMon
ADD FILEGROUP FG5

--Bước 1: Tạo filegroup
ALTER DATABASE QLDatMon
ADD FILE (
	NAME = FG2_0,
	FILENAME = 'F:\PartitionCSDL\FG2\DBPartition_2.ndf',
	SIZE = 1MB,
	MAXSIZE = UNLIMITED,
	FILEGROWTH = 1
) TO FILEGROUP FG2

ALTER DATABASE QLDatMon
ADD FILE (
	NAME = FG3_1,
	FILENAME = 'F:\PartitionCSDL\FG3\DBPartition_3.ndf',
	SIZE = 1MB,
	MAXSIZE = UNLIMITED,
	FILEGROWTH = 1
) TO FILEGROUP FG3

ALTER DATABASE QLDatMon
ADD FILE (
	NAME = FG4_2,
	FILENAME = 'F:\PartitionCSDL\FG4\DBPartition_4.ndf',
	SIZE = 1MB,
	MAXSIZE = UNLIMITED,
	FILEGROWTH = 1
) TO FILEGROUP FG4

ALTER DATABASE QLDatMon
ADD FILE (
	NAME = FG5_3,
	FILENAME = 'F:\PartitionCSDL\FG5\DBPartition_5.ndf',
	SIZE = 1MB,
	MAXSIZE = UNLIMITED,
	FILEGROWTH = 1
) TO FILEGROUP FG5

--Bước 2: Tạo partition function
CREATE PARTITION FUNCTION trangThaiDonHangPartitions(SMALLINT)
AS RANGE LEFT
FOR VALUES(-1, 0, 1, 2)

--Bước 3: Tạo partition scheme
CREATE PARTITION SCHEME trangThaiDonHangPartitionsScheme
AS PARTITION trangThaiDonHangPartitions
TO ([PRIMARY], FG2, FG3, FG4, FG5)

--Bước 4: Tạo clustered index trên cột chia partition
-- Xóa ràng buộc khóa ngoại nối vào khóa chính
ALTER TABLE dbo.CHITIETDONHANG
DROP CONSTRAINT FK_CHITIETD_CHITIETDO_DONHANG

-- Xóa khóa chính (nếu có)
ALTER TABLE dbo.DONHANG
DROP CONSTRAINT PK_DONHANG

-- Tạo khóa chính với non-clusterIndex
ALTER TABLE dbo.DONHANG
ADD PRIMARY KEY NONCLUSTERED(MADON)
ON [PRIMARY]

-- Tạo lại liên kết khóa ngoại cho khóa chính
alter table CHITIETDONHANG
   add constraint FK_CHITIETD_CHITIETDO_DONHANG foreign key (MADON)
      references DONHANG (MADON)
GO

-- Tạo clusterIndex cho thuộc tính partition
CREATE CLUSTERED INDEX IX_DONHANG
ON dbo.DONHANG
(
	TRANGTHAI
) ON trangThaiDonHangPartitionsScheme(TRANGTHAI)

SELECT p.partition_number AS partition_number, f.name AS file_group, p.rows AS row_count
FROM sys.partitions p
JOIN sys.destination_data_spaces dds ON p.partition_number = dds.destination_id
JOIN sys.filegroups f ON dds.data_space_id = f.data_space_id
WHERE OBJECT_NAME(OBJECT_ID) = 'DonHang' 
order by partition_number
