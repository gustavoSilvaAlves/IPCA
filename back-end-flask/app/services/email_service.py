import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

def send_calculation_email(recipient_email: str, input_data: dict, calculation_results: dict):
    """
    Monta e envia um e-mail formatado com os resultados do cálculo.
    """
    # Carrega as credenciais das variáveis de ambiente
    sender_email = os.getenv("MAIL_USERNAME")
    password = os.getenv("MAIL_PASSWORD")
    smtp_server = os.getenv("MAIL_SERVER")
    port = int(os.getenv("MAIL_PORT", 465))

    if not all([sender_email, password, smtp_server]):
        raise ValueError("Credenciais de e-mail não configuradas nas variáveis de ambiente.")

    # Cria a mensagem do e-mail
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Ofício Nº {input_data.get('numero_oficio', 'N/A')}"
    message["From"] = sender_email
    message["To"] = recipient_email

    valor_bruto_corrigido_fmt = f"R$ {calculation_results.get('valor_bruto_corrigido', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    valor_liquido_final_fmt = f"R$ {calculation_results.get('valor_liquido_final_ir', 0):,.2f}".replace(",","X").replace(".", ",").replace("X", ".")
    valor_bruto_original_fmt = f"R$ {input_data.get('valor_bruto', 0):,.2f}".replace(",", "X").replace(".",",").replace("X",".")

    cpf = input_data.get('cpf_beneficiario')
    cpf_fmt = cpf
    if cpf and isinstance(cpf, str) and len(cpf) == 11:
        cpf_fmt = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    # Cria o corpo do e-mail em HTML para uma formatação melhor
    html_body = f"""
        <html>
      <body>
        <h2>Resultado do Cálculo de Correção </h2>
        <p>Olá,</p>
        <p>Segue o resultado do cálculo solicitado para o Ofício Nº {input_data.get('numero_oficio', 'N/A')}.</p>

        <h3>Resumo do Cálculo</h3>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
          <tr style="background-color:#f2f2f2;">
            <th style="text-align: left;">Descrição</th>
            <th style="text-align: right;">Valor</th>
          </tr>
          <tr>
            <td>Valor Bruto Original</td>
            <td style="text-align: right;">{valor_bruto_original_fmt}</td>
          </tr>
          <tr>
            <td>Data Base do Cálculo</td>
            <td style="text-align: right;">{input_data.get('data_base_calculo')}</td>
          </tr>
          <tr>
            <td>Corrigido até (Último IPCA)</td>
            <td style="text-align: right;">{calculation_results.get('ultimo_mes_corrigido')}</td>
          </tr>
          <tr>
            <td>Valor Bruto Corrigido</td>
            <td style="text-align: right;">{valor_bruto_corrigido_fmt}</td>
          </tr>
          <tr style="font-weight: bold; background-color: #e8f5e9;">
            <td>Valor Líquido Final (com 3% IR)</td>
            <td style="text-align: right;">{valor_liquido_final_fmt}</td>
          </tr>
        </table>
        <br>
         <h3>Dados Extraídos do Documento</h3>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color:#f2f2f2;">
                <th style="text-align: left;">Campo</th>
                <th style="text-align: left;">Valor</th>
            </tr>
            <tr>
                <td>Número do Ofício</td>
                <td>{input_data.get('numero_oficio', 'N/A')}</td>
            </tr>
            <tr>
                <td>Nome do Beneficiário</td>
                <td>{input_data.get('nome_beneficiario', 'N/A')}</td>
            </tr>
            <tr>
                <td>CPF do Beneficiário</td>
                <td>{cpf_fmt}</td>
            </tr>
        </table>
        <br>
        <p>Atenciosamente,<br>Calculadora de Requisiórios</p>
      </body>
    </html>
        """

    message.attach(MIMEText(html_body, "html"))

    # Envia o e-mail
    try:
        context = ssl.create_default_context()

        logging.info(f"Conectando ao servidor SMTP para enviar e-mail para {recipient_email}...")

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        logging.info("E-mail enviado com sucesso!")

    except Exception as e:
        logging.error(f"Falha ao enviar e-mail: {repr(e)}")
        raise
