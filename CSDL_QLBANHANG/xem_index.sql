USE QLDatMon

SELECT so.name AS TableName, si.name AS IndexName, si.type_desc AS IndexType
FROM sys.indexes si
JOIN sys.objects so ON si.object_id = so.object_id
WHERE so.type = 'U' AND si.name IS NOT NULL
ORDER BY so.name, si.type