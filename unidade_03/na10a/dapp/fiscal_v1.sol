// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

import "./util/libs2.sol";
import "./cartorio_v4.sol";

contract Fiscal is Base {


    uint public multaBasePorHectare = 1 ether; // Valor base da multa por hectare desmatado irregularmente
    uint public totalMultas;


    mapping(uint => Entidades.Multa) public multas; // id da multa => multa
    mapping(uint => uint[]) public multasPorPropriedade; // idPropriedade => lista de IDs de multas


    event DesmatamentoDetectado(uint idPropriedade, address proprietario, uint areaDesmatada);
    event MultaAplicada(uint idMulta, uint idPropriedade, address proprietario, uint valorMulta, uint timestamp);
    event MultaPaga(uint idMulta, address pagador, uint valor);

    address private cartorioAddr;

    function setCartorio(address _addr) public onlyOwner {
        cartorioAddr = _addr;
    }

    function detectarDesmatamento(uint idPropriedade, uint areaDesmatadaDetectada) public onlyOwner {

        

        //propriedade alvo
        // chamando outro contrato
        Cartorio cartorio = Cartorio(cartorioAddr);
        Entidades.Propriedade memory propriedadeAlvo = cartorio.getPropriedade(idPropriedade); 
            
        require(propriedadeAlvo.registrada, "Propriedade nao registrada");

        emit DesmatamentoDetectado(idPropriedade, propriedadeAlvo.proprietario, areaDesmatadaDetectada);

        uint permitido = propriedadeAlvo.areaDesmatadaPermitida;
        if (areaDesmatadaDetectada > permitido) {
            uint areaIrregular = areaDesmatadaDetectada - permitido;
            uint valor = areaIrregular * multaBasePorHectare;

            totalMultas++;
            multas[totalMultas] = Entidades.Multa(
                idPropriedade,
                propriedadeAlvo.proprietario,
                areaIrregular,
                valor,
                block.timestamp,
                false
            );
            multasPorPropriedade[idPropriedade].push(totalMultas);

            emit MultaAplicada(totalMultas, idPropriedade, propriedadeAlvo.proprietario, valor, block.timestamp);
        }
    }


    function pagarMulta(uint idMulta) public payable {
        Entidades.Multa storage multa = multas[idMulta];
        require(!multa.paga, "Multa ja paga");
        // require(msg.sender == multa.proprietario, "Somente o proprietario pode pagar");
        require(msg.value == multa.valorMulta, "Valor da multa incorreto");

        multa.paga = true;

        emit MultaPaga(idMulta, msg.sender, msg.value);
    }

    // Retornar lista de multas de uma propriedade
    function getMultasPorPropriedade(uint idPropriedade) public view returns (uint[] memory) {
        return multasPorPropriedade[idPropriedade];
    }

    function multasEmAberto(address _proprietario) public view returns (uint[] memory) {
        // pode ser melhorado        
        uint[] memory temp = new uint[](totalMultas);
        uint count = 0;
        for (uint i = 1; i <= totalMultas; i++) {
            if (multas[i].proprietario == _proprietario && !multas[i].paga) {
                temp[count] = i;
                count++;
            }
        }
        uint[] memory result = new uint[](count);
        for (uint j = 0; j < count; j++) {
            result[j] = temp[j];
        }
        return result;
    }
}