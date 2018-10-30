from app import app
from flask import render_template,Flask,request
import pymysql,json

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
	return render_template("index.html", subjects = subjects)


@app.route('/todo/api/v1.0/add_project', methods=['POST'])
def add_project():
	print(123456)
	data = {}
	name = request.form.get('project')
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


@app.route('/register', methods=['POST'])
def register():
	print(request.headers)
	print(request.form.get('name'))
	print(request.form.getlist('name'))
	print(request.form.get('nickname', default='little apple'))
	return 'welcome'