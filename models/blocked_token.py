from db import db

class BlockedTokenModel(db.Model):
    __tablename__ = "blocked_tokens"
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(255),nullable=False)
    jti = db.Column(db.Text,nullable=False)
    token = db.Column(db.Text, nullable=False)
