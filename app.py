from flask import Flask, render_template, request, redirect, flash, url_for, session, g, template_rendered, message_flashed
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
# from signals import my_signal

app_ct = Flask(__name__)
app_ct.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
app_ct.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_ct.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'
app_ct.config.from_envvar('SITE_ON_FLASK_SETTINGS', silent=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6878h7f'
app.config['USERNAME'] = 'Zahar'
app.config['PASSWORD'] = 'z-1996'
app.config.from_envvar('SITE_ON_FLASK_SETTINGS', silent=True)


contacts_db = SQLAlchemy(app_ct)
db = SQLAlchemy(app)

contacts_db.init_app(app_ct)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_db():
    """Если ещё нет соединения с базой данных, открыть новое - для
    текущего контекста приложения
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Article %r>' % self.id


class Contact(contacts_db.Model):
    id = contacts_db.Column(contacts_db.Integer, primary_key=True)
    title = contacts_db.Column(contacts_db.String(100), nullable=True)
    text = contacts_db.Column(contacts_db.Text, nullable=True)
    date = contacts_db.Column(contacts_db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Contact %r>' % self.id


@app.route('/phone', methods=['POST', 'GET'])
def add_cont():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        contact_add = Contact(title=title, text=text)
        app_context = app_ct.app_context()
        app_context.push()
        contacts_db.session.add(contact_add)
        contacts_db.session.commit()
        flash("Ваше сообщение успешно отправлено, мы свяжемся с вами в ближайшее время!")
        return redirect(url_for('add_cont'))
    else:
        return render_template('phone.html')


@app.route('/1.html')
def html():
    return render_template('1.html')


@app.route('/phone_success')
def phone_success():
    return render_template('phone_success.html')


@app.route('/images_bee_trap')
def images_bee_trap():
    return render_template('images_bee_trap.html')


@app.route('/images_bee_hive')
def images_bee_hive():
    return render_template('images_bee_hive.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    article = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', article=article)

@app.route('/posts/<int:id>')
def post_detail(id):
    article_detail = Article.query.get(id)
    return render_template('post_detail.html', article_detail=article_detail)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    if not session.get('logged_in'):
        article_detail = Article.query.get(id)
        flash('Удалять заметки может только администратор!')
        return render_template('post_detail.html', article_detail=article_detail)
    article_detail = Article.query.get_or_404(id)
    try:
        db.session.delete(article_detail)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            flash("Заметка успешно добавлена!")
            return redirect('/posts')
        except:
            return 'При добавлении заметки произошла ошибка'
    else:
        return render_template('create_article.html')


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    if not session.get('logged_in'):
        article_detail = Article.query.get(id)
        flash('Редактировать заметки может только администратор!')
        return render_template('post_detail.html', article_detail=article_detail)
    article_detail = Article.query.get(id)
    if request.method == 'POST':
        article_detail.title = request.form['title']
        article_detail.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании заметки произошла ошибка'
    else:
        article_detail = Article.query.get(id)
        return render_template('post_update.html', article_detail=article_detail)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/delivery')
def delivery():
    return render_template('delivery.html')


@app.route('/beehaves')
def beehaves():
    return render_template('beehaves.html')


@app.route('/catch_bees')
def catch_bees():
    return render_template('catch_bees.html')


@app.route('/articles')
def articles():
    return render_template('articles.html')


@app.route('/description_bee_hive')
def description_bee_hive():
    return render_template('description_bee_hive.html')


@app.route('/price_bee_hive')
def price_bee_hive():
    return render_template('price_bee_hive.html')


@app.route('/description_bee_trap')
def description_bee_trap():
    return render_template('description_bee_trap.html')


@app.route('/price_bee_trap')
def price_bee_trap():
    return render_template('price_bee_trap.html')


# my_signal(app, template_rendered, message_flashed)


if __name__ == '__main__':
    app.run(debug=True)