from backend import db
from flask_login import UserMixin

""" Model for parent and children """
class AccountInfo(db.Model, UserMixin):
    
    _id = db.Column(db.Integer, primary_key=True)

    parent_username = db.Column(db.String(100), unique=True, nullable=False)
    parent_email = db.Column(db.String(100), unique=True, nullable=False)
    parent_password = db.Column(db.String(100), unique=False, nullable=False)

    child_username = db.Column(db.String(100), unique=True, nullable=True)
    child_email = db.Column(db.String(100), unique=True, nullable=True)
    child_password = db.Column(db.String(100), unique=False, nullable=True)
    
    balance = db.Column(db.Integer, nullable=False)
    last_deposit = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Parent: {self.parent_username}, Children: {self.child_username}"
    
    def get_id(self):
           return (self._id)