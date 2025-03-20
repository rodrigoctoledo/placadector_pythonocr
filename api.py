# api.py
import datetime

import requests
import time
from config import API_BASE_URL, jwt_token, user_id, occurrences_list


def login_api(email, senha):
    data = {"email": email, "senha": senha}
    try:
        response = requests.post(f"{API_BASE_URL}/Auth/login", json=data, verify=False)

        # Imprime o status e o conteúdo retornado para debug
        print("Status Code:", response.status_code)
        json_data = response.json()
        print("Response JSON:", json_data)

        if response.status_code == 200:
            token = json_data.get("token")  # Certifique-se de que a chave é "Token"
            user_id_val = json_data.get("id")  # E que a chave é "Id"
            return token, user_id_val
        else:
            print("Erro no login:", response.status_code, response.text)
            return None, None
    except Exception as e:
        print("Exceção no login:", e)
        return None, None


def create_occurrence(occurrence_data):
    headers = {"Authorization": f"Bearer {config.jwt_token}"}
    try:
        response = requests.post(f"{API_BASE_URL}/Ocorrencias", json=occurrence_data, headers=headers, verify=False)
        if response.status_code in [200, 201]:
            print("Ocorrência cadastrada com sucesso!")
        else:
            print(f"Falha ao cadastrar ocorrência: {response.status_code} - {response.text}")
    except Exception as e:
        print("Exceção ao cadastrar ocorrência:", e)
import requests
import config  # Importa o módulo inteiro para acessar config.jwt_token e config.API_BASE_URL

def get_occurrences():
    headers = {"Authorization": f"Bearer {config.jwt_token}"}
    try:
        response = requests.get(f"{config.API_BASE_URL}/Ocorrencias", headers=headers, verify=False)
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            occurrences = response.json()
            config.occurrences_list.clear()
            config.occurrences_list.extend(occurrences)
            print("Lista de ocorrências atualizada.")
        else:
            print(f"Erro ao buscar ocorrências: {response.status_code} - {response.text}")
    except Exception as e:
        print("Erro ao conectar com a API:", e)

def check_and_register_occurrence(plate):
    headers = {"Authorization": f"Bearer {config.jwt_token}"}
    try:
        # Faz uma requisição GET para obter as Plates já registradas
        response = requests.get(f"{config.API_BASE_URL}/Plates", headers=headers, verify=False)
        if response.status_code == 200:
            plates = response.json()
            # Atualiza a lista global (caso esteja usando para outras operações)
            config.occurrences_list.clear()
            config.occurrences_list.extend(plates)

            # Verifica se a placa já está cadastrada (comparação case-insensitive)
            match = next((p for p in plates if p.get("Placa", "").upper() == plate.upper()), None)
            if match:
                print(f"Placa {plate} já existe nos registros.")
            else:
                # Monta o JSON com os dados esperados pela API para criar um novo Plate
                plate_data = {
                    "Placa": plate,
                    "Local": "Local Padrão",  # Substitua por um valor adequado ou obtenha via input
                    "Horario": datetime.datetime.now().isoformat(),  # Formato ISO 8601 para DataTime
                    "UsuarioId": int(config.user_id)  # Garante que seja enviado como inteiro
                }
                print("Dados enviados para criação de Plate:", plate_data)
                post_response = requests.post(f"{config.API_BASE_URL}/Plates", json=plate_data, headers=headers,
                                              verify=False)
                if post_response.status_code in [200, 201]:
                    print(f"Plate registrada com sucesso para a placa {plate}.")
                else:
                    print(f"Falha ao registrar Plate: {post_response.status_code} - {post_response.text}")
        else:
            print(f"Erro ao buscar Plates: {response.status_code}")
    except Exception as e:
        print("Erro ao conectar com a API:", e)
