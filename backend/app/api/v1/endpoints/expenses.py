"""Expense endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseResponse, status_code=201)
async def create_expense(
    expense_create: ExpenseCreate,
    db: AsyncSession = Depends(get_db)
) -> ExpenseResponse:
    """Create a new expense."""
    expense = await ExpenseService.create_expense(db, expense_create)
    return expense


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db)
) -> ExpenseResponse:
    """Get expense by ID."""
    expense = await ExpenseService.get_expense_by_id(db, expense_id)
    return expense


@router.get("/group/{group_id}", response_model=list[ExpenseResponse])
async def list_group_expenses(
    group_id: int,
    db: AsyncSession = Depends(get_db)
) -> list[ExpenseResponse]:
    """List all expenses for a group."""
    expenses = await ExpenseService.get_group_expenses(db, group_id)
    return expenses


@router.patch("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: AsyncSession = Depends(get_db)
) -> ExpenseResponse:
    """Update expense."""
    expense = await ExpenseService.update_expense(db, expense_id, expense_update)
    return expense


@router.delete("/{expense_id}", status_code=204)
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete expense."""
    await ExpenseService.delete_expense(db, expense_id)
