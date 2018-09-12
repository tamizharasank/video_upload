from __future__ import unicode_literals

import os
import datetime
import sys
import random
import math
import time
import glob
import uuid
from PIL import Image
import pandas as pd
import xml.etree.ElementTree as ET
import hashlib

from video_mysql import Select,Insert,Update,Delete

from flask import Flask, request,url_for, render_template, session, redirect, jsonify, send_from_directory,g, current_app
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
con=MySQLdb.connect("localhost","root1","whizible@123","videos")
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


@app.route("/image_to_xml")
def xml_to_csv(path):
    xml_list = []
    for xml_file in sorted(glob.glob(path + '/*.xml')):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df
def image_to_xml_test(vv,fname):
	f=fname
	vv=str(vv)
	for x in sorted(glob.iglob('static/img/upload/video/training/%s/images/test/*.jpg'%(fname))):		
		g=x.split("/")[::-1]
		h=g[0].split(".")[0]
		# print x.split("/")[1]
		i=Image.open('static/img/upload/video/training/%s/images/test/%s'%(f,g[0]))
		width,height=i.size
		new_width=300
		new_height=300
		left = (width - new_width)/2
		top = (height - new_height)/2
		right = (width + new_width)/2
		bottom = (height + new_height)/2
		xml="""<annotation>
		<folder>%s</folder>
		<filename>%s</filename>
		<path>/var/www/whizible.in/public_html/videos/static/img/upload/video/training/%s/images/test/%s</path>
		<source>
			<database>Unknown</database>
		</source>
		<size>
			<width>%s</width>
			<height>%s</height>
			<depth>3</depth>
		</size>
		<segmented>0</segmented>
		<object>
			<name>%s</name>
			<pose>Unspecified</pose>
			<truncated>0</truncated>
			<difficult>0</difficult>
			<bndbox>
				<xmin>%s</xmin>
				<ymin>%s</ymin>
				<xmax>%s</xmax>
				<ymax>%s</ymax>
			</bndbox>
		</object>
	</annotation>"""%(f,g[0],f,g[0],width,height,vv,left,bottom,right,top)
		file=open("static/img/upload/video/training/"+f+"/images/test/"+h+".xml","w+")
		file.write(xml)		
	return "success"	
def image_to_xml_train(vv,fname):
	f=fname
	vv=str(vv)
	for x in sorted(glob.iglob('static/img/upload/video/training/%s/images/train/*.jpg'%(fname))):		
		g=x.split("/")[::-1]
		h=g[0].split(".")[0]
		# print x.split("/")[1]
		i=Image.open('static/img/upload/video/training/%s/images/train/%s'%(f,g[0]))
		width,height=i.size
		new_width=300
		new_height=300
		left = (width - new_width)/2
		top = (height - new_height)/2
		right = (width + new_width)/2
		bottom = (height + new_height)/2
		xml="""<annotation>
		<folder>%s</folder>
		<filename>%s</filename>
		<path>/var/www/whizible.in/public_html/videos/static/img/upload/video/training/%s/images/train/%s</path>
		<source>
			<database>Unknown</database>
		</source>
		<size>
			<width>%s</width>
			<height>%s</height>
			<depth>3</depth>
		</size>
		<segmented>0</segmented>
		<object>
			<name>%s</name>
			<pose>Unspecified</pose>
			<truncated>0</truncated>
			<difficult>0</difficult>
			<bndbox>
				<xmin>%s</xmin>
				<ymin>%s</ymin>
				<xmax>%s</xmax>
				<ymax>%s</ymax>
			</bndbox>
		</object>
	</annotation>"""%(f,g[0],f,g[0],width,height,vv,left,bottom,right,top)
		file=open("static/img/upload/video/training/"+f+"/images/train/"+h+".xml","w+")
		file.write(xml)

	return "success"	


