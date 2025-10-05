import streamlit as st
import requests
import pandas as pd



st.set_page_config(
    page_title="Calculadora de Requisiórios",
    page_icon="⚖️",
    layout="centered"
)

API_URL = "http://127.0.0.1:5001/api/calculate"

st.title("⚖️ Calculadora de Atualização de Requisiórios")
st.write("Faça o upload do arquivo PDF do requisitório para calcular o valor corrigido e o valor líquido final.")

st.divider()

uploaded_file = st.file_uploader(
    "Selecione o arquivo PDF",
    type="pdf"
)

submit_button = st.button("Calcular Valor")


if submit_button:
    if uploaded_file is not None:
        with st.spinner("Analisando o PDF e conectando com a API... Por favor, aguarde."):
            try:
                # Prepara o arquivo para ser enviado para a API
                files = {"pdf_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

                # Chama a nossa API Flask
                response = requests.post(API_URL, files=files)
                response.raise_for_status()

                # Processa a resposta de sucesso
                data = response.json()
                st.success("Cálculo realizado com sucesso!")

                st.subheader("Resultados do Cálculo")

                # Exibe os resultados principais de forma clara
                col1, col2 = st.columns(2)
                # Formata os valores para o padrão brasileiro (R$ 1.234,56)
                valor_bruto_formatado = f"R$ {data['result']['valor_bruto_corrigido']:,.2f}".replace(",", "X").replace(
                    ".", ",").replace("X", ".")
                valor_liquido_formatado = f"R$ {data['result']['valor_liquido_final_ir']:,.2f}".replace(",", "X").replace(
                    ".", ",").replace("X", ".")

                col1.metric("Valor Bruto Corrigido", valor_bruto_formatado)
                col2.metric("Valor Líquido Final (com IR)", valor_liquido_formatado)

                st.divider()

                st.subheader("Dados Extraídos do Documento")

                input_data = data['input_data']

                friendly_names = {
                    "numero_oficio": "Número do Ofício",
                    "nome_beneficiario": "Nome do Beneficiário",
                    "cpf_beneficiario": "CPF do Beneficiário",
                    "valor_bruto": "Valor Bruto (Original)",
                    "data_base_calculo": "Data Base do Cálculo"
                }

                display_data = []
                for key, value in input_data.items():
                    if value is None:
                        continue


                    if key == "valor_bruto":
                        formatted_value = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    elif key == "cpf_beneficiario" and isinstance(value, str) and len(value) == 11:
                        formatted_value = f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
                    else:
                        formatted_value = value

                    display_data.append({
                        "Campo": friendly_names.get(key, key),
                        "Valor": formatted_value
                    })

                if display_data:
                    df = pd.DataFrame(display_data)
                    st.table(df.set_index('Campo'))

            except requests.RequestException as e:
                st.error(f"Erro de conexão com a API: {e}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")
                try:
                    error_data = response.json()
                    st.error(f"Detalhe da API: {error_data.get('error', 'Sem detalhes adicionais.')}")
                except:
                    pass
    else:
        st.warning("Por favor, faça o upload de um arquivo PDF antes de calcular.")