var Web3 = require("web3")

//Trying to connect direct to a node
//const web3 = new Web3("https://bsc-dataseed.binance.org")

//Trying to use Metamask instead
const web3 = new Web3(window.ethereum)

const bnxAddress = "0x8c851d1a123ff703bd1f9dabe631b69902df5f97";
const diamondAddress = "0x5f16128A0A10fF02AB645A81d9E6589D1c599850";
const alfaceAddress = "0xfe360bb3421af9e4a142fe2adbdfd84ea22860dd"

//####################### Get Account #######################
const enableMetaMaskButton = document.getElementById('enableMetaMaskButton');
const showAccount = document.getElementById('walletAddress');

enableMetaMaskButton.addEventListener('click', () => {
  console.log("Enabling MetaMask")
  getAccount();
});

async function getAccount() {
  try {
    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    const account = accounts[0];
    enableMetaMaskButton.disabled = true;
    showAccount.innerHTML = "Wallet=" + account;
    return account;
  }
  catch (err) {
    alert(err.message);
  };
}

//####################### Get Current Block ################
const getCurrentBlockButton = document.getElementById('getCurrentBlockButton');
const currentBlock = document.getElementById('currentBlock');

getCurrentBlockButton.addEventListener('click', () => {
  console.log("getCurrentBlock")
  currentBlock.innerHTML = "Loading....";
  getBlockNumber();
});

async function getBlockNumber() {
  const currentBlockNumber = await web3.eth.getBlockNumber()
  console.log(currentBlockNumber);
  currentBlock.innerHTML = currentBlockNumber;
  return currentBlockNumber
}
//###################### BNX Handling ######################
const getBNXBalanceButton = document.getElementById('getBNXBalanceButton');

getBNXBalanceButton.addEventListener('click', () => {
  console.log("Calling getBNXBalance")
  BNXBalance();
});

async function BNXBalance() {
  const abiJson = [
    { "constant": true, "inputs": [{ "name": "who", "type": "address" }], "name": "balanceOf", "outputs": [{ "name": "", "type": "uint256" }], "payable": false, "stateMutability": "view", "type": "function" },
  ];

  const contract = new web3.eth.Contract(abiJson, bnxAddress);
  const balance = await contract.methods.balanceOf(await getAccount()).call();
  // note that this number includes the decimal places (in case of BUSD, that's 18 decimal places)
  console.log(balance);
  bnxBalance.innerHTML = balance / (10 ** 18);
}

//###################### Diamond Handling ######################
const getDiamondBalanceButton = document.getElementById('getDiamondBalanceButton');
const diamondBalance = document.getElementById('diamondBalance');

getDiamondBalanceButton.addEventListener('click', () => {
  console.log("Calling diamondBalance");
  DiamondBalance();
});

async function DiamondBalance() {
  const abiJson = [
    { "constant": true, "inputs": [{ "name": "who", "type": "address" }], "name": "balanceOf", "outputs": [{ "name": "", "type": "uint256" }], "payable": false, "stateMutability": "view", "type": "function" },
  ];

  const contract = new web3.eth.Contract(abiJson, diamondAddress);
  const balance = await contract.methods.balanceOf(await getAccount()).call();
  // note that this number includes the decimal places (in case of BUSD, that's 18 decimal places)
  console.log(balance);
  diamondBalance.innerHTML = balance / (10 ** 18);
}

//###################### ALFC Handling ######################
const getAlfaceBalanceButton = document.getElementById('getAlfaceBalanceButton');
const alfaceMintButton = document.getElementById('alfaceMintButton');
const mintALFCAmount = document.getElementById('mintALFCAmount');
const alfaceBurnButton = document.getElementById('alfaceBurnButton');
const burnALFCAmount = document.getElementById('burnALFCAmount');

getAlfaceBalanceButton.addEventListener('click', () => {
  console.log("Calling getALFC")
  AlfaceBalance();
});

alfaceMintButton.addEventListener('click', () => {
  console.log("Calling alfaceMint");
  mintAlface();
});

alfaceBurnButton.addEventListener('click', () => {
  console.log("Calling alfaceMint");
  burnAlface();
});

async function AlfaceBalance() {
  const abiJson = [
    { "constant": true, "inputs": [{ "name": "who", "type": "address" }], "name": "balanceOf", "outputs": [{ "name": "", "type": "uint256" }], "payable": false, "stateMutability": "view", "type": "function" },
  ];

  const contract = new web3.eth.Contract(abiJson, alfaceAddress);
  const balance = await contract.methods.balanceOf(await getAccount()).call();
  // note that this number includes the decimal places (in case of BUSD, that's 18 decimal places)
  console.log(balance);
  alfaceBalance.innerHTML = balance / (10 ** 18);
}

async function mintAlface() {
  console.log("Inside mintAlface");
  console.log("Amount:" + mintALFCAmount.value);

  const abiJson = [
    { "constant": true, "inputs": [{ "name": "Amount", "type": "uint256" }], "name": "mint", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" },
  ];
  try {
    const contract = new web3.eth.Contract(abiJson, alfaceAddress);
    const gas = await contract.methods.mint(mintALFCAmount.value).send({ "from": await getAccount() });
    console.log("Gas=" + gas)
  } catch (err) {
    alert(err.message);
  };
}

async function burnAlface() {
  console.log("Inside burnAlface");
  console.log("Amount:" + burnALFCAmount.value);
  try {
    const abiJson = [
      { "constant": true, "inputs": [{ "name": "Amount", "type": "uint256" }], "name": "burn", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" },
    ];
    const contract = new web3.eth.Contract(abiJson, alfaceAddress);
    const gas = await contract.methods.burn(burnALFCAmount.value).send({ "from": await getAccount() });
    console.log("Gas=" + gas)
  }
  catch (err) {
    alert(err.message);
  };
}

//###################### Sign Message ######################