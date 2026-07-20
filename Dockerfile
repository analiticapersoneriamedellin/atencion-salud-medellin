FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Spaces con Docker corre el contenedor como usuario sin
# privilegios (UID 1000) por defecto -- nos aseguramos de que los archivos
# sean legibles/ejecutables para ese usuario.
RUN chmod -R 777 /app

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
