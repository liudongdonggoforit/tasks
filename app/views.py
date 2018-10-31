#coding:utf-8
from app import app
from flask import render_template,Flask,request
import pymysql,json,datetime

#获取所有科目
@app.route('/todo/api/v1.0/subjects', methods=['GET'])
def getSubjects():
	db = pymysql.connect("118.25.217.21", "root", "123456", "task")
	cursor = db.cursor()
	sql = "select * from tb_subject"
	try:
		cursor.execute(sql)
		subjects = cursor.fetchall()
		data = []
		for subject in subjects:
			result = {}
			result["id"] = subject[0]
			result["name"] = subject[1]
			data.append(result)
	except Exception as e:
		db.rollback()
	db.close()
	print(json.dumps(data))
	return  json.dumps(data)

@app.route('/')
@app.route('/index')
def index():
	subjects = json.loads(getSubjects())
	tasks = json.loads(get_tasks())
	return render_template("index.html", subjects = subjects, tasks = tasks)

#获取所有任务
@app.route('/todo/api/v1.0/tasks')
def get_tasks():
	print("get_tasks")
	db = pymysql.connect("118.25.217.21", "root", "123456", "task")
	cursor = db.cursor()
	sql = "select * from tb_tasks"
	try:
		cursor.execute(sql)
		tasks = cursor.fetchall()
		data = []
		for task in tasks:
			result = {}
			result["t_id"] = task[0]
			result["title"] = task[2]
			result["des"] = task[3]
			result["createtime"] = task[4]
			result["finishtime"] = task[5]
			result["content"] = task[6]

			data.append(result)
	except Exception as e:
		print(e)
		db.rollback()
	db.close()
	return json.dumps(data, default=datetime_handler)

@app.route('/todo/api/v1.0/tasks_by_sid', methods=['GET'])
def get_tasks_by_sid():
	s_id = long(request.args.get('subject_id'))
	print(s_id)
	db = pymysql.connect("118.25.217.21", "root", "123456", "task")
	cursor = db.cursor()
	sql = "select * from tb_tasks where s_id = %d" % s_id
	print(sql)
	data = []
	try:
		cursor.execute(sql)
		tasks = cursor.fetchall()
		for task in tasks:
			result = {}
			result["t_id"] = task[0]
			result["title"] = task[2]
			result["des"] = task[3]
			result["createtime"] = task[4]
			result["finishtime"] = task[5]
			result["content"] = task[6]

			data.append(result)
	except Exception as e:
		db.rollback()
	db.close()
	return json.dumps(data,default=datetime_handler)


#添加新科目
@app.route('/todo/api/v1.0/add_subject', methods=['POST'])
def add_project():
	print(123456)
	data = {}
	name = request.form.get('subject')
	db = pymysql.connect("118.25.217.21","root","123456","task")
	cursor = db.cursor()
	sql = "insert into tb_subject(s_name) value ('%s')" % (name)
	try:
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		db.rollback()
	db.close()
	return json.dumps(data)

#增加任务
@app.route('/todo/api/v1.0/add_task', methods=['POST'])
def add_task():
	print("add_task")
	db = pymysql.connect("118.25.217.21","root", "123456", "task")
	cursor = db.cursor()
	id = long(request.form.get('project_id'))
	title = request.form.get('title')
	content = request.form.get('content')
	des = request.form.get('des')
	createtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	sql = "insert into tb_tasks(s_id, t_title, t_content, t_des, t_createtime)" \
	" values ('%d','%s','%s','%s','%s')" % (id, title, content, des, createtime)
	try:
		print(sql)
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	db.close()
	return "add_task"

#测试
@app.route('/register', methods=['POST'])
def register():
	print(request.headers)
	print(request.form.get('name'))
	print(request.form.getlist('name'))
	print(request.form.get('nickname', default='little apple'))
	return 'welcome'

def datetime_handler(x):
	if isinstance(x, datetime.datetime):
		return x.isoformat()
	raise TypeError("Unknown type")