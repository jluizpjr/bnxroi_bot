var Web3 = require("web3")
const web3 = new Web3("https://bsc-dataseed.binance.org")

const getCurrentBlock = document.querySelector('.getCurrentBlock');
const bnxBalance = document.querySelector('.bnxBalance');
const alfaceBalance = document.querySelector('.alfaceBalance');

const ethereumButton = document.querySelector('.enableEthereumButton');
const showAccount = document.querySelector('.enableEthereumButton');
const diamondBalance = document.querySelector('.diamondBalance');
const alfaceMint = document.querySelector('.alfaceMint');
const mintALFCToAddress = document.querySelector('.mintALFCToAddress');
const mintALFCAmount = document.querySelector('.mintALFCAmount');


const bnxAddress = "0x8c851d1a123ff703bd1f9dabe631b69902df5f97";
const diamondAddress = "0x5f16128A0A10fF02AB645A81d9E6589D1c599850";
const alfaceAddress = "0xfe360bb3421af9e4a142fe2adbdfd84ea22860dd"


getCurrentBlock.addEventListener('click', () => {
  console.log("getCurrentBlock")
  getBlockNumber();
});

async function getBlockNumber() {
  const latestBlockNumber = await web3.eth.getBlockNumber()
  console.log(latestBlockNumber)
  getCurrentBlock.innerHTML = latestBlockNumber;
  return latestBlockNumber
}
//###################### BNX Handling ######################
bnxBalance.addEventListener('click', () => {
  console.log("Calling getBNX")
  getBNX();
});

async function getBNX(){
  const abiJson = [
    {"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
  ];
  
  const contract = new web3.eth.Contract(abiJson, bnxAddress);
  const balance = await contract.methods.balanceOf(await getAccount()).call();
  // note that this number includes the decimal places (in case of BUSD, that's 18 decimal places)
  console.log(balance);
  bnxBalance.innerHTML = balance/(10**18);


}


//###################### ALFC Handling ######################
alfaceBalance.addEventListener('click', () => {
  console.log("Calling getALFC")
  getALFC();
});

alfaceMint.addEventListener('click', () => {
  console.log("Calling diamondMint");
  mintAlface();
});

async function getALFC(){
  const abiJson = [
    {"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
  ];
  
  const contract = new web3.eth.Contract(abiJson, alfaceAddress);
  const balance = await contract.methods.balanceOf(await getAccount()).call();
  // note that this number includes the decimal places (in case of BUSD, that's 18 decimal places)
  console.log(balance);
  alfaceBalance.innerHTML = balance/(10**18);
}

async function mintAlface() {
  console.log("Inside mintAlface");
  console.log("Address:"+mintALFCToAddress.value);
  console.log("Amount:"+mintALFCAmount.value);

  const abiJson = [
    {"constant":true,"inputs":[{"name":"Amount","type":"uint256"},{"name":"Addr","type":"address"}],"name":"mintToAddress","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},
  ];
  const contract = new web3.eth.Contract(abiJson, alfaceAddress);
  await contract.methods.mintToAddress(mintALFCAmount.value, mintALFCToAddress.value).call();
}

//###################### Diamond Handling ######################
diamondBalance.addEventListener('click', () => {
  console.log("Calling diamondBalance");
  getdiamondBalance();
});



async function getdiamondBalance(){
  const abiJson = [
    {"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
  ];
  
  const contract = new web3.eth.Contract(abiJson, diamondAddress);
  const balance = await contract.methods.balanceOf(await getAccount()).call();
  // note that this number includes the decimal places (in case of BUSD, that's 18 decimal places)
  console.log(balance);
  diamondBalance.innerHTML = balance/(10**18);
}



//####################### Get Account #######################
ethereumButton.addEventListener('click', () => {
  console.log("Teste")
  getAccount();
});

async function getAccount() {
  const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
  const account = accounts[0];
  showAccount.innerHTML = account;
  return account;
}

