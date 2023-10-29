#!/usr/bin/python3
""" Test link Many-To-Many Place <> Amenity
"""
from models.state import State
from models.user import User
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models import storage

place = list(storage.all(Place).values())[0]
amenities =  ["f4dfd576-7c29-4bdf-9fbd-5c95a170ebce"]
print(place.to_dict())
if amenities:
    amenity_ids = [amenity.id for amenity in place.amenities]
    print(place.__dict__)
