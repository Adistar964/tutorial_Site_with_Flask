from flaskfile.models import User, Post
from flask import redirect, url_for, render_template, request, session, flash, abort
from flaskfile.dataneeded import Register, Login, update, new_post
from flaskfile import app, db
from flaskfile import bcrypt
from flask_login import login_user, current_user, logout_user,login_required


@app.route('/comments', methods=['GET', 'POST'])
@login_required
def feedback():
	global link_data
	posts = Post.query.all()
	form = new_post()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('post has been successfully uploaded', 'success')
		return render_template('index.html', posts=posts, form=form)
	return render_template('index.html', posts=posts, form=form)


@app.route('/home')
@app.route('/')
def homepage():
	return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		redirect(url_for('homepage'))
	form = Register()
	if form.validate_on_submit():
		password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=password)
		db.session.add(user)
		db.session.commit()
		flash('Account created!   You Can Now Login', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)



@app.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('homepage'))
	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.forgot.data)
			flash('You are successfully logged in!', 'success')
			return redirect(url_for('homepage'))
		else:
			flash('Login unsuccessful! username or password is incorrect!', 'danger')
			return render_template('login.html', form=form)

	else:
		return render_template('login.html', form=form)



@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
	logout_user()
	flash('You are successfully logged out!', 'success')
	return redirect(url_for('homepage'))


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
	form = update()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Updated Your Account Successfully.', 'success')
		return redirect(url_for('homepage'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image = url_for('static', filename='pics/' + current_user.image)
	return render_template('account.html', image_file=image, form=form)



@app.route('/comments/<int:post_id>/update', methods=['POST','GET'])
@login_required
def post_update(post_id):
	form = new_post()
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	elif form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your Post has been successfully updated!', 'success')
		return redirect(url_for('feedback'))

	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('update_post.html', form=form)

@app.route('/comments/<int:post_id>/delete', methods=['POST','GET'])
@login_required
def post_delete(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		if current_user.username == 'Ali':
			db.session.delete(post)
			db.session.commit()
			flash('The requested Post is successfully deleted!', 'success')
			return redirect(url_for('feedback'))
		abort(404)
	db.session.delete(post)
	db.session.commit()
	flash('The requested Post is successfully deleted!', 'success')
	return redirect(url_for('feedback'))


@app.route('/home/tkintertutorials/FirstProgram')
def video():
	return render_template('tkinter1.html')

@app.route('/home/tkintertutorials/Buttons')
def tkinterbuttons():
	return render_template('tkinter2.html')


@app.route('/YourPosts')
@login_required
def YourPosts():
	posts = Post.query.filter_by(author=current_user).all()
	if posts:
		return render_template('YourPosts.html', posts=posts)
	else:
		return render_template('nopost.html')

@app.route('/home/tkintertutorials')
def tkintertuts():
	return render_template('tkinter.html')


