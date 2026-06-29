"""Expense schemas."""
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field, model_validator


class ExpenseBase(BaseModel):
    """Base expense schema."""
    description: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    created_by: int


class ExpenseCreate(ExpenseBase):
    """Expense creation schema."""
    group_id: int
    paid_by_id: int
    split_between: list[int] = None  # List of user IDs to split the expense between



class ExpenseUpdate(ExpenseBase):
    """Expense update schema."""
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[float] = Field(None, gt=0)
    created_by: Optional[int] = None
    paid_by_id: Optional[int] = None
    split_between: list[int] = None 


class Expense(ExpenseBase):
    """Expense response schema."""
    id: int
    group_id: int
    paid_by_id: int
    payer_name: str
    creator_name: str

    @model_validator(mode="before")
    @classmethod
    def extract_nested_user(cls, data: Any) -> Any:

        is_orm = hasattr(data, "__dict__")
        if is_orm:
            data_dict = dict(data.__dict__)
            payer = data_dict.get("payer")
            if payer is not None:
                data_dict["payer_name"] = payer.username

            creator = data_dict.get("creator")
            if creator is not None:
                data_dict["creator_name"] = creator.username
        else:
            data_dict = data
            if isinstance(data, dict) and "payer" in data and data["payer"]:
                data_dict["payer_name"] = data["payer"].get("username")
            
            if isinstance(data, dict) and "creator" in data and data["creator"]:
                data_dict["creator_name"] = data["creator"].get("username")
        return data_dict

    class Config:
        from_attributes = True


class ExpenseSharer(BaseModel):
    """Expense sharer schema."""
    user_id: int
    amount_owed: float
    username: str
    email: str

    @model_validator(mode="before")
    @classmethod
    def extract_nested_user(cls, data: Any) -> Any:
        # Check if we are reading from an ORM object instance
        if hasattr(data, "__dict__"):
            data_dict = dict(data.__dict__)
            user = data_dict.get("user")
            if user is not None:
                # Map the nested data up to the root schema layout
                data_dict["username"] = user.username
                data_dict["email"] = user.email
                return data_dict
            return data_dict
            
        # Fallback tracking if data is passed directly as a nested dict
        if isinstance(data, dict) and "user" in data and data["user"]:
            data["username"] = data["user"].get("username")
            data["email"] = data["user"].get("email")
            return data

        return data

    class Config:
        from_attributes = True


class ExpenseResponse(Expense):
    """Expense response with details."""
    sharers: list[ExpenseSharer]
