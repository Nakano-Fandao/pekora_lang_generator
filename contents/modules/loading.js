const displayLoading = () => {

    let loading;

    // 既に作成済みの場合は表示して戻る;
    loading = document.getElementById("loading");
    if (loading !== null) {
        loading.style.display = "block";
        console.log("Start loading")
        return;
    };

    // body全体に薄いフィルターをかけ、loading gifを表示
    loading = document.createElement("div");
    loading.id = "loading";
    const loading_msg = chrome.extension.getURL("../images/loading/loading_msg.gif");
    loading.innerHTML = "\
    <div class='loading-div'>\
        <img src=" + loading_msg + " class='loading-msg' alt='Loading...peko'>\
    </div>\
    ";

    document.body.appendChild(loading);
    console.log("Start loading")
}

// Remove loading elements
const removeLoading = () => {
    $("#loading").delay(300).fadeOut(300);
    console.log("Stop loading");
}

export {displayLoading, removeLoading};
