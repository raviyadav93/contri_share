"""Expense service."""
from app.services.group_service import GroupService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from sqlalchemy.orm import selectinload, load_only

from app.exceptions import InvalidExpenseError, ResourceNotFoundError
from app.models import Expense, ExpenseSharer, User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


class ExpenseService:
    """Expense business logic service."""

    _eager_load_options = (
        selectinload(Expense.sharers)
        .selectinload(ExpenseSharer.user)
        .options(load_only(User.id, User.email, User.username)),

        selectinload(Expense.payer)
        .options(load_only(User.id, User.username)),

        selectinload(Expense.creator)
        .options(load_only(User.id, User.username))
    )

    @staticmethod
    async def create_expense(
        db: AsyncSession,
        expense_create: ExpenseCreate
    ) -> Expense:
        """Create a new expense."""
        # Create expense without split_between field
        await GroupService.get_group_by_id(db, expense_create.group_id)
        expense_data = expense_create.model_dump(exclude={"split_between"})
        expense = Expense(**expense_data)
        
        db.add(expense)
        await db.flush()  # Flush to get the expense ID before committing
        
        # Create expense sharers for each user in split_between
        expense_sharers = expense_create.split_between or []

        if not expense_sharers:
            raise InvalidExpenseError()
        
        unique_sharers = set(expense_sharers)

        if len(unique_sharers) != len(expense_sharers):
            raise InvalidExpenseError()
        
        stmt = select(func.count(User.id)).where(User.id.in_(unique_sharers))
        result = await db.execute(stmt)

        db_user_count = result.scalar_one()

        if db_user_count != len(unique_sharers):
            raise InvalidExpenseError()
        
        share_amount = expense.amount / len(expense_sharers)
        
        sharers = [
            ExpenseSharer(
                expense_id=expense.id,
                user_id=user_id,
                amount_owed=share_amount
            )
            for user_id in expense_sharers
        ]

        # Bulk add all sharers at once instead of a loop
        db.add_all(sharers)

        await db.commit()

        stmt = (
            select(Expense)
            .where(Expense.id == expense.id)
            .options(*ExpenseService._eager_load_options)
        )
        result = await db.execute(stmt)
        return result.scalar_one()
       

    @staticmethod
    async def get_group_expenses(
        db: AsyncSession,
        group_id: int
    ) -> list[Expense]:
        """Get all expenses for a group."""
        statement = (
            select(Expense)
            .where(Expense.group_id == group_id)
            .options(*ExpenseService._eager_load_options)            
        )
        result = await db.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def update_expense(
        db: AsyncSession,
        expense_id: int,
        expense_update: ExpenseUpdate
    ) -> Expense:
        """Update expense."""
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        
        update_data = expense_update.model_dump(exclude_unset=True, exclude={"split_between"})
        expense_sharers = expense_update.split_between or []

        if not expense_sharers:
            raise InvalidExpenseError()
        
        unique_sharers = set(expense_sharers)
        if len(unique_sharers) != len(expense_sharers):
            raise InvalidExpenseError()
        
        stmt = select(func.count(User.id)).where(User.id.in_(unique_sharers))
        result = await db.execute(stmt)
        db_user_count = result.scalar_one()
        if db_user_count != len(unique_sharers):
            raise InvalidExpenseError()
        
        share_amount = update_data.get("amount", expense.amount) / len(expense_sharers)

        for key, value in update_data.items():
            setattr(expense, key, value)

        # Update sharers
        expense.sharers = [
            ExpenseSharer(
                user_id=user_id,
                amount_owed=share_amount
            )
            for user_id in expense_sharers
        ]  
        
        await db.commit()
        db.expire(expense)  # Expire the expense instance to refresh its state from the database
        return await ExpenseService.get_expense_by_id(db, expense_id) 
        
    @staticmethod
    async def delete_expense(
        db: AsyncSession,
        expense_id: int
    ) -> None:
        """Delete expense."""
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        await db.delete(expense)
        await db.commit()

    @staticmethod
    async def get_expense_by_id(
        db: AsyncSession,
        expense_id: int
    ) -> Expense:
        """Get expense by ID."""

        # stmt = (
        #     select(Expense)
        #     .where(Expense.id == expense_id)
        #     .options(*ExpenseService._eager_load_options)
        # )
        # result = await db.execute(stmt)
        # expense = result.scalar_one_or_none()
        
        # if not expense:
        #     raise ResourceNotFoundError("Expense", expense_id)
            
        # return expense

        expense = await db.get(
            Expense, 
            expense_id, 
            options = ExpenseService._eager_load_options,
        )
        
        if not expense:
            raise ResourceNotFoundError("Expense", expense_id)
            
        return expense
