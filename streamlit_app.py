import streamlit as st
import pandas as pd

st.title("Loan Repayment Calculator (Quarterly Interest)")

# Input fields
loan_amount = st.number_input("Outstanding Loan Amount (EUR)", value=100000.0, step=1000.0)
interest_rate = st.number_input("Annual Interest Rate (%)", value=3.5, step=0.1)
monthly_payment = st.number_input("Monthly Payment (EUR)", value=1000.0, step=50.0)
extra_payment = st.number_input("Extra Monthly Payment (EUR)", value=0.0, step=50.0)

# Convert interest rate to decimal
annual_rate = interest_rate / 100
monthly_interest = (1 + annual_rate) ** (1 / 12) - 1  # Monthly effective interest

# Simulation variables
balance = loan_amount
month = 0
schedule = []

while balance > 0 and month < 1000:
    month += 1
    interest = 0

    # Quarterly interest added
    if month % 3 == 0:
        interest = balance * ((1 + annual_rate / 4) - 1)
        balance += interest

    payment = min(monthly_payment + extra_payment, balance)
    balance -= payment

    schedule.append({
        "Month": month,
        "Interest Added": round(interest, 2),
        "Payment": round(payment, 2),
        "Remaining Balance": round(balance, 2)
    })

# Output
st.subheader(f"Loan Repaid in {month} months ({month//12} years and {month%12} months)")

df = pd.DataFrame(schedule)
st.dataframe(df)

st.line_chart(df.set_index("Month")[["Remaining Balance"]])
