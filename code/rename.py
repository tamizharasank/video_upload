
import os 


import MySQLdb
con=MySQLdb.connect("localhost","root","root","videos")
cursor=con.cursor()
# os.system('ls')

# old=os.path.join('/home/panamon/Videos/','El Chombo - Dame Tu Cosita feat. Cutty Ranks (Official Video) [Ultra Music].mp4')
# os.rename(old,'step_1.mp4')

cursor.execute("SELECT COUNT(id) from video_collection as id1 ")
d=cursor.fetchall()
c=d[0][0]+1
print str(c)+"jhhg"


# print os.path.join('')