@app.route("/configfile_2_pbtxt")
def configfile_2_pbtxt(f,b,name):
    name=str(name)
    b=b.split("_")[::-1][0]
    
    # print b
    for x in xrange(1,int(b)+1):
    	file=open("static/img/upload/video/training/%s/ssd_mobilenet_v1_pets.config"%(f),"w+")
    	n="""model {
  ssd {
    num_classes: %s
    box_coder {
      faster_rcnn_box_coder {
        y_scale: 10.0
        x_scale: 10.0
        height_scale: 5.0
        width_scale: 5.0
      }
    }
    matcher {
      argmax_matcher {
        matched_threshold: 0.5
        unmatched_threshold: 0.5
        ignore_thresholds: false
        negatives_lower_than_unmatched: true
        force_match_for_each_row: true
      }
    }
    similarity_calculator {
      iou_similarity {
      }
    }
    anchor_generator {
      ssd_anchor_generator {
        num_layers: 6
        min_scale: 0.2
        max_scale: 0.95
        aspect_ratios: 1.0
        aspect_ratios: 2.0
        aspect_ratios: 0.5
        aspect_ratios: 3.0
        aspect_ratios: 0.3333
      }
    }
    image_resizer {
      fixed_shape_resizer {
        height: 300
        width: 300
      }
    }
    box_predictor {
      convolutional_box_predictor {
        min_depth: 0
        max_depth: 0
        num_layers_before_predictor: 0
        use_dropout: false
        dropout_keep_probability: 0.8
        kernel_size: 1
        box_code_size: 4
        apply_sigmoid_to_scores: false
        conv_hyperparams {
          activation: RELU_6,
          regularizer {
            l2_regularizer {
              weight: 0.00004
            }
          }
          initializer {
            truncated_normal_initializer {
              stddev: 0.03
              mean: 0.0
            }
          }
          batch_norm {
            train: true,
            scale: true,
            center: true,
            decay: 0.9997,
            epsilon: 0.001,
          }
        }
      }
    }
    feature_extractor {
      type: 'ssd_mobilenet_v1'
      min_depth: 16
      depth_multiplier: 1.0
      conv_hyperparams {
        activation: RELU_6,
        regularizer {
          l2_regularizer {
            weight: 0.00004
          }
        }
        initializer {
          truncated_normal_initializer {
            stddev: 0.03
            mean: 0.0
          }
        }
        batch_norm {
          train: true,
          scale: true,
          center: true,
          decay: 0.9997,
          epsilon: 0.001,
        }
      }
    }
    loss {
      classification_loss {
        weighted_sigmoid {
          anchorwise_output: true
        }
      }
      localization_loss {
        weighted_smooth_l1 {
          anchorwise_output: true
        }
      }
      hard_example_miner {
        num_hard_examples: 3000
        iou_threshold: 0.99
        loss_type: CLASSIFICATION
        max_negatives_per_positive: 3
        min_negatives_per_image: 0
      }
      classification_weight: 1.0
      localization_weight: 1.0
    }
    normalize_loss_by_num_matches: true
    post_processing {
      batch_non_max_suppression {
        score_threshold: 1e-8
        iou_threshold: 0.6
        max_detections_per_class: 100
        max_total_detections: 100
      }
      score_converter: SIGMOID
    }
  }
}

train_config: {
  batch_size: 10
  optimizer {
    rms_prop_optimizer: {
      learning_rate: {
        exponential_decay_learning_rate {
          initial_learning_rate: 0.004
          decay_steps: 800720
          decay_factor: 0.95
        }
      }
      momentum_optimizer_value: 0.9
      decay: 0.9
      epsilon: 1.0
    }
  }
  fine_tune_checkpoint: "/var/www/whizible.in/public_html/videos/static/img/upload/video/training/ssd_mobilenet_v1_coco_11_06_2017/model.ckpt"
  from_detection_checkpoint: true
  data_augmentation_options {
    random_horizontal_flip {
    }
  }
  data_augmentation_options {
    ssd_random_crop {
    }
  }
}

train_input_reader: {
  tf_record_input_reader {
    input_path: "/var/www/whizible.in/public_html/videos/static/img/upload/video/training/%s/data/train.record"
  }
  label_map_path: "/var/www/whizible.in/public_html/videos/static/img/upload/video/training/%s/data/customObjDetect.pbtxt"
}

eval_config: {
  num_examples: 10
}

eval_input_reader: {
  tf_record_input_reader {
    input_path: "/var/www/whizible.in/public_html/videos/static/img/upload/video/training/%s/data/test.record"
  }
  label_map_path: "/var/www/whizible.in/public_html/videos/static/img/upload/video/training/%s/data/customObjDetect.pbtxt"
  shuffle: false
  num_readers: 1
}"""%(str(x),f,f,f,f)
    	# print x
    	file.write(n)
	f1=open("static/img/upload/video/training/%s/data/customObjDetect.pbtxt"%(f),"a+")
    c="""item {
 id: %s
 name: '%s'
}\n"""%(b,name)


    f1.write(c)
    return "success"
    
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
def api_videotoimage(folder,video,id,idc,vvid):
    cursor.execute("SELECT count(id) from video_collection where instruction_id=%s"%(id))
    c=cursor.fetchall()
    c=c[0][0]+1
    
    b=video.split(".")[0]
    b=str(b)
    print vvid
    f=str(folder)
    with closing(VideoSequence("static/img/upload/video/"+video)) as frames:
            for idx, frame in enumerate(frames[0:]):
                s="static/img/upload/img/"+str(id)+"_"+str(c)
                vid=str(folder)
                s1="static/img/upload/video/training/"+f+"/images/train/"+str(id)+"_"+str(c)
                s2="static/img/upload/video/training/"+f+"/images/test/"+str(id)+"_"+str(c)
                frame.save(s+"_{:04d}.jpg".format(idx+1))
                if (idx+1)<=90:                	
                	frame.save(s1+"_{:04d}.jpg".format(idx+1))
                if (idx+1)<=10:
                	frame.save(s2+"_{:04d}.jpg".format(idx+1))
                x=str(id)+"_"+str(c)+"_{:04d}.jpg".format(idx+1)
                order=idx+1
                label=str(id)+"_"+str(c)+"_{:04d}".format(idx+1)
                insert.training_images(idc,vvid,x,label,c,"Finished")
            update.video_collection(c,order,video)
            vv=str(id)+"_step_"+str(c)
            image_to_xml_test(vv,str(f))
            image_to_xml_train(vv,str(f))
            bb=b.split("_")[::-1][0]
            if int(bb)!=1:
            	if f in os.listdir('static/img/upload/video/training'):

		            for dir in ['test','train']:
		            	
		            	image_path = os.path.join(os.getcwd(), 'static/img/upload/video/training/{}/images/{}'.format(f,dir))
		            	xml_df = xml_to_csv(image_path)
		            	f1=open('static/img/upload/video/training/{}/data/{}_labels.csv'.format(f,dir),'a+')
		            	xml_df.to_csv(f1, index=None,header=False)
            else:


      				for dir in ['test','train']:
      					image_path = os.path.join(os.getcwd(), 'static/img/upload/video/training/{}/images/{}'.format(f,dir))
      					xml_df = xml_to_csv(image_path)
      					xml_df.to_csv('static/img/upload/video/training/{}/data/{}_labels.csv'.format(f,dir), index=None)	        
            
            os.system("python generate_tfrecord.py --csv_input=static/img/upload/video/training/{}/data/test_labels.csv  --output_path=static/img/upload/video/training/{}/data/test.record --file_name={}".format(f,f,b))
            os.system("python generate_tfrecord.py --csv_input=static/img/upload/video/training/{}/data/train_labels.csv  --output_path=static/img/upload/video/training/{}/data/train.record --file_name={}".format(f,f,b))
            configfile_2_pbtxt(f,b,vv)
            # print f,b
            
    return "Finished"

