class Account:
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.deposits = []
        self.withdrawals = []
        self.loan = 0.0
        self.is_frozen = False
        self.min_balance = 0.0
        self.is_closed = False

    def deposit(self, amount):
        if self.is_closed:
            return "Account is closed. Cannot deposit."
        if self.is_frozen:
            return "Account is frozen. Cannot deposit."
        if amount <= 0:
            return "Deposit amount must be positive."
        self.deposits.append(amount)
        return f"Deposit successful. New balance: {self.get_balance():.2f}"

    def withdraw(self, amount):
        if self.is_closed:
            return "Account is closed. Cannot withdraw."
        if self.is_frozen:
            return "Account is frozen. Cannot withdraw."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if self.get_balance() - amount < self.min_balance:
            return f"Cannot withdraw. Balance cannot go below minimum balance of {self.min_balance:.2f}."
        if self.get_balance() < amount:
            return "Insufficient funds. Cannot overdraw."
        self.withdrawals.append(amount)
        return f"Withdrawal successful. New balance: {self.get_balance():.2f}"

    def transfer_funds(self, amount, target_account):
        if self.is_closed:
            return "Account is closed. Cannot transfer funds."
        if self.is_frozen:
            return "Account is frozen. Cannot transfer funds."
        if amount <= 0:
            return "Transfer amount must be positive."
        if self.get_balance() < amount:
            return "Insufficient funds to transfer."
        if not isinstance(target_account, Account):
            return "Target account must be an Account instance."
        if target_account.is_closed:
            return "Target account is closed. Cannot transfer funds."
        if target_account.is_frozen:
            return "Target account is frozen. Cannot receive funds."

        self.withdrawals.append(amount)
        target_account.deposits.append(amount)
        return (f"Transfer successful. Your new balance: {self.get_balance():.2f}. "
                f"{target_account.owner_name}'s new balance: {target_account.get_balance():.2f}")

    def get_balance(self):
        return sum(self.deposits) - sum(self.withdrawals) - self.loan

    def request_loan(self, amount):
        if self.is_closed:
            return "Account is closed. Cannot request loan."
        if amount <= 0:
            return "Loan amount must be positive."
        self.loan += amount
        return f"Loan approved for {amount:.2f}. Total loan amount: {self.loan:.2f}"

    def repay_loan(self, amount):
        if self.is_closed:
            return "Account is closed. Cannot repay loan."
        if amount <= 0:
            return "Repayment amount must be positive."
        if amount > self.loan:
            return f"Repayment amount exceeds loan balance of {self.loan:.2f}."
        if self.get_balance() < amount:
            return "Insufficient funds to repay loan."
        self.withdrawals.append(amount)
        self.loan -= amount
        return f"Loan repayment successful. Remaining loan balance: {self.loan:.2f}"

    def view_account_details(self):
        details = (
            f"Account Owner: {self.owner_name}\n"
            f"Current Balance: {self.get_balance():.2f}\n"
            f"Loan Balance: {self.loan:.2f}\n"
            f"Account Frozen: {self.is_frozen}\n"
            f"Minimum Balance Requirement: {self.min_balance:.2f}\n"
            f"Account Closed: {self.is_closed}"
        )
        return details

    def change_account_owner(self, new_owner_name):
        if self.is_closed:
            return "Account is closed. Cannot change owner."
        if not new_owner_name:
            return "New owner name cannot be empty."
        self.owner_name = new_owner_name
        return f"Account owner name updated to {self.owner_name}."

    def account_statement(self):
        if self.is_closed:
            return "Account is closed. No statement available."
        print(f"Account Statement for {self.owner_name}:")
        print("Deposits:")
        for i, amount in enumerate(self.deposits, 1):
            print(f"  {i}. Deposit: +{amount:.2f}")
        print("Withdrawals:")
        for i, amount in enumerate(self.withdrawals, 1):
            print(f"  {i}. Withdrawal: -{amount:.2f}")
        print(f"Loan Balance: {self.loan:.2f}")
        print(f"Current Balance: {self.get_balance():.2f}")

    def calculate_and_apply_interest(self):
        if self.is_closed:
            return "Account is closed. Cannot apply interest."
        if self.is_frozen:
            return "Account is frozen. Cannot apply interest."
        interest_rate = 0.05
        balance = self.get_balance()
        if balance <= 0:
            return "No positive balance to apply interest."
        interest = balance * interest_rate
        self.deposits.append(interest)
        return f"Interest of {interest:.2f} applied. New balance: {self.get_balance():.2f}"

    def freeze_account(self):
        if self.is_closed:
            return "Account is closed. Cannot freeze."
        self.is_frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        if self.is_closed:
            return "Account is closed. Cannot unfreeze."
        self.is_frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if self.is_closed:
            return "Account is closed. Cannot set minimum balance."
        if amount < 0:
            return "Minimum balance cannot be negative."
        self.min_balance = amount
        return f"Minimum balance set to {self.min_balance:.2f}"

    def close_account(self):
        self.deposits.clear()
        self.withdrawals.clear()
        self.loan = 0.0
        self.is_frozen = False
        self.min_balance = 0.0
        self.is_closed = True
        return "Account has been closed. All balances and transactions cleared."
