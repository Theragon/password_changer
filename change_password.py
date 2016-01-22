from flask import Flask
from flask import request
from flask import render_template
#from flask import jsonify
from flask import flash
from flask import redirect
from flask import url_for

from wtforms import Form, TextField, PasswordField, validators

#import subprocess as sub
from subprocess import Popen, PIPE
import sys

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'cocacolazero'

test_user = 'tdurden'
test_pass = '1OfficeBitch'
ad_url = sys.argv[1]


class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=1, max=25)])
	oldpass = PasswordField('Current password')
	newpass = PasswordField('New password', [
		validators.Required(),
		validators.EqualTo('confpass', message='Passwords must match')
	])
	confpass = PasswordField('Confirm password')


@app.route('/', methods=['GET', 'POST'])
def index():
	form = RegistrationForm(request.form)
	if request.method == 'GET':
		return render_template('index.html', form=form)

	if request.method == 'POST' and form.validate():
		print('form validated')
		username = request.form['username']
		newpass = request.form['newpass']
		oldpass = request.form['oldpass']
		#confpass = request.form['confpass']

		p = Popen(['./change_pass.sh', oldpass, newpass, username, ad_url], stdout=PIPE, stderr=PIPE)
		out, err = p.communicate()
		if err:
			flash(err)
			return redirect(url_for('index'))
		else:
			msg = out.split('\n')[-2]
			flash(msg)
			return redirect(url_for('index'))

	for key, value in form.errors.iteritems():
		flash(value[0])
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
