from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from ..config.env import ENV_VARIABLES
from ..models.schemas import (
    Category, CategoryCreate, InterestPlace, 
    InterestPlaceCreate, InterestPlaceUpdate, InterestPlaceResponse, CategoryResponse 
)
from ..models import models
from ..config.db import SessionLocal as get_db
from ..methods import methods as repo
from ..config.db import SessionLocal
from typing import List
import logging
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Category Endpoints

@router.post("/categories/", response_model=Category, status_code=status.HTTP_201_CREATED, tags=["Categories"])
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = repo.create_category(db=db, category=category)
    return db_category

@router.get("/all_categories/", response_model=List[Category], tags=["Categories"])
def read_categories(db: Session = Depends(get_db)):
    categories = repo.get_categories(db=db, skip=-1)
    return categories

@router.get("/categories/", response_model=List[Category], tags=["Categories"])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = repo.get_categories(db=db, skip=skip, limit=limit)
    return categories

@router.get("/categories/{category_id}", response_model=Category, tags=["Categories"])
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = repo.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/categories/{category_id}", response_model=Category, tags=["Categories"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = repo.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    repo.delete_category(db=db, category_id=category_id)
    return db_category

# InterestPlace Endpoints

@router.post("/places/", response_model=InterestPlaceResponse, status_code=status.HTTP_201_CREATED, tags=["Interest Places"])
def create_interest_place(place: InterestPlaceCreate, db: Session = Depends(get_db)):
    db_place = repo.create_interest_place(db=db, place=place)
    return InterestPlaceResponse.from_orm(db_place)

@router.get("/places_by_category{category_id}", response_model=List[InterestPlaceResponse], tags=["Interest Places"])
def search_by_category(category_id: int, db: Session = Depends(get_db)):
    db_places = repo.get_interest_place_by_category(db=db, category_id=category_id)
    places = [InterestPlaceResponse.from_orm(place) for place in db_places]
    return places

@router.get("/places/", response_model=List[InterestPlaceResponse], tags=["Interest Places"])
def read_interest_places(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    places = repo.get_interest_places(db=db, skip=skip, limit=limit)
    return [InterestPlaceResponse.from_orm(place) for place in places]

@router.get("/places/{place_id}", response_model=InterestPlaceResponse, tags=["Interest Places"])
def read_interest_place(place_id: int, db: Session = Depends(get_db)):
    db_place = repo.get_interest_place(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Interest Place not found")
    return InterestPlaceResponse.from_orm(db_place)

@router.put("/places/{place_id}", response_model=InterestPlaceResponse, tags=["Interest Places"])
def update_interest_place(place_id: int, place: InterestPlaceUpdate, db: Session = Depends(get_db)):
    db_place = repo.get_interest_place(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Interest Place not found")
    updated_place = repo.update_interest_place(db=db, place_id=place_id, place=place)
    return InterestPlaceResponse.from_orm(updated_place)

@router.delete("/places/{place_id}", response_model=InterestPlaceResponse, tags=["Interest Places"])
def delete_interest_place(place_id: int, db: Session = Depends(get_db)):
    db_place = repo.get_interest_place(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Interest Place not found")
    repo.delete_interest_place(db=db, place_id=place_id)
    return InterestPlaceResponse.from_orm(db_place)


# Test Endpoints

@router.get("/test-db-connection/",tags=["Test"])
def ex(db: Session = Depends(get_db)):
    try:
        count = db.query(models.Category).count()
        return {"status": "success", "category_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))