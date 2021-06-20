const icon_dir = chrome.extension.getURL("../images/icons/")

const giveAlmond = (almond) => {
	almond.src = icon_dir + "almond.png";;
	almond.alt = "almond";
	almond.parentElement.getElementsByClassName('almond-description')[0].innerText = "あーもんどーあーもんどー！！"
}

const loseAlmond = (almond) => {
	almond.src = icon_dir + "no_almond.png";
	almond.alt = "no-almond";
	almond.parentElement.getElementsByClassName('almond-description')[0].innerText = "アーモンドちょうだいぺこー！！"
}

// popup読み込み時に、アーモンド初期化
const initializeAlmond = () => {

	// actionを登録
	const action = "almond";

	console.log(action + " initialized");

	// 対象のタブのidを取得したい
	chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {

		return new Promise( (resolve, reject) => {

			// 取得したタブid(tabs[0].id)を利用してsendMessageする
			chrome.tabs.sendMessage(tabs[0].id, {action: action, flag: NaN}, response => {

				console.log("Return to popup.js after initializing almonds");
				console.log(response);

				if (action === "almond") {
					// responseがtrueであれば、アーモンドを色付け
					const almonds = document.getElementsByClassName('almond');
					console.log(almonds);
					for (let i = 0; i < almonds.length; i++) {
						(response[i] === true) ? giveAlmond(almonds[i]) : loseAlmond(almonds[i]);
					}
				}
				console.log("Initialization successful");
			})

		})

	})
}

// アーモンドの操作
const operateAlmond = (elem) => {

	// altがno-almondなら、flagはtrue
	const almond = $(elem).parent().find(".almond")[0];
	const almond_flag = (almond.alt === "no-almond") ? true : false;

	if (almond_flag === true) {
		giveAlmond(almond);
		console.log("Almond was given");

	} else {
		loseAlmond(almond);
		console.log("Almond was lost");
	}

	return almond_flag;
}

// アーモンドの吹き出し操作
const displayAlmondBalloon = () => {

	// almondのdivを取得し、ひとつずつイベントリスナーを登録
	const almond_divs = document.getElementsByClassName("almond-div");
	Array.from(almond_divs).forEach( (almond_div) => {

		// マウスエンターで、吹き出しを出す
		almond_div.addEventListener('mouseenter', () => {
			const description = almond_div.lastElementChild;
			description.style.display = "block";
			// 500ms後から、透明度を1000msかけて、1から0に変化させる
			setTimeout(() => {
				description.animate({opacity: [1, 0]}, 1000);
			}, 500);

			// 1500ms後（透明度が0になるとき）に吹き出しを非表示にする
			setTimeout(() => {
				description.style.display = "none";
			}, 1500);
		})
	});
}

export {initializeAlmond, operateAlmond, displayAlmondBalloon};
