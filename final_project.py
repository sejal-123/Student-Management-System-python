from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import socket
import requests
import bs4
from datetime import *
import pandas as pd
import matplotlib.pyplot as plt

#LOACTION

try:
	socket.create_connection( ("www.google.com", 80))
	res = requests.get("https://ipinfo.io")
	print(res)
	data=res.json()
	city_name=data['city']
except OSError as e:
	print("issue ", e)


#TEMPERATURE

try:
	socket.create_connection( ("www.google.com", 80))
	city = city_name
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city 
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address =  a1 + a2  + a3 		
	res = requests.get(api_address)
	print(res)
	data=res.json()
	main=data['main']
	temp=main['temp']
except KeyError as e1:
	print("check city name ",e1)
except OSError as e:
	print("issue ", e)


#QUOTE OF THE DAY

try:
	socket.create_connection(("www.google.com",80))

	res=requests.get("https://www.brainyquote.com/quote_of_the_day")
	print(res)
	
	soup=bs4.BeautifulSoup(res.text,'lxml')

	data=soup.find("img",{"class":"p-qotd"})

	qotd=data['alt']
except Exception as e:
	print("issue ",e)

degree_sign= u'\N{DEGREE SIGN}'
loctemp="Location : " + city_name + "\t" + "Temp : " + str(temp)+ str(degree_sign)+"C"
qotd="Quote of the day : \n" + qotd

#GRAPH

def graph():

	data=pd.read_sql_query("select * from student;",connect("student_record.db"))
	sorted_data=data.sort_values(by='marks',ascending=0)
	sdata=sorted_data.head()
	name=sdata['name'].tolist()
	marks=sdata['marks'].tolist()
	colors=['red','green','blue','red','green']

	plt.bar(name, marks, color=colors)
	plt.title("Batch Performance!")
	plt.xlabel("Names")
	plt.ylabel("Marks")
	plt.show()


def f1():
	adst.deiconify()
	root.withdraw()

def f2():
	root.deiconify()
	adst.withdraw()

def f3():
	vist.deiconify()
	root.withdraw()

def f4():
	root.deiconify()
	vist.withdraw()

def f5():
	upst.deiconify()
	root.withdraw()

def f6():
	root.deiconify()
	upst.withdraw()

def f7():
	dest.deiconify()
	root.withdraw()

def f8():
	root.deiconify()
	dest.withdraw()

def add():
	con=None
	try:
		con=connect("student_record.db")
		print("connected")
		try:
			rno=int(entrno.get())
			if rno<=0:
				entrno.delete(0,END)
				raise Exception ("rno should be a natural no")
		except ValueError:
			showerror("Error","invalid rno")
			entrno.delete(0,END)
			return
		name=entname.get()
		if name=="":
			raise Exception("Name cannot be empty")
		if (name.isalpha())!=True:
			entname.delete(0,END)
			raise Exception("invalid name")
		if len(name)<2:
			entname.delete(0,END)
			raise Exception("invalid name")
		try:
			marks=int(entmarks.get())
			if marks < 0 or marks > 100:
				entmarks.delete(0,END)
				raise Exception("marks should be between 1 - 100") 
		except ValueError:
			showerror("Error","invalid marks")
			entmarks.delete(0,END)
			return
		args=(rno,name,marks)
		cursor=con.cursor()
		sql="insert into student values('%d','%s','%d')"
		cursor.execute(sql % args)
		con.commit()
		showinfo("success","record added")
	except ValueError:
		showerror("Error","Input cannot be empty or invalid input")
	except Exception as e:
		showerror("Error","issue in insertion " + str(e))
		con.rollback()
	else:
		entrno.delete(0,END);		entname.delete(0,END);		entmarks.delete(0,END)
	finally:
		if con is not None:
			con.close()		
			print("disconnected")    
	
def view():
	stdata.delete(1.0,END)
	vist.deiconify()
	root.withdraw()
	con=None
	try:
		con=connect("student_record.db")
		print("connected")
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for d in data:
			info = info + str(d[0]) +"\t\t"+str(d[1])+"\t\t"+str(d[2]) +"\n"
		stdata.insert(INSERT,"ROLL NO"+"\t\t"+"NAME"+"\t\t"+"MARKS"+"\n\n"+info)	
	except Exception as e:
		showerror("select issue",e)
	finally:
		if con is not None:
			con.close()
			print("disconnected")

def update():
	con=None
	try:
		con=connect("student_record.db")
		print("connected")
		try:	
			rno=int(enturno.get())
			if rno<0:
				enturno.delete(0,END)
				raise Exception ("rno should be positive")
		except ValueError:
			showerror("Error","invalid rno")
			enturno.delete(0,END)
			return
		name=entuname.get()
		if name=="":
			raise Exception("Name cannot be empty")
		if (name.isalpha())!=True:
			entname.delete(0,END)
			raise Exception("invalid name")
		if len(name)<2:
			entname.delete(0,END)
			raise Exception("invalid name")
		try:
			marks=int(entumarks.get())
			if marks < 0 or marks > 100:
				entumarks.delete(0,END)
				raise Exception("marks should be between 1 - 100")
		except ValueError:
			showerror("Error","invalid marks")
			entumarks.delete(0,END)
			return
		args=(name,marks,rno)
		cursor=con.cursor()
		sql="update student set name='%s', marks='%d' where rno='%d' "
		cursor.execute(sql % args)
		if cursor.rowcount >= 1:
			con.commit()
			showinfo("success","record updated")
		else:
			showerror("issue","rno does not exist")
	except ValueError:
		showerror("Error","Input cannot be empty or invalid input")
	except Exception as e:
		showerror("Error","update issue " + str(e))
		con.rollback()
	else:
		enturno.delete(0,END);		entuname.delete(0,END);		entumarks.delete(0,END)	
	finally:	
		if con is not None:
			con.close()		
			print("disconnected")    


