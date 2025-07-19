import streamlit as st
import pandas as pd

st.title("Loan Repayment Calculator – quarterly compounding, monthly payments")

loan_amount     = st.number_input("Outstanding loan (EUR)", 100_000.0, step=1_000.0)
annual_rate_pct = st.number_input("Annual nominal rate (%)", 3.5, step=0.1)
monthly_payment = st.number_input("Regular monthly payment (EUR)", 1_000.0, step=50.0)
extra_payment   = st.number_input("Extra monthly payment (EUR)", 0.0, step=50.0)

annual_rate     = annual_rate_pct / 100
quarterly_rate  = annual_rate / 4
monthly_rate    = (1 + quarterly_rate) ** (1/3) - 1      # effective monthly, 3× = quarterly

balance  = loan_amount
month    = 0
schedule = []

while balance > 0 and month < 1000:
    month += 1
    interest = balance * monthly_rate
    balance += interest

    payment = min(monthly_payment + extra_payment, balance)
    balance -= payment

    schedule.append({
        "Month": month,
        "Interest": round(interest, 2),
        "Payment":  round(payment, 2),
        "Balance":  round(balance, 2)
    })

years, rem_months = divmod(month, 12)
st.subheader(f"Loan repaid in {month} months ({years} years {rem_months} months)")

df = pd.DataFrame(schedule)
st.dataframe(df)
st.line_chart(df.set_index("Month")["Balance"])
