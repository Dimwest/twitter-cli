from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, Boolean, JSON

Base = declarative_base()
schema_name = 'twitter'


class Tweet(Base):

    __tablename__ = 'tweets'
    __table_args__ = {"schema": schema_name}

    id = Column(BigInteger, primary_key=True)
    id_str = Column(String)
    created_at = Column(String, primary_key=True)
    full_text = Column(String)
    truncated = Column(Boolean)
    source = Column(String)
    retweeted = Column(Boolean)
    retweeted_status = Column(JSON)
    entities = Column(JSON)
    user = Column(JSON)
    favorite_count = Column(BigInteger)
    in_reply_to_screen_name = Column(String)
    in_reply_to_status_id = Column(BigInteger)
    in_reply_to_status_id_str = Column(String)
    in_reply_to_user_id = Column(BigInteger)
    in_reply_to_user_id_str = Column(String)
    is_quote_status = Column(Boolean)
    geo = Column(String)
    lang = Column(String)
    place = Column(String)
