import re
from pypdf import PdfReader
from typing import Optional
import pprint
from pathlib import Path
from app.schemas.schemasPydantic import DadosRequisicaoSchema

def _extract_full_text(pdf_path: str) -> str:
    """Abre um PDF e extrai o texto completo de todas as páginas."""
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text


def _search_pattern(text: str, pattern: str) -> Optional[str]:
    """Busca um padrão de regex no texto e retorna o primeiro grupo de captura."""
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def _clean_monetary_value(value_str: Optional[str]) -> Optional[float]:
    """Converte um valor monetário em string (ex: '650.266,04') para float."""
    if not value_str:
        return None
    try:
        cleaned_value = value_str.replace('.', '').replace(',', '.')
        return float(cleaned_value)
    except (ValueError, AttributeError):
        return None

def _clean_cpf(cpf_str: Optional[str]) -> Optional[str]:
    """Remove qualquer caractere não numérico de uma string de CPF."""
    if not cpf_str:
        return None
    return re.sub(r'[^\d]', '', cpf_str)


def extract_data_from_pdf(pdf_path: str) -> DadosRequisicaoSchema:
    """
    Função principal que orquestra a extração de dados de um PDF de requisição.
    """
    full_text = _extract_full_text(pdf_path)
    full_text = full_text.replace('\xa0', ' ')

    patterns = {
        "numero_oficio": r"Definitivo OFÍCIO Nº:\s*([\d\./A-Z]+)",
        "nome_beneficiario": r"III - BENEFICIÁRIO\s+Nome:\s*([^\r\n]+)",
        "cpf_beneficiario": r"III - BENEFICIÁRIO\s+Nome:\s*[^\r\n]+\s+CPF:\s*(\d+)",
        "valor_bruto": r"Valor bruto da requisição:\s*R\$\s*([\d\.,]+)",
        "data_base_calculo": r"Data base do cálculo:\s*(\d{2}/\d{2}/\d{4})",
    }

    extracted_data_dict = {}
    for key, pattern in patterns.items():
        extracted_data_dict[key] = _search_pattern(full_text, pattern)

    extracted_data_dict["valor_bruto"] = _clean_monetary_value(extracted_data_dict.get("valor_bruto"))
    extracted_data_dict["cpf_beneficiario"] = _clean_cpf(extracted_data_dict.get("cpf_beneficiario"))

    return DadosRequisicaoSchema(**extracted_data_dict)


if __name__ == '__main__':
    try:

        script_dir = Path(__file__).parent.resolve()

        base_dir = script_dir.parent.parent
        test_pdf_path = base_dir / 'Exemplo2.pdf'

        print(f"Tentando carregar o PDF de: {test_pdf_path}")

        data = extract_data_from_pdf(test_pdf_path)


        print("\nDados Extraídos:")
        pprint.pprint(data)

    except FileNotFoundError:
        print(f"\nErro: O arquivo de teste não foi encontrado.")
        print("Verifique se 'Exemplo1.pdf' está na pasta 'back-end-flask'.")