import streamlit as st
import datetime

st.set_page_config(page_title="Friday – Finance Assistant", layout="wide")

st.title("💼 Friday – Finance & Tax Assistant")


# =====================================================
# EMI CALCULATOR
# =====================================================

st.header("🏦 EMI Calculator")

def calculate_emi(p, r, y):
    r = r/12/100
    n = y*12
    emi = p*r*(1+r)**n/((1+r)**n-1)
    return round(emi, 0)

col1, col2, col3 = st.columns(3)

with col1:
    loan = st.number_input("Loan Amount (₹)", value=2000000)

with col2:
    rate = st.number_input("Interest %", value=10.0)

with col3:
    years = st.number_input("Years", value=5)

if st.button("Calculate EMI"):
    emi = calculate_emi(loan, rate, years)
    total = emi*years*12
    st.success(f"Monthly EMI = ₹{emi:,.0f}")
    st.info(f"Total Payment = ₹{total:,.0f}")


# =====================================================
# CALCULATOR
# =====================================================

st.header("🧮 Quick Calculator")

expr = st.text_input("Enter math (example: 20*0.01*100)")

if st.button("Compute"):
    try:
        result = eval(expr)
        st.success(result)
    except:
        st.error("Invalid expression")


# =====================================================
# QUICK LINKS
# =====================================================

st.header("🌐 Quick Portals")

st.link_button("NSE", "https://www.nseindia.com")
st.link_button("GST Portal", "https://www.gst.gov.in")
st.link_button("ITR Portal", "https://www.incometax.gov.in")
st.link_button("Screener", "https://www.screener.in")


# =====================================================
# NOTES
# =====================================================

st.header("📝 Notes")

note = st.text_area("Write note")

if st.button("Save Note"):
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {note}\n")
    st.success("Saved")


# =====================================================
# TAXATION HUB
# =====================================================

st.header("📘 Taxation Hub")

tab1, tab2 = st.tabs(["Direct Tax – TDS Handbook", "GST – Coming Soon"])


# =====================================================
# FULL TDS HANDBOOK (DETAILED + COMPLETE)
# =====================================================

with tab1:

    st.subheader("📚 Complete TDS Compliance Handbook")
    st.info("Search any section → click to view full applicability, rate, forms & notes")

    tds_sections = [

    {
    "Section":"192",
    "Nature":"Salary",
    "Who deducts":"Employer",
    "Threshold":"Basic exemption",
    "Rate":"Slab rates",
    "Deposit":"7th next month",
    "Return":"24Q",
    "Certificate":"Form 16",
    "Notes":"Monthly TDS based on estimated tax"
    },

    {
    "Section":"192A",
    "Nature":"EPF premature withdrawal",
    "Threshold":"₹50,000",
    "Rate":"10%",
    "Return":"26Q"
    },

    {
    "Section":"193",
    "Nature":"Interest on securities",
    "Threshold":"₹10,000",
    "Rate":"10%",
    "Return":"26Q"
    },

    {
    "Section":"194A",
    "Nature":"Bank/FD interest",
    "Threshold":"₹40k/₹50k senior",
    "Rate":"10%",
    "Return":"26Q",
    "Notes":"15G/15H allowed"
    },

    {
    "Section":"194B",
    "Nature":"Lottery/gambling winnings",
    "Threshold":"₹10,000",
    "Rate":"30%"
    },

    {
    "Section":"194C",
    "Nature":"Contractor/Sub-contractor",
    "Threshold":"₹30k single / ₹1L yearly",
    "Rate":"1%/2%",
    "Return":"26Q"
    },

    {
    "Section":"194D",
    "Nature":"Insurance commission",
    "Threshold":"₹15,000",
    "Rate":"5%"
    },

    {
    "Section":"194H",
    "Nature":"Commission/Brokerage",
    "Threshold":"₹15,000",
    "Rate":"5%"
    },

    {
    "Section":"194I",
    "Nature":"Rent",
    "Threshold":"₹2.4 lakh yearly",
    "Rate":"10% building / 2% plant",
    "Return":"26Q"
    },

    {
    "Section":"194J",
    "Nature":"Professional/Technical fees",
    "Threshold":"₹30,000",
    "Rate":"10%/2%",
    "Return":"26Q"
    },

    {
    "Section":"194K",
    "Nature":"Mutual fund income",
    "Threshold":"₹5,000",
    "Rate":"10%"
    },

    {
    "Section":"194Q",
    "Nature":"Purchase of goods",
    "Threshold":"₹50 lakh",
    "Rate":"0.1%",
    "Notes":"Buyer turnover > ₹10Cr"
    },

    {
    "Section":"194R",
    "Nature":"Business benefit/perquisite",
    "Threshold":"₹20,000",
    "Rate":"10%"
    },

    {
    "Section":"194S",
    "Nature":"Crypto/Virtual assets",
    "Threshold":"₹10k/₹50k",
    "Rate":"1%"
    },

    {
    "Section":"194IA",
    "Nature":"Property purchase",
    "Threshold":"₹50 lakh property",
    "Rate":"1%",
    "Form":"26QB"
    },

    {
    "Section":"194M",
    "Nature":"High value payment by Individual/HUF",
    "Threshold":"₹50 lakh yearly",
    "Rate":"5%",
    "Form":"26QD"
    },

    {
    "Section":"195",
    "Nature":"Payment to Non-resident",
    "Threshold":"No limit",
    "Rate":"DTAA/Act",
    "Return":"27Q"
    },

    {
    "Section":"206C(1H)",
    "Nature":"TCS on sale of goods",
    "Threshold":"₹50 lakh sale",
    "Rate":"0.1%",
    "Return":"27EQ"
    }
    ]

    search = st.text_input("🔍 Search section or keyword")

    for row in tds_sections:
        text = str(row).lower()

        if search.lower() in text or search == "":
            with st.expander(f"{row['Section']} – {row['Nature']}"):
                for k, v in row.items():
                    if k not in ["Section", "Nature"]:
                        st.write(f"**{k}:** {v}")


with tab2:
    st.info("GST section coming next (rates, returns, due dates, interest & penalties)")
