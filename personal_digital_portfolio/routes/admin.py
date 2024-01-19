import bcrypt
from articles.articles import Article, ArticleService
from articles.article_form import ArticleForm
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from routes import app
from users.users import User, UserService
from users.users_form import DeleteUserForm, UserForm, ChangePswForm


################################# article #################################


# upload new article
@app.route('/new_article', methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article()
        new_article.title = form.title.data
        new_article.content = form.content.data
        try:
            ArticleService().upload_article(new_article)
            flash('Article successfully uploaded', category='success')
            return redirect(url_for('index'))
        except:
            flash('Article upload failed', category='danger')
    return render_template('edit_article.html', form=form, edit=False)


# edit article
@app.route('/edit_article/<article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    form = ArticleForm()
    if request.method == 'GET':
        try:
            article = ArticleService().get_article(int(article_id))
            if not article:
                flash('No such an article in database', category='warning')
                return redirect(url_for('index'))
            else:
                form.title.data = article.title
                form.content.data = article.content
        except:
            flash('Failed on getting the article', category='danger')   
            return redirect(url_for('index'))
    # after click on submit btn    
    if form.validate_on_submit():
        edited_article = Article()
        edited_article.id = int(article_id)
        edited_article.title = form.title.data
        edited_article.content = form.content.data
        try:
            ArticleService().edit_article(edited_article)
            flash('Article successfully updated', category='success')
            return redirect(url_for('index'))
        except:
            flash('Article update failed', category='danger')
    return render_template('edit_article.html', form=form, edit=True)


################################# user #################################


# user dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# append new user into database
@app.route('/dashboard/new_user', methods=['GET', 'POST'])
@login_required
def new_user():    
    #print('admin.py new user run')
    if current_user.id != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = UserForm()
        if form.validate_on_submit():
            new_user = User()
            new_user.username = form.username.data            
            hsd_psw = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt())
            new_user.password = hsd_psw.decode('utf-8')
            print(new_user.username)
            print(new_user.password)
            try:
                UserService().new_user(new_user)
                flash('User successfully created', category='success')
                return redirect(url_for('dashboard'))
            except:
                flash('User create failed', category='danger')
        return render_template('edit_user.html', form=form, edit=False)


# change password
@app.route('/dashboard/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    # print('admin.py changepsw run')
    form = ChangePswForm()     
    # after click on submit btn    
    if form.validate_on_submit():
        hsd_psw = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt()).decode('utf-8')
        #hsd_psw_old = bcrypt.hashpw(form.old_password.data.encode(), bcrypt.gensalt()).decode('utf-8')
        #print(f'current user psw: {current_user.password}')
        #print(f'inputted psw: {hsd_psw_old}')
        #print(current_user.check_psw(hsd_psw_old))
        if current_user.check_psw(form.old_password.data):
            if form.password.data != form.cfm_password.data:
                flash('New password is not same with confirm password', category='danger')
            else:
                try:
                    UserService().change_password(current_user, hsd_psw)
                    flash('Password successfully updated', category='success')
                    return redirect(url_for('dashboard'))
                except:
                    flash('Password update failed', category='danger')
        else:
            flash('Old password unmatch', category='danger')
    return render_template('edit_user.html', form=form, edit=True)


# delete user account
@app.route('/dashboard/del_account', methods=['GET', 'POST'])
@login_required
def del_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        user = current_user
        try:
            UserService().delete_user(user)
            print('userservice called')
            flash('User account successfully deleted', category='success')
            return redirect(url_for('index'))
        except:
            flash('User delete failed', category='danger')
    return render_template('del_user.html', form=form)
