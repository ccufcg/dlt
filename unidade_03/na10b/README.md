# DApp Cartório & Fiscalização de Desmatamento

Este projeto é a implatenção completa do DApp (`backend` & `frontend`) descrito na aula [anterior](https://github.com/ccufcg/dlt/tree/main/unidade_03/na10a) com as interação com os contratos **Cartorio** e **DesmatamentoFiscalizador** em uma rede Hyperledger Besu local.


> ⚠️ O código js desse repositorio foi gerado por AI.


## Como usar

1. Inicie sua rede Besu privada em `127.0.0.1:8545` com `chainId = 1337`.
2. Faça o deploy dos contratos `Cartorio` e `DesmatamentoFiscalizador`.
3. Copie as ABIs para `config/cartorio.json` e `config//DesmatamentoFiscalizador.json`.
4. Atualize os endereços em `config/default.json`.
5. Abra cada página HTML em um navegador com **MetaMask** configurado para a rede local.

O passo a passo esta descrito no [repositorio](https://github.com/ccufcg/bc101-dev-env) do ambiente de teste da disciplina!

## Páginas

- **cartorio.html**: Registrar e consultar propriedades (somente owner pode registrar).
- **fiscal.html**: Detectar desmatamento, consultar multas e ver saldo do contrato.
- **proprietario.html**: Consultar multas em aberto do proprietário conectado e pagar.

## Requisitos
- MetaMask conectado à rede local Besu, tutorial disponivel no [repositorio](https://github.com/ccufcg/bc101-dev-env).
- Node opcional, mas basta abrir os HTMLs em navegador com MetaMask.
    - `python3 -m http.server`

