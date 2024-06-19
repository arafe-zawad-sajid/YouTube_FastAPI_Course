from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

#whenever we start our app, sql alchemy will check for a table named "posts"
#if it's there it won't do anything, otherwise it'll create it for us based on what we defined in the model
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'), nullable=False)

#sql alchemy will generate a table only if one does not exist, it does not modify the tables
#for migrations (changing the cols and the schema) we use alembic, sql alchemy isn't meant for this