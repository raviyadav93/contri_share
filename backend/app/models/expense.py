"""Expense model."""
from datetime import datetime
from typing import Optional

from app.models.expense_sharers import ExpenseSharer
from app.models.user import User
from sqlmodel import Field, SQLModel, Relationship

from app.models.base import TimestampMixin


class Expense(SQLModel, TimestampMixin, table=True):
    """Expense model."""
    
    __tablename__ = "expenses"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="groups.id", index=True, ondelete="CASCADE")
    paid_by_id: int = Field(foreign_key="users.id")
    created_by: int = Field(foreign_key="users.id")
    description: str
    amount: float = Field(gt=0)

    sharers: list["ExpenseSharer"] = Relationship(
            sa_relationship_kwargs={
                "foreign_keys": "[ExpenseSharer.expense_id]",
                "cascade": "all, delete-orphan"  # <-- Automatically deletes removed splits
            }
        )  # Relationship to ExpenseSharer model
    payer: "User" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Expense.paid_by_id]"})  # Relationship to User model for paid_by_id
    creator: "User" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Expense.created_by]"})  # Relationship to User model for created_by
