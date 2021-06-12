const carrot = document.getElementById("carrot");

document.addEventListener('click', e => {
	carrot.style.display = "inline";
	carrot.style.left = e.pageX;
	carrot.style.top = e.pageY;
	carrot.classList.add("expand");

	setTimeout(() => {
		carrot.classList.remove("expand");
		carrot.style.display = "none";
	}, 500)
})


// document.getElementById('pekora_rap').setAttribute("src", imageUrl)


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