def delete():
	con=None
	try:
		con=connect("student_record.db")
		print("connected")
		rno=int(entdrno.get())
		if rno<0:
			entdrno.delete(0,END)
			raise Exception ("rno should be positive")
		args=(rno)
		cursor=con.cursor()
		sql="delete from student where rno = '%d' "
		cursor.execute(sql % args)
		if cursor.rowcount >= 1:
			con.commit()
			showinfo("success","record deleted")
		else:
			showerror(rno," student does not exist")
	except ValueError:
		showerror("Error","invalid input")
		entdrno.delete(0,END)
	except Exception as e:
		showerror("issue","deletion issue "+str(e))
		entdrno.delete(0,END)
	else:
		entdrno.delete(0,END)
	finally:
		if con is not None:
			con.close()
			print("disconnected")


#ROOT SMS

root=Tk()
root.title("S. M. S")
root.geometry("500x500+400+200")
root.configure(background="#3f72af")
root.resizable(False,False)

btnAdd=Button(root, text="Add", width=10, font=("arial",18,"bold"),command=f1)
btnView=Button(root, text="View", width=10, font=("arial",18,"bold"),command=view)
btnUpdate=Button(root, text="Update", width=10, font=("arial",18,"bold"),command=f5)
btnDelete=Button(root, text="Delete", width=10, font=("arial",18,"bold"),command=f7)
btnCharts=Button(root, text="Charts", width=10, font=("arial",18,"bold"),command=graph)
lblLocTemp=Label(root, text=loctemp, font=("arial",18))
lblQuote=Label(root, wraplength=500, text=qotd, anchor='w', justify='left', font=("arial",16))

btnAdd.pack(pady=5)
btnView.pack(pady=5)
btnUpdate.pack(pady=5)
btnDelete.pack(pady=5)
btnCharts.pack(pady=5)
lblLocTemp.pack(pady=5)
lblQuote.pack(pady=5)

#ADD STUDENT

adst=Toplevel(root)
adst.title("Add Student")
adst.geometry("500x500+400+200")
adst.configure(background="#dbe2ef")
adst.withdraw()

lblrno=Label(adst, text="Enter roll no", font=("arial",18,"bold"))
entrno=Entry(adst, bd=3, font=("arial",18))
lblname=Label(adst, text="Enter name", font=("arial",18,"bold"))
entname=Entry(adst, bd=3, font=("arial",18))
lblmarks=Label(adst, text="Enter marks", font=("arial",18,"bold"))
entmarks=Entry(adst, bd=3, font=("arial",18))
btnSave=Button(adst, text="Save", font=("arial",18,"bold"),command=add)
btnBack=Button(adst, text="Back", font=("arial",18,"bold"),command=f2)

lblrno.pack(pady=5)
entrno.pack(pady=5)
lblname.pack(pady=5)
entname.pack(pady=5)
lblmarks.pack(pady=5)
entmarks.pack(pady=5)
btnSave.pack(pady=5)
btnBack.pack(pady=5)

#VIEW STUDENT

vist=Toplevel(root)
vist.title("View Student")
vist.geometry("500x500+400+200")
vist.configure(background="#dbe2ef")
vist.withdraw()

stdata=ScrolledText(vist,width=45, height=25)
btnvback=Button(vist,text="Back", font=("arial",18,"bold"),command=f4)

stdata.pack(pady=5)
btnvback.pack(pady=5)

#UPDATE STUDENT

upst=Toplevel(root)
upst.title("Update Student")
upst.geometry("500x500+400+200")
upst.configure(background="#dbe2ef")
upst.withdraw()

lblurno=Label(upst, text="Enter roll no", font=("arial",18,"bold"))
enturno=Entry(upst, bd=3, font=("arial",18))
lbluname=Label(upst, text="Enter name", font=("arial",18,"bold"))
entuname=Entry(upst, bd=3, font=("arial",18))
lblumarks=Label(upst, text="Enter marks", font=("arial",18,"bold"))
entumarks=Entry(upst, bd=3, font=("arial",18))
btnuSave=Button(upst, text="Save", font=("arial",18,"bold"),command=update)
btnuBack=Button(upst, text="Back", font=("arial",18,"bold"),command=f6)

lblurno.pack(pady=5)
enturno.pack(pady=5)
lbluname.pack(pady=5)
entuname.pack(pady=5)
lblumarks.pack(pady=5)
entumarks.pack(pady=5)
btnuSave.pack(pady=5)
btnuBack.pack(pady=5)

#DELETE STUDENT

dest=Toplevel(root)
dest.title("Delete Student")
dest.geometry("500x500+400+200")
dest.configure(background="#dbe2ef")
dest.withdraw()

lbldrno=Label(dest, text="Enter roll no", font=("arial",18,"bold"))
entdrno=Entry(dest, bd=3, font=("arial",18))
btndSave=Button(dest, text="Save", font=("arial",18,"bold"),command=delete)
btndBack=Button(dest, text="Back", font=("arial",18,"bold"),command=f8)

lbldrno.pack(pady=5)
entdrno.pack(pady=5)
btndSave.pack(pady=5)
btndBack.pack(pady=5)


root.mainloop()