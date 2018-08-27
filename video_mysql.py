import MySQLdb
con=MySQLdb.connect("localhost","root","Whizible@123","videos")
cursor=con.cursor()





class Insert():
	"""docstring for Insert"""
	def instruction_set(self,name,video_name,fine):
		sql=cursor.execute("INSERT INTO instruction_set(`instruction_name`,`uploaded_by`,`status`) VALUES ('%s','%s','%s')"%(name,video_name,fine))
		c=con.insert_id()
		con.commit()
		return c
	def training_images(self,ids,vid,path,label,order,fine):
		sql=cursor.execute("INSERT INTO training_images(`instruction_id`,`video_id`,`image_path`,`label_name`,`order_n`,`status`) VALUES ('%s','%s','%s','%s','%s','%s')"%(ids,vid,path,label,order,fine))
		con.commit()
	def video_collection(self,idx,path,label,fine,dur):
		sql=cursor.execute("INSERT INTO video_collection(`instruction_id`,`video_path`,`no_images`,`label_name`,`order_n`,`status`,`duration`) VALUES ('%s','%s','s','%s','1','%s','%s')"%(idx,path,label,fine,dur))	
		c=con.insert_id()
		con.commit()
		return c	
	def api_instruction_set(self,name,admin,fine):
		sql=cursor.execute("INSERT INTO instruction_set(`instruction_name`,`uploaded_by`,`status`) VALUES ('%s','%s','%s')"%(name,admin,fine))
		c=con.insert_id()
		con.commit()
		return c				
class Select():
	"""docstring for Select"""
	def instruction_set(self):
		sql=cursor.execute("SELECT  instruction_set(`instruction_name`,`uploaded_by`) ")
		
	def training_images(self):
		sql=cursor.execute("SELECT  training_images(`instruction_id`,`video_id`,`image_path`,`label_name`,`order_n`) ")
		con.commit()
	def video_collection(self):
		sql=cursor.execute("SELECT * FROM video_collection")	
		v=cursor.fetchall()
		return v
	def api_instruction_select(self):
		cursor.execute("SELECT instruction_name from instruction_set")
		d=cursor.fetchall()
		return d
class Delete():
	"""docstring for Delete"""
	def instruction_set(self):
		sql=cursor.execute("DELETE FROM instruction_set WHERE ")
		con.commit()
	def training_images(self):
		sql=cursor.execute("DELETE FROM training_images WHERE")
		con.commit()
	def video_collection(self,id):
		sql=cursor.execute("DELETE FROM video_collection WHERE instruction_id='%s'"%(id))	
		con.commit()
class Update():
	"""docstring for Update"""
	def instruction_set(self):
		sql=cursor.execute("UPDATE instruction_set SET `instruction_name`='%s',`uploaded_by`='%s'")
		con.commit()
	def training_images(self):
		sql=cursor.execute("UPDATE training_images SET `instruction_id`='%s',`video_id`='%s',`image_path`='%s',`label_name`='%s',`order_n`='%s'")
		con.commit()
	def video_collection(self,image,order,idx):
		# print data[2]
		sql=cursor.execute("UPDATE video_collection SET `no_images`='%s',`order_n`='%s' WHERE `video_path`='%s'"%(order,image,idx))
		con.commit()

										

# i=Insert()	
# u=Update()
# de=Delete()
# i.video_collection()

# d=[2,"jhggj","twoimg","flower","oojjj",5]
# u.video_collection(d)
# de.video_collection(2)


if __name__ == '__main__':
	Insert()
	Select()
	Update()
	Delete()
