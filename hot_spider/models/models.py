import configparser
from peewee import *
from playhouse.pool import PooledMySQLDatabase

conf = configparser.ConfigParser()
conf.read('../conf/conf.ini', encoding="UTF-8")
user = conf.get('db', 'user')
passwd = conf.get('db', 'passwd')

db = PooledMySQLDatabase('hotnews', max_connections=100, stale_timeout=300, user=user, passwd=passwd)


class BaseModel(Model):
    class Meta:
        database = db


class HotSearch(BaseModel):
    class Meta:
        table_name = 'hot_search'

    id = BigAutoField()
    title = CharField()
    describe = CharField(default='')
    url = CharField()
    type = SmallIntegerField()
    new_url = CharField()
    video_url = CharField()
    image_url = CharField()


class TimeRank(BaseModel):
    class Meta:
        table_name = 'time_rank'

    id = BigAutoField()
    time = CharField()
    ranking = SmallIntegerField()
    hot_id = BigIntegerField()
    count = IntegerField()

