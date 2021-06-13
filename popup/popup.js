const carrot = document.getElementById("carrot");

// にんじんを膨らませる操作
const carrotExpansion = (event) => {

	// にんじんをマウスのにんじんの場所にもってくる
	carrot.style.left = event.pageX - 24 + "px";
	carrot.style.top = event.pageY - 24 + "px";

	// にんじんを表示し、拡大する
	carrot.style.display = "inline";
	carrot.classList.add("expand");

	// 100ms後、にんじんを非表示にし、拡大を解除する
	setTimeout(() => {
		carrot.style.display = "none";
		carrot.classList.remove("expand");
	}, 100)
}

// アーモンドの操作
const operateAlmond = (elem) => {

	// altがno-almondなら、flagはtrue
	const almond_tag = $(elem).parent().find(".almond")[0];
	const almond_description = $(elem).parent().find(".almond-description")[0];
	const almond_flag = (almond_tag.alt === "no-almond") ? true : false

	if (almond_flag === true) {
		almond_tag.src = "../images/icons/almond.png";
		almond_tag.alt = "almond";
		console.log("Almond was given")
		almond_description.innerText = "あーもんどーあーもんどー！！"

	} else {
		almond_tag.src = "../images/icons/no_almond.png";
		almond_tag.alt = "no-almond";
		console.log("Almond was lost")
		almond_description.innerText = "アーモンドちょうだいぺこー！！"
	}

	return almond_flag
}

// アーモンドの吹き出し操作
const displayAlmondBalloon = () => {

	// 吹き出しを非表示にする
	$('.almond-description').hide();

	// almondのdivを取得し、ひとつずつイベントリスナーを登録
	const almond_divs = document.getElementsByClassName("almond-div");
	Array.from(almond_divs).forEach( (almond_div) => {

		// マウスエンターで、吹き出しを出す
		almond_div.addEventListener('mouseenter', () => {
			const description = almond_div.lastElementChild
			description.style.display = "block";

			// 500ms後から、透明度を1000msかけて、1から0に変化させる
			setTimeout(() => {
				description.animate({opacity: [1, 0]}, 1000)
			}, 500);

			// 1500ms後（透明度が0になるとき）に吹き出しを非表示にする
			setTimeout(() => {
				description.style.display = "none"
			}, 1500);
		})
	});
}


// Main

// アーモンドの吹き出し登録
displayAlmondBalloon();

//画面がクリックされたとき、にんじんを拡大する
$("body").click( e => carrotExpansion(e) );

//ボタンが押されたとき、リンクに応じて
$('.action').click(function(event){
	event.preventDefault();

	// アーモンドの操作
	flag = operateAlmond(this);

	// ボタンのidを取得
	const action = this.id;
	console.log(action + " button clicked");

	// 対象のタブのidを取得したい
	chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
		// 取得したタブid(tabs[0].id)を利用してsendMessageする
		chrome.tabs.sendMessage(tabs[0].id, {action: action, flag: flag})
	})
});
