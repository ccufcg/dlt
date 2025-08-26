from flask import Flask, request, jsonify , Blueprint
from web3 import Web3
from eth_account import Account
import json
import logging

# Configuração básica
logging.basicConfig(level=logging.INFO)

fiscal_api = Blueprint('fiscal_api', __name__)

# Carregar configuração
with open("config/default.json") as f:
    config = json.load(f)
with open("config/fiscal.idl") as f:
    fiscal_info = json.load(f)


w3 = Web3(Web3.HTTPProvider(config["provider"]))
fiscal = w3.eth.contract(address=config["fiscal_address"], abi=fiscal_info)
admin_account = Account.from_key(config.get("admin_private_key"))


# nao testado
@fiscal_api.route('/detectar', methods=['POST'])
def detectar_desmatamento():
    data = request.get_json()
    id_prop = int(data["id_propriedade"])
    area_detectada = int(data["area_desmatada_detectada"])
    tx = fiscal.functions.detectarDesmatamento(id_prop, area_detectada).build_transaction({'from': w3.eth.accounts[0], 'gas': 2000000, 'nonce': w3.eth.get_transaction_count(w3.eth.accounts[0])})
    return jsonify({"tx": tx})

# ok
@fiscal_api.route('/multas/<int:id_propriedade>', methods=['GET'])
def get_multas(id_propriedade):
    multas = fiscal.functions.getMultasPorPropriedade(id_propriedade).call()
    return jsonify({"id_propriedade": id_propriedade, "multas": multas})

# com problema
@fiscal_api.route('/multas_abertas/<proprietario>', methods=['GET'])
def multas_abertas(proprietario):
    arr = fiscal.functions.multasEmAberto(proprietario).call()
    return jsonify({"proprietario": proprietario, "multas_abertas": arr})

# testada
@fiscal_api.route('/pagar', methods=['POST'])
def pagar_multa():
    data = request.get_json()
    id_multa = int(data["id_multa"])
    valor = int(data["valor"])
    tx = fiscal.functions.pagarMulta(id_multa).build_transaction({'from': w3.eth.accounts[0], 'value': valor, 'gas': 2000000, 'nonce': w3.eth.get_transaction_count(w3.eth.accounts[0])})
    return jsonify({"tx": tx})