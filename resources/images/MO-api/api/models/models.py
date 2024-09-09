from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, Table
from sqlalchemy.orm import relationship
from ..config.db import Base

place_categories = Table(
    'place_categories',
    Base.metadata,
    Column('place_id', Integer, ForeignKey('interest_places.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class InterestPlace(Base):
    """
    This is an aproximation on the real implementation we need to consider, the way to save images, for example on a S3 bucket or a CDN etc.
    And the way to save the comments, maybe we need to create a new table for that and much others.
    """
    __tablename__ = "interest_places"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    images = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    comments = Column(Text, nullable=True)
    status = Column(Boolean, default=True)
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    categories = relationship("Category", secondary=place_categories, back_populates="places")

    def coordinates(self):
        return [self.latitude, self.longitude]

Category.places = relationship("InterestPlace", secondary=place_categories, back_populates="categories")
