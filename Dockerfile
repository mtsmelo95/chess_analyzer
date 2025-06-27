# Usa uma imagem Python oficial e otimizada ('slim') como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /code

# Define variáveis de ambiente para otimizar a execução em containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia todo o código da API para o diretório de trabalho
COPY . .

# IMPORTANTE: Dá permissão de execução para o binário do Stockfish
RUN chmod +x ./stockfish

# Expõe a porta em que a API vai rodar. Usaremos 8000 como padrão para a API.
EXPOSE 8000

# O comando para iniciar o servidor Uvicorn.
# Ele vai rodar o objeto 'app' do arquivo 'main.py' dentro da pasta 'app'.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]