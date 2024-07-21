import streamlit as st 
import google.generativeai as genai 
import google.ai.generativelanguage as glm 
from dotenv import load_dotenv
from PIL import Image
import os 
import io 

st.set_page_config(page_title="ByteBrain - Chat with PDF", page_icon="✨")

load_dotenv()

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr=imgByteArr.getvalue()
    return imgByteArr

API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

st.image("./Google-Gemini-AI-Logo.png", width=200)
st.write("Nama Kelompok:")
st.write("- Username1")
st.write("- Username2")
st.write("- Username3")
st.write("- Username4")

gemini_pro, gemini_vision = st.tabs(["Chat with Text", "Chat with Image"])

def main():
    with gemini_pro:
        st.header("I'm your AI Assistant, ask me anything ")
        st.write("")

        prompt = st.text_input("Tanyakan sesuatu disini!")
        model = genai.GenerativeModel("gemini-pro")

        if st.button("Kirim",use_container_width=True):
            response = model.generate_content(prompt)

            st.write("")
            st.header(":blue[Response]")
            st.write("")

            st.markdown(response.text)

    with gemini_vision:
        st.header("I'm your AI Assistant, ask me about your image")
        st.write("")

        image_prompt = st.text_input("Tanyakan sesuatu disini tentang gambar anda!")
        uploaded_file = st.file_uploader("Choose Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)

            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)
            
        if st.button("kirim", use_container_width=True):
            model = genai.GenerativeModel("gemini-1.5-flash")

            if uploaded_file is not None:
                if image_prompt != "":
                    image = Image.open(uploaded_file)

                    response = model.generate_content(
                        glm.Content(
                            parts = [
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()

                    st.write("")
                    st.write(":blue[Response]")
                    st.write("")

                    st.markdown(response.text)

                else:
                    st.write("")
                    st.header(":red[Please Provide a prompt]")

            else:
                st.write("")
                st.header(":red[Please Provide an image]")

if __name__ == "__main__":
    main()
