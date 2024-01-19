from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):

    title = StringField(label='title:', validators=[DataRequired()])
    content = TextAreaField(label='content:', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class DeleteArticleForm(FlaskForm):

    article_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Confirm delete')