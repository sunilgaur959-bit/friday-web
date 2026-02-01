import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import os
import re
import time
from io import BytesIO


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(page_title="Friday – Finance Assistant", layout="wide")


# ======================================================
# NAVIGATION STATE (STABLE)
# ======================================================

if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Home"


# ======================================================
# GST TEMPLATE CREATOR
# ======================================================

def create_gst_template():
    cols = ["Supplier_Name", "Invoice_No", "IGST", "CGST", "SGST"]

    sample = pd.DataFrame([
        ["ABC Traders", "INV001", 1800, 0, 0],
        ["XYZ Pvt Ltd", "BILL45", 0, 900, 900]
    ], columns=cols)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        sample.to_excel(writer, sheet_name="GSTR_2B", index=False)
        sample.to_excel(writer, sheet_name="BOOKS", index=False)

    output.seek(0)
    return output


# ======================================================
# SIDEBAR
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
        "🌐 Portals",
        "📊 GST Reconciliation",
    ],
    key="menu"
)

st.sidebar.markdown("---")
st.sidebar.info("Built for CA / Finance Professionals")


# ======================================================
# 🏠 HOME DASHBOARD
# ======================================================

if menu == "🏠 Home":

    st.title("💼 Friday – Finance Automation Dashboard")
    st.markdown("### 📊 GST Reconciliation Summary")

    output_file = "GST_Reco_Reconciled.xlsx"

    if os.path.exists(output_file):

        books = pd.read_excel(output_file, sheet_name="BOOKS")

        total = len(books)
        matched = (books["RECO_REMARK"] == "MATCHED").sum()
        unmatched = total - matched
        percent = round((matched/total)*100, 2) if total else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Invoices", total)
        c2.metric("Matched", matched)
        c3.metric("Unmatched", unmatched)
        c4.metric("Match %", f"{percent}%")

        chart_df = pd.DataFrame({
            "Status": ["Matched", "Unmatched"],
            "Count": [matched, unmatched]
        })

        fig = px.pie(chart_df, names="Status", values="Count", hole=0.5)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Run GST reconciliation first to see dashboard metrics")

    st.markdown("---")
    st.markdown("### ⚡ Quick Tools")

    b1, b2, b3 = st.columns(3)

    if b1.button("📊 Run GST Reconciliation"):
        st.session_state.menu = "📊 GST Reconciliation"
        st.rerun()

    if b2.button("📘 View TDS Handbook"):
        st.session_state.menu = "📘 Taxation Hub"
        st.rerun()

    if b3.button("🏦 EMI Calculator"):
        st.session_state.menu = "🏦 EMI Calculator"
        st.rerun()


# ======================================================
# EMI PAGE
# ======================================================

elif menu == "🏦 EMI Calculator":

    st.title("🏦 EMI Calculator")

    def calculate_emi(p, r, y):
        r = r/12/100
        n = y*12

        if r == 0:
            return round(p/n, 0)

        emi = p*r*(1+r)**n/((1+r)**n-1)
        return round(emi, 0)

    c1, c2, c3 = st.columns(3)

    loan = c1.number_input("Loan (₹)", value=2000000)
    rate = c2.number_input("Rate %", value=10.0)
    years = c3.number_input("Years", value=5)

    if st.button("Calculate"):
        emi = calculate_emi(loan, rate, years)
        total = emi*years*12
        st.success(f"Monthly EMI: ₹{emi:,.0f}")
        st.info(f"Total Payment: ₹{total:,.0f}")


# ======================================================
# CALCULATOR
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
# TAXATION HUB
# ======================================================

