from articles.articles import Article, ArticleService
from articles.article_form import DeleteArticleForm
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, logout_user
from routes import app
from users.users_form import LoginForm
from users.users import UserService


# routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # rendering delete article form if login 
    if current_user.is_authenticated:
        delete_article_form = DeleteArticleForm()
        if delete_article_form.validate_on_submit():
            del_result = ArticleService().delete_article(int(delete_article_form.article_id.data))
            if del_result:
                flash('Article successfully deleted', category='success')
                return redirect(url_for('index'))
            else:
                flash('Failed on deleting the article')
    # load article form            
    articles = ArticleService().get_all_articles()
    # return page
    if current_user.is_authenticated:
        return render_template('index.html', articles=articles, delete_article_form=delete_article_form)
    else:
        return render_template('index.html', articles=articles)


@app.route('/article/<int:article_id>')
def article(article_id):
    article = ArticleService().get_article(article_id)
    if article:
        return render_template('article.html', article=article)
    else:
        abort(404)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        result = UserService().login_action(username, password=form.password.data)
        if result:
            flash(f'Welcome {username}', category='success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or/and password', category='warning')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

