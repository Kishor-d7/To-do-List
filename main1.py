from flask import Flask, url_for, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle_complete', methods=['POST'])
def toggle_complete():
    todo_id = request.form.get('id')
    todo = Todo.query.get(todo_id)
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
        return jsonify({'success': True, 'complete': todo.complete})
    else:
        return jsonify({'success': False, 'error': 'Todo not found'})

@app.route('/delete_task', methods=['POST'])
def delete_task():
    todo_id = request.form.get('id')
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Todo not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
