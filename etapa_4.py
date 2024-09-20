import json

import requests

base_url = "https://obnoxious-albatross-isadora-d7a76efe.koyeb.app/api/data"


def get_data():
    response = requests.get(base_url)
    if response.status_code == 200:
        print("Dados obtidos com sucesso:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Erro ao obter dados: {response.status_code}")
        exit()


def insert_data(new_data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(base_url, data=json.dumps(new_data), headers=headers)
    if response.status_code == 201:
        print("Dados inseridos com sucesso.")
    else:
        print(f"Erro ao inserir dados: {response.status_code}")
        exit()


def update_data(name, notes):
    url = f"{base_url}/{name}/{notes}"
    response = requests.patch(url)
    if response.status_code == 200:
        print("Dados atualizados com sucesso:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Erro ao atualizar dados: {response.status_code}")
        exit()


def delete_data(name):
    url = f"{base_url}/{name}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("Dados deletados com sucesso.")
    else:
        print(f"Erro ao deletar dados: {response.status_code}")
        exit()


if __name__ == "__main__":
    new_wine = {
        "name": "Cabernet Isa, Viini, Ramiro",
        "notes": "Notas sobre o novo vinho",
        "rating": 90.1,
    }
    get_data()

    print("----------------------------------------")

    insert_data(new_wine)

    print("----------------------------------------")

    update_data("Cabernet Isa, Viini, Ramiro", "Novas notas sobre o novo vinho")

    print("----------------------------------------")

    delete_data("Cabernet Isa, Viini, Ramiro")

    print("----------------------------------------")
