"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy import text

query = text ('SELECT * FROM users')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
app.app_context().push()
db.create_all()


app.config['SECRET_KEY'] = 'SecretKey1!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


@app.route('/')
def show_user():

    """Redirect to list of users"""

    return redirect ('/users')

@app.route('/users')
def users_listing():

    """Show lists of all users"""
    
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', users=users)

@app.route('/users/new')
def show_add_user():
    
    """Show add form"""

    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def create_users():

    """Creates a new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")
    
    

@app.route("/users/<int:user_id>")
def show_details(user_id):

    """Show details about the user"""

    user = User.query.get_or_404(user_id)

    return render_template("details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):

    """Show edit page on user"""

    user = User.query.get_or_404(user_id)
    
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):

    "submit edit user"

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delte_user(user_id):

    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect ("/users")
