    import streamlit as st
import datetime
import time


import pandas as pd
from io import BytesIO

def create_gst_template():
    sample = pd.DataFrame({
        "Supplier_Name": ["ABC Traders", "XYZ Pvt Ltd"],
        "GSTIN": ["27ABCDE1234F1Z5", "29PQRSX5678L1Z2"],
        "Invoice_Date": ["01-01-2026", "02-01-2026"],
        "Invoice_No": ["INV001", "BILL45"],
        "IGST": [0, 0],
        "CGST": [900, 450],
        "SGST": [900, 450]
    })

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        sample.to_excel(writer, sheet_name="GSTR_2B", index=False)
        sample.to_excel(writer, sheet_name="BOOKS", index=False)

    output.seek(0)
    return output



# ===== Navigation state (simple & stable) =====
if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Home"



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
        "🌐 Portals",
        "📊 GST Reconciliation",

    ],
    key="menu"
)

st.sidebar.markdown("---")
st.sidebar.info("Built for CA / Finance Professionals")
with st.sidebar:
    page = st.radio(
        "Tools",
        ["GST Reco", "Trial Balance", "TDS Calc", "History"]
    )

import pandas as pd
import os

if page == "History":

    st.header("📜 Run History")

    os.makedirs("history", exist_ok=True)
    files = os.listdir("history")


    if not files:
        st.info("No history available yet")
    else:
        data = []

        for f in files:
            path = os.path.join("history", f)
            size = round(os.path.getsize(path)/1024, 2)

            data.append([f, size])

        df = pd.DataFrame(data, columns=["File Name", "Size (KB)"])

        st.dataframe(df, use_container_width=True)

        for f in files:
            with open(f"history/{f}", "rb") as file:
                st.download_button(
                    label=f"⬇ Download {f}",
                    data=file,
                    file_name=f
        )



# ======================================================
# HOME PAGE
# ======================================================

# ======================================================
# 🏠 HOME DASHBOARD (PROFESSIONAL)
# ======================================================

if menu == "🏠 Home":

    import pandas as pd
    import plotly.express as px
    import os

    st.title("💼 Friday – Finance Automation Dashboard")

    st.markdown("### 📊 GST Reconciliation Summary")

    output_file = "GST_Reco_Reconciled.xlsx"

    if os.path.exists(output_file):

        books = pd.read_excel(output_file, sheet_name="BOOKS")

        total = len(books)
        matched = (books["RECO_REMARK"] == "MATCHED").sum()
        unmatched = total - matched
        percent = round((matched/total)*100, 2) if total else 0

        # ======================
        # METRICS CARDS
        # ======================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Invoices", total)
        c2.metric("Matched", matched)
        c3.metric("Unmatched", unmatched)
        c4.metric("Match %", f"{percent}%")

        # ======================
        # PIE CHART
        # ======================

        chart_df = pd.DataFrame({
            "Status": ["Matched", "Unmatched"],
            "Count": [matched, unmatched]
        })

        fig = px.pie(chart_df, names="Status", values="Count", hole=0.5)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Run GST Reconciliation first to see dashboard metrics")

    # ======================
    # QUICK TOOLS
    # ======================

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

        # zero interest fix
        if r == 0:
            return round(p/n, 0)

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
    # ======================================================
# 📘 TAXATION HUB – UPDATED TDS HANDBOOK (FY 2025-26)
# ======================================================

