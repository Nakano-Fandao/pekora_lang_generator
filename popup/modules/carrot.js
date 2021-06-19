// にんじんを膨らませる操作
const carrot = document.getElementById("carrot");

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

export {carrotExpansion};
