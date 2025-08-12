// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

library Entidades {  

    struct Propriedade {
        address proprietario;
        uint areaTotal; // em hectares
        uint areaDesmatadaPermitida; // em hectares
        bool registrada;
    }

    struct Multa {
        uint idPropriedade;
        address proprietario;
        uint areaDesmatada;
        uint valorMulta;
        uint timestamp;
        bool paga;
    }

}

contract Base {

    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Apenas o tabeliao pode executar");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

}