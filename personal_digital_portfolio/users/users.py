import bcrypt
from flask_login import UserMixin, login_user
from routes import db, login_manager
from sqlalchemy import Integer, String, Select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    
    # check if input psw == database psw
    def check_psw(self, input_psw):
        hashed_psw = self.password.encode()
        return bcrypt.checkpw(input_psw.encode(), hashed_psw)
    

class UserService:


    # login 
    def login_action(self, username, password):
        # search from database
        query = Select(User).where(User.username == username)
        user_db = db.session.scalar(query)
        # if there exist user and psw correct
        if user_db and user_db.check_psw(password):
            # put user into section
            login_user(user_db)
            return True
        return False
    
    
    # get an user by accepting id
    def get_user(self, id):
        return db.session.get(User, id)
    
    # create new user
    def new_user(self, user: User):
        #print('userservice new_user run')
        db.session.add(user)
        db.session.commit()
        #print(user.username)
        #print(user.password)
        return user
    
    # change password
    def change_password(self, current_user: User, password):
        #print('userservice changepsw run')
        current_user.password = password
        db.session.commit()
        return current_user
    
    
    # delete user
    def delete_user(self, user: User):
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False       