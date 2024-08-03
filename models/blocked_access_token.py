from db import db

class BlockedAccessTokenModel(db.Model):
    __tablename__ = "blocked_access_tokens"
    id = db.Column(db.Integer,primary_key=True)
    token = db.Column(db.Text, nullable=False)
