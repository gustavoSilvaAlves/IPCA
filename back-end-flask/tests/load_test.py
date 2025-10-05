# back-end-flask/tests/load_test.py

import asyncio
import httpx
import time
from pathlib import Path

API_URL = "http://127.0.0.1:5001/api/calculate"
PDF_PATH = Path(__file__).parent.parent / 'Exemplo2.pdf'

NUM_REQUESTS = 50  # Número total de requisições a serem feitas
CONCURRENCY_LEVEL = 10 # Quantas requisições fazer em paralelo


async def make_request(client: httpx.AsyncClient, pdf_data: dict):
    """Faz uma única requisição para a API e retorna se foi bem-sucedida."""
    try:
        response = await client.post(API_URL, files=pdf_data)
        response.raise_for_status() # Lança um erro para status 4xx ou 5xx
        print(f"Sucesso! Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"--- Falha na requisição: {type(e).__name__} ---")
        return False

async def run_test():
    """Orquestra o teste de carga, controlando a concorrência."""
    print(f"--- Iniciando teste de carga com concorrência de {CONCURRENCY_LEVEL} (total de {NUM_REQUESTS} reqs) ---")

    if not PDF_PATH.exists():
        print(f"ERRO: Arquivo PDF de teste não encontrado em '{PDF_PATH}'")
        return

    with open(PDF_PATH, "rb") as f:
        pdf_bytes = f.read()

    files_payload = {"pdf_file": (PDF_PATH.name, pdf_bytes, "application/pdf")}

    overall_start_time = time.monotonic()

    async with httpx.AsyncClient(timeout=30) as client:
        # Cria uma lista de "tarefas" a serem executadas
        tasks = [make_request(client, files_payload) for _ in range(NUM_REQUESTS)]

        results = await asyncio.gather(*tasks)

    overall_end_time = time.monotonic()
    total_time = overall_end_time - overall_start_time

    success_count = sum(1 for r in results if r)
    failure_count = NUM_REQUESTS - success_count

    print("\n" + "="*30)
    print("      Resultados do Teste")
    print("="*30)
    print(f"Tempo total: {total_time:.2f} segundos")
    print(f"Total de requisições: {NUM_REQUESTS}")
    print(f"Requisições bem-sucedidas: {success_count}")
    print(f"Requisições com falha: {failure_count}")
    if total_time > 0:
        rps = success_count / total_time
        print(f"Requisições por segundo (RPS): {rps:.2f}")
    print("="*30)

if __name__ == "__main__":
    asyncio.run(run_test())