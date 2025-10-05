from flask import Blueprint, request, jsonify
import tempfile
import os

from app.services.pdf_parser import extract_data_from_pdf
from app.services.value_calculator import ValueCalculator

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/ping', methods=['GET'])
def ping():
    """Rota de teste para verificar se a API está no ar."""
    return jsonify({"message": "Pong!"})

@api_bp.route('/calculate', methods=['POST'])
async def calculate():
    """
    Recebe um arquivo PDF, extrai os dados, calcula o valor líquido
    e retorna o resultado.
    """

    if 'pdf_file' not in request.files:
        return jsonify({"error": "Nenhum arquivo PDF foi enviado."}), 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = os.path.join(temp_dir, pdf_file.filename)

        pdf_file.save(temp_path)

        try:
            extracted_data = extract_data_from_pdf(temp_path)
            if not extracted_data.valor_bruto or not extracted_data.data_base_calculo:
                return jsonify({"error": "Não foi possível extrair 'valor_bruto' ou 'data_base_calculo' do PDF."}), 400
        except Exception as e:
            return jsonify({"error": f"Falha ao processar o PDF: {e}"}), 500

    try:
        calculator = await ValueCalculator.create()
        calculation_results = calculator.calculate_values(
            gross_value=extracted_data.valor_bruto,
            base_date_str=extracted_data.data_base_calculo
        )
    except Exception as e:
        return jsonify({"error": f"Falha ao calcular o valor: {e}"}), 500

    response_data = {
        "status": "success",
        "input_data": extracted_data.dict(),
        "result":calculation_results

    }
    return jsonify(response_data), 200