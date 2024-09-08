from sqlalchemy.orm import Session
from ..config.db import SessionLocal
from ..models.models import Category, InterestPlace, place_categories
from ..models.schemas import CategoryCreate, InterestPlaceCreate, InterestPlaceUpdate
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

# Category CRUD Operations

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    if skip < 0:
        return db.query(Category).all()
    return db.query(Category).offset(skip).limit(limit).all()

def get_interest_place_by_category(db: Session, category_id: int):
    return (
        db.query(InterestPlace)
        .join(place_categories, InterestPlace.id == place_categories.c.place_id)
        .join(Category, Category.id == place_categories.c.category_id)
        .filter(Category.id == category_id)
        .all()
    )

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# InterestPlace CRUD Operations

def get_interest_place(db: Session, place_id: int):
    return db.query(InterestPlace).filter(InterestPlace.id == place_id).first()

def get_interest_places(db: Session, skip: int = 0, limit: int = 10):
    return db.query(InterestPlace).offset(skip).limit(limit).all()

def create_interest_place(db: Session, place: InterestPlaceCreate):
    db_place_data = place.model_dump(exclude={'categories'})
    db_place_data['categories'] = []
    db_place = InterestPlace(**db_place_data)
    
    if place.categories:
        for category_id in place.categories:
            category = get_category(db, category_id)
            if category:
                db_place.categories.append(category)
            else:
                return {"error": f"Category with id {category_id} not found"}, 404

    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place


def update_interest_place(db: Session, place_id: int, place: InterestPlaceUpdate):
    db_place = get_interest_place(db, place_id)
    if db_place:
        for key, value in place.dict(exclude_unset=True).items():
            setattr(db_place, key, value)
        db.commit()
        db.refresh(db_place)
    return db_place

def delete_interest_place(db: Session, place_id: int):
    db_place = get_interest_place(db, place_id)
    if db_place:
        db.delete(db_place)
        db.commit()
    return db_place