@app.route("/api/api_videoto_image_new",methods=['POST','GET'])
def api_videotoimage_new(folder,video,id,idc,vvid):
    cursor.execute("SELECT count(id) from video_collection where instruction_id=%s"%(id))
    c=cursor.fetchall()
    c=c[0][0]
    
    b=video.split(".")[0]
    b=str(b)
    print vvid
    f=str(folder)
    with closing(VideoSequence("static/img/upload/video/"+video)) as frames:
            for idx, frame in enumerate(frames[0:]):
                s="static/img/upload/img/"+str(id)+"_"+str(c)
                
                vid=str(folder)
                s1="static/img/upload/video/training/"+vid+"/images/train/"+str(id)+"_"+str(c)
                s2="static/img/upload/video/training/"+vid+"/images/test/"+str(id)+"_"+str(c)
                frame.save(s+"_{:04d}.jpg".format(idx+1))
                if (idx+1)<=90:
                	frame.save(s1+"_{:04d}.jpg".format(idx+1))
                if (idx+1)<=10:
                	frame.save(s2+"_{:04d}.jpg".format(idx+1))
                x=str(id)+"_"+str(c)+"_{:04d}.jpg".format(idx+1)
                order=idx+1
                label=str(id)+"_"+str(c)+"_{:04d}".format(idx+1)
                insert.training_images(idc,vvid,x,label,c,"Finished")
            update.video_collection(c,order,video)
            vv=str(id)+"_step_"+str(c)
            image_to_xml_test(vv,str(f))
            image_to_xml_train(vv,str(f))
            bb=b.split("_")[::-1][0]
            if int(bb)!=1:
            	
	            if f in os.listdir('static/img/upload/video/training'):
		            for dir in ['test','train']:
		            	image_path = os.path.join(os.getcwd(), 'static/img/upload/video/training/{}/images/{}'.format(f,dir))
		            	xml_df = xml_to_csv(image_path)
		            	f1=open('static/img/upload/video/training/{}/data/{}_labels.csv'.format(f,dir),'a+')
		            	xml_df.to_csv(f1, index=None,header=False)
            else:            	

      				for dir in ['test','train']:
      					image_path = os.path.join(os.getcwd(), 'static/img/upload/video/training/{}/images/{}'.format(f,dir))
      					xml_df = xml_to_csv(image_path)
      					xml_df.to_csv('static/img/upload/video/training/{}/data/{}_labels.csv'.format(f,dir), index=None)
            
            os.system("python generate_tfrecord.py --csv_input=static/img/upload/video/training/{}/data/test_labels.csv  --output_path=static/img/upload/video/training/{}/data/test.record --file_name={}".format(f,f,b))
            os.system("python generate_tfrecord.py --csv_input=static/img/upload/video/training/{}/data/train_labels.csv  --output_path=static/img/upload/video/training/{}/data/train.record --file_name={}".format(f,f,b))           
            configfile_2_pbtxt(f,b,vv)
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
    vid=str(id)+"_step"
    if len(os.listdir('static/img/upload/video/training'))!=0:    	
    	if vid in os.listdir('static/img/upload/video/training'):
    		print "Exists"
    	else:
    		os.mkdir('static/img/upload/video/training/'+str(vid),0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/data',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/test',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/train',0777)    	

    else:
		os.mkdir('static/img/upload/video/training/'+str(vid),0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/data',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/test',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/train',0777)    	


    insert.video_collection(id,new,label,"Pending",dur)
    # api_videotoimage(new,id,id)
    # insert.video_collection(app.config['video'])


    con.commit()
    return jsonify({"error":"false","id":id,"msg":"video Uploaded successfully"})




@app.route("/")
def login():
	x=uuid.uuid4().hex
	return render_template("login.html",id=x)
@app.route("/login_validate", methods=['POST'])
def login_validate():
    data = request.get_json()
    user_id = data.get("user_name")
    password = data.get("password")
    idd=data.get("id")
    pp=hashlib.md5(password.encode('utf')).hexdigest()

    cursor.execute("SELECT access_token from admin where username='%s' AND password='%s'" % (user_id, pp))
    d=cursor.fetchone()
    # print d

    # acc=d[0]
    # print d
    if d==None:

    	re = "n"
    elif idd!=d[0]:
      cursor.execute("UPDATE admin SET access_token='%s' where username='%s'"%(idd,user_id))
      con.commit()
      
      session['username'] = user_id
      user_id = user_id
      session['access_token'] = idd
      idd = idd
      user_session(user_id)
      re = "s"
    else:
      session['username'] = user_id
      user_id = session['username']
      session['access_token'] = idd
      user_session(user_id)
      cursor.execute("UPDATE admin SET access_token='%s' where username='%s'"%(idd,user_id))
      con.commit()

      re = "n"        
    # print re

    return re
def user_session(userid):
  cursor.execute("SELECT * from admin where username = '%s'"%(userid))
  x=cursor.fetchone()
  session['username'] = x[1]
  user_id=session['username']
  session['password'] = x[2]
  password = session['password']
  session['access_token'] = x[4]
  idd=session['access_token']
  return user_id,idd,password
def session_check(name,pas,new_acc):
  cursor.execute("SELECT access_token FROM admin where username='%s' and password = '%s'"%(name,pas))
  d=cursor.fetchone()
  access=d[0]
  if access==new_acc:
    re="s"
  else:
    re="n"
    redirect("/logout")
  return re

@app.route("/video-upload")
def video_upload_new():
	# x=user_session()
	# id=session['username']
  if session.get('username','not')!='not':    
    ids=session['username']
    pas=session['password']
    new=session['access_token']
    xx=session_check(ids,pas,new)
    if xx=='s':
      # pass
      # print xx
      con.commit()
      return render_template("video_upload.html",id=id)

    else:
      return redirect("/logout")
  else:
    # print "logout"
    return redirect("/logout")  
	
@app.route("/video_training")
def video_training():
  if session.get('username','not')!='not':    
    ids=session['username']
    pas=session['password']
    new=session['access_token']
    xx=session_check(ids,pas,new)
    if xx=='s':
      # pass
      # print xx
      con.commit()
      return render_template("video_train.html",id=id)

    else:
      return redirect("/logout")
  else:
    # print "logout"
    return redirect("/logout")  

@app.route("/get_training_data",methods=['POST','GET'])
def get_training_data():

  des = []
  i = []    

  cursor.execute("SELECT * from train ")        
  for y in cursor.description:
      des.append(y[0])
  for x in cursor.fetchall():            
      i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4],des[5]: x[5]})

  return jsonify(i)
