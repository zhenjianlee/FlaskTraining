from db import db

class ItemTagModel(db.Model):
    __tablename__="items_tags"
    id =db.Column(db.Integer,primary_key=True)
    tag_id=db.Column(db.Integer,db.ForeignKey("tags.id"))
    item_id=db.Column(db.Integer,db.ForeignKey("items.id"))