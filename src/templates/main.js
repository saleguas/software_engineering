let filepath = document.location.href;
let dataIndex = filepath.indexOf("?equation="); //index where the data starts
let input = document.getElementById("input");
let outputHeader = document.getElementById("output header");
let output = document.getElementById("output");
let resetBtn = document.getElementById("reset");
let length = document.getElementById("solution length");

let fullSolution = "full solution goes here";
let simpleSolution = "simple solution goes here";

if (dataIndex != -1 && filepath.length > dataIndex + 10) {
	//if there is an equation specified...
	outputHeader.innerHTML = "Solution";
	output.innerHTML = fullSolution;
	//length.elements["solution length"].value = "full";
}

resetBtn.onclick = function() {
	input.elements["equation"].value = "";
	input.submit();
}

length.onchange = function() {
	if (dataIndex != -1 && filepath.length > dataIndex + 10) {
		if (length.elements["solution length"].value == "full")
			output.innerHTML = fullSolution;
		else
			output.innerHTML = simpleSolution;
	}
}