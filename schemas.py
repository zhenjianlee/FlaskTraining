from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)

class PlainStoreSchema(Schema):
    id =fields.Str(dump_only=True)
    name=fields.Str(required=True)

class PlainUserSchema(Schema):
    id = fields.Str(required=True,dump_only=True)
    username=fields.Str(required=True)
    password =fields.Str(required=True, load_only=True)

class UserUpdateSchema(PlainUserSchema):
    username=fields.Str()
    password=fields.Str()

class ItemUpdateSchema(Schema):
    name=fields.Str()
    price=fields.Float()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) 
    store= fields.Nested(PlainStoreSchema,dump_only=True)

class StoreSchema(PlainStoreSchema):
    items=fields.Nested(PlainItemSchema,many=True)

