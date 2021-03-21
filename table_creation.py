from sqlite3 import *
con=None
try:
	con=connect("student_record.db")		#connect to dbms
	print("connected")
	cursor=con.cursor()
	sql="create table student(rno int not null primary key CONSTRAINT positive_rno CHECK(rno > 0),name text CONSTRAINT Length_should_be_atleast_2 CHECK(LENGTH(name) > 1),marks int CONSTRAINT marks_within_range_1_to_100 CHECK(marks > 0))"
	cursor.execute(sql)
	print("table created")
except Exception as e:
	print("creation issue ",e)
finally:
	if con is not None:
		con.close()		#close the connection
		print("disconnected") 