import {initializeAlmond, operateAlmond, displayAlmondBalloon} from "./modules/almond.js";
import {carrotExpansion} from "./modules/carrot.js";

// Main

// アーモンドの初期化
initializeAlmond();

// アーモンドの吹き出し登録
displayAlmondBalloon();

//画面がクリックされたとき、にんじんを拡大する
$("body").click( e => carrotExpansion(e) );

//ボタンが押されたとき、リンクに応じて
$('.action').click(function(event){
	event.preventDefault();

	// アーモンドの操作
	const flag = operateAlmond(this);

	// ボタンのidを取得
	const action = this.id;
	console.log(action + " button clicked");

	// 対象のタブのidを取得したい
	chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
		// 取得したタブid(tabs[0].id)を利用してsendMessageする
		chrome.tabs.sendMessage(tabs[0].id, {action: action, flag: flag}, response => {
			console.log("Return to popup.js after " + action);
		})
	})
});
