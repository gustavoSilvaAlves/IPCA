# ⚖️ Calculadora de Correção
![Python](https://img.shields.io/badge/Python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green.svg) ![LangChain](https://img.shields.io/badge/LangChain-blue?logo=langchain) ![LangGraph](https://img.shields.io/badge/LangGraph-orange?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiB2aWV3Qm94PSIwIDAgMjQgMjQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik00IDdoMnYxMEg0em0zIDBoMnYxMEg3em0zIDBoMnYxMEgxMHptMyAwaDJ2MTBIMTN6bTggMi42OThsLTIuNzk4IDIuNzk3bC0xLjQxNC0xLjQxNEwxOC4xNzIgMTBMMTYuNTggOC40MTNsMS40MTQtMS40MTRaTTIgN2gxNHYxMEgyek0xIDV2MTRoMTZWNWEyIDIgMCAwIDAtMi0ySDNBMiAyIDAgMCAwIDEgNSIvPjwvc3ZnPg==) ![Keycloak](https://img.shields.io/badge/Keycloak-2F81B7.svg?logo=keycloak) ![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker) ![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)

Este projeto é uma aplicação web completa projetada para automatizar o processo de cálculo de atualização de valores de requisitórios judiciais. A aplicação extrai dados de documentos PDF, aplica a correção monetária com base no índice IPCA, aplica o desconto dos 3% do imposto de renda e envia um relatório detalhado por e-mail.

## 🎯 Objetivo do Projeto

O objetivo principal é fornecer uma ferramenta robusta e de fácil utilização para:
1.  Fazer o upload de um documento de requisitório em formato PDF.
2.  Extrair automaticamente os dados-chave do documento, como valor bruto original, data base do cálculo e informações do beneficiário.
3.  Calcular o valor bruto corrigido, aplicando o índice IPCA mensalmente a partir da data base.
4.  Calcular o valor líquido final, com o desconto de 3% de Imposto de Renda.
5.  Enviar um e-mail formatado com o resumo completo do cálculo para um destinatário especificado.

## 🛠️ Tecnologias Utilizadas

O projeto segue uma arquitetura moderna com serviços desacoplados (monorepo).

**Backend (`back-end-flask`):**
* **Framework:** Python 3.11+ com Flask
* **Validação de Dados:** Pydantic
* **Extração de PDF:** `pypdf`
* **Comunicação HTTP (Assíncrona):** `httpx`
* **Envio de E-mail:** `smtplib` (biblioteca padrão do Python)
* **Servidor de Produção (WSGI):** `Waitress`
* **Variáveis de Ambiente:** `python-dotenv`

**Frontend (`front-end-streamlit`):**
* **Framework:** Streamlit
* **Comunicação HTTP:** `requests`
* **Visualização de Dados:** Pandas

## 🏗️ Arquitetura

A aplicação é dividida em dois componentes independentes que se comunicam via API REST:

1.  **Backend (API Flask):** Um serviço "headless" responsável por toda a lógica de negócio: receber o PDF, orquestrar os serviços de extração e cálculo, e enviar o e-mail. Ele não possui interface gráfica.
2.  **Frontend (Streamlit):** Uma interface de usuário web, simples e interativa, onde o usuário final faz o upload do arquivo, insere o e-mail e visualiza o resultado.

## 🚀 Começando

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

* Python 3.11 ou superior
* Git

### Instalação

O projeto é dividido em duas partes, e cada uma precisa ter seu próprio ambiente virtual configurado.

1.  **Clone o repositório:**
    ```bash
    git clone <URL-do-seu-repositorio-github>
    cd nome-do-repositorio
    ```

2.  **Configure o Backend:**
    ```bash
    # Navegue até a pasta do backend
    cd back-end-flask

    # Crie e ative o ambiente virtual
    python -m venv venv
    .\venv\Scripts\Activate.ps1

    # Instale as dependências
    pip install -r requirements.txt
    ```

3.  **Configure o Frontend:**
    ```bash
    # A partir da raiz do projeto, navegue até a pasta do frontend
    cd front-end-streamlit

    # Crie e ative o ambiente virtual
    python -m venv venv
    .\venv\Scripts\Activate.ps1

    # Instale as dependências
    pip install -r requirements.txt
    ```

### Configuração (Variáveis de Ambiente)

Ambos os serviços precisam de um arquivo `.env` para suas configurações.

1.  **Backend:**
    * Na pasta `back-end-flask`, renomeie `env.example` para `.env`.
    * Preencha todas as variáveis, especialmente `SECRET_KEY` e as credenciais de e-mail (`MAIL_*`).

    <details>
    <summary><strong>Clique aqui para ver o passo a passo de como gerar a Senha de App (MAIL_PASSWORD) para o Gmail</strong></summary>

    1.  **Pré-requisito:** Certifique-se de que a **Verificação em Duas Etapas** esteja ativada na sua Conta Google. Você pode ativá-la na aba "Segurança" da sua conta.
    2.  Acesse a página de **[Senhas de app](https://myaccount.google.com/apppasswords)** da sua Conta Google. (Pode ser necessário fazer login novamente).
    3.  Na tela "Senhas de app", em "Selecionar app", escolha a opção **"Outro (*nome personalizado*)**".
    4.  Digite um nome para a sua senha, como `API Flask Calculadora`, e clique em **GERAR**.
    5.  O Google irá exibir uma caixa amarela com a sua senha de **16 letras**, sem espaços (ex: `ilqrginkqekwmoyf`).
    6.  **Copie esta senha de 16 letras**. É ela que você deve colar no seu arquivo `.env` na variável `MAIL_PASSWORD`.
    7.  **Atenção:** Guarde esta senha, pois o Google só a exibe uma vez. Após fechar a janela, você não poderá vê-la novamente e terá que gerar uma nova.

    </details>

2.  **Frontend:**
    * Na pasta `front-end-streamlit`, renomeie `env.example` para `.env`.
    * Verifique se a `API_URL` está apontando para o endereço correto do seu backend.

## ▶️ Executando a Aplicação

Você precisará de **dois terminais** abertos para executar a aplicação completa.

**Terminal 1: Iniciar o Backend**
```bash
# Navegue até a pasta do backend
cd back-end-flask

# Ative o ambiente virtual
.\venv\Scripts\Activate.ps1

# Inicie o servidor de produção Waitress
waitress-serve --host=127.0.0.1 --port=5001 main:app
```

**Terminal 2: Iniciar o Frontend**
```bash
# Navegue até a pasta do frontend
cd front-end-streamlit

# Ative o ambiente virtual
.\venv\Scripts\Activate.ps1

# Inicie a aplicação Streamlit
streamlit run app.py
```
Após executar o último comando, o Streamlit abrirá uma aba no seu navegador com a interface da aplicação, pronta para ser usada.

## ✅ Testando a Solução

O projeto inclui scripts para testes isolados e de performance.

* **Teste do Parser de PDF:**
    Para testar apenas a extração de dados do PDF, execute (na pasta `back-end-flask`):
    ```bash
    python -m app.services.pdf_parser
    ```

* **Teste da Calculadora de Valores:**
    Para testar apenas a lógica de cálculo, execute (na pasta `back-end-flask`):
    ```bash
    python -m app.services.value_calculator
    ```

* **Teste de Carga da API:**
    Para simular múltiplos acessos concorrentes à API, execute (na pasta `back-end-flask`):
    ```bash
    python -m tests.load_test

    ```

