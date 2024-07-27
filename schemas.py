from marshmallow import Schema, fields

# Plain Schema
class PlainItemSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)

class PlainStoreSchema(Schema):
    id =fields.Int(dump_only=True)
    name=fields.Str(required=True)

class PlainTagSchema(Schema):
    id =fields.Int(dump_only=True,required=True)
    name=fields.Str(required=True)

class PlainUserSchema(Schema):
    id = fields.Int(required=True,dump_only=True)
    username=fields.Str(required=True)
    password =fields.Str(required=True, load_only=True)


#Update Schema
class UserUpdateSchema(PlainUserSchema):
    username=fields.Str()
    password=fields.Str()

class ItemUpdateSchema(Schema):
    name=fields.Str()
    price=fields.Float()


# Full Schema
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) 
    store= fields.Nested(PlainStoreSchema,dump_only=True)

class StoreSchema(PlainStoreSchema):
    items=fields.List(fields.Nested(PlainItemSchema, lazy="dynamic"))
    tags=fields.List(fields.Nested(PlainTagSchema, lazy="dynamic"))

class TagSchema(PlainTagSchema):
    store_id=fields.Int(load_only=True)
    store=fields.Nested(PlainStoreSchema, dump_only=True)

