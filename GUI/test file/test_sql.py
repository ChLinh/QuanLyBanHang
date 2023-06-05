import pyodbc


DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-8LHJRLR'
DATABASE_NAME = 'QLSV'
username = 'hoang2'
password = '123'
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; Server=DESKTOP-8LHJRLR; Database=QLBanHangOnline; UID=' + username + '; PWD=' + password)

cursor = conn.cursor()
# for a in cursor.execute("select * from khachhang where makh = " + str('\''+'KH0001'+'\'')):
# #     print(a)
# for a in cursor.execute('SELECT CURRENT_USER'):
#     print(a)
# results = cursor.fetchall()



# dt = 'DT0001'
# sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
# sql = sql + f"EXEC @return_value = USP_XEMDANHSACHDONHANG N'Đang chờ tiếp nhận'"
# #sql = sql + f"EXEC @return_value = usp_TaoDonHang DT0001, N'Lê Lai'"
# #sql = sql + f"EXEC @return_value = usp_Xoa1DonHang_KH @madh = 'DH0001'"
# sql = sql + "\nselect @return_value"
# print(sql)
# #thanhCong = int(cursor.execute(sql).fetchone()[0])
# thanhCong = cursor.execute(sql).fetchall()
# #cursor.commit()
# print(thanhCong)

try:
    sql1 = f'exec usp_kiemtra'
    sql2 = f'select * from detai '
    res1 = cursor.execute(sql1)
    res2 = cursor.execute(sql2)
    pass
except:
    import ctypes  # An included library with Python install.   
    ctypes.windll.user32.MessageBoxW(0, "Lỗi transaction", "Thông báo", 0)
    print('error')
    pass



# for a in cursor.execute(f'declare @return_value int\nEXEC @return_value = USP_XEMDANHSACHCUAHANG {dt}'):
#     print(a)

# import ctypes  # An included library with Python install.   
# ctypes.windll.user32.MessageBoxW(0, "Xác nhận món ăn thành công", "Thông báo", 0)