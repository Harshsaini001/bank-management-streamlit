import json
import random
import string
from pathlib import Path


class Bank:

    database = Path(__file__).parent / "data.json"

    def __init__(self):
        self.data = self.load_data()

    # -----------------------------
    # Load Data
    # -----------------------------
    def load_data(self):
        try:
            if not self.database.exists():
                return []

            with open(self.database, "r") as file:
                content = file.read().strip()

                if not content:
                    return []

                return json.loads(content)

        except json.JSONDecodeError:
            return []

        except Exception as e:
            print(f"Error loading data: {e}")
            return []

    # -----------------------------
    # Save Data
    # -----------------------------
    def save_data(self):
        try:
            with open(self.database, "w") as file:
                json.dump(self.data, file, indent=4)

        except Exception as e:
            print(f"Error saving data: {e}")

    # -----------------------------
    # Generate Account Number
    # -----------------------------
    def generate_account_number(self):

        while True:

            letters = ''.join(
                random.choices(string.ascii_uppercase, k=3)
            )

            numbers = ''.join(
                random.choices(string.digits, k=6)
            )

            account_number = letters + numbers

            # Make sure account number is unique
            if not any(
                user["accountNo"] == account_number
                for user in self.data
            ):
                return account_number

    # -----------------------------
    # Find User
    # -----------------------------
    def find_user(self, account_number, pin):

        for user in self.data:

            if (
                user["accountNo"] == account_number
                and user["pin"] == pin
            ):
                return user

        return None

    # -----------------------------
    # Create Account
    # -----------------------------
    def create_account(self, name, age, email, pin):

        if not name.strip():
            return False, "Name cannot be empty."

        if age < 18:
            return False, "You must be at least 18 years old."

        if not email.strip():
            return False, "Email cannot be empty."

        if len(str(pin)) != 4:
            return False, "PIN must contain exactly 4 digits."

        account_number = self.generate_account_number()

        new_user = {
            "name": name.strip(),
            "age": age,
            "email": email.strip(),
            "pin": pin,
            "accountNo": account_number,
            "balance": 0
        }

        self.data.append(new_user)
        self.save_data()

        return True, new_user

    # -----------------------------
    # Deposit Money
    # -----------------------------
    def deposit_money(self, account_number, pin, amount):

        user = self.find_user(account_number, pin)

        if user is None:
            return False, "Invalid Account Number or PIN."

        if amount <= 0:
            return False, "Amount must be greater than ₹0."

        if amount > 10000:
            return False, "Maximum deposit allowed is ₹10,000."

        user["balance"] += amount

        self.save_data()

        return True, user["balance"]

    # -----------------------------
    # Withdraw Money
    # -----------------------------
    def withdraw_money(self, account_number, pin, amount):

        user = self.find_user(account_number, pin)

        if user is None:
            return False, "Invalid Account Number or PIN."

        if amount <= 0:
            return False, "Amount must be greater than ₹0."

        if amount > user["balance"]:
            return False, "Insufficient balance."

        user["balance"] -= amount

        self.save_data()

        return True, user["balance"]

    # -----------------------------
    # Get User Details
    # -----------------------------
    def get_details(self, account_number, pin):

        user = self.find_user(account_number, pin)

        if user is None:
            return None

        # Don't expose PIN
        details = user.copy()
        details.pop("pin", None)

        return details

    # -----------------------------
    # Update User
    # -----------------------------
    def update_details(
        self,
        account_number,
        pin,
        name=None,
        email=None,
        new_pin=None
    ):

        user = self.find_user(account_number, pin)

        if user is None:
            return False, "Invalid Account Number or PIN."

        if name and name.strip():
            user["name"] = name.strip()

        if email and email.strip():
            user["email"] = email.strip()

        if new_pin is not None:

            if len(str(new_pin)) != 4:
                return False, "New PIN must contain 4 digits."

            user["pin"] = new_pin

        self.save_data()

        return True, "Details updated successfully."

    # -----------------------------
    # Delete Account
    # -----------------------------
    def delete_account(self, account_number, pin):

        user = self.find_user(account_number, pin)

        if user is None:
            return False, "Invalid Account Number or PIN."

        self.data.remove(user)

        self.save_data()

        return True, "Account deleted successfully."