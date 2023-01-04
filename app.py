from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app_ct = Flask(__name__)
app_ct.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
app_ct.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


contacts_db = SQLAlchemy(app_ct)
db = SQLAlchemy(app)

contacts_db.init_app(app_ct)



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

        try:
            app_context = app_ct.app_context()
            app_context.push()
            contacts_db.session.add(contact_add)
            contacts_db.session.commit()
            return redirect('/phone_success')
        except:
            return 'При добавлении заметки произошла ошибка'
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
            return redirect('/posts')
        except:
            return 'При добавлении заметки произошла ошибка'
    else:
        return render_template('create_article.html')


@app.route('//posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
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


if __name__ == '__main__':
    app.run(debug=True)