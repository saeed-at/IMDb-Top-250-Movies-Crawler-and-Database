from peewee import SqliteDatabase, Model, CharField, DateTimeField, BigIntegerField, FloatField, TextField, BooleanField
import datetime

db = SqliteDatabase('Top_250_Movies.db')


class BaseModel(Model):
    """
    Create a base model to prevent writing Meta class and created_time for each instance in a database by inheritance it
    """
    created_time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


class Movie(BaseModel):
    """
    This class defines a table in Top_250_Movies.db that has these columns:
        1.name 2.url 3.rank 4.rating 5.director 6.writers 7.starts 8.date
        9.pg 10.duration 11.description 12.category 13.is_completed
    """
    # These columns will crawl at the beginning, so they do not need any null=True configuration, but other columns need
    # this
    rank = BigIntegerField()
    url = TextField()
    name = TextField()
    rating = FloatField()
    # These columns will crawl after extract of urls, so the need null=True
    date = DateTimeField(null=True)
    duration = BigIntegerField(null=True)
    category = CharField(null=True)
    description = TextField(null=True)
    director = CharField(null=True)
    writers = CharField(null=True)
    stars = CharField(null=True)

    is_completed = BooleanField(default=False)
