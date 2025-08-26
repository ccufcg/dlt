let web3, contract, accounts;

(async () => {
  const config = await loadConfig();
  web3 = await initWeb3();
  accounts = await web3.eth.getAccounts();
  contract = await loadContract(web3, config, "Cartorio");
})();

async function registrar() {
  const addr = document.getElementById("propAddr").value;
  const area = document.getElementById("propArea").value;
  const permitida = document.getElementById("propPermitida").value;
  await contract.methods.registrarPropriedade(addr, area, permitida).send({ from: accounts[0] });
  alert("Propriedade registrada!");
}

async function consultar() {
  const id = document.getElementById("propId").value;
  const prop = await contract.methods.getPropriedade(id).call();
  document.getElementById("propOut").innerText = JSON.stringify(prop, null, 2);
}
