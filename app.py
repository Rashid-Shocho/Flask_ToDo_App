from flask import Flask, render_template, request ,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here' 

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self)  -> str:
        return f"{self.sno} - {self.title}"




@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is product page"

@app.route("/update/<int:sno>", methods = ['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()

    if not todo:
        return "❌ Error: Todo item not found!", 404  # Debugging message
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        print(f"✅ Received title: {title}, desc: {desc}")

        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/webpage")


    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/webpage")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/webpage", methods=['GET', 'POST'])
def webpage():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        if title and desc:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    
    # Get search query from request
    search_query = request.args.get('search', '')

    if search_query:
        allTodo = Todo.query.filter(
            (Todo.title.ilike(f"%{search_query}%")) | (Todo.desc.ilike(f"%{search_query}%"))
        ).all()
    else:
        allTodo = Todo.query.all()

    return render_template('index.html', allTodo=allTodo)


if __name__ == "__main__":
    app.run(debug=True)