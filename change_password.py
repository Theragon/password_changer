from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

from wtforms import Form, TextField, PasswordField, validators

import subprocess as sub
#from subprocess import Popen, PIPE
import sys

app = Flask(__name__)

test_user = 'tdurden'
test_pass = 'NewPassword1'
ad_url = sys.argv[1]


class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=1, max=25)])
	oldpass = PasswordField('Current password')
	newpass = PasswordField('New password', [
		validators.Required(),
		validators.EqualTo('confpass', message='Passwords must match')
	])
	confpass = PasswordField('Confirm password')


@app.route('/')
def index():
	form = RegistrationForm(request.form)
	return render_template('index.html', form=form)


@app.route('/change_password', methods=['POST'])
def change_password():
	form = RegistrationForm(request.form)
	if form.validate():
		print('form validated')
		username = request.form['username']
		newpass = request.form['newpass']
		oldpass = request.form['oldpass']
		#confpass = request.form['confpass']

		p = sub.Popen(['./change_pass.sh', oldpass, newpass, username, ad_url], stdout=sub.PIPE, stderr=sub.PIPE)
		out, err = p.communicate()
		if err:
			print(err)
			return err
		else:
			msg = out.split('\n')[-2]
			return msg

	return jsonify(form.errors)


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
