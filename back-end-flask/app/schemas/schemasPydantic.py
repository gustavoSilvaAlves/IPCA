from pydantic import BaseModel
from typing import Optional

class DadosRequisicaoSchema(BaseModel):
    """
    Define a estrutura de dados para as informações
    extraídas do PDF de requisição.
    """
    numero_oficio: Optional[str] = None
    nome_beneficiario: Optional[str] = None
    cpf_beneficiario: Optional[str] = None
    valor_bruto: Optional[float] = None
    data_base_calculo: Optional[str] = None