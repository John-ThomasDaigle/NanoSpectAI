#$env:GEMINI_API_KEY="AIzaSyCxyknCDDpt5Eb2LhiZios9qmEshTCHlmI"
import streamlit as st
from fixedapi import generate_inspection_report

# Page Config
st.set_page_config(
    page_title="NanoSpect AI Tool",
    layout="centered"
)


# Header
st.title("NanoSpect AI Inspection Tool")
st.markdown(
    "Upload building inspection documents and generate an AI-powered inspection report."
)

st.divider()


#Document Upload Section
st.header("Inspection Documents")

documents = st.file_uploader(
    "Upload inspection document",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if documents:
    st.success(f"{len(documents)} document(s) uploaded.")

st.divider()


# Building Info
st.header("Building Information")

address = st.text_input(
    "Building Address",
    placeholder="123 Main St, City, State"
)

building_style = st.text_input(
    "Building Style",
    
       placeholder= "e.g. Residential Housing, Dormitory, Commercial, Industrial, Mixed-Use"
        
)

building_photo = st.file_uploader(
    "Upload Building Photo",
    type=["jpg", "jpeg", "png"]
)

if building_photo:
    st.image(building_photo, caption="Uploaded Building Photo", use_column_width=True)

st.divider()


# Generate Section
# Generate Section
st.header("Generate Report")

if st.button("Generate Inspection Report", use_container_width=True):

    if not documents:
        st.error("Please upload a document.")
    elif not address:
        st.error("Please enter the building address.")
    else:
        with st.spinner("Generating report..."):

            # Save first uploaded document temporarily
            temp_doc_path = "temp_input.docx"
            with open(temp_doc_path, "wb") as f:
                f.write(documents[0].read())

            temp_photo_path = None
            if building_photo:
                temp_photo_path = "temp_photo.jpg"
                with open(temp_photo_path, "wb") as f:
                    f.write(building_photo.read())

            final_pdf = generate_inspection_report(
                temp_doc_path,
                address,
                building_style,
                temp_photo_path
            )

            st.session_state["final_pdf"] = final_pdf

        st.success("Report Generated Successfully!")

# Download Section
st.header("Download Report")

if "final_pdf" in st.session_state:

    with open(st.session_state["final_pdf"], "rb") as file:
        st.download_button(
            label="Download Inspection Report",
            data=file,
            file_name="NanoSpectAI_Inspection_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# Download Section 

if st.button("Generate Inspection Report"):

    #with st.spinner("Generating report..."):
    print(generate_inspection_report)
    final_pdf = generate_inspection_report(
    input_docx_path=temp_doc_path,
    building_type=building_style,
    building_name=address,
    inspection_date="N/A",
    building_image_path=temp_photo_path
)

    st.success("Report Generated Successfully!")

    # Store in session state
    st.session_state["final_pdf"] = final_pdf