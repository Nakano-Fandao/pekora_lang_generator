const carrot = document.getElementById("carrot");

const carrotExpansion = (event) => {
	carrot.style.display = "inline";
	carrot.style.left = event.pageX - 32 + "px";
	carrot.style.top = event.pageY - 32 + "px";
	carrot.classList.add("expand");

	setTimeout(() => {
		carrot.classList.remove("expand");
		carrot.style.display = "none";
	}, 100)
}

//画面がクリックされたとき
document.addEventListener("click",  e => carrotExpansion(e));


//ボタンが押されたとき
$('.btn').click(function(event){
	event.preventDefault();

	console.log("Button clicked");

	// ボタンのidを取得
	const action = this.id;

	// 対象のタブのidを取得したい
	chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
		// 取得したタブid(tabs[0].id)を利用してsendMessageする
		chrome.tabs.sendMessage(tabs[0].id, {message: action})
	})
});
