// #region slider feedback

var slider1 = document.getElementById("formControlRange1");
var output1 = document.getElementById("value1");

var slider2 = document.getElementById("formControlRange2");
var output2 = document.getElementById("value2");

let update1 = () => { value1.innerHTML = slider1.value; opcio_sum.innerHTML = parseInt(slider1.value) + parseInt(slider2.value); };
let update2 = () => { value2.innerHTML = slider2.value; opcio_sum.innerHTML = parseInt(slider1.value) + parseInt(slider2.value); };

slider1.addEventListener('input', update1);
slider2.addEventListener('input', update2);
update1();
update2();

// #endregion