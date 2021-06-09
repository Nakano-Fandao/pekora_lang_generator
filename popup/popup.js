//ボタンが押されたとき
$('.btn').click(function(){

	console.log("click");

	// ボタンのidを取得
	const action = this.id;

	// 対象のタブのidを取得したい
	chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
		// 取得したタブid(tabs[0].id)を利用してsendMessageする
		chrome.tabs.sendMessage(tabs[0].id, {message: action})
	})
  });
