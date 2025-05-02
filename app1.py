import streamlit as st
import os
import time
import glob
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

st.markdown("""
    <style>

        body, .stApp {
            background-color: #7D007D;
            color: #8B008B !important; 
        }

        .st-cb, .st-af, .st-ag, .stMarkdown, .stText, .stWrite, .stRadio>div>label, 
        .stSelectbox>div>label, .stCheckbox>div>label, .stButton>button, 
        .css-1aumxhk, .css-10trblm, .stSidebar, .stSidebar .css-1aumxhk, 
        .stSidebar .stMarkdown, .stSidebar .stText, .stSidebar .stWrite {
            color: #8B008B !important;
        }

        .css-1aumxhk, .css-10trblm, .stHeader, .stSubheader, .stTitle {
            color: white !important;
        }

        /* Botones */
        .stButton>button, .css-1v0mbdj button {
            background-color: #0a3d0a;
            color: white;
            border: 1px solid white;
        }

        /* Enlaces */
        a {
            color: #0a3d0a !important;
        }

        /* Personalización de la barra lateral */
        .css-1d391kg {
            background-color: #d1f5d3 !important;
            color: #0a3d0a !important;
        }

        /* Ajustes para las entradas de texto, checkboxes y demás campos */
        .st-cb label, .st-radio label, .stSelectbox>div>label, .stCheckbox>div>label {
            color: #0a3d0a !important;
        }

        /* Específicos para "Cargar Imagen" y "Usar Cámara" */
        .stFileUploader>label, .stButton>button, .stCheckbox>div>label {
            color: #0a3d0a !important;  /* En verde */
        }

        /* Asegurarse de que el texto junto al checkbox de "Usar cámara" y "Cargar imagen" también esté en verde */
        .stCheckbox>div>label, .stFileUploader>label {
            color: #0a3d0a !important;
        }
    </style>
""", unsafe_allow_html=True)

text = " "

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

st.title("Reconocimiento Óptico de Caracteres")
st.subheader("Elige la fuente de la imagen, esta puede venir de la cámara o cargando un archivo")

cam_ = st.checkbox("Usar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Toma una Foto")
else:
    img_file_buffer = None

with st.sidebar:
    st.subheader("Procesamiento para Cámara")
    filtro = st.radio("Filtro para imagen con cámara", ('Sí', 'No'))

bg_image = st.file_uploader("Cargar Imagen:", type=["png", "jpg"])
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='Imagen cargada.', use_container_width=True)

    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())

    st.success(f"Imagen guardada como {uploaded_file.name}")
    img_cv = cv2.imread(f'{uploaded_file.name}')
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

st.write(text)

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.write(text)

with st.sidebar:
    st.subheader("Parámetros de traducción")

    try:
        os.mkdir("temp")
    except:
        pass

    translator = Translator()

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
    )
    if in_lang == "Ingles":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "koreano":
        input_language = "ko"
    elif in_lang == "Mandarin":
        input_language = "zh-cn"
    elif in_lang == "Japones":
        input_language = "ja"

    out_lang = st.selectbox(
        "Seleccione el lenguaje de salida",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
    )
    if out_lang == "Ingles":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "koreano":
        output_language = "ko"
    elif out_lang == "Mandarin":
        output_language = "zh-cn"
    elif out_lang == "Japones":
        output_language = "ja"

    english_accent = st.selectbox(
        "Seleccione el acento",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )

    if english_accent == "Default":
        tld = "com"
    elif english_accent == "India":
        tld = "co.in"
    elif english_accent == "United Kingdom":
        tld = "co.uk"
    elif english_accent == "United States":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Ireland":
        tld = "ie"
    elif english_accent == "South Africa":
        tld = "co.za"

    display_output_text = st.checkbox("Mostrar texto")

    if st.button("convert"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("## Texto de salida:")
            st.write(output_text)
    


    


