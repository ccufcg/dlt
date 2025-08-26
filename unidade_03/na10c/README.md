# API Flask para Cartorio e Fiscalizador

Esta API permite interagir com os contratos `Cartorio` e `DesmatamentoFiscalizador` em uma blockchain Besu local.

## Configuração

Edite `config/default.json` para definir:
- provider RPC
- endereços dos contratos
- chainId

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

### Cartório
- POST /cartorio/registrar
```json
{"proprietario": "0x...", "area_total": 100, "area_desmatada_permitida": 10}
```
- GET /cartorio/propriedade/<id>

### Fiscalizador
- POST /fiscal/detectar
```json
{"id_propriedade": 1, "area_desmatada_detectada": 15}
```
- GET /fiscal/multas/<id_propriedade>
- GET /fiscal/multas_abertas/<proprietario>
- POST /fiscal/pagar
```json
{"id_multa": 1, "valor": 1000000000000000000}
```
