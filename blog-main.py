import re
import string
import webapp2
import jinja2
import os
from google.appengine.ext import db

USER_RE=re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE=re.compile(r"^.{3,20}$")
EMAIL_RE=re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
	return USER_RE.match(str(username))

def valid_password(password):
	return PASS_RE.match(str(password))

def valid_email(email):
	return EMAIL_RE.match(str(email))

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class mainpage(handler):
	def get(self):
		self.render("frontpage.html",pagetitle="BlogUp")

class signup(handler):
	def get(self):
		self.render('signup.html',pagetitle="Signup Page")
	def post(self):
		username=self.request.get('username')
		password=self.request.get('password')
		verify_password=self.request.get('verify_password')
		email=self.request.get('email')
		if username:
			if valid_username(username):
				username_error=""
			else:
				username_error="atleast 3 characters"
		else:
				username_error="username is required"
		
		if password:
			if valid_password(password):
				password_error=""
			else:
				password_error="atleast 3 characters"
		else:
			password_error="password is required"

		if email:
			if valid_email(email):
				email_error=""
			else:
				email_error="wmail is incorrect"
		else:
			email_error="email is required"

		if verify_password==password:
			verify_error=""
		else:
			verify_error="passwords do not match"

		if (username_error=="" and password_error=="" and verify_error=="" and email_error==""):
			self.redirect('/welcome')
		else:
			self.render('signup.html',pagetitle='Signup Page',username=username,password=password,email=email,username_error=username_error,password_error=password_error,email_error=email_error,verify_error=verify_error)

class login(handler):
	def get(self):
		self.render('login.html',pagetitle="Login Page")
	def post(self):
		username=self.request.get('username')
		password=self.request.get('password')
		if username and password:
			self.redirect('/welcome')
		else:
			self.render('login.html',pagetitle="Login Page",error="**Both fields are mandatory")

class welcome(handler):
	def get(self):
		self.render('posts.html',pagetitle='BLOGS')
	


app=webapp2.WSGIApplication([('/',mainpage),('/signup',signup),('/login',login),('/welcome',welcome)],debug=True)