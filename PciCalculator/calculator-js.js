const maxBus = 256;
const maxDev = 32;
const maxFunc = 8;

// Initialization value
let inputValueCal = document.createAttribute("value");
let inputValueRes = document.createAttribute("value");
let inputValueMmioAddr = document.createAttribute("value");

inputValueCal.value = "f8000000"
inputValueRes.value = "f8000000"

document.getElementById("cal").attributes.setNamedItem(inputValueCal);
document.getElementById("res").attributes.setNamedItem(inputValueRes);

inputValueMmioAddr.value = document.getElementById("res").getAttribute("value")
document.getElementById("adr").attributes.setNamedItem(inputValueMmioAddr);

let busSelect = document.getElementsByTagName("select")[0];
let devSelect = document.getElementsByTagName("select")[1];
let funcSelect = document.getElementsByTagName("select")[2];
let nodeText;
let option;

for (let index = 0; index < maxBus; index++) {
  if (index < 16) {
    nodeText = document.createTextNode("0" + index.toString(16));
  } else {
    nodeText = document.createTextNode(index.toString(16));
  }

  option = document.createElement("option");
  option.appendChild(nodeText);
  busSelect.appendChild(option);
}

for (let index = 0; index < maxDev; index++) {
  if (index < 16) {
    nodeText = document.createTextNode("0" + index.toString(16));
  } else {
    nodeText = document.createTextNode(index.toString(16));
  }

  option = document.createElement("option");
  option.appendChild(nodeText);
  devSelect.appendChild(option);
}

for (let index = 0; index < maxFunc; index++) {
  if (index < 16) {
    nodeText = document.createTextNode("0" + index.toString(16));
  } else {
    nodeText = document.createTextNode(index.toString(16));
  }

  option = document.createElement("option");
  option.appendChild(nodeText);
  funcSelect.appendChild(option);
}

function calculateMmioAddr() {
  const baseAddr = parseInt(document.getElementById("cal").value, 16)
  const bus = document.getElementsByTagName("select")[0].value;
  const dev = document.getElementsByTagName("select")[1].value;
  const func = document.getElementsByTagName("select")[2].value;
  let resString = (baseAddr + parseInt(bus, 16) * parseInt('100000', 16) + parseInt(dev, 16) * parseInt('8000', 16) + parseInt(func) * parseInt('1000', 16)).toString(16);
  return resString;
}

function restoreMmioAddr() {
  const baseAddr = parseInt(document.getElementById("res").value, 16);
  const Addr = parseInt(document.getElementById("adr").value, 16);
  let list = [];
  let modulus = Addr - baseAddr;

  bus = (Math.floor(modulus / parseInt('100000', 16))).toString(16)
  list.push(bus)
  modulus = modulus % parseInt('100000', 16)

  dev = (Math.floor((modulus) / parseInt('8000', 16))).toString(16)
  list.push(dev)
  modulus = modulus % parseInt('8000', 16)

  func = (Math.floor((modulus) / parseInt('1000', 16))).toString(16)
  list.push(func)

  return list;
}

function calculate() {
  let Addr = calculateMmioAddr();
  document.getElementById("iAddr").value = Addr
};

function restore() {
  let list;
  let bus, dev, func;
  list = restoreMmioAddr();

  func = list.pop();
  if (parseInt(func, 16) < 16) {
    func = '0' + func;
  }

  dev = list.pop()
  if (parseInt(dev, 16) < 16) {
    dev = '0' + dev;
  }

  bus = list.pop()
  if (parseInt(bus, 16) < 16) {
    bus = '0' + bus;
  }

  document.getElementById("iBus").value = bus
  document.getElementById("iDev").value = dev
  document.getElementById("iFunc").value = func
}