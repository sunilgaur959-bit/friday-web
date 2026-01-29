import streamlit as st
import math
import datetime
import webbrowser

st.set_page_config(page_title="Friday Assistant", layout="centered")

st.title("🤖 Friday – Finance Assistant")

# ---------------- EMI ----------------
st.header("EMI Calculator")

def calculate_emi(p, r, y):
    r = r/12/100
    n = y*12
    emi = p*r*(1+r)**n/((1+r)**n-1)
    return round(emi, 0)

loan = st.number_input("Loan (₹)", value=2000000)
rate = st.number_input("Rate %", value=10.0)
years = st.number_input("Years", value=5)

if st.button("Calculate EMI"):
    emi = calculate_emi(loan, rate, years)
    total = emi*years*12
    st.success(f"EMI = ₹{emi:,.0f}")
    st.info(f"Total Payment = ₹{total:,.0f}")


# ---------------- Calculator ----------------
st.header("Calculator")

expr = st.text_input("Enter math (example: 20*0.01*100)")

if st.button("Compute"):
    try:
        result = eval(expr)
        st.success(result)
    except:
        st.error("Invalid expression")


# ---------------- Tax Info ----------------
st.header("Tax Quick Guide")

tax_data = {
    "80C": "₹1.5 lakh deduction limit",
    "44AB": "Tax audit above ₹1 Cr turnover",
    "GST Composition": "₹1.5 Cr limit",
    "TDS Interest": "10% above ₹40,000"
}

sec = st.selectbox("Choose section", list(tax_data.keys()))
st.write(tax_data[sec])


# ---------------- Quick Links ----------------
st.header("Quick Portals")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("NSE"):
        webbrowser.open("https://www.nseindia.com")

with col2:
    if st.button("GST"):
        webbrowser.open("https://www.gst.gov.in")

with col3:
    if st.button("ITR"):
        webbrowser.open("https://www.incometax.gov.in")


# ---------------- Notes ----------------
st.header("Notes")

note = st.text_area("Write note")

if st.button("Save"):
    with open("notes.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {note}\n")
    st.success("Saved")
