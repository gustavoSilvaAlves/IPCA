# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código da aplicação
COPY . .

# Expõe a porta que a aplicação vai usar
EXPOSE 5001

# Comando para executar a aplicação quando o contêiner iniciar
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5001", "main:app"]