elif menu == "📘 Taxation Hub":

    st.title("📘 TDS Handbook – Updated FY 2025-26 (AY 2026-27)")
    st.info("Includes latest amended thresholds & rates (194I, 194J etc)")

    search = st.text_input("🔍 Search section or keyword")

    tds_data = [

    # ================= SALARY =================
    {"Section":"192","Nature":"Salary",
     "Threshold":"Basic exemption limit",
     "Rate":"Slab rates",
     "Notes":"Employer deducts monthly based on estimated income tax"},

    {"Section":"192A","Nature":"EPF premature withdrawal",
     "Threshold":"₹50,000",
     "Rate":"10%"},

    # ================= INTEREST =================
    {"Section":"193","Nature":"Interest on securities",
     "Threshold":"₹10,000","Rate":"10%"},

    {"Section":"194A","Nature":"Interest other than securities (Bank/FD)",
     "Threshold":"₹50,000 (₹1,00,000 senior citizens) / ₹10,000 others",
     "Rate":"10%",
     "Notes":"Form 15G/15H allowed"},

    # ================= LOTTERY / GAMING =================
    {"Section":"194B","Nature":"Lottery/Gambling winnings",
     "Threshold":"₹10,000","Rate":"30%"},

    {"Section":"194BA","Nature":"Online gaming winnings",
     "Threshold":"₹10,000","Rate":"30%"},

    {"Section":"194BB","Nature":"Horse race winnings",
     "Threshold":"₹10,000","Rate":"30%"},

    # ================= CONTRACT =================
    {"Section":"194C","Nature":"Contractor/Sub-contractor",
     "Threshold":"₹30,000 single / ₹1,00,000 yearly",
     "Rate":"1% (Ind/HUF), 2% (Others)"},

    # ================= INSURANCE =================
    {"Section":"194D","Nature":"Insurance commission",
     "Threshold":"₹20,000","Rate":"5%"},

    {"Section":"194DA","Nature":"Life insurance payout",
     "Threshold":"₹1,00,000",
     "Rate":"5% (income portion only)"},

    # ================= COMMISSION =================
    {"Section":"194G","Nature":"Lottery commission",
     "Threshold":"₹20,000","Rate":"2%"},

    {"Section":"194H","Nature":"Commission/Brokerage",
     "Threshold":"₹20,000","Rate":"2%"},

    # ================= RENT (AMENDED) =================
    {"Section":"194I","Nature":"Rent – Land/Building/Furniture",
     "Threshold":"₹50,000 per month (₹6 lakh yearly)",
     "Rate":"10%",
     "Notes":"Amended from old ₹2.4L yearly limit"},

    {"Section":"194I","Nature":"Rent – Plant/Machinery",
     "Threshold":"₹50,000 per month",
     "Rate":"2%"},

    {"Section":"194IB","Nature":"Rent by Individual/HUF (no audit)",
     "Threshold":"₹50,000 per month",
     "Rate":"2%",
     "Notes":"Single deduction at year end"},

    # ================= PROFESSIONAL (AMENDED) =================
    {"Section":"194J","Nature":"Professional fees (CA, lawyer, doctor etc)",
     "Threshold":"₹50,000 yearly",
     "Rate":"10%",
     "Notes":"Amended from ₹30k → ₹50k"},

    {"Section":"194J","Nature":"Technical services / royalty",
     "Threshold":"₹50,000 yearly",
     "Rate":"2%"},

    # ================= MUTUAL FUND =================
    {"Section":"194K","Nature":"Mutual fund income",
     "Threshold":"₹5,000","Rate":"10%"},

    # ================= PROPERTY =================
    {"Section":"194IA","Nature":"Property purchase",
     "Threshold":"₹50 lakh property value",
     "Rate":"1%","Notes":"Form 26QB, no TAN required"},

     {"Section":"194IB",
     "Nature":"Rent paid by Individual/HUF (not liable for tax audit)",
    "Who deducts":"Individual or HUF not covered under 194I",
    "Threshold":"₹50,000 per month",
    "Rate":"2%",
    "When to deduct":"Only once in last month of FY or tenancy",
    "Deposit due date":"Within 30 days from month end",
    "Form":"26QC",
    "Certificate":"Form 16C",
    "Notes":"TAN not required. Single deduction only (not monthly)."},

    {"Section":"194LA","Nature":"Land acquisition compensation",
     "Threshold":"₹2.5 lakh","Rate":"10%"},

    # ================= HIGH VALUE IND/HUF =================
    {"Section":"194M","Nature":"High value contract/professional by Individual/HUF",
     "Threshold":"₹50 lakh yearly","Rate":"5%"},

    # ================= CASH WITHDRAWAL =================
    {"Section":"194N","Nature":"Cash withdrawal",
     "Threshold":"₹1 crore (₹20L if no ITR filed)",
     "Rate":"2% / 5%",
     "Notes":"Bank withdrawals"},

    # ================= E-COMMERCE =================
    {"Section":"194O","Nature":"E-commerce operator payments",
     "Threshold":"₹5 lakh","Rate":"0.1%"},

    # ================= PURCHASE OF GOODS =================
    {"Section":"194Q","Nature":"Purchase of goods",
     "Threshold":"₹50 lakh purchase & buyer turnover > ₹10 Cr",
     "Rate":"0.1%"},

    # ================= BENEFIT =================
    {"Section":"194R","Nature":"Business benefit/perquisite",
     "Threshold":"₹20,000","Rate":"10%"},

    # ================= CRYPTO =================
    {"Section":"194S","Nature":"Virtual Digital Assets (Crypto)",
     "Threshold":"₹10k / ₹50k","Rate":"1%"},

    # ================= NON RESIDENT =================
    {"Section":"195","Nature":"Payment to Non-resident",
     "Threshold":"No limit","Rate":"As per DTAA/Act"},

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

# ======================================================
# 📊 GST RECONCILIATION – FINAL WEB VERSION
# (Your exact logic wrapped for Streamlit)
# ======================================================

elif menu == "📊 GST Reconciliation":

    import pandas as pd
    import re
    import time
    from io import BytesIO

    st.title("📊 GST 2B vs Books Reconciliation Tool")

    st.info("Upload GST_Reco.xlsx containing sheets: GSTR_2B and BOOKS")

    st.subheader("Step 1 — Download Template")

    template_file = create_gst_template()

    st.download_button(
        "⬇ Download GST Template",
        template_file,
        file_name="Friday_GST_Template.xlsx"
    )
    

    st.markdown("---")

    st.subheader("Step 2 — Upload Filled File")

    uploaded_file = st.file_uploader(
    "Upload filled template",
    type=["xlsx"]
    )


    TOLERANCE = 1


    # ==============================
    # YOUR ORIGINAL FUNCTIONS (UNCHANGED)
    # ==============================

    def read_sheet_safely(file, sheet):
        raw = pd.read_excel(file, sheet_name=sheet, header=None)
        header_row = None
        for i in range(10):
            row_text = " ".join(raw.iloc[i].astype(str)).lower()
            if "supplier" in row_text or "party" in row_text:
                header_row = i
                break
        if header_row is None:
            raise Exception(f"Header row not found in sheet: {sheet}")
        return pd.read_excel(file, sheet_name=sheet, header=header_row)


    def normalise_columns(df):
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.replace("\u00a0", "", regex=True)
            .str.replace("\n", "", regex=True)
            .str.replace("\r", "", regex=True)
        )
        return df


    def map_columns(df):
        mapping = {
            "Supplier Name": "Supplier_Name",
            "Party Name": "Supplier_Name",
            "Vendor Name": "Supplier_Name",
            "Invoice No": "Invoice_No",
            "Invoice Number": "Invoice_No",
            "Bill No": "Invoice_No",
            "Integrated Tax": "IGST",
            "Central Tax": "CGST",
            "State Tax": "SGST",
        }
        df.rename(columns=mapping, inplace=True)
        return df


    def clean_supplier(x):
        if pd.isna(x):
            return ""
        return (
            str(x).upper()
            .replace("PVT", "")
            .replace("LTD", "")
            .replace("LIMITED", "")
            .replace("LLP", "")
            .replace(".", "")
            .strip()
        )


    def clean_invoice(x):
        if pd.isna(x):
            return ""
        return re.sub(r"[^A-Z0-9]", "", str(x).upper())


    def tax_structure(r):
        if r["IGST"] > 0 and r["CGST"] == 0 and r["SGST"] == 0:
            return "IGST"
        if r["IGST"] == 0 and r["CGST"] > 0 and r["SGST"] > 0:
            return "CGST_SGST"
        return "OTHER"


    # ==============================
    # RUN BUTTON
    # ==============================

    # ==============================
