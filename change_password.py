from flask import Flask
from flask import request
from flask import render_template

import subprocess as sub
#from subprocess import Popen, PIPE
import sys

app = Flask(__name__)

test_user = 'tdurden'
test_pass = 'DoubleRa1nbow'
ad_url = sys.argv[1]


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/change_password', methods=['POST'])
def change_password():
	username = request.form['username']
	newpass = request.form['newpass']
	oldpass = request.form['oldpass']
	conf_pass = request.form['conf_pass']


	if newpass == conf_pass:
		try:
			result = sub.check_output(["/home/lleifsson/tmp/change_pass.sh", oldpass, newpass, username, ad_url])
			#p = Popen(["/home/lleifsson/tmp/change_pass.sh", oldpass, newpass, username], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			#output, err = p.communicate(b"input data that is passed to subprocess' stdin")
			#result = p.returncode
			return 'Password successfully changed'
		except sub.CalledProcessError as e:
			#print('e: ' + str(e))
			return 'Failed to change password'
		except:
			print('failure')
			#print('result: ' + result)
			return 'Failure'
		if result == 0:
			return 'OK'
		else:
			return result

	return 'Something went wrong'


if __name__ == '__main__':
	app.run(host='0.0.0.0')
