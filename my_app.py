import requests
import base64
from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
	return 'Index Page'

@app.route('/add/')
def add_attachment_description():
	return render_template('add_attachment_description.html')

@app.route('/submit_data/', methods=["POST"])
def submit_data():
	username = request.form["Username"]
	password = request.form["pwd"]
	bug_id = request.form["bugid"]
	reporter_email = request.form["email"]
	amount = request.form["amount"]
	reported_date = request.form["reported_date"]
	fixed_date = request.form["fixed_date"]
	awarded_date = request.form["awarded_date"]
	publish = request.form["deserves_recognition"]
	credit1 = request.form["credit1"]
	credit2 = request.form["credit2"]
	credit3 = request.form["credit3"]
	r = add_attachment_to_bugzilla(username, password, bug_id, reporter_email, amount, reported_date, fixed_date, awarded_date, publish, credit1, credit2, credit3)
	return r

def add_attachment_to_bugzilla(username, password, bug_id, reporter_email, amount, reported_date, fixed_date, awarded_date, publish, credit1, credit2, credit3):
	if publish == "Yes":
		publish = "True"
	elif publish == "No":
		publish = "False"
	else:
		publish = ""
	base_url = "http://localhost:8080/bmo/rest/"
	headers = {'Accept': 'application/json'}
	login_url = base_url + 'login' + '?login=' + username + '&password=' + password 
	login_resp = requests.get(login_url, headers=headers)
	token = login_resp.json()['token']
	print token
	add_attachment_url = base_url + 'bug/' + str(bug_id) + '/attachment'
	token_attachment_url = add_attachment_url + '?token=' + token
	encoded_data = base64.b64encode('Bug bounty data')
	bounty_summary = reporter_email + ',' + amount + ',' + reported_date + ',' + fixed_date + ',' + awarded_date + ','+ publish + ',' + credit1 + ',' + credit2 + ',' + credit3 
	params = {
			'content_type': 'text/plain',
			'data': encoded_data,
			'summary': bounty_summary,
			'encoding': 'base64',
			'file_name': 'bugbounty.data',
			'is_obsolete': '0',
			'is_patch': '0',
			'is_private': '1'
		}
	r = requests.post(url=token_attachment_url, data=params, headers=headers)
	print r.text
	return "Aabha"
if __name__ == '__main__':
		app.debug = True
		app.run()

