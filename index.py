from __future__ import unicode_literals

import os
import datetime
import sys
import random
import math
import time




from video_mysql import Select,Insert,Update,Delete

from flask import Flask, request, render_template, session, redirect, jsonify, send_from_directory,g, current_app
from flask_restful import Resource, Api





from flask_paginate import Pagination, get_page_args
import click

click.disable_unicode_literals_warning = True

from werkzeug import secure_filename
from contextlib import closing
from videosequence import VideoSequence
import moviepy.editor as mp
from multiprocessing import Process, Queue

from livereload import Server, shell


server = Server()

# run a shell command
server.watch('static/css/*.css', 'make static')
server.watch('static/js/*.js', 'make static')



some_queue = None



insert=Insert()
select=Select()
update=Update()
delete=Delete()
import MySQLdb
con=MySQLdb.connect("localhost","root","Whizible@123","videos")
cursor=con.cursor()

# from database import insert,select,update,delete
now = datetime.datetime.now().strftime('%d-%m-%Y')
now1 = datetime.datetime.now()
app = Flask(__name__)
api = Api(app)

server = Server(app.wsgi_app)

app.secret_key = "root"
app.config['img'] = 'static/img/upload/img'
app.config['video'] = 'static/img/upload/video'



# remember to use DEBUG mode for templates auto reload
# https://github.com/lepture/python-livereload/issues/144
app.debug = True



#CORS(app)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/index")
def login():
    return render_template("login.html")
    # API
@app.route("/api/create_module")
def api_index():
    return jsonify({"error":"success","msg":"created successfully"})
@app.route("/api/instruction_module",methods=['POST','GET'])
def api_instruction_module():
    name=request.form['name']
    admin=request.form['uploaded_by']
    d=select.api_instruction_select()    
    for x in range(0,len(d)):
        # print d[x][x]
        if str(d[x][0])==name:
            return jsonify({"error":"name already exists","uploaded_by":admin,"msg":""})        
        else:
            print d[x][0]
    d=insert.api_instruction_set(name,admin,"Finished")

    return jsonify({"error":"success","uploaded_by":admin,"id":d,"msg":"created successfully"})

@app.route("/api/api_videoto_image",methods=['POST','GET'])
def api_videotoimage(video,id,idc,vvid):
    cursor.execute("SELECT count(id) from video_collection where instruction_id=%s"%(id))
    c=cursor.fetchall()
    c=c[0][0]+1
    print vvid
    with closing(VideoSequence("static/img/upload/video/"+video)) as frames:
            for idx, frame in enumerate(frames[0:]):
                s="static/img/upload/img/"+str(id)+"_"+str(c)
                frame.save(s+"_{:04d}.jpg".format(idx+1))
                x=str(id)+"_"+str(c)+"_{:04d}.jpg".format(idx+1)
                order=idx+1
                label=str(id)+"_"+str(c)+"_{:04d}".format(idx+1)
                insert.training_images(idc,vvid,x,label,c,"Finished")
            update.video_collection(c,order,video)
    return "Finished"
@app.route("/api/video_module",methods=['POST','GET'])    
def api_video_module():
    id=request.form['id']   
    files1 = request.files['file']
    print id
    filename1 = secure_filename(files1.filename)
    filename1.replace(' ', '-')
    ff=filename1.split('.')
    files1.save(os.path.join(app.config['video'], filename1))
    cursor.execute("SELECT COUNT(id) from video_collection as id1 where instruction_id=%s"%(id))
    d=cursor.fetchall()
    ad=d[0][0]+1
    old=os.path.join(app.config['video'],filename1) 
    new=str(id)+"_step_"+str(ad)+"."+ff[1]
    new1=os.path.join(app.config['video'],new)
    os.rename(old,new1)
    label=str(id)+"_step_"+str(ad)    
    cursor.execute("SELECT count(id) from instruction_set")
    dat=cursor.fetchall()
    duration =  mp.VideoFileClip("static/img/upload/video/"+new).duration
    dur=int(duration)
    insert.video_collection(id,new,label,"Pending",dur)
    # api_videotoimage(new,id,id)
    # insert.video_collection(app.config['video'])



    return jsonify({"error":"false","id":id,"msg":"video Uploaded successfully"})





@app.route("/")
def index():
    return render_template("video_upload.html",id=id)

