
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsfeed.db'
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)

# Define the NewsArticle model
class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    author = db.Column(db.String(120))
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<NewsArticle %r>' % self.title

# Define the main route
@app.route('/')
def index():
    """Render the main newsfeed page."""
    articles = NewsArticle.query.all()
    return render_template('index.html', articles=articles)

# Define the article route
@app.route('/article/<int:id>')
def article(id):
    """Render the individual news article page."""
    article = NewsArticle.query.get(id)
    return render_template('article.html', article=article)

# Define the add article route
@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    """Add a new article to the newsfeed."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        date = request.form['date']
        new_article = NewsArticle(title=title, content=content, author=author, date=date)
        db.session.add(new_article)
        db.session.commit()
        flash('Article added successfully.')
        return redirect(url_for('index'))
    return render_template('add_article.html')

# Define the edit article route
@app.route('/edit_article/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    """Edit an existing news article."""
    article = NewsArticle.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.author = request.form['author']
        article.date = request.form['date']
        db.session.commit()
        flash('Article updated successfully.')
        return redirect(url_for('index'))
    return render_template('edit_article.html', article=article)

# Define the delete article route
@app.route('/delete_article/<int:id>')
def delete_article(id):
    """Delete an existing news article."""
    article = NewsArticle.query.get(id)
    db.session.delete(article)
    db.session.commit()
    flash('Article deleted successfully.')
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
