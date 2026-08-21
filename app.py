import streamlit as st
from bank import Bank


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide"
)


# --------------------------------
# Bank Object
# --------------------------------

bank = Bank()


# --------------------------------
# Title
# --------------------------------

st.title("🏦 Bank Management System")

st.write(
    "A simple Bank Management System built using "
    "Python, JSON and Streamlit."
)


# --------------------------------
# Sidebar Menu
# --------------------------------

st.sidebar.title("Bank Menu")

option = st.sidebar.radio(
    "Select Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Account Details",
        "Update Details",
        "Delete Account"
    ]
)


# =================================
# CREATE ACCOUNT
# =================================

if option == "Create Account":

    st.header("📝 Create New Account")

    name = st.text_input("Full Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=18
    )

    email = st.text_input("Email")

    pin = st.text_input(
        "4 Digit PIN",
        type="password",
        max_chars=4
    )

    if st.button("Create Account"):

        if not pin.isdigit() or len(pin) != 4:

            st.error("PIN must contain exactly 4 digits.")

        else:

            success, result = bank.create_account(
                name,
                age,
                email,
                int(pin)
            )

            if success:

                st.success(
                    "Account created successfully!"
                )

                st.info(
                    f"Your Account Number: **{result['accountNo']}**"
                )

                st.warning(
                    "Please save your account number safely."
                )

            else:

                st.error(result)


# =================================
# DEPOSIT MONEY
# =================================

elif option == "Deposit Money":

    st.header("💰 Deposit Money")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    amount = st.number_input(
        "Deposit Amount",
        min_value=0,
        step=100
    )

    if st.button("Deposit"):

        if not pin.isdigit():

            st.error("Invalid PIN.")

        else:

            success, result = bank.deposit_money(
                account_number,
                int(pin),
                amount
            )

            if success:

                st.success(
                    "Amount deposited successfully!"
                )

                st.metric(
                    "Current Balance",
                    f"₹{result}"
                )

            else:

                st.error(result)


# =================================
# WITHDRAW MONEY
# =================================

elif option == "Withdraw Money":

    st.header("💸 Withdraw Money")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    amount = st.number_input(
        "Withdrawal Amount",
        min_value=0,
        step=100
    )

    if st.button("Withdraw"):

        if not pin.isdigit():

            st.error("Invalid PIN.")

        else:

            success, result = bank.withdraw_money(
                account_number,
                int(pin),
                amount
            )

            if success:

                st.success(
                    "Amount withdrawn successfully!"
                )

                st.metric(
                    "Remaining Balance",
                    f"₹{result}"
                )

            else:

                st.error(result)


# =================================
# ACCOUNT DETAILS
# =================================

elif option == "Account Details":

    st.header("👤 Account Details")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    if st.button("View Details"):

        if not pin.isdigit():

            st.error("Invalid PIN.")

        else:

            details = bank.get_details(
                account_number,
                int(pin)
            )

            if details:

                st.success("Account found!")

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Name:** {details['name']}"
                    )

                    st.write(
                        f"**Age:** {details['age']}"
                    )

                    st.write(
                        f"**Email:** {details['email']}"
                    )

                with col2:

                    st.write(
                        f"**Account No:** {details['accountNo']}"
                    )

                    st.metric(
                        "Balance",
                        f"₹{details['balance']}"
                    )

            else:

                st.error(
                    "Invalid Account Number or PIN."
                )


# =================================
# UPDATE DETAILS
# =================================

elif option == "Update Details":

    st.header("✏️ Update Account Details")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "Current PIN",
        type="password",
        max_chars=4
    )

    st.subheader("New Details")

    new_name = st.text_input(
        "New Name (optional)"
    )

    new_email = st.text_input(
        "New Email (optional)"
    )

    new_pin = st.text_input(
        "New PIN (optional)",
        type="password",
        max_chars=4
    )

    if st.button("Update Account"):

        if not pin.isdigit():

            st.error("Invalid current PIN.")

        elif new_pin and (
            not new_pin.isdigit()
            or len(new_pin) != 4
        ):

            st.error(
                "New PIN must contain exactly 4 digits."
            )

        else:

            success, message = bank.update_details(
                account_number,
                int(pin),
                new_name,
                new_email,
                int(new_pin) if new_pin else None
            )

            if success:

                st.success(message)

            else:

                st.error(message)


# =================================
# DELETE ACCOUNT
# =================================

elif option == "Delete Account":

    st.header("🗑️ Delete Account")

    st.warning(
        "⚠️ Deleting an account is permanent."
    )

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    confirm = st.checkbox(
        "I understand that this action cannot be undone."
    )

    if st.button("Delete Account"):

        if not confirm:

            st.error(
                "Please confirm account deletion."
            )

        elif not pin.isdigit():

            st.error("Invalid PIN.")

        else:

            success, message = bank.delete_account(
                account_number,
                int(pin)
            )

            if success:

                st.success(message)

            else:

                st.error(message)