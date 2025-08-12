// SPDX-License-Identifier: GPL
pragma solidity ^0.8.0;

import "./util/libs.sol";

contract Cartorio {

    address public owner;

    mapping(uint => Entidades.Propriedade) public propriedades;
    uint private totalPropriedades;

    event PropriedadeRegistrada(uint id, address proprietario, uint areaTotal, uint areaDesmatadaPermitida);

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

        propriedades[totalPropriedades] = Entidades.Propriedade(_proprietario, _areaTotal, _areaDesmatadaPermitida, true);
        emit PropriedadeRegistrada(totalPropriedades, _proprietario, _areaTotal, _areaDesmatadaPermitida);
        return totalPropriedades;
    }

    function getTotalPropriedades() public view returns (uint) {
        return totalPropriedades;
    }
}