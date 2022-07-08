const maxBus = 256;
const maxDev = 32;
const maxFunc = 8;

const $inputBaseAddrField = $("#input[name='baseaddr']");
const $inputBusField = $("#select[name='bus']");
const $inputDevField = $("#select[name='dev']");
const $inputFuncField = $("#select[name='func']");
const $generateButton = $('#calculate');
const $responseField = $('#responseField');

let optionText;

function calculateMmioAddr(){
  const baseAddr = parseInt($inputBaseAddrField.val(), 16);
  const bus = $inputBusField.val();
  const dev = $inputDevField.val();
  const func = $inputFuncField.val();
  let resString = (baseAddr + bus * parseInt('100000', 16) + dev * parseInt('8000', 16) + func * parseInt('1000', 16)).toString(16);
  resString = '0x' + resString;
  $responseField.append(resString);
}

function generate() {
  $responseField.empty();
  calculateMmioAddr();
  return false;
};

for (let index = 0; index < maxBus; index++) {
  if (index < 16) {
    optionText = "0" + index.toString(16);
  } else {
    optionText = index.toString(16);
  }

  $("#select[name='bus']").append($('<option>', {
    value: index,
    text: optionText
  }))
}

for (let index = 0; index < maxDev; index++) {
  if (index < 16) {
    optionText = "0" + index.toString(16);
  } else {
    optionText = index.toString(16);
  }

  $("#select[name='dev']").append($('<option>', {
    value: index,
    text: optionText
  }))
}

for (let index = 0; index < maxFunc; index++) {
  if (index < 16) {
    optionText = "0" + index.toString(16);
  } else {
    optionText = index.toString(16);
  }

  $("#select[name='func']").append($('<option>', {
    value: index,
    text: optionText
  }))
}

$inputBaseAddrField.attr({'value': 'f8000000', 'maxlength': 8});

$inputBaseAddrField.on ("keypress", function(e) {
  if (((e.which > 47) && (e.which < 58)) || ((e.which > 96) && (e.which < 103)) || (e.which == 8) || (e.which == 0)) {

  } else {
    e.preventDefault();
  }
})

$generateButton.click(generate);
