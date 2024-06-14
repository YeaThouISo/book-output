from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# モデルの定義
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    read_date = db.Column(db.Date, nullable=False)
    review = db.Column(db.Text, nullable=False)

# データベースの初期化
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        read_date = datetime.strptime(request.form['read_date'], '%Y-%m-%d')
        review = request.form['review']
        
        new_book = Book(title=title, author=author, read_date=read_date, review=review)
        db.session.add(new_book)
        db.session.commit()
        
        return redirect(url_for('book_list'))
    return render_template('add_book.html')

@app.route('/books')
def book_list():
    books = Book.query.all()
    return render_template('book_list.html', books=books)

if __name__ == "__main__":
    app.run(debug=True)
