'''Flask Feedback routes'''
from flask import Flask, request, render_template,redirect, session,flash
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import CreateUserForm, LogInForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def index_view():
    ''' Show homepage with links to site'''
    return redirect('/register')

@app.route('/register', methods=['POST','GET'])
def register_view():
    ''' Show register form'''
    if "username" in session:
        username= session['username']
        return redirect(f"/users/{username}")
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        user = User.register(username,pwd,first_name,last_name,email)
        db.session.add(user)
        db.session.commit()
        
        session['username'] = user.username
        return redirect(f'/users/{username}')
    return render_template('/forms/register_form.html',form=form)

@app.route('/secret')
def secret_view():
    '''Show secret view; only for logged in users '''
    if 'username' not in session:
        return redirect('/')
    return render_template('secret.html')

@app.route('/login', methods=["POST","GET"])
def login_view():
    '''Log in view for existing users'''
    if 'username' in session:
        username = session['username']
        return redirect(f'/users/{username}')
    form = LogInForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        user = User.authenticate(username,pwd)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad name/password"]
    return render_template('/forms/login_form.html',form=form)

@app.route('/logout')
def logout():
    '''Logs out of user, and redirects to homepage'''
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>', methods=['GET','POST'])
def user_view(username):
    '''Template that shows information about the user, except passord
    Only a logged in user can access this page
    '''
    if 'username' not in session:
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        
        return render_template('user.html',user=user)

@app.route('/users/<username>/delete',methods=['POST'])
def delete_user(username):
    '''Delete a user from the database'''
    if 'username' not in session or username != session['username']:
        flash('Error!')
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    ''' Template that shows a form to add feedback'''
    if 'username' not in session or username != session['username']:
        flash('Error!')
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        form = FeedbackForm()
        if form.validate_on_submit():
            title= form.title.data
            content = form.content.data
            feedback = Feedback(title=title,content=content,username=user.username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{user.username}')
        return render_template('/feedback/add_feedback.html',user=user,form=form)

@app.route('/feedback/<int:feedback_id>/update',methods=['POST','GET'])
def update_feedback(feedback_id):
    '''Up date a feedback. A user with a matching username should only get this view '''
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        flash('Error!')
        return redirect('/')
    
    else:
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('/feedback/edit_feedback.html',form=form,feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete',methods=['POST'])
def delete_feedback(feedback_id):
    '''delete a feedback. a user with a matching username should only be able to delete'''
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        flash('Error!')
        return redirect('/')
    else:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')