"""Debt service."""
from app.services.expense_service import ExpenseService
from sqlalchemy.ext.asyncio import AsyncSession

class DebtService:
    @classmethod
    async def simplify_debts(cls, db: AsyncSession, group_id: int) -> list[any]:
        """Simplify debts for a group."""
        # Get all expenses for the group
        expenses = await ExpenseService.get_group_expenses(db, group_id)

        # Calculate net balance for each user
        user_balances = {}
        user_map = {}
        for expense in expenses:
            for sharer in expense.sharers:
                user_balances[sharer.user.id] = user_balances.get(sharer.user.id, 0) - sharer.amount_owed
                user_map[sharer.user.id] = sharer.user.username
            user_balances[expense.payer.id] = user_balances.get(expense.payer.id, 0) + expense.amount
            user_map[expense.payer.id] = expense.payer.username

        # Separate users into creditors and debtors
        creditors = [(user_id, balance) for user_id, balance in user_balances.items() if balance > 0]
        debtors = [(user_id, balance) for user_id, balance in user_balances.items() if balance < 0]       

        simplified_debts = []

        while creditors and debtors:

            # Sort creditors and debtors by amount
            creditors.sort(key=lambda x: x[1], reverse=True)
            debtors.sort(key=lambda x: x[1])

            creditor_id, creditor_amount = creditors[0]
            debtor_id, debtor_amount = debtors[0]

            amount_to_settle = min(abs(creditor_amount), abs(debtor_amount))
            simplified_debts.append({
                "from_user_id": debtor_id,
                "to_user_id": creditor_id,
                "from_user_name": user_map[debtor_id],
                "to_user_name": user_map[creditor_id],
                "amount": amount_to_settle,
                "group_id": group_id
            })

            # Update balances
            creditors[0] = (creditor_id, creditor_amount - amount_to_settle)
            debtors[0] = (debtor_id, debtor_amount + amount_to_settle)

            if creditors[0][1] == 0:
                creditors.pop(0)

            if debtors[0][1] == 0:
                debtors.pop(0)


        return simplified_debts