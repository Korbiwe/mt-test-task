from uuid import uuid4


# we can't pass a property to sqlalchemy as default, we need a method
def uuid4hex():
    return uuid4().hex