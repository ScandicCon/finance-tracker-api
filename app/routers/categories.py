import json

from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db
from app.models.categories import Category
from app.schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from app.core.secutity import get_current_user
from app.models.users import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.redis import redis_client




router = APIRouter(prefix="/categories", tags=["Category"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_categories(data: CategoryCreate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    category = Category(
        name=data.name,
        type=data.type,
        user_id= current_user.id
    )

    session.add(category)
    session.commit()
    redis_client.delete (f"categories:user:{current_user.id}")
    session.refresh(category)
    return category

@router.get("/", response_model=list[CategoryResponse])
def get_category(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cache_key = f"categories:user:{current_user.id}"

    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    stmt = select(Category).where(Category.user_id == current_user.id)
    categories = session.execute(stmt).scalars().all()

    result = [
        CategoryResponse.model_validate(c).model_dump(mode="json")
        for c in categories
    ]

    redis_client.set(cache_key, json.dumps(result), ex=60)

    return result

@router.delete("/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Category).where(Category.id == category_id, Category.user_id == current_user.id)
    category = session.execute(stmt).scalar_one_or_none()
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    session.delete(category)
    session.commit()
    redis_client.delete(f"categories:user:{current_user.id}")
    

@router.patch("/{category_id}", response_model=CategoryUpdate)
def rename_category(category_id: int,data:CategoryUpdate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Category).where(
        Category.id == category_id,
        Category.user_id == current_user.id
    )
    category = session.execute(stmt).scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    if data.name is not None:
        category.name = data.name

    session.commit()
    redis_client.delete (f"categories:user:{current_user.id}")

    session.refresh(category)

    return category