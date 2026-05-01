from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.secutity import get_current_user
from app.models.users import User
from app.models.transaction import Transaction
from app.db.session import get_db
from app.schemas.ai import AIQuestion, AIAnswer
from app.services.ai_service import ask_openai

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/ask", response_model=AIAnswer)
def ask_ai(
    data: AIQuestion,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    stmt = select(Transaction).where(Transaction.user_id == current_user.id)

    transaction = session.execute(stmt).scalars().all()

    transaction_data = [
        {
            "amount": str(t.amount),
            "type": t.type.value if hasattr(t.type, "value") else str(t.type),
            "description": t.description,
            "date": str(t.date),
            "category_id": t.category_id,
        }
        for t in transaction
    ]

    answer = ask_openai(
        question=data.question,
        transaction=transaction_data,
    )

    return AIAnswer(answer = answer)