@app.route("/videotoimage", methods=['POST', 'GET'])
def videotoimage(video,id,vvid):
    cursor.execute("SELECT count(id) from video_collection where instruction_id=%s"%(id))
    c=cursor.fetchall()
    c=c[0][0]+1
    print video
    print c
    with closing(VideoSequence("static/img/upload/video/"+video)) as frames:
        for idx, frame in enumerate(frames[0:]):
                s="static/img/upload/img/"+str(id)+"_"+str(c)
                frame.save(s+"_{:04d}.jpg".format(idx))
                x=str(id)+"_"+str(c)+"_{:04d}.jpg".format(idx)
                label=str(id)+"_"+str(c)+"_{:04d}".format(idx)                
                order=idx+1
                insert.training_images(id,vvid,x,label,c,"Finished")
        update.video_collection(c,order,video)
	return "success"
# @app.route("/video_upload", methods=['POST', 'GET'])
# def video_upload():
# 	name=request.form['name']
# 	uploaded=request.form['label']

# 	# image upload
#     # files = request.files['image']
#     # file_type = request.form['selectbasic']
#     # filename = secure_filename(files.filename)
#     # filename.replace(' ', '-')
#     # files.save(os.path.join(app.config['img'], filename))
#     # video upload

    
# 	files1 = request.files['file']
# 	filename1 = secure_filename(files1.filename)
#  	ff=filename1.split('.')

# 	files1.save(os.path.join(app.config['video'], filename1))

#     cursor.execute("SELECT COUNT(id) from video_collection as id1 where instruction_id=%s"%(dat))
#     d=cursor.fetchall()
#     ad=d[0][0]+1
#     old=os.path.join(app.config['video'],filename1)	
#     new=str(dat)+"_step_"+str(ad)+"."+ff[1]
#     label=str(dat)+"_step_"+str(ad)
#     new1=os.path.join(app.config['video'],new)
#     os.rename(old,new1)
#     dat=insert.instruction_set(name,uploaded,"Finished")
#     insert.video_collection(dat,new,label,"Finished")
# videotoimage(new,dat)
# 	# insert.video_collection(app.config['video'])



# 	return redirect("/model")
@app.route("/reload_page",methods=['POST','GET'])
def reload():
    data=request.get_json()
    re=data.get('re')
    # print re
    con.commit()
    return "r"
@app.route("/video_upload", methods=['POST', 'GET'])
def video_upload():
    name=request.form['name']
    uploaded=request.form['label']

    # image upload
    # files = request.files['image']
    # file_type = request.form['selectbasic']
    # filename = secure_filename(files.filename)
    # filename.replace(' ', '-')
    # files.save(os.path.join(app.config['img'], filename))
    # video upload

    
    files1 = request.files['file']
    filename1 = secure_filename(files1.filename)
    ff=filename1.split('.')

    files1.save(os.path.join(app.config['video'], filename1))
    dat=insert.instruction_set(name,uploaded,"Finished")
    cursor.execute("SELECT COUNT(id) from video_collection as id1 where instruction_id=%s"%(dat))
    d=cursor.fetchall()
    ad=d[0][0]+1
    old=os.path.join(app.config['video'],filename1) 
    new=str(dat)+"_step_"+str(ad)+"."+ff[1]
    label=str(dat)+"_step_"+str(ad)
    new1=os.path.join(app.config['video'],new)
    os.rename(old,new1)
    duration =  mp.VideoFileClip("static/img/upload/video/"+new).duration
    dur=int(duration)    
    vvid=insert.video_collection(dat,new,label,"Finished",dur)
    videotoimage(new,dat,vvid)
    return redirect("/model")
    
    
@app.route("/existing_video_update",methods=['POST','GET'])
def existing_video_update():
    
    id=request.form['id']   
    files1 = request.files['file']
    print id
    filename1 = secure_filename(files1.filename)
    filename1.replace(' ', '-')
    ff=filename1.split('.')
    files1.save(os.path.join(app.config['video'], filename1))
    cursor.execute("SELECT COUNT(id) from video_collection as id1 where instruction_id=%s"%(id))
    d=cursor.fetchall()
    ad=d[0][0]+1
    old=os.path.join(app.config['video'],filename1) 
    new=str(id)+"_step_"+str(ad)+"."+ff[1]
    new1=os.path.join(app.config['video'],new)
    os.rename(old,new1)
    label=str(id)+"_step_"+str(ad)    
    cursor.execute("SELECT count(id) from instruction_set")
    dat=cursor.fetchall()
    duration =  mp.VideoFileClip("static/img/upload/video/"+new).duration
    dur=int(duration)
    vvid=insert.video_collection(id,new,label,"Pending",dur)
    # api_videotoimage(new,id,id)
    # insert.video_collection(app.config['video'])    
    status=api_videotoimage(new,id,id,vvid)
    cursor.execute("UPDATE video_collection SET status='%s' WHERE video_path='%s'"%(status,new))
    con.commit()
    return redirect("/model")