@app.route("/training_data_update",methods=['POST','GET'])
def training_data_update_start():
  data=request.get_json()
  id=data.get('id')
  n=data.get('name')
  rid=data.get('rid')
  cursor.execute("UPDATE train SET status='TS',kill_id='',`dis`='onprocess'")
  con.commit()
  s=str(rid)+"_step"
  os.system("bin/protoc object_detection/protos/*.proto --python_out=.")
  os.system("export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim")
  # ../../protoc/bin/protoc object_detection/protos/*.proto --python_out=.
  # export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
  os.system("nohup python legacy/train.py --logtostderr --train_dir=static/img/upload/video/training/{}/ --pipeline_config_path=static/img/upload/video/training/{}/ssd_mobilenet_v1_pets.config > static/img/upload/video/training/{}/loss.txt &".format(s,s,s))
  pid = os.popen("ps aux | grep train.py | awk '{print $2}'").readlines()[0]
  cursor.execute("UPDATE train SET status='T',kill_id='%s',`dis`='start' where id=%s"%(pid,id))
  con.commit()


  return "success"
@app.route("/training_data_update_stop",methods=['POST','GET'])
def training_data_update_stop():
  data=request.get_json()
  id=data.get('id')
  n=data.get('name')
  k=data.get('kill')
  os.system("kill -9 %s"%(k))
  cursor.execute("UPDATE `train` SET `kill_id`='',`status`='NOT',`dis` = 'stop'")
  con.commit()
  rid=str(id)+"_step"
  dd=glob.glob('static/img/upload/video/training/{}/*.meta'.format(rid))
  dd=max(dd,key=os.path.getctime).split('.')[1]
  dd=dd.split("-")[::-1][0]
  dd="model.ckpt-"+str(dd)
  os.system("python legacy/export_inference_graph.py --input_type image_tensor --pipeline_config_path static/img/upload/video/training/{}/ssd_mobilenet_v1_pets.config --trained_checkpoint_prefix static/img/upload/video/training/{}/{} --output_directory static/img/upload/video/training/{}".format(rid,rid,dd,rid))
  return "Killed Your Process => %s"  %(k)

  
