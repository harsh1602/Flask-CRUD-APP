from flask import Flask, request, redirect 
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy     # SQLalchemy allows us to use any databse we want to use. we just need to change the path to the database. 
from datetime import datetime 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db' # inside this-[] is the path where database is stored. we are using sqlite here since in the development phase, once in production mode we can use a different database. 
                                                              # /// is used to give the relative location of the database.

db = SQLAlchemy(app)    # Connecting db created above to the app through SQLAlchemy. 

class BlogPost(db.Model):    # BlogPost is the name of db model we are defining here. 
    id = db.Column(db.Integer, primary_key=True)    # this primary key will always be unique. 
    title = db.Column(db.String(100), nullable=False)  #nullable=false makes sure that title is neverr empty.
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(200), nullable=False, default='N/A')  #default is set incase nothing is there in author. 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):     # this function will print out whenever a blogpost is created.  
        return 'Blog Post ' + str(self.id)   
 

# THIS DATA IS PASSED TO POSTS.HTML PAGE. 

# all_posts = [
#     { 
#         'title': 'Post 1',
#         'content': 'This is the content of Post 1.',
#         'author': 'Harsh'
#     },
#     {
#         'title': 'Post 2',
#         'content': 'This is the content of Post 2.' 
#     }
# ]

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/posts', methods=['GET','POST'])    # If the method is not specified then by default it is GET. Using POST we can have a form that can we filled and saved in the database.
def posts():

    if request.method =='POST': 
        post_title = request.form['title']  # the title id from the form. 
        post_content = request.form['content'] 
        post_author = request.form['author'] 
        new_post = BlogPost(title=post_title, content=post_content, author=post_author) 
        db.session.add(new_post)  # adding new_post created above to the database in this current session. Addition to the database is only done in that session. So to save something in db we need to commit it.
        db.session.commit()
        return redirect('/posts')   # redirecting to the same page after saving in the database. 
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()     #  reading all of the blogpost from the database and ordering them by the date posted.
    return render_template('posts.html',posts=all_posts)    # sending it to the front end 


@app.route('/posts/delete/<int:id>')  # id is the primary key and thus using it to get the post we want to delete.
def delete(id):
    post = BlogPost.query.get_or_404(id)  # incase the blogpost doesnt exist then providing the 404 case else the blog will break. 
    db.session.delete(post)  
    db.session.commit() 
    return redirect('/posts') 


@app.route('/posts/edit/<int:id>', methods=['GET','POST'])  # POST is also required bcoz we also need to update in the database. 
def edit(id):
    post = BlogPost.query.get_or_404(id)    # If the post if the id provided exists then it will be returned to the 'post' else 404 will be returned.

    if request.method=='POST':  
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']  
        db.session.commit()
        return redirect('/posts')   
    else:
        return render_template('edit.html', post=post) 



@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
         
    else:
        return render_template('new_post.html') 


# writing dynamic URLs. 
@app.route('/home/<string:name>/posts/<int:id>') 
def hello(name,id): 
    return "Hello "+name+", your id is: "+  str(id) 

 
# POST METHOD WONT WORK BCOZ WE WANT TO RETURN SOMETHING WHEREAS THE POST METHOD IS FOR SENDING SOMETHING TO URL OR FOR MAKING A SAVE TO THE DATABASE. 

# @app.route('/onlyget', methods=['POST']) 
# def get_req():
#     return "Your page for testing GET and POST request." 



if __name__ == "__main__":
    app.run(debug=True)     #this will make sure to automatically save the changes and thus the server needs not to reload. 