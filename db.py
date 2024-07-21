import uuid

one = uuid.uuid4().hex
two=  uuid.uuid4().hex
three= uuid.uuid4().hex

stores = {
    one:{'name':'Fairprice', 'id':one},
    two:{'name':'Challenger', 'id':two},
    three: {'name':'Abloy', 'id':three},
}

items = {
    one: ['Food', 'Groceries','Daily use'],
    two: ['Laptop','Mobiles','Electronics'],
    three: ['Locks', 'Smart Locks'],
}
