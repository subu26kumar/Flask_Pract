from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
# track modification warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    @app.before_first_request
    def create_tables():
        db.create_all()
    
    # def __repr__(self) -> str:
    #     return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        add_todo= Todo(title=title, desc=desc)
        db.session.add(add_todo)
        db.session.commit()
    allTodo = Todo.query.all()   
    total=Todo.query.count()
    return render_template('index.html', allTodo=allTodo, total=total)
    

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    
    return 'this is product page'

@app.route('/delete/<int:sno>')
def delete(sno):
    delete_todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        update_todo=Todo.query.filter_by(sno=sno).first()
        update_todo.title=title
        update_todo.desc=desc
        db.session.add(update_todo)
        db.session.commit()
        return redirect('/')
    update_todo=Todo.query.filter_by(sno=sno).first()    
    # allTodo = Todo.query.all()
    return render_template('update.html', update_todo=update_todo)



if __name__=="__main__":
    app.run('0.0.0.0',debug=True)