from models import db, Movie


def create_tables():
    db.create_tables([Movie])  # attention put models in [], if you don't you will get error :-)