@app.route("/view")
def view():
    return render_template("dashboard.html",id=id)
@app.route("/model")
def model():
    con.commit()
    return render_template("model.html",id=id)
@app.route("/images")
def images():

    return render_template("images.html",id=id)

@app.route("/video_pending")
def video_pending():
    return render_template("video_pending.html",id=id)    
@app.route("/videos/<id>",methods=['POST','GET'])
def videos(id):
    # c=c
    cursor.execute("SELECT (SELECT COUNT(id) FROM video_collection) as nom,id,video_path,no_images,label_name,order_n,instruction_id FROM `video_collection` where instruction_id=%s"%(id))
    des = []
    for x in cursor.description:
        des.append(x[0])
    i = []
    for x in cursor.fetchall():

        i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4],des[5]: x[5],des[6]: x[6]})    
    return render_template("videos.html",data=i)    
@app.route("/get_instruction_data")
def get_instruction_data():
    des = []
    i = []    
    cursor.execute("SELECT id from instruction_set")
    for c in cursor.fetchall():
    # print c[0]
        cursor.execute("SELECT (SELECT count(instruction_id) from video_collection where instruction_id=%s) as nom,id,instruction_name,uploaded_by,status from instruction_set where id=%s"%(c[0],c[0]))        
        for y in cursor.description:
            des.append(y[0])
        for x in cursor.fetchall():            
            i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4]})
    return jsonify(i)
    
@app.route("/get_existing_model")
def get_existing_model():
    cursor.execute("SELECT * FROM `instruction_set`")
    des = []
    for x in cursor.description:
        des.append(x[0])
    i = []
    for x in cursor.fetchall():

        i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4],des[5]: x[5]})
    # c=videos(i)
    return jsonify(i)
@app.route("/get_model_data")
def get_model_data():
    cursor.execute("SELECT (SELECT COUNT(id) FROM video_collection) as nom,id,video_path,no_images,label_name,order_n FROM `video_collection`")
    des = []
    for x in cursor.description:
        des.append(x[0])
    i = []
    for x in cursor.fetchall():

        i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4],des[5]: x[5]})
    # c=videos(i)
    return jsonify(i)
@app.route("/get_videopending_data")
def get_videopending_data():
    cursor.execute("SELECT * FROM `video_collection`")
    des = []
    for x in cursor.description:
        des.append(x[0])
    i = []
    for x in cursor.fetchall():

        i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4],des[5]: x[5],des[6]: x[6],des[7]: x[7],des[8]: x[8]})
    # c=videos(i)
    return jsonify(i)

@app.route("/video_pending_update",methods=['POST','GET'])
def video_pending_update():
    data=request.get_json()
    ids=data.get("id")
    path=data.get("path")
    vvid=data.get("vvid")
    print ids,path
    status=api_videotoimage(path,ids,ids,vvid)
    cursor.execute("UPDATE video_collection SET status='%s' WHERE id='%s'"%(status,vvid))
    con.commit()
    return jsonify({"succ":"Updated successfully"})

@app.route("/instruction_data_update",methods=['POST','GET'])
def instruction_data_update():
    data=request.get_json()
    ids=data.get("id")
    name=data.get("name")
    # print ids,name
    cursor.execute("UPDATE instruction_set SET instruction_name='%s' WHERE id='%s'"%(name,ids))
    con.commit()
    return "Updated successfully"
@app.route("/view.json")
def viewjson():
    cursor.execute("SELECT * FROM instruction_set")
    des = []
    for x in cursor.description:
        des.append(x[0])
    i = []
    for x in cursor.fetchall():
        i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2], des[3]: x[3] })

    return jsonify(i)
@app.route("/dashboard_data")
def dashboard_data():
    cursor.execute("SELECT (select COUNT(id) from instruction_set) as id,(select COUNT(id) from video_collection) as id1 FROM instruction_set as i LEFT JOIN video_collection as v ON i.id = v.id")
    des = []
    for x in cursor.description:
        des.append(x[0])
    i = []
    for x in cursor.fetchall():
        i.append({des[0]: x[0],des[1]: x[1]})
    return jsonify(i)

@app.route('/image_select/', defaults={'page': 1})
@app.route("/image_select/<page>/<id>",methods=['POST','GET'])
def image_select(page,id):

	limit=20
	page=int(page)
	if(page):
		page=page
	else:
		page=1
	start_from = (page-1) * limit
	# print start_from,limit
	cursor.execute("SELECT * FROM training_images where instruction_id=%s ORDER BY image_path ASC LIMIT %s, %s"%(id,start_from,limit))
	des = []
	for x in cursor.description:
		des.append(x[0])
	i = []
	for x in cursor.fetchall():
		i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4]})
	return jsonify(i)
