from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,String,Integer
engine = create_engine("postgresql://cdy038:wf25shjcrzali$Mix%tMt@@rm-2zen988pb49xf833mo.pg.rds.aliyuncs.com:3432/winter_olympics",echo=True)
# session = sessionmaker()
# session.configure(bind = engine)
# s = session()


Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    name = Column(String(10))
    fullname = Column(String(10))
    password = Column(String(10))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname,self.password)

