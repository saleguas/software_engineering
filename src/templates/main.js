//get HTML elements
let input = document.getElementById("input");
let outputHeader = document.getElementById("output header");
let output = document.getElementById("output");
let resetBtn = document.getElementById("reset");
let length = document.getElementById("solution length");
let fullExplanation = document.getElementById("full explanation").innerHTML;
let simpleExplanation = document.getElementById("simple explanation").innerHTML;

if (fullExplanation.trim() != "") {
	//if there is an equation specified...
	outputHeader.innerHTML = "Solution";
	output.innerHTML = fullExplanation;
}

resetBtn.onclick = function() {
	fullExplanation = "";
	simpleExplanation = "";
	outputHeader.innerHTML = "";
	output.innerHTML = "";
	length.reset();
}

length.onchange = function() {
	if (fullExplanation.trim() != "") {
		if (length.elements["solution length"].value == "full")
			output.innerHTML = fullExplanation;
		else
			output.innerHTML = simpleExplanation;
	}
}