@app.route("/get_image_page/<pp>")
def get_image_page(pp):
	limit=20
	cursor.execute("SELECT COUNT(id) as id,instruction_id FROM training_images where instruction_id=%s"%(pp))
	des = []
	for x in cursor.description:
		des.append(x[0])
	i = []
	for x in cursor.fetchall():
		total_records=x[0]
		total_pages=math.ceil( total_records / limit)
		print int(total_pages)
		for y in range(0,int(total_pages)):
			i.append({des[0]: total_pages,des[1]:x[1]})
	return render_template("images.html",page=i)     

@app.route("/video_delete",methods=['POST','GET'])
def video_delete():
    data=request.get_json()
    dd=data.get("val")
    name=data.get("n")
    print dd,name        
    cursor.execute("DELETE from `video_collection` WHERE id='%s'"%(dd))
    con.commit()
    os.system("rm -r static/img/upload/video/%s"%(name))
    cursor.execute("SELECT image_path from training_images where video_id=%s"%(dd))
    for x in cursor.fetchall():
		nam=x[0]
		os.system("rm -r static/img/upload/img/%s"%(nam))
    cursor.execute("DELETE from `training_images` WHERE video_id=%s"%(dd))
    con.commit()		
    return "video deleted successfully"
@app.route("/image_delete",methods=['POST','GET'])
def image_delete():
    data=request.get_json()
    dd=data.get("val")
    name=data.get("n")        
    cursor.execute("DELETE from `training_images` WHERE id='%s'"%(dd))
    con.commit()
    os.system("rm -r static/img/upload/img/%s"%(name))
    return "Image deleted successfully"
@app.route("/model_data_delete",methods=['POST','GET'])
def model_data_delete():
    data=request.get_json()
    dd=data.get("id")    
    cursor.execute("SELECT image_path from training_images where instruction_id=%s"%(dd))
    for x in cursor.fetchall():        
        os.system("rm -r static/img/upload/img/%s"%(x[0]))
    cursor.execute("SELECT video_path from video_collection where instruction_id=%s"%(dd))    
    for y in cursor.fetchall():
        os.system("rm -r static/img/upload/video/%s"%(y[0]))

    cursor.execute("DELETE from `training_images` WHERE instruction_id=%s"%(dd))
    con.commit()
    cursor.execute("DELETE from `video_collection` WHERE instruction_id=%s"%(dd))
    con.commit()
    cursor.execute("DELETE from `instruction_set` WHERE id=%s"%(dd))
    con.commit()

    
    return "All data deleted successfully"

# @app.route("/dashboard_video_data")
# def dashboard_video_data():
#     cursor.execute("SELECT count(id) as id FROM video_collection")
#     des = []
#     for x in cursor.description:
#         des.append(x[0])
#     i = []
#     for x in cursor.fetchall():
#         i.append({des[0]: x[0]})
#     return jsonify(i)
    # file = request.files['file']
    # file.filename.encode("utf8")
    # status = 'success'
    # filename = secure_filename(file.filename)
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # file=filename
    # print(file)
    # return jsonify({'result': status})


@app.route("/page/<id>")
def page(id):
    cursor.execute('SELECT count(*) from training_images where video_id=%s'%(id))
    total = cursor.fetchone()[0]
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    sql = 'SELECT id,image_path from training_images where video_id={} order by image_path limit {}, {}'\
    .format(id,offset, per_page)
    cursor.execute(sql)
    users = cursor.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='users',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('images.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@app.route('/users/', defaults={'page': 1})
@app.route('/users', defaults={'page': 1})
@app.route('/users/page/<int:page>/')
@app.route('/users/page/<int:page>')
def users(page):
    cursor.execute('select count(*) from training_images')
    total = cursor.fetchone()[0]
    page, per_page, offset = get_page_args()
    sql = 'select id,image_path from training_images order by image_path limit {}, {}'\
        .format(offset, per_page)
    cursor.execute(sql)
    users = cursor.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='users',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('images.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           active_url='users-page-url',
                           )


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap4')


def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')


def get_alignment():
    return current_app.config.get('LINK_ALIGNMENT', '')


def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      alignment=get_alignment(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )







if __name__ == '__main__':
	# server.serve(liveport=5000)
# use custom host and port
	# server.serve(port=5000, host='0.0.0.0',debug=True)

    app.run("0.0.0.0","5000",debug=True)
           
	
