from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select 
from app.db.session import get_db
from app.core.secutity import get_current_user
from app.models.categories import Category
from app.models.users import User
from app.models.transaction import Transaction
from app.schemas.transactions import TransactionCreate,TransactionResponse, TransactionUpdate
from datetime import date
from app.utils.enums import TransactionType

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transactions(transaction:TransactionCreate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Category).where(Category.id == transaction.category_id,
                                      Category.user_id == current_user.id)
    category = session.execute(stmt).scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.type != transaction.type:
        raise HTTPException(status_code=400)
    transaction_create = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        category_id = transaction.category_id,
        description=transaction.description,
        date = transaction.date,
        user_id = current_user.id
    )

    session.add(transaction_create)
    session.commit()
    session.refresh(transaction_create)
    return transaction_create
@router.get("/", response_model=list[TransactionResponse])
def get_transactions(session: Session = Depends(get_db), current_user: User = Depends(get_current_user),
                    type: TransactionType  | None = None,
                    category_id: int | None = None,
                    date_from: date | None = None,
                    date_to: date | None = None ):
        
        filters = [Transaction.user_id == current_user.id]

        if type is not None:
            filters.append(Transaction.type == type)

        if category_id is not None:
            filters.append(Transaction.category_id == category_id)

        if date_from is not None:
            filters.append(Transaction.date >= date_from)

        if date_to is not None:
            filters.append(Transaction.date <= date_to)

        stmt = select(Transaction).where(*filters)
        transactions = session.execute(stmt).scalars().all()


        return transactions


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int , session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    stmt = select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user.id)
    transaction = session.execute(stmt).scalar_one_or_none()
    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )
    session.delete(transaction)
    session.commit()

@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    stmt = select(Transaction).where(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    )
    transaction = session.execute(stmt).scalar_one_or_none()

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if data.category_id is not None:
        stmt = select(Category).where(
            Category.id == data.category_id,
            Category.user_id == current_user.id
        )
        category = session.execute(stmt).scalar_one_or_none()

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

        if data.type is not None:
            if category.type != data.type:
                raise HTTPException(status_code=400, detail="Type mismatch")

        else:
            if category.type != transaction.type:
                raise HTTPException(status_code=400, detail="Type mismatch")

        transaction.category_id = data.category_id


    if data.type is not None:
        stmt = select(Category).where(Category.id == transaction.category_id)
        category = session.execute(stmt).scalar_one()

        if category.type != data.type:
            raise HTTPException(status_code=400, detail="Type mismatch")

        transaction.type = data.type


    if data.amount is not None:
        transaction.amount = data.amount

    if data.description is not None:
        transaction.description = data.description

    if data.date is not None:
        transaction.date = data.date

    session.commit()
    session.refresh(transaction)

    return transaction