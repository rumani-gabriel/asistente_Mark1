# Chat Inteligente con PDFs

Bienvenido a **Mark1**, una aplicación creada con Streamlit que te permite cargar documentos PDF y hacer preguntas basadas en el contenido de esos documentos.

## Características

- **Carga de PDFs**: Sube múltiples archivos PDF a la aplicación.
- **Procesamiento de PDFs**: Extrae y analiza el texto de los PDFs cargados.
- **Interfaz amigable**: Interfaz intuitiva y fácil de usar con un diseño atractivo.
- **Respuestas inteligentes**: Haz preguntas sobre el contenido de los PDFs y obtén respuestas detalladas.

## Tecnologías Utilizadas

- **Streamlit**: Para construir la interfaz de usuario.
- **PyPDF2**: Para extraer texto de los archivos PDF.
- **Langchain**: Para dividir el texto en chunks y procesar el lenguaje natural.
- **Google Generative AI**: Para generar embeddings y respuestas inteligentes.
- **FAISS**: Para el almacenamiento y búsqueda eficiente de vectores.
- **dotenv**: Para manejar variables de entorno.

## Requisitos

- Python 3.7 o superior
- Claves de API para Google Generative AI

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/rumani-gabriel/asistente_Mark1.git
    cd asistente_Mark1.git
    ```

2. Crea un entorno virtual y activa el entorno (opcional pero recomendado):
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura las claves de API:
    - Crea un archivo `.env` en el directorio raíz del proyecto.
    - Añade tu clave de API de Google Generative AI al archivo `.env`:
        ```env
        GOOGLE_API_KEY=tu_clave_de_api
        ```

## Uso

1. Ejecuta la aplicación de Streamlit:
    ```bash
    streamlit run app.py
    ```

2. Abre tu navegador web y ve a `http://localhost:8501`.

3. Sigue estos pasos en la aplicación:
    - **Paso 1**: Sube tus archivos PDF usando el cargador de archivos en la barra lateral.
    - **Paso 2**: Haz clic en "Procesar PDFs" para extraer y analizar el texto.
    - **Paso 3**: Haz preguntas sobre el contenido de los PDFs en el campo de entrada de texto.

## Ejemplo de Uso

1. **Carga de PDFs**: Sube uno o más archivos PDF a la aplicación.
    

2. **Procesamiento de PDFs**: Procesa los archivos PDF cargados.
    

3. **Haz preguntas**: Haz preguntas sobre el contenido de los PDFs.
    

## Estilo de la Aplicación

La aplicación utiliza un estilo oscuro con un encabezado que tiene un gradiente de color de violeta a azul. Este diseño moderno y atractivo mejora la experiencia del usuario.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras un problema o tienes una sugerencia para una nueva funcionalidad, por favor abre un issue o envía un pull request.

---

¡Gracias por usar **Mark1**! Esperamos que esta herramienta te sea útil y te permita interactuar de manera eficiente con tus documentos PDF.