@app.route("/videotoimage", methods=['POST', 'GET'])
def videotoimage(folder,video,id,vvid):
    cursor.execute("SELECT count(id) from video_collection where instruction_id=%s"%(id))
    c=cursor.fetchall()
    c=c[0][0]+1
    
    b=video.split(".")[0]
    # print b
    b=str(b)
    print video
    print c
    f=str(folder)
    with closing(VideoSequence("static/img/upload/video/"+video)) as frames:
        for idx, frame in enumerate(frames[0:]):
                s="static/img/upload/img/"+str(id)+"_"+str(c)
                vid=str(folder)
                s1="static/img/upload/video/training/"+vid+"/images/train/"+str(id)+"_"+str(c)
                s2="static/img/upload/video/training/"+vid+"/images/test/"+str(id)+"_"+str(c)
                frame.save(s+"_{:04d}.jpg".format(idx+1))
                if (idx+1)<=90:
                	frame.save(s1+"_{:04d}.jpg".format(idx+1))
                if (idx+1)<=10:
                	frame.save(s2+"_{:04d}.jpg".format(idx+1))
                x=str(id)+"_"+str(c)+"_{:04d}.jpg".format(idx+1)
                label=str(id)+"_"+str(c)+"_{:04d}".format(idx+1)                
                order=idx+1
                insert.training_images(id,vvid,x,label,c,"Finished")
        update.video_collection(c,order,video)
        vv=str(id)+"_step_"+str(c)
        image_to_xml_test(vv,str(f))
        image_to_xml_train(vv,str(f))
        bb=b.split("_")[::-1][0]
        if int(bb)!=1:
        	
	        if f in os.listdir('static/img/upload/video/training') and int(bb)==1:            	
		            	image_path = os.path.join(os.getcwd(), 'static/img/upload/video/training/{}/images/{}'.format(f,dir))
		            	xml_df = xml_to_csv(image_path)
		            	f1= open('static/img/upload/video/training/{}/data/{}_labels.csv'.format(f,dir),'a+')
		            	xml_df.to_csv(f1, index=None,header=False)
        else:


    			for dir in ['test','train']:
    				image_path = os.path.join(os.getcwd(), 'static/img/upload/video/training/{}/images/{}'.format(f,dir))
    				xml_df = xml_to_csv(image_path)
    				xml_df.to_csv('static/img/upload/video/training/{}/data/{}_labels.csv'.format(f,dir), index=None)

        os.system("python generate_tfrecord.py --csv_input=static/img/upload/video/training/{}/data/test_labels.csv  --output_path=static/img/upload/video/training/{}/data/test.record --file_name={}".format(f,f,b))        
        os.system("python generate_tfrecord.py --csv_input=static/img/upload/video/training/{}/data/train_labels.csv  --output_path=static/img/upload/video/training/{}/data/train.record --file_name={}".format(f,f,b))
        configfile_2_pbtxt(f,b,vv)
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
    ded=select.api_instruction_select()
    for x in xrange(0,len(ded)):
    	if str(ded[x][0])==name:
    		return render_template("video_upload.html",data="name is already exists")
    	else:
    		print "None"

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
    vid=str(dat)+"_step"

    if len(os.listdir('static/img/upload/video/training'))!=0:    	    	

    	if vid in os.listdir('static/img/upload/video/training'):
    		print "Exists"
    	else:
    		os.mkdir('static/img/upload/video/training/'+str(vid),0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/data',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/test',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/train',0777)    	

    else:
		os.mkdir('static/img/upload/video/training/'+str(vid),0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/data',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/test',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/train',0777)    	
    vvid=insert.video_collection(dat,new,label,"Finished",dur)
    videotoimage(vid,new,dat,vvid)
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
    vid=str(id)+"_step"

    if len(os.listdir('static/img/upload/video/training'))!=0:
    	

    	if vid in os.listdir('static/img/upload/video/training'):
    		print "Exists"
    	else:
    		os.mkdir('static/img/upload/video/training/'+str(vid),0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/data',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/test',0777)
    		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/train',0777)    	

    else:
		os.mkdir('static/img/upload/video/training/'+str(vid),0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/data',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/test',0777)
		os.mkdir('static/img/upload/video/training/'+str(vid)+'/images/train',0777)    	
    vvid=insert.video_collection(id,new,label,"Pending",dur)
    # api_videotoimage(new,id,id)
    # insert.video_collection(app.config['video']) 
    vid=str(id)+"_step"      
    status=api_videotoimage(vid,new,id,id,vvid)
    cursor.execute("UPDATE video_collection SET status='%s' WHERE video_path='%s'"%(status,new))
    con.commit()
    return redirect("/model")
@app.route("/view")
def view():
	# x=user_session()
  if session.get('username','not')!='not':    
    ids=session['username']
    pas=session['password']
    new=session['access_token']
    xx=session_check(ids,pas,new)
    if xx=='s':
      pass
      print xx
      return render_template("dashboard.html",id=id)

    else:
      return redirect("/logout")
  else:
    print "logout"
    return redirect("/logout")

  # return render_template("dashboard.html",id=id)

@app.route("/model")
def model():
  
  if session.get('username','not')!='not':    
    ids=session['username']
    pas=session['password']
    new=session['access_token']
    xx=session_check(ids,pas,new)
    if xx=='s':
      # pass
      # print xx
      con.commit()
      return render_template("model.html",id=id)

    else:
      return redirect("/logout")
  else:
    # print "logout"
    return redirect("/logout")
    
@app.route("/images")
def images():
  if session.get('username','not')!='not':    
    ids=session['username']
    pas=session['password']
    new=session['access_token']
    xx=session_check(ids,pas,new)
    if xx=='s':
      # pass
      # print xx
      con.commit()
      return render_template("images.html",id=id)

    else:
      return redirect("/logout")
  else:
    # print "logout"
    return redirect("/logout")

@app.route("/video_pending")
def video_pending():
  if session.get('username','not')!='not':    
    ids=session['username']
    pas=session['password']
    new=session['access_token']
    xx=session_check(ids,pas,new)
    if xx=='s':
      # pass
      # print xx
      con.commit()
      return render_template("video_pending.html",id=id)

    else:
      return redirect("/logout")
  else:
    # print "logout"
    return redirect("/logout")    
@app.route("/videos/<id>",methods=['POST','GET'])
def videos(id):
    # c=c        
	# x=user_session()
	# id=session['username']
  if session.get('username','not')!='not':    
    ids=session['username']
    pas=session['password']
    new=session['access_token']
    xx=session_check(ids,pas,new)
    if xx=='s':
      # pass
      # print xx
      con.commit()
      cursor.execute("SELECT (SELECT COUNT(id) FROM video_collection) as nom,id,video_path,no_images,label_name,order_n,instruction_id FROM `video_collection` where instruction_id=%s"%(id))
      des = []
      for x in cursor.description:
        des.append(x[0])
      i = []
      for x in cursor.fetchall():
        i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4],des[5]: x[5],des[6]: x[6]})
      return render_template("videos.html",data=i,id=id)

    else:
      return redirect("/logout")
  else:
    # print "logout"
    return redirect("/logout")      
	
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
        	en=int((x[1]/4)-1)
        	en=hashlib.md5(str(en).encode('utf')).hexdigest()
        	i.append({des[0]: x[0], des[1]: x[1], des[2]: x[2],des[3]: x[3],des[4]: x[4],"enc":en})
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
    vid=path.split("_")[0]
    vid=str(vid)+"_step"
    print ids,path
    status=api_videotoimage_new(vid,path,ids,ids,vvid)
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
	# x=user_session()
	# id=session['username']
  if session.get('username','not')!='not':    
    ids=session['username']
    pas=session['password']
    new=session['access_token']
    xx=session_check(ids,pas,new)
    if xx=='s':
      # pass
      # print xx
      con.commit()
      limit=20
      cursor.execute("SELECT COUNT(id) as id,instruction_id FROM training_images where instruction_id=%s"%(pp))
      des = []
      for x in cursor.description:
        des.append(x[0])
      i = []
      for x in cursor.fetchall():
        total_records=x[0]
        total_pages=math.ceil( total_records / limit)      
      for y in range(0,int(total_pages)):
        i.append({des[0]: total_pages,des[1]:x[1]})      
      return render_template("images.html",page=i,id=id)

    else:
      return redirect("/logout")
  else:
    # print "logout"
    return redirect("/logout")      
	

