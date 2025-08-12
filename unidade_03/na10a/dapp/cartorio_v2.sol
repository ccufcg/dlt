// SPDX-License-Identifier: GPL
pragma solidity ^0.8.0;

contract Cartorio {

    address public owner;

    struct Propriedade {
        address proprietario;
        uint areaTotal; // em hectares
        uint areaDesmatadaPermitida; // em hectares
        bool registrada;
    }

    mapping(uint => Propriedade) public propriedades;
    uint public totalPropriedades;

    modifier onlyOwner() {
        require(msg.sender == owner, "Apenas o owner pode executar");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registrarPropriedade( address _proprietario, uint _areaTotal, uint _areaDesmatadaPermitida ) 
        public onlyOwner returns (uint) {
        totalPropriedades++;

        propriedades[totalPropriedades] = Propriedade(_proprietario, _areaTotal, _areaDesmatadaPermitida, true);
        return totalPropriedades;
    }

    function getTotalPropriedades() public view returns (uint) {
        return totalPropriedades;
    }

}