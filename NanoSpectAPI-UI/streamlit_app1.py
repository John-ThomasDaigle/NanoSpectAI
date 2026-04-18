import os
import streamlit as st
import warnings
warnings.filterwarnings("ignore", message=".*use_column_width.*")
from nanospectai import generate_inspection_report

# Page Config
st.set_page_config(
    page_title="NanoSpect AI Tool",
    layout="centered"
)

# Header
st.title("NanoSpect AI Inspection Report Generator")
st.markdown("Upload building inspection documents and generate an AI-powered inspection report.")

st.divider()

# API Key Section
st.header("API Configuration")
api_key = st.text_input(
    "Google Gemini 2.5 Pro API Key",
    type="password",
    placeholder="Paste your Gemini API key here",
    help="Generate an API Key to Use NanoSpect AI. Your key is never stored, it is only ever used for the current session."
)
if api_key:
    st.success("API key received.")

st.link_button("Get API Key Here", "https://aistudio.google.com/app/api-keys?project=gen-lang-client-0440836714")

st.divider()

# Document Upload Section
st.header("Inspection Documents")

documents = st.file_uploader(
    "Upload inspection document",
    type=["docx"],
    accept_multiple_files=True,
    key="doc_upload"
)

if documents:
    st.success(f"{len(documents)} document(s) uploaded.")

st.divider()

# Company Branding
st.header("Company Branding")
logo_upload = st.file_uploader(
    "Upload Company Logo",
    type=["jpg", "jpeg", "png"],
    key="logo_upload"
)

if logo_upload:
    st.image(logo_upload, width=200)

st.divider()

# Building Info
st.header("Building Information")
address = st.text_input(
    "Building Address",
    placeholder="123 Main St, City, State"
)
building_style = st.selectbox(
    "Building Style",
    options=[
        "Residential Housing",
        "Dormitory",
        "Commercial",
        "Industrial",
        "Mixed-Use"
    ]
)
inspection_date = st.date_input("Inspection Date")
building_photo = st.file_uploader(
    "Upload Building Photo",
    type=["jpg", "jpeg", "png"],
    key="building_photo"
)
if building_photo:
    st.image(building_photo, caption="Uploaded Building Photo", width=700)

st.divider()

# Inspector Information
st.header("Inspector Information")
num_inspectors = st.number_input(
    "Number of Inspectors",
    min_value=1,
    max_value=5,
    value=1
)

inspectors = []
for i in range(num_inspectors):
    st.subheader(f"Inspector {i + 1}")
    photo = st.file_uploader(
        f"Upload Photo for Inspector {i + 1}",
        type=["jpg", "jpeg", "png"],
        key=f"photo_{i}"
    )
    name = st.text_input(f"Inspector {i + 1} Name", key=f"name_{i}")
    email = st.text_input(f"Inspector {i + 1} Email", key=f"email_{i}")
    inspectors.append({"photo": photo, "name": name, "email": email})

st.divider()

# Generate Section
st.header("Generate Report")

if st.button("Generate Inspection Report", width=700):
    if not api_key:
        st.error("Please enter your Gemini API key.")
    elif not documents:
        st.error("Please upload a document.")
    elif not address:
        st.error("Please enter the building address.")
    else:
        # Set the key as an environment variable so nanospectai.py picks it up
        os.environ["GEMINI_API_KEY"] = api_key

        with st.spinner("Generating report, please wait..."):

            # Save input document
            temp_doc_path = "temp_input.docx"
            with open(temp_doc_path, "wb") as f:
                f.write(documents[0].read())

            # Save building photo if provided
            temp_photo_path = None
            if building_photo:
                temp_photo_path = "temp_building_photo.jpg"
                with open(temp_photo_path, "wb") as f:
                    f.write(building_photo.read())

            # Save logo if provided
            logo_path = None
            if logo_upload:
                logo_path = "temp_logo.jpg"
                with open(logo_path, "wb") as f:
                    f.write(logo_upload.read())

            # Save inspector photos if provided
            inspector_data = []
            for i, inspector in enumerate(inspectors):
                photo_path = None
                if inspector["photo"]:
                    photo_path = f"temp_inspector_{i}.jpg"
                    with open(photo_path, "wb") as f:
                        f.write(inspector["photo"].read())
                inspector_data.append({
                    "name": inspector["name"],
                    "email": inspector["email"],
                    "image": photo_path
                })

            final_pdf = generate_inspection_report(
                input_docx_path=temp_doc_path,
                building_type=building_style,
                building_name=address,
                inspection_date=inspection_date.strftime("%m/%d/%Y"),
                building_image_path= temp_photo_path,
                inspectors=inspector_data,
                logo_path=logo_path
            )

            st.session_state["final_pdf"] = final_pdf

        st.success("Report Generated Successfully!")

st.divider()

# Download Section
st.header("Download Report")
if "final_pdf" in st.session_state:
    with open(st.session_state["final_pdf"], "rb") as f:
        st.download_button(
            label="Download Inspection Report",
            data=f,
            file_name="NanoSpectAI_Inspection_Report.pdf",
            mime="application/pdf",
            width=700
        )