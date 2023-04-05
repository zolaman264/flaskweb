from flask import Flask, render_template, request, redirect
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///friends.db'
#initialize the databse 
db= SQLAlchemy(app)
#create database model 
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow())
#create functun to return string when we add something 
def __repr__(self):
        return '<Name %r>' % self.id


subscribers=[]

@app.route('/')
def index():
    title= "Zelalem Website"
    return render_template("index.html",title=title)

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete=Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "there was problem deleting"


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    friend_to_update=Friends.query.get_or_404(id)
    if request.method=="POST":
        friend_to_update.name= request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "there was an error updating"
    else:
        return render_template('update.html',friend_to_update=friend_to_update)


@app.route('/friends',methods=['POST','GET'])
def friends():
    
    if request.method=="POST":
         friend_name=request.form['name']
         new_friend=Friends(name=friend_name)
         try: 
            db.session.add(new_friend)
            db.session.commit()
            return redirect("/friends")
         except:
            return "there was error"
    else:
         friends=Friends.query.order_by(Friends.date_created)
         return render_template("friends.html", friends=friends )

@app.route('/about')
def about():
     
    return render_template("about.html",  )
@app.route('/subscribe')
def subscribe():
    title= "Subscribe to my email"
    return render_template("subscribe.html",title=title)

@app.route('/form',methods=["POST"])
def form():

    first_name = request.form.get("first_name")
    last_name =request.form.get("last_name")
    email =request.form.get("email")

 

    if not first_name or not last_name or not email:
        error_statement="All form fields required....."
        return render_template("subscribe.html", error_statement=error_statement,
                               first_name=first_name,last_name=last_name,
                               email=email)
    subscribers.append(f"{first_name} {last_name} || {email}")
    title= "Thank you"
    return render_template("form.html",title=title, subscribers=subscribers,)