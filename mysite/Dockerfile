# Use a imagem oficial do Python.
FROM python:3.11-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o código do projeto para o diretório de trabalho
COPY . .

# Expõe a porta em que o gunicorn vai rodar
EXPOSE 8080

# Comando para iniciar a aplicação
CMD exec gunicorn --bind :8080 --workers 2 --threads 8 --timeout 0 base.wsgi:application
