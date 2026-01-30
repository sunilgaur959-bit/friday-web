import streamlit as st
import datetime

st.set_page_config(page_title="Friday – Finance Assistant", layout="wide")

# ======================================================
# SIDEBAR (NAVIGATION)
# ======================================================

st.sidebar.title("🤖 Friday Assistant")

menu = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "🏦 EMI Calculator",
        "🧮 Calculator",
        "📘 Taxation Hub",
        "📝 Notes",
        "🌐 Portals"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Built for CA / Finance Professionals")


# ======================================================
# HOME PAGE
# ======================================================

if menu == "🏠 Home":

    st.title("💼 Friday – Finance & Tax Assistant")

    col1, col2, col3 = st.columns(3)

    col1.metric("Tools", "6")
    col2.metric("Modules", "Finance + Tax")
    col3.metric("Status", "Live 🚀")

    st.write("""
    ### Welcome!
    This is your personal **Finance Automation Dashboard**.

    Use left menu to:
    - Calculate EMI
    - Do quick maths
    - Check TDS sections
    - Save notes
    - Open portals
    """)


# ======================================================
# EMI PAGE
# ======================================================

elif menu == "🏦 EMI Calculator":

    st.title("🏦 EMI Calculator")

    def calculate_emi(p, r, y):
        r = r/12/100
        n = y*12
        emi = p*r*(1+r)**n/((1+r)**n-1)
        return round(emi, 0)

    c1, c2, c3 = st.columns(3)

    with c1:
        loan = st.number_input("Loan (₹)", value=2000000)

    with c2:
        rate = st.number_input("Rate %", value=10.0)

    with c3:
        years = st.number_input("Years", value=5)

    if st.button("Calculate"):
        emi = calculate_emi(loan, rate, years)
        total = emi*years*12
        st.success(f"Monthly EMI: ₹{emi:,.0f}")
        st.info(f"Total Payment: ₹{total:,.0f}")


# ======================================================
# CALCULATOR PAGE
# ======================================================

elif menu == "🧮 Calculator":

    st.title("🧮 Quick Calculator")

    expr = st.text_input("Enter expression (example: 20*0.01*100)")

    if st.button("Compute"):
        try:
            st.success(eval(expr))
        except:
            st.error("Invalid expression")


# ======================================================
# ======================================================
# TAXATION HUB – CLEAR TAX STYLE (EXPANDABLE CARDS)
# ======================================================

