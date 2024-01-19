from datetime import datetime
from routes import db
from sqlalchemy import BLOB, Integer, String, TIMESTAMP, Select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


# article object               
class Article(db.Model):


    __tablename__ = 'articles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    __content: Mapped[bytes] = mapped_column(BLOB, name="content", nullable=False) # BLOB have bigger capacity that TEXT
    created: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())


    @property
    def content(self):
        return self.__content.decode('utf-8')


    @content.setter
    def content(self, content_value: str):
        self.__content = content_value.encode()
    

class ArticleService:


    # get one article by accepting id
    def get_article(self, id):
        return db.session.get(Article, id)
    

    # get all articles
    def get_all_articles(self):
        query = Select(Article)
        return db.session.scalars(query).all()
    

    # upload new article
    def upload_article(self, article: Article):
        db.session.add(article)
        db.session.commit()
        return article
    

    # edit article
    def edit_article(self, article: Article):
        exist_article = db.session.get(Article, article.id)
        if not exist_article:
            return article
        exist_article.title = article.title
        exist_article.content = article.content
        exist_article.created = func.now()
        db.session.commit()
        return article
    

    # delete article
    def delete_article(self, article_id):
        if type(article_id) == str:
            article_id = int(article_id)
        article = db.session.get(Article, article_id)
        if article:
            db.session.delete(article)
            db.session.commit()
            return True
        else:
            return False    
