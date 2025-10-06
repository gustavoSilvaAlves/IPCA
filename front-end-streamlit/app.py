import streamlit as st
import requests
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Calculadora de Correção ",
    page_icon="⚖️",
    layout="centered"
)

# --- Configuração da API ---
API_URL = "http://127.0.0.1:5001/api/calculate"

# --- Interface do Usuário (UI) ---
st.title("⚖️ Calculadora de Correção ")
st.write("Faça o upload do arquivo PDF com as informações para calcular o valor corrigido e o valor líquido final com o desconto dos 3% do IR.")

st.divider()

# 1. Inputs do Usuário
uploaded_file = st.file_uploader(
    "Selecione o arquivo PDF",
    type="pdf"
)
recipient_email = st.text_input("Endereço de e-mail para envio do resultado")

# 2. Botão Único para Ação
submit_button = st.button("Calcular e Enviar Resultado por E-mail")

# --- Lógica de Processamento ---
if submit_button:
    if uploaded_file is not None and recipient_email:
        with st.spinner("Analisando o PDF e conectando com a API... Por favor, aguarde."):
            try:
                files = {"pdf_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                form_data = {"recipient_email": recipient_email}

                response = requests.post(API_URL, files=files, data=form_data)

                if response.status_code != 200:
                    error_data = response.json()
                    st.error(f"Erro retornado pela API: {error_data.get('error', 'Erro desconhecido.')}")
                else:
                    data = response.json()
                    st.success("Cálculo realizado com sucesso!")

                    st.subheader("Resultados do Cálculo")
                    col1, col2 = st.columns(2)
                    valor_bruto_formatado = f"R$ {data['result']['valor_bruto_corrigido']:,.2f}".replace(",","X").replace( ".", ",").replace("X", ".")

                    valor_liquido_formatado = f"R$ {data['result']['valor_liquido_final_ir']:,.2f}".replace(",","X").replace(".", ",").replace("X", ".")

                    col1.metric("Valor Bruto Corrigido", valor_bruto_formatado)
                    col2.metric("Valor Líquido Final (com IR)", valor_liquido_formatado)

                    st.divider()
                    st.subheader("Dados Extraídos do Documento")

                    input_data = data['input_data']
                    friendly_names = {
                        "numero_oficio": "Número do Ofício", "nome_beneficiario": "Nome do Beneficiário",
                        "cpf_beneficiario": "CPF do Beneficiário", "valor_bruto": "Valor Bruto (Original)",
                        "data_base_calculo": "Data Base do Cálculo"
                    }

                    # Este loop garante que todos os valores sejam formatados e convertidos para string
                    display_data = []
                    for key, value in input_data.items():
                        if value is None:
                            continue

                        if key == "valor_bruto":
                            formatted_value = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        elif key == "cpf_beneficiario" and isinstance(value, str) and len(value) == 11:
                            formatted_value = f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
                        else:
                            formatted_value = str(value)

                        display_data.append({"Campo": friendly_names.get(key, key), "Valor": formatted_value})

                    if display_data:
                        df = pd.DataFrame(display_data)
                        st.table(df.set_index('Campo'))

            except requests.RequestException as e:
                st.error(f"Erro de conexão com a API. O servidor backend está rodando? Detalhe: {e}")

    else:
        st.warning("Por favor, faça o upload de um arquivo PDF e preencha o campo de e-mail antes de calcular.")