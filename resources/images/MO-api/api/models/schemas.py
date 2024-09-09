from pydantic import BaseModel
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes

class CategoryResponse(Category):
    pass

class InterestPlaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    images: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None
    status: Optional[bool] = True
    latitude: float
    longitude: float
    categories: Optional[List[int]] = []

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes

class InterestPlaceCreate(InterestPlaceBase):
    pass

class InterestPlaceUpdate(InterestPlaceBase):
    name: Optional[str] = None
    description: Optional[str] = None
    images: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None
    status: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    categories: Optional[List[int]] = None

class InterestPlace(InterestPlaceBase):
    id: int

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes

class InterestPlaceResponse(InterestPlaceBase):
    id: int
    categories: List[CategoryResponse]  # Aquí devolvemos una lista de esquemas Category

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes

    id: int
    categories: List[CategoryResponse]  # Aquí devolvemos una lista de esquemas Category

    class Config:
        orm_mode = True