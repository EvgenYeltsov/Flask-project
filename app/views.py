from werkzeug.urls import url_parse
from app import fapp, render_template, flash, redirect, url_for, request, db
from app.forms import LoginForm, RegistrationForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from datetime import datetime
import requests


@fapp.route('/')
@fapp.route('/index')
@login_required
def index():
	posts = db.session.query(Post.body, Post.id, Post.title, Post.user_id, Post.timestamp, User.username).join(Post, Post.user_id==User.id).all()
	return render_template('index.html', title='Home Page', posts=posts, data=weather_app())


@fapp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		# if not user or not user.check_password(form.password.data):
		# 	return redirect(url_for('login'))
		login_user(user)
		next_page = request.args.get('next', url_for('index'))
		return redirect(next_page)
		# return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)


@fapp.route('/register', methods=['GET', 'POST'])
def register():
	reg_form = RegistrationForm()
	message = None

	if reg_form.validate_on_submit():
		username = reg_form.username.data
		email = reg_form.email.data

		user = User(username=username, email=email)
		user.set_password(reg_form.password.data)
		db.session.add(user)
		db.session.commit()
		message = 'Congratulations, you are now a registered user!'

	return render_template('register.html', title='Register', form=reg_form, message=message)


@fapp.route('/add_post', methods=['GET', 'POST'])
def add_post():
	p_form = PostForm()
	message = None

	if p_form.validate_on_submit():
		body = p_form.body.data
		title = p_form.title.data
		post = Post(body=body, timestamp=datetime.utcnow(), user_id=current_user.id, title=title)
		db.session.add(post)
		db.session.commit()
		message = 'Congratulations, your post add!'

	return render_template('add_post.html', title='New Post', form=p_form, message=message)


@fapp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
	post = Post.query.get(post_id)
	p_form = PostForm()
	message = None
	if p_form.validate_on_submit():
		post.body = p_form.body.data
		db.session.commit()
		message = 'Congratulations, your post edit!'

	return render_template('edit_post.html', title='Edit Post', form=p_form, message=message)


@fapp.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
	post = Post.query.get(post_id)
	db.session.delete(post)
	db.session.commit()
	return render_template('profile.html', title='Profile')


@fapp.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
		return render_template('profile.html', title='Profile')


@fapp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))


# @fapp.route('/weather_app', methods=['GET', 'POST'])
def weather_app():
	appid = "fc00fa7fab519f8e6bb68be3f364cb43"
	res = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Zaporizhzhia",
				 params={'units': 'metric', 'lang': 'ru', 'APPID': appid})
	data = res.json()
	# print(data)
	# print("Zaporizhzhia, UA")
	# print("conditions:", data['weather'][0]['description'])
	# print("temp:", data['main']['temp'])
	# print("temp_min:", data['main']['temp_min'])
	# print("temp_max:", data['main']['temp_max'])
	# print("Exception (weather):", e)
	temp1 = data['weather'][0]['description']
	temp2 = data['main']['temp']
	return f"Zaporozhye conditions: {temp1} , temp: {temp2} C"
