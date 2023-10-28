#!/usr/bin/python3
""" Test link Many-To-Many Place <> Amenity
"""
from models.state import State
from models.user import User
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models import storage

""" # creation of a State
state = State(name="California")
state.save()

# creation of a City
city = City(state_id=state.id, name="San Francisco")
city.save()

# creation of a User
user = User(email="john@snow.com", password="johnpwd")
user.save() """


user = list(storage.all(User).values())[0]
print(user.password)
print(user.__dict__)
print(user.to_dict())
print(user.to_dict(True))