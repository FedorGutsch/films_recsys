from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector
import enum

Base = declarative_base()

class AgeLimitEnum(str, enum.Enum):
    ALL_AGES = '0+'
    AGE_6 = '6+'
    AGE_12 = '12+'
    AGE_16 = '16+'
    ADULTS = '18+'

film_actor_assoc = Table(
    'film_actor', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id', ondelete="CASCADE"), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id', ondelete="CASCADE"), primary_key=True)
)

film_genre_assoc = Table(
    'film_genre', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)
)

film_director_assoc = Table(
    'film_director', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id', ondelete="CASCADE"), primary_key=True),
    Column('director_id', Integer, ForeignKey('directors.id', ondelete="CASCADE"), primary_key=True)
)

film_country_assoc = Table(
    'film_country', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id', ondelete="CASCADE"), primary_key=True),
    Column('country_id', Integer, ForeignKey('countries.id', ondelete="CASCADE"), primary_key=True)
)


class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Director(Base):
    __tablename__ = 'directors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, index=True)
    title_ru = Column(String, nullable=False)
    title_en = Column(String)
    year = Column(Integer)
    rating_kp = Column(Float)
    plot = Column(Text)
    duration = Column(Integer) # Длительность в минутах
    poster_url = Column(String)
    age_limit = Column(SQLEnum(AgeLimitEnum), nullable=False, default=AgeLimitEnum.ALL_AGES)

    actors = relationship('Actor', secondary=film_actor_assoc, backref='films')
    genres = relationship('Genre', secondary=film_genre_assoc, backref='films')
    directors = relationship('Director', secondary=film_director_assoc, backref='films')
    countries = relationship('Country', secondary=film_country_assoc, backref='films')


class Admin(Base):
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Поле Вектора. dim=384 - это размерность вектора. 
    # Зависит от того, какую нейросеть вы используете (например, у BERT часто 384 или 768).
    # Спроси у напарника, какая размерность эмбеддингов планируется.
    preferences = Column(Vector(384))