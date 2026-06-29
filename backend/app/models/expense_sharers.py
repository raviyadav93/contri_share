"""ExpenseSharer model."""
from datetime import datetime
from typing import Optional

from app.models.user import User
from sqlmodel import Field, SQLModel, Relationship

from app.models.base import TimestampMixin


class ExpenseSharer(SQLModel, TimestampMixin, table=True):
    """ExpenseSharer model."""
    
    __tablename__ = "expense_sharers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    expense_id: int = Field(foreign_key="expenses.id", index=True, ondelete="CASCADE")
    user_id: int = Field(foreign_key="users.id")
    amount_owed: float = Field(gt=0)

    user: "User" = Relationship()  # Relationship to User model
