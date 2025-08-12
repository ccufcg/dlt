# Utilizando a Blockchain para contralar o desmatamento

Para o **IBAMA**, a fiscalização começa no espaço, com satélites que detectam o desmatamento em tempo real. Nesse contexto, após identificar uma área desmatada, um analista, iniciava-se um processo lento e analógico para conectar aquela coordenada geográfica a um CPF ou CNPJ, uma jornada que passava por ofícios, telefonemas e meses de espera por respostas dos diversos **Cartórios de Registro de Imóveis** espalhados pelo país.

Essa demora era um convite à impunidade. Para resolver isso, foi proposto um projeto: criar sistema entre o IBAMA e os cartórios usando a tecnologia de Smart Contracts.

- [O Cartorio](#cartorio)
    - [v2](#cartorio-v2)
    - [v3](#cartorio-v3)
    - [v4](#cartorio-v4)
- [O Fiscal](#fiscal-v1)

### Cartorio

O primeiro passo não é a fiscalização, mas a criação de um registro de imovel. O objetivo é desenvolver um padrão nacional para o registro de imóveis em blockchain. Nasce a primeira versão do contrato `Cartorio`.

Esse sistema tem a função de permitir que uma autoridade (o tabelião, dono do contrato) registre uma propriedade com seus dados: 
- o proprietário, 
- a área total e o 
- limite legal de desmatamento (Reserva Legal). 

Ai final do registro, cada imóvel recebe uma "matrícula digital" (um ID).

**Código:** [cartorio_v1.sol](./dapp/cartorio_v1.sol)


**Funcionalidades:**
- cadastra a propriedade
- consulta por id da propriedade
- retorna o numero propriedade

**Conceitos:**
Os conceitos didáticos são os blocos de construção de qualquer contrato.
    - contrutor
    - mapping
    - tipos
    - assinaturas metodos

*   **`struct Propriedade`**: A "escritura digital" do imóvel, padronizando os dados.
*   **`mapping(uint => Propriedade)`**: O grande "livro de registros" digital, acessível e incorruptível.
*   **`function registrarPropriedade(...)`**: O ato de "carimbar" o registro.
*   **`modifier onlyOwner`**: A garantia de que apenas a autoridade competente do Cartório pode registrar um novo imóvel.

```solidity
// Cartorio v1: A base de tudo.
contract Cartorio {
    address public owner; // O tabelião digital
    struct Propriedade {
        address proprietario;
        uint areaTotal;
        uint areaDesmatadaPermitida;
        bool registrada;
    }
    mapping(uint => Propriedade) public propriedades; // O livro de registros
    // ...
}
```



#### Cartorio v2

Um agente do IBAMA está em uma operação na Amazônia. Ele confirma um novo desmatamento e, com o CPF do suspeito, encontra o endereço de sua carteira digital. No entanto, ele não tem o número da matrícula do imóvel para consultar no sistema. Ele precisa de uma forma de puxar a ficha da propriedade usando o dado que ele tem em mãos: o endereço do proprietário.

A equipe de desenvolvimento atende ao pedido. O contrato [cartorio_v2.sol](./dapp/cartorio_v2.sol) é atualizado com uma nova funcionalidade: a capacidade de pesquisar um imóvel diretamente pelo endereço de seu dono.

**A evolução do código:**
*   **A Mudança:** A adição de uma nova função de busca.
*   **Conceito Didático:** O modificador `view`. O agente pode "visualizar" os dados sem alterar o estado da blockchain, o que significa que a consulta é rápida e, mais importante, **não consome gás** (é gratuita para quem chama de fora).

```solidity
// A nova ferramenta do agente do IBAMA:
function getPropriedade(address _proprietario) public view returns (Propriedade memory) {
    // ... Procura no mapping e retorna os dados ...
}
```

#### Cartorio v3

O sistema funciona, mas ele é "silencioso". Os sistemas de monitoramento do IBAMA precisam saber, em tempo real, quando um novo imóvel é registrado ou alterado. Além disso, a equipe do IBAMA está pronta para construir seu próprio contrato, o "Fiscalizador", e é absolutamente crítico que ambos os sistemas entendam a estrutura de uma "Propriedade" da mesma maneira.

A solução vem em duas partes, construindo uma verdadeira ponte de comunicação:
1.  **Um "Dicionário de Dados" Unificado (`library`):** A definição de `Propriedade` é extraída para uma `library` compartilhada, garantindo que Cartório e IBAMA "falem a mesma língua".
2.  **Um "Mural de Anúncios" Público (`event`):** O contrato agora emite um evento `PropriedadeRegistrada` sempre que um registro é feito. Os sistemas do IBAMA podem "assinar" esse mural e ser notificados instantaneamente.

**A evolução do código:** [cartorio_v3.sol](./dapp/cartorio_v3.sol)

O foco é a modularidade, a reutilização de código e a comunicação entre sistemas.

*   **`library Entidades`**: Garante um padrão único e reutilizável para as estruturas de dados.
*   **`event PropriedadeRegistrada(...)`**: Cria um log público e rastreável de ações importantes.
*   **`emit`**: A ação de "publicar no mural" para que todos os interessados vejam.

```solidity
import "./Entidades.sol"; // Importando o dicionário comum

contract CartorioV3 {
    // ...
    event PropriedadeRegistrada(uint id, address proprietario, ...); // O modelo do anúncio

    function registrarPropriedade(...) ... {
        // ...lógica de registro...
        emit PropriedadeRegistrada(totalPropriedades, ...); // O anúncio é publicado!
    }
}
```

### Cartorio v4

Com a integração avançando, uma auditoria técnica é realizada para otimizar o sistema e garantir o uso eficiente dos recursos públicos. Os auditores do `TCU` fazem uma recomendação: é preciso ser explícito sobre como os dados são manipulados para reduzir os custos operacionais (taxas de gás). Também foi solicitado um metodo de busca pelo dono.

Eles explicam a diferença entre o **"arquivo permanente"** da blockchain (`storage`), que é seguro, mas caro de acessar, e a **"memória de trabalho temporária"** (`memory`), que é ágil e barata. A nova diretriz é: para qualquer consulta, o sistema deve copiar a informação do arquivo permanente para a memória de trabalho antes de entregá-la.

**A evolução do código:** [cartorio_v4.sol](./dapp/cartorio_v4.sol)

*   **A Mudança:** A palavra-chave `memory` é adicionada explicitamente no retorno das funções de consulta.
*   **Conceito Didático:** Entender as localizações de dados (`storage` vs. `memory`) é fundamental para escrever contratos eficientes e econômicos, um requisito essencial para projetos governamentais.
*

```solidity
// A mudança sutil que demonstra maturidade técnica:
function getPropriedade(uint _id) public view returns (Entidades.Propriedade memory prop) {
    // ...
}
```

### Fiscal v1

Com o `Cartorio` digital funcionando como uma base de dados nacional, o **IBAMA lança seu contrato `DesmatamentoFiscalizador`**.

O [fiscal_v1.sol](./dapp/fiscal_v1.sol) é o "juiz digital". Ele é configurado com o endereço do contrato `Cartorio`, criando um link de confiança inquebrável. Agora, o fluxo é totalmente automatizado:
1.  O satélite do IBAMA detecta um desmatamento e envia um alerta ao `Fiscalizador`: "Propriedade ID 54321, área desmatada: 30 hectares."
2.  O `Fiscalizador` instantaneamente chama o contrato `Cartorio`: "Quais são as regras para a propriedade 54321?"
3.  O `Cartorio` responde em milissegundos: "Proprietário 0xabc..., Área Permitida: 20 hectares."
4.  O `Fiscalizador` executa a lógica: 30 (detectado) > 20 (permitido). Ele calcula a multa com base em uma fórmula pré-definida (`multaBasePorHectare`), cria um registro de `Multa` e a associa ao proprietário.
5.  A multa agora existe na blockchain, e o proprietário pode pagá-la diretamente ao contrato `Fiscalizador`, que garante que o dinheiro chegue aos cofres públicos de forma transparente e auditável.


Este contrato é integrado com o `Cartorio` e a execução de lógica de negócios com consequências financeiras.

*   **Interação entre Contratos:** `Cartorio cartorio = Cartorio(cartorioAddr)` cria a ponte viva entre os dois sistemas.
*   **Lógica de Negócio:** O `if` que compara a área desmatada com a permitida é o coração do sistema de fiscalização.
*   **`payable`**: A função `pagarMulta` é `payable`, permitindo que o contrato receba criptomoedas para liquidar a multa, fechando o ciclo de fiscalização de forma 100% digital.

```solidity
// O Fiscalizador em ação:
contract DesmatamentoFiscalizador {
    // ...
    function detectarDesmatamento(uint idPropriedade, uint areaDesmatada) public {
        // 1. Pega os dados do Cartório
        Entidades.Propriedade memory p = cartorio.getPropriedade(idPropriedade);
        
        // 2. Aplica a regra
        if (areaDesmatada > p.areaDesmatadaPermitida) {
            // 3. Aplica a multa
            // ...
        }
    }

    // 4. Recebe o pagamento
    function pagarMulta(uint idMulta) public payable {
        // ...
    }
}
```