# RUN BUTTON
# ==============================

    if uploaded_file:

        if st.button("Run Reconciliation"):

            progress = st.progress(0)
            status = st.empty()
            start_time = time.time()

            # STEP 1 — Read files
            gstr2b = pd.read_excel(uploaded_file, sheet_name="GSTR_2B")
            books = pd.read_excel(uploaded_file, sheet_name="BOOKS")
            status.text("📂 Files loaded")
            progress.progress(15)

            # STEP 2 — Clean data
            gstr2b = normalise_columns(gstr2b)
            books = normalise_columns(books)

            gstr2b = map_columns(gstr2b)
            books = map_columns(books)
            status.text("🧹 Data cleaned")
            progress.progress(35)

            # STEP 3 — Prepare fields
            for df in [gstr2b, books]:

                df["Invoice_No"] = df.get("Invoice_No", "")
                df["Invoice_No_CLEAN"] = df["Invoice_No"].astype(str).apply(clean_invoice)
                df["Supplier_Name_CLEAN"] = df["Supplier_Name"].apply(clean_supplier)

                for col in ["IGST", "CGST", "SGST"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

                df["RECO_REMARK"] = "NOT MATCHED"
                df["USED"] = False

            status.text("⚙ Preparing reconciliation")
            progress.progress(55)

            # STEP 4 — Matching (dynamic)
            gstr2b["TAX_STRUCTURE"] = gstr2b.apply(tax_structure, axis=1)
            books["TAX_STRUCTURE"] = books.apply(tax_structure, axis=1)

            books_grouped = books[books["Invoice_No_CLEAN"] != ""].groupby("Invoice_No_CLEAN")

            total_groups = len(books_grouped)
            done = 0

            for inv_no, grp in books_grouped:

                done += 1
                progress.progress(55 + int((done/total_groups)*35))
                status.text(f"🔍 Matching {done}/{total_groups} invoices...")

                igst_sum = grp["IGST"].sum()
                cgst_sum = grp["CGST"].sum()
                sgst_sum = grp["SGST"].sum()
                tax_struct = grp.iloc[0]["TAX_STRUCTURE"]

                candidates = gstr2b[
                    (~gstr2b["USED"]) &
                    (gstr2b["Invoice_No_CLEAN"] == inv_no) &
                    (gstr2b["TAX_STRUCTURE"] == tax_struct)
                ]

                for j, g in candidates.iterrows():
                    if (
                        abs(g["IGST"] - igst_sum) <= TOLERANCE and
                        abs(g["CGST"] - cgst_sum) <= TOLERANCE and
                        abs(g["SGST"] - sgst_sum) <= TOLERANCE
                    ):
                        books.loc[grp.index, ["RECO_REMARK", "USED"]] = ["MATCHED", True]
                        gstr2b.loc[j, ["RECO_REMARK", "USED"]] = ["MATCHED", True]
                        break

                # ================= STEP 4B — Tax amount fallback matching =================

            status.text("🔁 Running fallback tax matching...")
            progress.progress(90)

            unmatched_books = books[~books["USED"]]

            for i, b in unmatched_books.iterrows():

                candidates = gstr2b[
                    (~gstr2b["USED"]) &
                    (gstr2b["TAX_STRUCTURE"] == b["TAX_STRUCTURE"]) &
                    (abs(gstr2b["IGST"] - b["IGST"]) <= TOLERANCE) &
                    (abs(gstr2b["CGST"] - b["CGST"]) <= TOLERANCE) &
                    (abs(gstr2b["SGST"] - b["SGST"]) <= TOLERANCE)
                ]

                if len(candidates) >= 1:
                    j = candidates.index[0]
                    books.loc[i, ["RECO_REMARK", "USED"]] = ["MATCHED", True]
                    gstr2b.loc[j, ["RECO_REMARK", "USED"]] = ["MATCHED", True]


            # STEP 5 — Finish
            progress.progress(100)
            status.success("✅ Reconciliation Completed")

            matched = (books["RECO_REMARK"] == "MATCHED").sum()
            total = len(books)

            st.success(f"Matched: {matched}/{total}")
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

            # =============================
            # AUTO SAVE TO HISTORY
            # =============================

            import os, datetime

            os.makedirs("history", exist_ok=True)

            timestamp = datetime.datetime.now().strftime("%d_%b_%Y_%H_%M")
            filename = f"history/GST_Reco_{timestamp}.xlsx"

            with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                gstr2b.to_excel(writer, sheet_name="GSTR_2B", index=False)
                books.to_excel(writer, sheet_name="BOOKS", index=False)

            
  
    