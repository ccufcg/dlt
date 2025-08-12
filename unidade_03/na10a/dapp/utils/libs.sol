// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

library Entidades {  

    struct Propriedade {
        address proprietario;
        uint areaTotal; // em hectares
        uint areaDesmatadaPermitida; // em hectares
        bool registrada;
    }

}

/// DARK ENTITIES
library SystemEntities {
    
    struct Multa {
        uint idPropriedade;
        address proprietario;
        uint areaDesmatada;
        uint valorMulta;
        uint timestamp;
        bool paga;
    }
}
    

