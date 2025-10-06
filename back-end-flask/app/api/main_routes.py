from flask import Blueprint, request, jsonify
import tempfile
import os
import logging
from app.services.pdf_parser import extract_data_from_pdf
from app.services.value_calculator import ValueCalculator
from app.services.email_service import send_calculation_email

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Pong!"})


@api_bp.route('/calculate', methods=['POST'])
async def calculate():
    logging.info(f"Recebida nova requisição para /api/calculate.")

    # 1. Validação dos dados de entrada
    if 'pdf_file' not in request.files:
        logging.warning("Requisição recebida sem 'pdf_file'.")
        return jsonify({"error": "Nenhum arquivo PDF foi enviado."}), 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        logging.warning("Requisição recebida com nome de arquivo vazio.")
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    recipient_email = request.form.get('recipient_email')
    if not recipient_email:
        logging.warning("Requisição recebida sem 'recipient_email'.")
        return jsonify({"error": "O e-mail do destinatário não foi fornecido."}), 400

    try:
        # 2. Processamento do PDF
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = os.path.join(temp_dir, pdf_file.filename)
            pdf_file.save(temp_path)

            logging.info("Iniciando extração de dados do PDF...")
            extracted_data = extract_data_from_pdf(temp_path)
            if not extracted_data.valor_bruto or not extracted_data.data_base_calculo:
                logging.error("Dados essenciais (valor_bruto, data_base_calculo) não encontrados no PDF.")
                return jsonify({"error": "Não foi possível extrair 'valor_bruto' ou 'data_base_calculo' do PDF."}), 400
            logging.info("Dados do PDF extraídos com sucesso.")

        # 3. Cálculo dos valores
        logging.info("Iniciando cálculo de valores...")
        calculator = await ValueCalculator.create()
        calculation_results = calculator.calculate_values(
            gross_value=extracted_data.valor_bruto,
            base_date_str=extracted_data.data_base_calculo
        )
        logging.info("Cálculo de valores finalizado com sucesso.")

        # 4. Envio de E-mail
        try:
            send_calculation_email(
                recipient_email=recipient_email,
                input_data=extracted_data.dict(),
                calculation_results=calculation_results
            )
        except Exception as e:
            logging.error(f"Cálculo bem-sucedido, mas o envio de e-mail falhou: {repr(e)}")
            response_data = {
                "status": "success_with_email_failure",
                "message": f"Cálculo realizado, mas falha ao enviar e-mail: {repr(e)}",
                "input_data": extracted_data.dict(),
                "result": calculation_results
            }
            return jsonify(response_data), 200

        logging.info("Processo finalizado com sucesso (cálculo e e-mail).")
        response_data = {
            "status": "success",
            "input_data": extracted_data.dict(),
            "result": calculation_results
        }
        return jsonify(response_data), 200

    except Exception as e:
        logging.error(f"Ocorreu uma falha inesperada no servidor durante o cálculo: {repr(e)}")
        return jsonify({"error": f"Ocorreu uma falha inesperada no servidor."}), 500