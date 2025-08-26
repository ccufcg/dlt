let web3, contract, accounts;

(async () => {
  const config = await loadConfig();
  web3 = await initWeb3();
  accounts = await web3.eth.getAccounts();
  contract = await loadContract(web3, config, "DesmatamentoFiscalizador");
})();

async function minhasMultas() {
  const multas = await contract.methods.multasEmAberto(accounts[0]).call();
  document.getElementById("multasOut").innerText = JSON.stringify(multas, null, 2);
}

async function pagarMulta() {
  const id = document.getElementById("idMulta").value;
  const multa = await contract.methods.multas(id).call();
  await contract.methods.pagarMulta(id).send({ from: accounts[0], value: multa.valorMulta });
  alert("Multa paga com sucesso!");
}