elif menu == "📘 Taxation Hub":

    st.title("📘 TDS Handbook – FY 2025-26 (AY 2026-27)")
    st.info("Search any section → threshold → rate → notes")

    search = st.text_input("🔍 Search section or keyword")

    tds_data = [

        {"Section":"192","Nature":"Salary","Threshold":"Basic exemption","Rate":"Slab rates","Notes":"Employer deducts monthly"},

        {"Section":"192A","Nature":"EPF premature withdrawal","Threshold":"₹50,000","Rate":"10%"},

        {"Section":"193","Nature":"Interest on securities","Threshold":"₹10,000","Rate":"10%"},

        {"Section":"194A","Nature":"Bank/FD interest","Threshold":"₹50,000 (₹1L senior citizen)","Rate":"10%"},

        {"Section":"194B","Nature":"Lottery winnings","Threshold":"₹10,000","Rate":"30%"},

        {"Section":"194C","Nature":"Contractor payments","Threshold":"₹30k single / ₹1L yearly","Rate":"1% / 2%"},

        {"Section":"194D","Nature":"Insurance commission","Threshold":"₹20,000","Rate":"5%"},

        {"Section":"194H","Nature":"Commission/Brokerage","Threshold":"₹20,000","Rate":"2%"},

        {"Section":"194I","Nature":"Rent – Land/Building","Threshold":"₹50,000 per month","Rate":"10%","Notes":"Amended limit"},

        {"Section":"194I","Nature":"Rent – Plant/Machinery","Threshold":"₹50,000 per month","Rate":"2%"},

        {"Section":"194IB","Nature":"Rent by Individual/HUF (no audit)","Threshold":"₹50,000 per month","Rate":"2%","Notes":"Single deduction, Form 26QC"},

        {"Section":"194J","Nature":"Professional fees","Threshold":"₹50,000 yearly","Rate":"10%"},

        {"Section":"194J","Nature":"Technical services","Threshold":"₹50,000 yearly","Rate":"2%"},

        {"Section":"194K","Nature":"Mutual fund income","Threshold":"₹5,000","Rate":"10%"},

        {"Section":"194IA","Nature":"Property purchase","Threshold":"₹50 lakh","Rate":"1%","Notes":"Form 26QB"},

        {"Section":"194M","Nature":"High value contract/professional by Individual/HUF","Threshold":"₹50 lakh","Rate":"5%"},

        {"Section":"194N","Nature":"Cash withdrawal","Threshold":"₹1 crore","Rate":"2% / 5%"},

        {"Section":"194O","Nature":"E-commerce operator","Threshold":"₹5 lakh","Rate":"0.1%"},

        {"Section":"194Q","Nature":"Purchase of goods","Threshold":"₹50 lakh","Rate":"0.1%"},

        {"Section":"194R","Nature":"Business benefit/perquisite","Threshold":"₹20,000","Rate":"10%"},

        {"Section":"194S","Nature":"Crypto/VDA","Threshold":"₹10k / ₹50k","Rate":"1%"},

        {"Section":"195","Nature":"Payment to Non-resident","Threshold":"No limit","Rate":"As per Act/DTAA"},
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

    st.link_button("GST Portal", "https://www.gst.gov.in")
    st.link_button("ITR Portal", "https://www.incometax.gov.in")
    st.link_button("NSE", "https://www.nseindia.com")


# ======================================================
# GST RECONCILIATION (TEMPLATE BASED)
# ======================================================

elif menu == "📊 GST Reconciliation":

    st.title("📊 GST 2B vs Books Reconciliation Tool")

    st.subheader("Step 1 — Download Template")

    template_file = create_gst_template()

    st.download_button(
        "⬇ Download GST Template",
        template_file,
        file_name="Friday_GST_Template.xlsx"
    )

    st.markdown("---")

    st.subheader("Step 2 — Upload Filled File")

    uploaded_file = st.file_uploader("Upload filled template", type=["xlsx"])

    TOLERANCE = 1

    if uploaded_file:

        if st.button("Run Reconciliation"):

            start_time = time.time()

            gstr2b = pd.read_excel(uploaded_file, sheet_name="GSTR_2B")
            books = pd.read_excel(uploaded_file, sheet_name="BOOKS")

            required_cols = ["Supplier_Name", "Invoice_No", "IGST", "CGST", "SGST"]

            for col in required_cols:
                if col not in gstr2b.columns or col not in books.columns:
                    st.error(f"Missing column: {col}. Please use template.")
                    st.stop()

            for df in [gstr2b, books]:

                df["Invoice_No_CLEAN"] = df["Invoice_No"].astype(str).str.replace(r"[^A-Z0-9]", "", regex=True)
                df["RECO_REMARK"] = "NOT MATCHED"
                df["USED"] = False

                for col in ["IGST", "CGST", "SGST"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

            for i, b in books.iterrows():
                candidates = gstr2b[
                    (~gstr2b["USED"]) &
                    (gstr2b["Invoice_No_CLEAN"] == b["Invoice_No_CLEAN"]) &
                    (abs(gstr2b["IGST"] - b["IGST"]) <= TOLERANCE) &
                    (abs(gstr2b["CGST"] - b["CGST"]) <= TOLERANCE) &
                    (abs(gstr2b["SGST"] - b["SGST"]) <= TOLERANCE)
                ]

                if len(candidates) > 0:
                    j = candidates.index[0]
                    books.loc[i, "RECO_REMARK"] = "MATCHED"
                    gstr2b.loc[j, "USED"] = True

            matched = (books["RECO_REMARK"] == "MATCHED").sum()
            total = len(books)

            st.success(f"Matched: {matched} / {total}")
            st.info(f"Time taken: {round(time.time()-start_time,2)} sec")

            output = BytesIO()

            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                gstr2b.to_excel(writer, sheet_name="GSTR_2B", index=False)
                books.to_excel(writer, sheet_name="BOOKS", index=False)

            output.seek(0)

            st.download_button(
                "⬇ Download Reconciled File",
                output,
                file_name="GST_Reco_Reconciled.xlsx"
            )
