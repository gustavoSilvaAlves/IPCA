import httpx
import asyncio
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


class ValueCalculator:
    """
    Calcula o valor líquido atualizado de uma requisição de pagamento
    de forma assíncrona.
    """
    IPCA_API_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"

    def __init__(self, ipca_data: dict):
        if not ipca_data:
            raise ValueError("Os dados do IPCA não podem estar vazios para inicializar a calculadora.")
        self.ipca_data = ipca_data

    @classmethod
    async def create(cls):
        """
        Cria e inicializa de forma assíncrona uma instância de ValueCalculator.
        """
        ipca_data = await cls._fetch_and_process_ipca_data()
        return cls(ipca_data)

    @classmethod
    async def _fetch_and_process_ipca_data(cls) -> dict:
        """Busca os dados do IPCA da API do BACEN de forma assíncrona."""
        print("Buscando dados do IPCA de forma assíncrona...")
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(cls.IPCA_API_URL)
                response.raise_for_status()
                raw_data = response.json()

            processed_data = {
                datetime.strptime(item['data'], '%d/%m/%Y').date(): Decimal(item['valor'])
                for item in raw_data
            }
            print("Dados do IPCA carregados com sucesso.")
            return processed_data
        except httpx.RequestError as e:
            print(f"Erro ao buscar dados do IPCA: {e}")
            return {}

    def calculate_values(self, gross_value: float, base_date_str: str) -> dict:
        """
        Orquestra o cálculo e retorna um dicionário com o valor bruto
        atualizado e o valor líquido.
        """
        updated_gross_value, last_update_date = self._calculate_updated_gross_value(gross_value, base_date_str)

        net_value = updated_gross_value * Decimal('0.97')

        penny = Decimal('0.01')

        return {
            "valor_bruto_corrigido": float(updated_gross_value.quantize(penny, rounding=ROUND_HALF_UP)),
            "valor_liquido_final_ir": float(net_value.quantize(penny, rounding=ROUND_HALF_UP)),
            "ultimo_mes_corrigido": last_update_date.strftime('%m/%Y') if last_update_date else base_date_str[3:]
        }

    def _calculate_updated_gross_value(self, gross_value: float, base_date_str: str) -> Decimal:

        current_value = Decimal(str(gross_value))
        base_date = datetime.strptime(base_date_str, '%d/%m/%Y').date().replace(day=1)
        relevant_ipca = {
            date: value for date, value in self.ipca_data.items() if date >= base_date
        }
        if not relevant_ipca:
            return current_value

        penny = Decimal('0.01')

        last_update_date = None

        for date, index in sorted(relevant_ipca.items()):
            multiplier = Decimal('1') + (index / Decimal('100'))
            current_value *= multiplier
            current_value = current_value.quantize(penny, rounding=ROUND_HALF_UP)
            last_update_date = date
        return current_value, last_update_date


async def main_test():
    """Função principal assíncrona para testar a calculadora."""
    print("--- Testando a Calculadora de Valores (Assíncrona) ---")
    valor_inicial = 650266.04
    data_base_inicial = "01/01/2024"

    try:
        calculator = await ValueCalculator.create()
        valor_liquido_final = calculator.calculate_net_value(valor_inicial, data_base_inicial)

        print("\n--- RESULTADO FINAL ---")
        print(f"Valor Bruto Inicial: R$ {valor_inicial:.2f}")
        print(f"Data Base: {data_base_inicial}")
        print(f"Valor Líquido Atualizado: R$ {valor_liquido_final:.2f}")

    except (ValueError, Exception) as e:
        print(f"\nOcorreu um erro durante o teste: {e}")


if __name__ == '__main__':
    asyncio.run(main_test())