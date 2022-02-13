const ethereumButton = document.querySelector('.enableEthereumButton');
//const showAccount = document.querySelector('.showAccount');
const showAccount = document.querySelector('.enableEthereumButton');




ethereumButton.addEventListener('click', () => {
  console.log("Teste")
  getAccount();
});

async function getAccount() {
  const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
  const account = accounts[0];
  showAccount.innerHTML = account;
  return account
}




