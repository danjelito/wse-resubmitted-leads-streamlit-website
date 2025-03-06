import streamlit as st
import pandas as pd
from processor import (
    generate_report,
    load_file,
    create_download_link,
    generate_download_dict,
)
import time

st.title("Gross Leads vs. Leads and Pipeline - Merged v1.0")
st.write("**Identify leads in Gross Leads that are missing from Leads and Pipeline.**")
st.write("Developed by Devan. Please report any errors.")

with st.sidebar:
    st.write("## 📌 Instructions")

    st.write("### 🌍 English")
    english_instructions = [
        "1. Go to **Erwin > CRM > Configuration > Gross Leads**.",
        "2. Add a filter: **'Created on is after'** (set to 30 days prior to today).",
        "3. Export the leads data using the export template **'Devan - Resubmitted Leads'**.",
        "4. Upload the exported file to this website.",
        "5. Go to **Erwin > CRM > Pipeline > Leads and Pipeline**.",
        "6. Add a filter: **'Created on is after'** (set to 30 days prior to today).",
        "7. Export the leads data using the export template **'Devan - Resubmitted Leads'**.",
        "8. Upload the exported file to this website.",
        "9. Click **'Generate Report'** to process the data and get the results.",
    ]

    for instruction in english_instructions:
        st.write(instruction)

    st.write("---")  # Adds a separator for better readability

    st.write("### 🇮🇩 Indonesia")
    indonesian_instructions = [
        "1. Buka **Erwin > CRM > Configuration > Gross Leads**.",
        "2. Tambahkan filter: **'Created on is after'** (atur ke 30 hari sebelum hari ini).",
        "3. Ekspor data leads menggunakan template ekspor **'Devan - Resubmitted Leads'**.",
        "4. Unggah file yang telah diekspor ke situs web ini.",
        "5. Buka **Erwin > CRM > Pipeline > Leads and Pipeline**.",
        "6. Tambahkan filter: **'Created on is after'** (atur ke 30 hari sebelum hari ini).",
        "7. Ekspor data leads menggunakan template ekspor **'Devan - Resubmitted Leads'**.",
        "8. Unggah file yang telah diekspor ke situs web ini.",
        "9. Klik **'Generate Report'** untuk memproses data dan mendapatkan hasilnya.",
    ]

    for instruction in indonesian_instructions:
        st.write(instruction)


st.write("---")
st.header("Upload Your Files")

# File uploader
uploaded_gross = st.file_uploader(
    "File from Gross Leads", type=["csv", "xlsx", "xls"], accept_multiple_files=False
)
uploaded_leads_pipeline = st.file_uploader(
    "File from Leads and Pipeline",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=False,
)


# File processing
if uploaded_gross and uploaded_leads_pipeline:
    st.success("Files uploaded successfully!", icon="📂")

    if st.button("Process Files"):
        with st.spinner("Processing files..."):
            time.sleep(3)  # Simulated processing delay

            # Load and process files
            df_gross = load_file(uploaded_gross)
            df_leads_pipeline = load_file(uploaded_leads_pipeline)

            result = generate_report(df_gross, df_leads_pipeline)
            download_dict = generate_download_dict(result)

            # ---- DOWNLOAD SECTION ----
            st.header("Download the Result")
            download_buffer = create_download_link(download_dict)

            st.success("Your file is ready!", icon="✅")
            st.download_button(
                label="Click to download",
                data=download_buffer,
                file_name="Result.xlsx",
                mime="application/vnd.ms-excel",
            )
