let filepath = document.location.href;
let dataIndex = filepath.indexOf("?equation="); //index where the data starts
let input = document.getElementById("input");
let outputHeader = document.getElementById("output header");
let output = document.getElementById("output");
let resetBtn = document.getElementById("reset");

if (dataIndex != -1 && filepath.length > dataIndex + 10) {
	//if there is an equation specified...
	outputHeader.innerHTML = "Solution";
	output.innerHTML = "solution goes here";
}

resetBtn.onclick = function() {
	input.elements["equation"].value = "";
	input.submit();
}