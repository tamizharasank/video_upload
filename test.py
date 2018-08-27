import MySQLdb
# from video_mysql import Select,Insert,Update,Delete
con=MySQLdb.connect("localhost","root","Whizible@123","videos")
cursor=con.cursor()

import os


select=Select()
d=select.api_instruction_select()
for x in range(0,len(d)):
	# print d[x][0]
	if d[x][0]=="naresh":
		print "already Exists"
	else:
		print "ff"
# for x in select.video_collection()										:
# 	print x,

i=Insert()	
# u=Update()
# de=Delete()
# d=i.instruction_set("myname","admin")
# print d
# dd=cursor.execute('SELECT last_insert_id()')
# path="/static/img/upload/video"
# sql=cursor.execute("INSERT INTO video_collection(`instruction_id`,`video_path`,`no_images`,`label_name`,`order_n`) VALUES (1,'%s','','','')"%(path))	
# print con.insert_id()

# d=[2,"jhggj","twoimg","flower","oojjj",5]
# u.video_collection(d)
# de.video_collection(2)

# os.system('rm -r static/img/upload/video/')



def a(v):
	d="Hello "+v
	return d
def b():
	c=a("world")
	print c
# cursor.execute("SELECT count(id) from instruction_set")
   
cursor.execute("SELECT count(id) from instruction_set")
# dat=con.last_insert_id()
# dat=cursor.fetchone()
# print dat