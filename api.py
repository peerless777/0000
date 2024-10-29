# FILTERS !!!
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags

from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, LoginManager, UserMixin, current_user
from webforms import postform, usersrform, passwordform, namerform, loginform, searchform
from flask_ckeditor import CKEditor



app = Flask(__name__)
# Add CKEditor
ckeditor = CKEditor(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:05060@localhost/our_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='peeeerless777'
# app.config['CKEDITOR_PKG_TYPE'] = 'basic'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id) :
    return User.query.get(int(user_id))

# Pass Stuff To Nevbar
@app.context_processor
def base() :
    form = searchform()
    return dict(form= form)


# Create Search Function
@app.route("/search", methods= ['POST'])
def search() :
    posts = Posts.query
    form = searchform()
    if form.validate_on_submit() :
        post.searched = form.searched.data
        # Database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template("search.html", form= form, searched = post.searched, posts= posts)


# Create Login Page
@app.route("/login", methods= ['POST', 'GET'])
def login() :
    form = loginform()
    if form.validate_on_submit() :
        user = User.query.filter_by(username= form.username.data).first()
        if user :
            if check_password_hash(user.password_hash, form.password_hash.data) :
                login_user(user)
                flash("User Login Successfull!!")
                return redirect(url_for("dashboard"))
            else :
                flash("Wrong Password!! Try Ageen....")
        else :
            flash("That User Dosen't Exist! Try ageen....")
    
    return render_template("login.html", form= form)

@app.route("/logout", methods= ['POST', 'GET'])
@login_required
def logout() :
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stooping By...")
    return redirect(url_for('login'))

# Create Dashboard Page
@app.route("/dashboard", methods= ['POST', 'GET'])
@login_required
def dashboard() :
    form = usersrform()
    id = current_user.id
    name_to_update = User.query.get_or_404(id)
    if request.method == 'POST' :
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.favorite_color = request.form["favorite_color"]
        name_to_update.username = request.form["username"]
        try :
            db.session.commit()
            flash("User Updated Successfuly!")
            return render_template("dashboard.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
        except :
            flash("Error!!  User Was Not Updated....Try Ageen")
            return render_template("dashboard.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else :
        return render_template("dashboard.html",
                                form=form,
                                name_to_update=name_to_update,
                                id=id)


    return render_template("dashboard.html", form=form, name_to_update=name_to_update)
# Create Post Page
@app.route("/add-post", methods= ['GET', 'POST'])
def add_post() :

    form= postform()

    if form.validate_on_submit() :

        poster = current_user.id

        post = Posts(title= form.title.data, content= form.content.data,  poster_id= poster, slug= form.slug.data)

        # Add To Database
        db.session.add(post)
        db.session.commit()
        
        # Clear The Form
        form.title.data = ''
        form.content.data = ''
        # form.author.data = ''
        form.slug.data = ''

        # Flash Messag
        flash("Blog Post Submitted Successfuly!")
    
    return render_template("add_post.html", form=form)


# Create Update Post Page
@app.route("/posts/edit/<int:id>", methods= ['POST', 'GET'])
def edit_post(id) :

    post = Posts.query.get_or_404(id)
    form = postform()

    if form.validate_on_submit():

        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        # Update database
        db.session.add(post)
        db.session.commit()

        flash("Post Has Been Updated!!")
        return redirect(url_for("post", id= post.id))
    
    if current_user.id == post.poster_id:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template("edit_post.html", form=form)
    else :
        flash("You Aren't Authorized To Edit That Post....")
        posts = Posts.query.order_by(Posts.post_time)
        return render_template("posts.html", posts=posts)

# Create delete post
@app.route("/post/delete/<int:id>")
def delete_post(id) :

    post_to_delete = Posts.query.get_or_404(id)

    id = current_user.id
    
    if id == post_to_delete.poster.id :
        try :

            # delete from database
            db.session.delete(post_to_delete)
            db.session.commit()

            # Flash Messag
            flash("Post Deleting Successfuly!!")

            posts = Posts.query.order_by(Posts.post_time)
            return render_template("posts.html", posts=posts)

        except :

            flash("Whooops!! There was an error  try ageen....")

            posts = Posts.query.order_by(Posts.post_time)
            return render_template("posts.html", posts=posts)

    else :
                # Flash Messag
        flash("You Aren't Authorized To Delete That Post!")

        posts = Posts.query.order_by(Posts.post_time)
        return render_template("posts.html", posts=posts)



# Create Posts Page 
@app.route("/posts")
def posts() :

    # Grab All Posts Form Database
    posts = Posts.query.order_by(Posts.post_time)

    return render_template("posts.html", posts=posts)


# Creat View Post Page
@app.route("/post/<int:id>")
def post(id) :

    post = Posts.query.get_or_404(id)

    return render_template("post.html", post=post)



# Git Some Json
@app.route("/date")
def git_current_date() :
    favoret_pizza = {
        "Peerless": "Pepperoni",
        "Lil": "Chees",
        "Loka": "Mushroom"
    }
    
    return favoret_pizza
    
    # return {"Date": date.today()}



@app.route("/delete/<int:id>")
def delete(id) :
    name_to_delete = User.query.get_or_404(id)
    name = None
    form = usersrform()

    try :
    
        db.session.delete(name_to_delete)
        db.session.commit()
        popo_users = User.query.order_by(User.date_add)
        flash("User Deleted Successfuly!!")
        return render_template("add_users.html",
                                form=form, name=name,
                                popo_users=popo_users)
    except :

        flash("Whoops!! Thir Were Problem To Deleteing User....Try Ageen")
        return render_template("add_users.html",
                                form=form, name=name,
                                popo_users=popo_users)




@app.route("/update/<int:id>", methods= ['GET', 'POST'])
@login_required
def update(id) :
    form = usersrform()
    name_to_update = User.query.get_or_404(id)
    if request.method == 'POST' :
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.favorite_color = request.form["favorite_color"]
        name_to_update.username = request.form["username"]
        try :
            db.session.commit()
            flash("User Updated Successfuly!")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
        except :
            flash("Error!!  User Was Not Updated....Try Ageen")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else :
        return render_template("update.html",
                                form=form,
                                name_to_update=name_to_update,
                                id=id)



@app.route("/name/add", methods= ['POST', 'GET'])
def add_user() :
    name = None
    form = usersrform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None :
            hash_password = generate_password_hash(form.password_hash.data,method='pbkdf2:sha256')
            user = User(name= form.name.data, username=form.username.data, email= form.email.data, favorite_color= form.favorite_color.data, password_hash= hash_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash("User Added Successfuly!")
    popo_users = User.query.order_by(User.date_add)
    return render_template("add_users.html", form=form, name=name, popo_users=popo_users)


@app.route("/") 

def index() :

    frist_name = "peerless"

    fevoret_pizza = ["pepperone", "chees", 41]

    return render_template("index777.html", frist_name=frist_name, fevoret_pizza=fevoret_pizza)


@app.route("/user/<name>") 

def user(name) :

    name = "peerless"

    return render_template("user.html", name=name)

@app.errorhandler(404)
def  Invalid_URL(n) :

    return render_template("404.html")


#Internal Server Error
@app.errorhandler(500)
def  Internal_Server_Error(m) :

    return render_template("500.html")



@app.route("/test_password", methods= ['GET', 'POST'])
def test_password() :

    email = None
    password = None
    password_to_check = None
    passed = None
    form = passwordform()

    if form.validate_on_submit() :

        email = form.email.data
        password = form.password_hash.data

        form.email.data = ''
        form.password_hash.data = ''
        # flash("Form Submitted Successfuly!")

        # Lookup User By Email Address
        password_to_check = User.query.filter_by(email= email).first()

        # Check Hashed Password
        passed = check_password_hash(password_to_check.password_hash, password)

    return render_template("test_password.html",
                            email=email,
                            password=password,
                            password_to_check =  password_to_check,
                            passed= passed,
                            form=form)




@app.route("/name", methods= ['GET', 'POST'])
def name() :

    name = None
    form = namerform()
    if form.validate_on_submit() :

        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfuly!")

    return render_template("name.html", name=name, form=form)




# Create Class
class Posts(db.Model) :
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    post_time = db.Column(db.DateTime, default= datetime.utcnow)
    slug = db.Column(db.String(255))
    # Create Foreing Key To Link User (refer to primary key)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    
# Create Model

class User(db.Model, UserMixin) :

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(21), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique= True)
    favorite_color = db.Column(db.String(120))
    date_add = db.Column(db.DateTime, default= datetime.utcnow)
    # user can have many posts
    posts = db.relationship('Posts', backref='poster')

    # Do Some Stuff !

    password_hash = db.Column(db.String(128))

    @property
    def password(self) :

        raise AttributeError("Password Is Not Readeble Attribute!")
    
    @password.setter
    def password(self, password) :

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) :

        return check_password_hash(self.password_hash, password)

    # Create A String
    def __repr__(self):
        return "<Name %r>" % self.name





if __name__ == "__main__" :

    app.run(debug=True, port=9000)