elif menu == "📘 Taxation Hub":

    st.title("📘 TDS Handbook – Detailed (FY 2025-26)")
    st.caption("Based on ClearTax TDS rate chart – thresholds & amended rates")

    search = st.text_input("🔍 Search section or payment type")

    tds_data = [

    {"Section":"192","Nature":"Salary","Threshold":"Basic exemption limit",
     "Rate":"Slab rates","Notes":"Employer deducts monthly TDS on estimated income"},

    {"Section":"192A","Nature":"EPF premature withdrawal","Threshold":"₹50,000",
     "Rate":"10%","Notes":"If service < 5 years"},

    {"Section":"193","Nature":"Interest on securities","Threshold":"₹10,000",
     "Rate":"10%","Notes":"Govt securities/bonds"},

    {"Section":"194","Nature":"Dividend","Threshold":"₹10,000",
     "Rate":"10%","Notes":"Dividend payments by companies/MFs"},

    {"Section":"194A","Nature":"Interest other than securities",
     "Threshold":"₹40k / ₹50k (senior)",
     "Rate":"10%","Notes":"Bank/FD interest, Form 15G/15H allowed"},

    {"Section":"194B","Nature":"Lottery/Gambling winnings","Threshold":"₹10,000",
     "Rate":"30%","Notes":"Flat rate, no deduction allowed"},

    {"Section":"194BA","Nature":"Online gaming winnings","Threshold":"₹10,000",
     "Rate":"30%","Notes":"Online games, fantasy apps etc"},

    {"Section":"194BB","Nature":"Horse race winnings","Threshold":"₹10,000",
     "Rate":"30%"},

    {"Section":"194C","Nature":"Contractor/Sub-contractor",
     "Threshold":"₹30k single / ₹1L yearly",
     "Rate":"1% (Ind/HUF), 2% (Others)","Notes":"Transporters with PAN exempt"},

    {"Section":"194D","Nature":"Insurance commission","Threshold":"₹15,000",
     "Rate":"5%"},

    {"Section":"194DA","Nature":"Life insurance payout","Threshold":"₹1,00,000",
     "Rate":"5% (income portion)"},

    {"Section":"194EE","Nature":"NSS withdrawal","Threshold":"₹2,500",
     "Rate":"10%"},

    {"Section":"194G","Nature":"Lottery commission","Threshold":"₹20,000",
     "Rate":"2%"},

    {"Section":"194H","Nature":"Commission/Brokerage","Threshold":"₹20,000",
     "Rate":"2%"},

    {"Section":"194I","Nature":"Rent – building/land","Threshold":"₹2.4 lakh",
     "Rate":"10%"},

    {"Section":"194I","Nature":"Rent – plant/machinery","Threshold":"₹2.4 lakh",
     "Rate":"2%"},

    {"Section":"194J","Nature":"Professional fees","Threshold":"₹30,000",
     "Rate":"10%"},

    {"Section":"194J","Nature":"Technical services","Threshold":"₹30,000",
     "Rate":"2%"},

    {"Section":"194K","Nature":"Mutual fund income","Threshold":"₹5,000",
     "Rate":"10%"},

    {"Section":"194LA","Nature":"Land acquisition compensation","Threshold":"₹2.5 lakh",
     "Rate":"10%"},

    {"Section":"194M","Nature":"High value contract/professional by Individual/HUF",
     "Threshold":"₹50 lakh",
     "Rate":"5%"},

    {"Section":"194N","Nature":"Cash withdrawal","Threshold":"₹1 crore (₹20L no ITR)",
     "Rate":"2%/5%","Notes":"Bank withdrawals"},

    {"Section":"194O","Nature":"E-commerce operator","Threshold":"₹5 lakh",
     "Rate":"1%"},

    {"Section":"194Q","Nature":"Purchase of goods","Threshold":"₹50 lakh",
     "Rate":"0.1%","Notes":"Buyer turnover > ₹10 Cr"},

    {"Section":"194R","Nature":"Business benefit/perquisite","Threshold":"₹20,000",
     "Rate":"10%"},

    {"Section":"194S","Nature":"Crypto/Virtual Digital Asset","Threshold":"₹10k/₹50k",
     "Rate":"1%"},

    {"Section":"195","Nature":"Payment to Non-resident","Threshold":"No limit",
     "Rate":"As per DTAA/Act","Notes":"Return 27Q"},

    ]

    for row in tds_data:
        text = f"{row['Section']} {row['Nature']}".lower()

        if search.lower() in text or search == "":
            with st.expander(f"{row['Section']} – {row['Nature']}"):
                st.write(f"**Threshold:** {row['Threshold']}")
                st.write(f"**Rate:** {row['Rate']}")
                if "Notes" in row:
                    st.write(f"**Notes:** {row['Notes']}")


# ======================================================
# NOTES
# ======================================================

elif menu == "📝 Notes":

    st.title("📝 Notes")

    note = st.text_area("Write your note")

    if st.button("Save"):
        with open("notes.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {note}\n")
        st.success("Saved")


# ======================================================
# PORTALS
# ======================================================

elif menu == "🌐 Portals":

    st.title("🌐 Quick Portals")

    st.link_button("NSE", "https://www.nseindia.com")
    st.link_button("GST Portal", "https://www.gst.gov.in")
    st.link_button("ITR Portal", "https://www.incometax.gov.in")
    st.link_button("Screener", "https://www.screener.in")
