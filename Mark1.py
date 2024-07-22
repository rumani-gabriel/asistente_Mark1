import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Carga las variables de entorno y configura la API de Google
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función para extraer texto de los PDFs de forma paralela
@st.cache_resource
def get_pdf_text(pdf_docs):
    text = ""
    total_pages = sum(len(PdfReader(pdf).pages) for pdf in pdf_docs)
    progress_bar = st.progress(0)
    pages_processed = 0
    
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() + f"\n--- Página {pages_processed + 1} del documento {pdf.name} ---\n"
            pages_processed += 1
            progress_bar.progress(pages_processed / total_pages)
    
    progress_bar.empty()
    return text

# Divide el texto en chunks más pequeños
@st.cache_resource
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

# Crea y guarda el almacén de vectores
@st.cache_resource
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Configura la cadena de conversación
def get_conversational_chain():
    prompt_template = """
    Basándote en el contexto proporcionado y tu conocimiento general, responde la pregunta de manera detallada y expresiva. 
    Asegúrate de incluir todos los detalles relevantes del contexto y complementa con tu conocimiento si es necesario.
    Si la respuesta no está en el contexto, indica que no está disponible pero ofrece información relacionada si es posible.
    Al final de tu respuesta, menciona específicamente en qué documento(s) y página(s) se encuentra la información utilizada.

    Contexto:
    {context}

    Pregunta: {question}

    Respuesta detallada:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

# Procesa la entrada del usuario y genera una respuesta
def user_input(user_question):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)

        chain = get_conversational_chain()
        
        response = chain.invoke(
            {"input_documents": docs, "question": user_question}
        )

        st.write("Respuesta:", response["output_text"])
    except RuntimeError as e:
        st.error("Error: No se ha encontrado el índice FAISS. Por favor, carga y procesa un PDF primero.")

# Función principal que configura la interfaz de Streamlit
def main():
    st.set_page_config(page_title="Chat PDF", layout="wide")
    
    # Estilo personalizado
    st.markdown(
        """
        <style>
        body {
            background-color: #1e1e1e;
            color: #e8e8e8;
        }
        .css-1d391kg {
            background-color: #1e1e1e;
            color: #e8e8e8;
        }
        .css-1offfwp {
            background-color: #1e1e1e;
            color: #e8e8e8;
        }
        .stButton button {
            background-color: #3b3b3b;
            color: #e8e8e8;
            border-radius: 5px;
        }
        .stTextInput input {
            background-color: #3b3b3b;
            color: #e8e8e8;
        }
        .stFileUploader label {
            background-color: #3b3b3b;
            color: #e8e8e8;
        }
        .stTextInput div {
            background-color: #3b3b3b;
            color: #e8e8e8;
        }
        .css-1n543e5 {
            background-color: #1e1e1e;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <h1 style='text-align: center; color: #D5D3D6;'>Hola, Soy Mark1, asistente inteligente para recopilar datos y conocimeinto </h1>
        <h3 style='text-align: center; color: #888888;'>¿En qué puedo ayudarte?</h3>
        """,
        unsafe_allow_html=True
    )

    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False

    # Configuración de la barra lateral
    with st.sidebar:
        st.title("Menú:")
        pdf_docs = st.file_uploader("Paso 1: Sube tus archivos PDF", accept_multiple_files=True)
        if st.button("Paso 2: Procesar PDFs"):
            if pdf_docs:
                with st.spinner("Procesando PDFs... Por favor, espera."):
                    st.text("Extrayendo texto de los PDFs...")
                    raw_text = get_pdf_text(pdf_docs)
                    st.text("Dividiendo el texto en chunks...")
                    text_chunks = get_text_chunks(raw_text)
                    st.text("Creando el índice de vectores...")
                    get_vector_store(text_chunks)
                    st.session_state.pdf_processed = True
                    st.success("¡PDFs procesados con éxito! Ahora puedes hacer preguntas.")
            else:
                st.warning("Por favor, sube al menos un archivo PDF antes de procesar.")

    # Instrucciones para el usuario
    if not st.session_state.pdf_processed:
        st.info("Para comenzar, sigue estos pasos:")
        st.markdown("1. Sube uno o más archivos PDF en el menú lateral.")
        st.markdown("2. Haz clic en 'Procesar PDFs' y espera a que se complete el procesamiento.")
        st.markdown("3. Una vez procesados los PDFs, podrás hacer preguntas sobre su contenido.")
    else:
        st.success("PDFs procesados. ¡Listo para responder preguntas!")

    # Campo de entrada para las preguntas del usuario
    user_question = st.text_input("Paso 3: Haz una pregunta sobre los PDFs cargados:")

    if user_question:
        if st.session_state.pdf_processed:
            user_input(user_question)
        else:
            st.warning("Por favor, carga y procesa al menos un PDF antes de hacer preguntas.")

if __name__ == "__main__":
    main()
