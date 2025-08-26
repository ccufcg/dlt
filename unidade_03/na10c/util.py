from flask import request, jsonify , Blueprint
from web3 import Web3
import json
import logging
from web3.exceptions import TimeExhausted


# Configuração básica
logging.basicConfig(level=logging.INFO)

util_api = Blueprint('util_api', __name__)

# Carregar configuração
with open("config/default.json") as f:
    config = json.load(f)


w3 = Web3(Web3.HTTPProvider(config["provider"]))

@util_api.route('/logs/<tx>', methods=['GET'])
def get_transaction_receipt(tx):
    tx_hash = tx
    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if receipt['status'] == 0:
            logging.error(f"Transação {tx_hash} falhou.")
            return jsonify({
                "error": "A transação foi revertida pelo contrato.",
                "receipt": json.loads(Web3.to_json(dict(receipt)))
            }), 400
        return jsonify({
            "status": "success",
            "transaction_hash": tx_hash,
            "receipt": json.loads(Web3.to_json(dict(receipt)))
        })

        # trecho gerado por ai (que não funciona direito)
        # Decodificar os logs/eventos do contrato
        # processed_logs = cartorio.events.PropriedadeRegistrada().process_receipt(receipt)

        # Formatar os logs
        # logs_list = []
        # for log in processed_logs:
        #     logs_list.append({
        #         'event': log.event,
        #         'args': dict(log.args)
        #     })

        # 
        # return jsonify({
        #     "status": "success",
        #     "transaction_hash": tx_hash,
        #     "block_number": receipt.blockNumber,
        #     "gas_used": receipt.gasUsed,
        #     "decoded_logs": logs_list
        # })

    except TimeExhausted:
        logging.warning(f"Timeout esperando pelo recibo da transação {tx_hash}.")
        return jsonify({"error": "Timeout. A transação está demorando para ser minerada ou o hash é inválido."}), 408 # Request Timeout

    except Exception as e:
        logging.error(f"Erro ao buscar recibo ou processar logs para {tx_hash}: {e}")
        return jsonify({"error": f"Erro ao buscar recibo. Verifique se o hash da transação é válido e se o evento está sendo decodificado corretamente. Detalhe: {str(e)}"}), 500