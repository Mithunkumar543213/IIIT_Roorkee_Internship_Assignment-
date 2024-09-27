import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2

# Cache the EasyOCR reader to avoid re-initializing it for every request
@st.cache_resource
def load_reader():
    return easyocr.Reader(["en", "hi"], gpu=False)

def extract_text_from_image(image):
    try:
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        reader = load_reader()
        result = reader.readtext(img_bgr)
        return " ".join([data[1] for data in result])
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return ""

def index():
    st.title("OCR Application (English and Hindi Support)")
    st.write("Upload an image and the extracted text in English and Hindi will appear below.")

    # Initialize session state variables
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""
    if 'file_name' not in st.session_state:
        st.session_state.file_name = None
    if 'file_size' not in st.session_state:
        st.session_state.file_size = None

    image_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])

    if image_file is not None:
        try:
            file_name = image_file.name
            image_file.seek(0, 2)  # Move to the end of the file to get its size
            file_size = image_file.tell()

            if st.session_state.file_name != file_name or st.session_state.file_size != file_size:
                st.session_state.extracted_text = ""  # Clear extracted text for new image
                st.session_state.file_name = file_name
                st.session_state.file_size = file_size  

                # Reset file pointer and process the image
                image_file.seek(0) 
                pil_image = Image.open(image_file)
                st.image(pil_image, caption="Uploaded Image", use_column_width=True)

                st.write("Processing the image, please wait...")
                st.session_state.extracted_text = extract_text_from_image(pil_image)

            # Display the extracted text
            if st.session_state.extracted_text:
                st.subheader("Extracted Text:")
                st.write(st.session_state.extracted_text)

            # Search functionality in extracted text
            search_term = st.text_input("Search in extracted text:")
            if search_term:
                if search_term in st.session_state.extracted_text:
                    st.success(f"Found: '{search_term}' in the extracted text.")
                else:
                    st.error(f"'{search_term}' not found in the extracted text.")
        except Exception as e:
            st.error(f"An error occurred while processing the image: {e}")
    else:
        st.write("Please upload an image file.")

if __name__ == "__main__":
    index()
