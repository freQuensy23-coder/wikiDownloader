from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from config import *
from sqlalchemy import Column, VARCHAR, ForeignKey, select, func, and_
from sqlalchemy.orm import relation, column_property
from sqlalchemy.orm.session import sessionmaker
import asyncio

engine = create_engine(f"mysql://{user}:{password}@{host}/{db}?charset=utf8", echo=False, pool_recycle=25)
session = sessionmaker(bind=engine)()
base = declarative_base()


class Page(base):
    __tablename__ = 'Pages'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(255), nullable=False)
    text = Column(Text, nullable=True)
    images_links = Column(Text, nullable=True)

    def __repr__(self):
        return f'{self.title} {self.link}'


base.metadata.create_all(engine)