@app.route("/video_delete",methods=['POST','GET'])
def video_delete():
    data=request.get_json()
    dd=data.get("val")
    name=data.get("n")
    print dd,name        
    cursor.execute("DELETE from `video_collection` WHERE id='%s'"%(dd))
    con.commit()
    h=name.split(".")
    os.system("rm -r static/img/upload/video/%s"%(name))
    os.system("rm -r static/img/upload/video/training/"+str(h[0]))
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

    h=str(dd)+"_step"
    # print h
    os.system("rm -r static/img/upload/video/training/"+str(h))    
    cursor.execute("DELETE from `training_images` WHERE instruction_id=%s"%(dd))
    con.commit()

    cursor.execute("DELETE from `video_collection` WHERE instruction_id=%s"%(dd))
    con.commit()
    cursor.execute("DELETE from `instruction_set` WHERE id=%s"%(dd))
    con.commit()
    cursor.execute("DELETE from `train` WHERE instruction_id=%s"%(dd))
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




@app.route("/logout")
def logout():
	# x=user_session()
  if session.get('access_token','not')!='not' and session.get('access_token','not')!='not':
    
  	idd=session['access_token']
  	user_id=session['username']
  	nnid=uuid.uuid1()
  	# cursor.execute("UPDATE admin SET access_token='%s' where username='%s'"%(nnid,user_id))
  	# con.commit()		
  	session.pop('username', None)
  	session.pop('access_token', None)
  	return redirect("/")
  else:
  	
	return redirect("/")



if __name__ == '__main__':
	# server.serve(liveport=5000)
# use custom host and port
	# server.serve(port=5000, host='0.0.0.0',debug=True)

    app.run("0.0.0.0","5000",debug=True)
           
	
