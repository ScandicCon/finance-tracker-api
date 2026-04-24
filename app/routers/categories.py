from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db
from app.models.categories import Category
from app.schemas.categories import CategoryCreate, CategoryResponce, CategoryUpdate
from app.core.secutity import get_current_user
from app.models.users import User
from sqlalchemy.orm import Session
from sqlalchemy import select




router = APIRouter(prefix="/categories", tags=["Category"])


@router.post("/create", response_model=CategoryResponce, status_code=status.HTTP_201_CREATED)
def create_categories(data: CategoryCreate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    category = Category(
        name=data.name,
        user_id= current_user.id
    )

    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.get("/get", response_model=list[CategoryResponce])
def get_category(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Category).where(Category.user_id == current_user.id)
    categories = session.execute(stmt).scalars().all()

    return categories

@router.delete("/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Category).where(Category.id == category_id, User.id == current_user.id)
    category = session.execute(stmt).scalar_one_or_none()
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    session.delete(category)
    session.commit()

@router.patch("/rename/{category_id}", response_model=CategoryUpdate)
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
    session.refresh(category)

    return category