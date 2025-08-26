from flask import Flask, request, jsonify , Blueprint
from web3 import Web3
from eth_account import Account
import json
import logging

# Configuração básica
logging.basicConfig(level=logging.INFO)

cartorio_api = Blueprint('cartorio_api', __name__)

# Carregar configuração
with open("config/default.json") as f:
    config = json.load(f)


w3 = Web3(Web3.HTTPProvider(config["provider"]))


with open("config/cartorio.idl") as f:
    cartorio_info = json.load(f)



admin_account = Account.from_key(config.get("admin_private_key"))
cartorio = w3.eth.contract(address=config["cartorio_address"], abi=cartorio_info)

@cartorio_api.route('/registrar', methods=['POST'])
def registrar_propriedade():
    data = request.get_json()
    proprietario_str = data["proprietario"]
    area_total = int(data["area_total"])
    area_permitida = int(data["area_desmatada_permitida"])


    if not w3.is_address(proprietario_str):
        logging.error(f"Endereço inválido recebido: {proprietario_str}")
        return jsonify({"error": f"O endereço '{proprietario_str}' não é um endereço Ethereum válido."}), 400

    # Converter para formato checksum
    # proprietario = proprietario_str
    proprietario = w3.to_checksum_address(proprietario_str)
    

    nonce = w3.eth.get_transaction_count(admin_account.address)
    # essa parte pode ser melhorada
    tx = cartorio.functions.registrarPropriedade(proprietario, area_total, area_permitida).build_transaction(
        {
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': w3.to_wei('20', 'gwei')
        }
    )

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=admin_account.key)
    logging.info(signed_tx)

    # Enviar a transação assinada
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    logging.info('tx hash:' + tx_hash.hex())


    return jsonify({"transaction_hash" : f"{tx_hash.hex()}",
                    "tx_url" : f"http://127.0.0.1:5000/tx/{tx_hash.hex()}",
                    "logs_url" : f"http://127.0.0.1:8080/util/logs/{tx_hash.hex()}"
                    })


@cartorio_api.route('/propriedade/<int:id>', methods=['GET'])
def get_propriedade(id):
    prop = cartorio.functions.getPropriedade(id).call()
    return jsonify({"id": id, "proprietario": prop[0], "area_total": prop[1], "area_desmatada_permitida": prop[2], "registrada": prop[3]})
