let web3, contract, accounts;

(async () => {
  const config = await loadConfig();
  web3 = await initWeb3();
  accounts = await web3.eth.getAccounts();
  contract = await loadContract(web3, config, "DesmatamentoFiscalizador");
})();

async function detectar() {
  const id = document.getElementById("idProp").value;
  const area = document.getElementById("areaDetectada").value;
  await contract.methods.detectarDesmatamento(id, area).send({ from: accounts[0] });
  alert("Desmatamento detectado e multa lançada (se aplicável)");
}

async function consultarMultas() {
  const id = document.getElementById("idPropConsulta").value;
  const multas = await contract.methods.getMultasPorPropriedade(id).call();
  document.getElementById("multasOut").innerText = JSON.stringify(multas, null, 2);
}

async function mostrarSaldo() {
  const balance = await web3.eth.getBalance(contract.options.address);
  alert("Saldo do contrato: " + web3.utils.fromWei(balance, "ether") + " ETH");
}
