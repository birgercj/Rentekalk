import streamlit as st
import numpy as np
import pandas as pd

def calculate_loan_reduction(loan_amount, interest_rate, monthly_payment, extra_payment):
    months = 0
    total_interest = 0
    balance = loan_amount

    while balance > 0:
        interest = balance * (interest_rate / 12)
        total_interest += interest
        principal_payment = monthly_payment + extra_payment - interest
        if principal_payment <= 0:
            st.error("Betalingen dekker ikke rentene. Øk terminbeløpet.")
            return None, None
        balance -= principal_payment
        months += 1

    return total_interest, months

st.title("Lånekalkulator - Spar renter med ekstra betaling")

# Brukerinput
loan_amount = st.number_input("Nåværende lånesaldo (kr):", min_value=0.0, value=2_000_000.0, step=10000.0)
interest_rate = st.number_input("Nominell årlig rente (%):", min_value=0.0, value=5.0, step=0.1) / 100
monthly_payment = st.number_input("Nåværende månedlig betaling (kr):", min_value=0.0, value=10_000.0, step=100.0)
extra_payment = st.number_input("Ekstra månedlig betaling (kr):", min_value=0.0, value=1000.0, step=100.0)

if st.button("Beregn"):
    original_interest, original_months = calculate_loan_reduction(loan_amount, interest_rate, monthly_payment, 0)
    new_interest, new_months = calculate_loan_reduction(loan_amount, interest_rate, monthly_payment, extra_payment)

    if original_interest is not None and new_interest is not None:
        saved_interest = original_interest - new_interest
        months_saved = original_months - new_months

        st.subheader("Resultat:")
        st.write(f"Du betaler **{original_interest:,.0f} kr** i renter med nåværende betaling.")
        st.write(f"Du betaler **{new_interest:,.0f} kr** i renter med ekstra betaling.")
        st.write(f"Du sparer **{saved_interest:,.0f} kr** i renter.")
        st.write(f"Du betaler ned lånet **{months_saved} måneder** raskere.")
        st.write(f"Ny lånetid: **{new_months} måneder** ({new_months // 12} år og {new_months % 12} måneder).")
