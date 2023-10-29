#!/usr/bin/python3
""" Test link Many-To-Many Place <> Amenity
"""
from models.state import State
from models.user import User
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models import storage

state = State(name="Texas")
state.save()
city = City(name="alex", state_id=state.id)
city.save()
user = User(
        name="khougha",
        email="khougha@khouga.com",
        password="pass"
    )
user.save()
place = Place(name='studio', user_id=user.id, city_id=city.id)
